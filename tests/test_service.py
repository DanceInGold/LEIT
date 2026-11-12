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
