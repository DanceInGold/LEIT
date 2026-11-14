"""Tests für die Anwendungsschicht: Ablauf Lektion → Karten → Wiederholung → Plan."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

from ap_trainer.content.loader import load_package_or_raise
from ap_trainer.core.models import BudgetPeriod, PlanSettings
from ap_trainer.service import Trainer
from ap_trainer.storage.db import Store

NOW = dt.datetime(2026, 11, 16, 8, 0, tzinfo=dt.UTC)


@pytest.fixture
def trainer(package_dir: Path, tmp_path: Path) -> Trainer:
    trainer = Trainer(load_package_or_raise(package_dir), Store(tmp_path / "db.sqlite"))
    trainer.save_settings(
        PlanSettings(
            pruefungsdatum=dt.date(2026, 12, 14),
            lernbeginn=NOW.date(),
            budget=[BudgetPeriod(ab=NOW.date(), stunden_pro_woche=10)],
        )
    )
    return trainer


def test_default_settings_use_package_date(package_dir: Path, tmp_path: Path) -> None:
    fresh = Trainer(load_package_or_raise(package_dir), Store(tmp_path / "neu.sqlite"))
    assert not fresh.is_configured()
    assert fresh.settings(NOW.date()).pruefungsdatum == dt.date(2027, 2, 24)


def test_ration_follows_plan_and_flags_missing_lessons(trainer: Trainer) -> None:
    ration = trainer.ration(NOW)
    # Hardware ist im Testpaket am schwersten gewichtet, hat aber noch keine Lektion
    assert ration.thema is not None and ration.thema.topic_id == "hardware"
    assert ration.lektion_fehlt and ration.lektion is None
    assert ration.wiederholungen == 0
    assert ration.minuten_budget == 120  # 10 h auf 5 Lerntage
    trainer.set_topic_done("hardware")
    ration = trainer.ration(NOW)
    assert ration.thema is not None and ration.thema.topic_id == "zahlen"
    assert ration.lektion is not None and ration.lektion.id == "zahlen-1"


def test_reading_lesson_creates_cards_and_reviews_work(trainer: Trainer) -> None:
    lesson = trainer.package.lektionen["zahlen-1"]
    assert trainer.mark_lesson_read(lesson, minutes=30, now=NOW) == 2  # Definition + Langform
    assert trainer.mark_lesson_read(lesson, minutes=5, now=NOW) == 0  # keine Dubletten
    assert trainer.store.progress()["zahlen"].zustand == "laufend"
    due = trainer.due_cards(NOW)
    assert {c.card_id for c in due} == {"bit:def", "bit:lang"}
    next_due = trainer.grade("bit:def", 3, NOW)
    assert next_due > NOW
    assert [c.card_id for c in trainer.due_cards(NOW)] == ["bit:lang"]


def test_finishing_topic_moves_plan_forward(trainer: Trainer) -> None:
    first = trainer.ration(NOW).thema
    assert first is not None
    trainer.set_topic_done(first.topic_id)
    second = trainer.ration(NOW).thema
    assert second is not None and second.topic_id != first.topic_id
    trainer.set_topic_done(first.topic_id, done=False)
    assert trainer.store.progress()[first.topic_id].zustand == "laufend"


def test_practice_flow_levels_and_attempts(trainer: Trainer) -> None:
    """Üben: Aufgabe ziehen, abgeben, Versuch speichern, Stufe steigt nach drei sicheren Lösungen."""
    import random

    from ap_trainer.tasks.validate import model_answer

    topics = trainer.practice_topics()
    assert [p.thema.id for p in topics] == ["zahlen"]
    assert topics[0].stufe == 1 and topics[0].stufen == [1, 2, 3, 4]
    rng = random.Random(7)
    for _ in range(3):
        task = trainer.next_task("zahlen", rng)
        assert task is not None and task.stufe == 1
        submission = trainer.submit(task, model_answer(task), seconds=30, now=NOW)
        assert submission.ergebnis.richtig
    assert submission.stufe_vorher == 1 and submission.stufe_nachher == 2
    task = trainer.next_task("zahlen", rng)
    assert task is not None and task.stufe == 2
    # Mit Lösungsweg gelöst zählt nicht als sicher, ist aber auch kein Fehler
    assert trainer.submit(task, model_answer(task), hints_opened=9, now=NOW).stufe_nachher == 2
    attempts = trainer.store.attempts("zahlen")
    assert len(attempts) == 4 and attempts[-1].hilfen == 4
    assert trainer.store.progress()["zahlen"].zustand == "laufend"
    assert trainer.store.minutes_by_day()[NOW.date()] == 1.5


def test_find_task_rebuilds_generated_tasks(trainer: Trainer) -> None:
    import random

    task = trainer.next_task("zahlen", random.Random(2))
    assert task is not None
    assert trainer.find_task(task.id, "zahlen") == task
    assert trainer.find_task("zahlen-nibble", "zahlen") is not None
    assert trainer.find_task("zahlen-nibble", "hardware") is None
    assert trainer.find_task("gen:ipv4-subnetting:1:5", "zahlen") is None
    assert trainer.find_task("quatsch", "zahlen") is None
    assert trainer.next_task("hardware") is None


def test_mastery_and_mistake_log_from_attempts(trainer: Trainer) -> None:
    """Fortschritt: Beherrschungsgrad je Thema (FT-01) und Fehlerprotokoll (FT-04)."""
    from ap_trainer.content.aufgaben import Rechnung
    from ap_trainer.tasks.validate import model_answer

    assert trainer.masteries(NOW)["zahlen"].grad is None
    assert trainer.mastery("hardware", NOW).grad is None  # Thema ohne Aufgaben
    task = trainer.find_task("gen:zahlensysteme:2:1", "zahlen")
    assert isinstance(task, Rechnung)
    trainer.submit(task, ["-1"] * len(task.schritte), now=NOW)
    groups = trainer.mistakes()
    assert len(groups) == 1 and groups[0].eintraege[0].aufgabe_id == task.id
    assert trainer.task_title(task.id, "zahlen") == task.titel
    assert trainer.task_title("gibt-es-nicht", "zahlen") == "gibt-es-nicht"
    trainer.submit(task, model_answer(task), now=NOW)
    assert trainer.mistakes(include_fixed=False) == []
    value = trainer.masteries(NOW)["zahlen"]
    assert value.grad is not None and 0 < value.grad < 100
    assert trainer.mastery("zahlen", NOW) == value


def test_wrong_answer_creates_mistake_card_for_review(trainer: Trainer) -> None:
    """Fehlerkarten (ZI-05): falsch gelöst → Karte fällig; erneut falsch → sofort wieder fällig."""
    from ap_trainer.content.aufgaben import Rechnung
    from ap_trainer.tasks.validate import model_answer

    task = trainer.find_task("gen:zahlensysteme:2:1", "zahlen")
    assert isinstance(task, Rechnung)
    assert trainer.submit(task, model_answer(task), now=NOW).fehlerkarte is False
    submission = trainer.submit(task, ["-1"] * len(task.schritte), now=NOW)
    assert submission.fehlerkarte
    cards = trainer.due_cards(NOW)
    mistake = next(c for c in cards if c.art == "fehler")
    assert mistake.aufgabe_id == task.id and mistake.hinten == task.loesungsweg
    due = trainer.grade(mistake.card_id, 3, NOW)  # „Gut“
    assert due > NOW
    trainer.submit(task, ["-1"] * len(task.schritte), now=NOW + dt.timedelta(hours=1))
    assert any(c.card_id == mistake.card_id for c in trainer.due_cards(NOW + dt.timedelta(hours=1)))
    # Eine andere Variante desselben Generators und derselben Stufe nutzt dieselbe Karte
    other = trainer.find_task("gen:zahlensysteme:2:2", "zahlen")
    assert isinstance(other, Rechnung)
    trainer.submit(other, ["-1"] * len(other.schritte), now=NOW)
    assert sum(c.startswith("fehler:") for c in trainer.store.card_ids()) == 1
    # Eine Karte zu einer verschwundenen Aufgabe wird übersprungen
    trainer.store.put_card("fehler:zahlen:gibt-es-nicht", NOW, {})
    assert all(c.card_id != "fehler:zahlen:gibt-es-nicht" for c in trainer.due_cards(NOW))


def test_mixed_test_over_learned_topics(trainer: Trainer) -> None:
    """Mischtest (WH-03): erst ab zwei begonnenen Themen fällig, danach wöchentlich."""
    import random

    from ap_trainer.content.aufgaben import Rechnung

    assert trainer.learned_topics() == []
    assert not trainer.mixed_test_due(NOW.date())
    task = trainer.find_task("gen:zahlensysteme:1:1", "zahlen")
    assert isinstance(task, Rechnung)
    trainer.submit(task, ["-1"] * len(task.schritte), now=NOW)
    assert trainer.learned_topics() == ["zahlen"]
    tasks = trainer.mixed_test(random.Random(1))
    assert len(tasks) == 10 and {t.thema for t in tasks} == {"zahlen"}
    trainer.finish_mixed_test(7, 10, NOW.date())
    assert trainer.mixed_test_last() == NOW.date()
    assert trainer.mixed_test_history() == [{"datum": NOW.date().isoformat(), "richtig": 7, "gesamt": 10}]
    assert not trainer.mixed_test_due(NOW.date() + dt.timedelta(days=6))
