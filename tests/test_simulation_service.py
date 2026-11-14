"""Ablauf einer Prüfungssimulation mit dem echten Inhaltspaket (PS-01, PS-02, PS-04)."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

from ap_trainer.content.aufgaben import Freitext
from ap_trainer.content.loader import load_package_or_raise
from ap_trainer.service import Trainer
from ap_trainer.storage.db import Store
from ap_trainer.tasks.check import FreitextAntwort
from ap_trainer.tasks.validate import model_answer

REAL = Path(__file__).parents[1] / "content" / "ap1"
START = dt.datetime(2027, 1, 20, 9, 0, tzinfo=dt.UTC)
END = START + dt.timedelta(minutes=85)


@pytest.fixture(scope="module")
def package():  # type: ignore[no-untyped-def]
    return load_package_or_raise(REAL)


@pytest.fixture
def trainer(package, tmp_path: Path) -> Trainer:  # type: ignore[no-untyped-def]
    return Trainer(package, Store(tmp_path / "db.sqlite"))


def test_perfect_run_reaches_goal_after_rating_free_text(trainer: Trainer) -> None:
    sim = trainer.package.simulationen["sim-01"]
    answers = {t.id: model_answer(t) for t in sim.tasks() if not isinstance(t, Freitext)}
    run = trainer.submit_simulation("sim-01", answers, START, END)
    free = [t for t in sim.tasks() if isinstance(t, Freitext)]
    assert not run.vollstaendig and run.punkte == 100 - sum(
        p.punkte for _a, p in sim.teile() if p.aufgabe in free
    )
    assert trainer.sim_goal() == []
    for task in free:
        run = trainer.rate_simulation_text(run.id, task.id, [True] * len(task.bewertungspunkte))
    assert run.vollstaendig and run.punkte == 100
    assert trainer.sim_goal() == ["sim-01"]
    assert trainer.sim_weak_topics() == []
    # Jede Teilaufgabe zählt als Versuch auf Stufe 5; 85 Minuten Lernzeit
    attempts = trainer.store.attempts()
    assert len(attempts) == len(sim.tasks()) and {a.stufe for a in attempts} == {5}


def _perfect_run(trainer: Trainer, sim_id: str) -> int:
    """Gibt die Musterlösung ab, bewertet alle Freitexte als erfüllt und liefert die Punkte."""
    sim = trainer.package.simulationen[sim_id]
    answers = {t.id: model_answer(t) for t in sim.tasks() if not isinstance(t, Freitext)}
    run = trainer.submit_simulation(sim_id, answers, START, END)
    for task in sim.tasks():
        if isinstance(task, Freitext):
            run = trainer.rate_simulation_text(run.id, task.id, [True] * len(task.bewertungspunkte))
    return run.punkte


def test_every_simulation_gives_full_points_for_model_answers(trainer: Trainer) -> None:
    # Jede Simulation im Paket muss mit der Musterlösung genau 100 Punkte ergeben (PS-01)
    sim_ids = sorted(trainer.package.simulationen)
    assert len(sim_ids) >= 2
    for sim_id in sim_ids:
        assert _perfect_run(trainer, sim_id) == 100, sim_id
    # Zwei verschiedene Simulationen mit ≥ 92 Punkten erfüllen das Ziel (PS-03)
    assert trainer.sim_goal() == sim_ids


def test_empty_run_feeds_weak_topics_mistakes_and_cards(trainer: Trainer) -> None:
    sim = trainer.package.simulationen["sim-01"]
    run = trainer.submit_simulation("sim-01", {}, START, END)
    assert run.punkte == 0
    for task in sim.tasks():
        if isinstance(task, Freitext):
            run = trainer.rate_simulation_text(run.id, task.id, [False] * len(task.bewertungspunkte))
    assert run.vollstaendig and run.punkte == 0
    weak = trainer.sim_weak_topics()
    assert set(weak) == {t.thema for t in sim.tasks()}
    assert sum(g.offen for g in trainer.mistakes()) == len(sim.tasks())
    assert any(c.art == "fehler" and c.aufgabe_id.startswith("sim-01-") for c in trainer.due_cards(END))
    # Fehlerprotokoll und Fehlerkarte finden die Teilaufgabe wieder
    task = sim.tasks()[0]
    assert trainer.find_task(task.id, task.thema) == task
    assert trainer.find_task(task.id, "falsches-thema") is None


def test_partial_points_and_answer_text(trainer: Trainer) -> None:
    sim = trainer.package.simulationen["sim-01"]
    subnet = next(t for t in sim.tasks() if t.id == "sim-01-2a")
    answer = list(model_answer(subnet))
    answer[2] = "64"  # Netz- und Broadcastadresse vergessen
    run = trainer.submit_simulation("sim-01", {subnet.id: answer}, START, END)
    part = next(p for p in run.teile if p.aufgabe_id == "sim-01-2a")
    assert part.punkte == 8 and part.max_punkte == 10
    assert "64" in part.antwort and any("Broadcast" in h for h in part.hinweise)
    assert trainer.sim_run(run.id).punkte == run.punkte
    with pytest.raises(KeyError):
        trainer.sim_run(999)


def test_runs_survive_export_and_import(trainer: Trainer, package, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    run = trainer.submit_simulation("sim-01", {}, START, END)
    data = trainer.store.export_json()
    fresh = Trainer(package, Store(tmp_path / "neu.sqlite"))
    fresh.store.import_json(data)
    assert [r.model_dump() for r in fresh.sim_runs()] == [r.model_dump() for r in trainer.sim_runs()]
    assert fresh.sim_runs()[0].id == run.id
    _ = FreitextAntwort
