"""Operatoren-Training (ZI-02): Aufgaben aus ``operatoren.yaml`` und ihre Bewertung ohne Versuch."""

from __future__ import annotations

import random
from pathlib import Path

import pytest
from pydantic import ValidationError

from ap_trainer.content.aufgaben import Freitext, MultipleChoice, Zuordnung
from ap_trainer.content.loader import load_package_or_raise
from ap_trainer.content.operatoren import OperatorenDatei
from ap_trainer.service import Trainer
from ap_trainer.storage.db import Store
from ap_trainer.tasks.check import evaluate
from ap_trainer.tasks.operators import RECOGNIZE_COUNT, WRITE_COUNT, all_tasks, training_round
from ap_trainer.tasks.validate import model_answer

REAL = Path(__file__).parents[2] / "content" / "ap1"


@pytest.fixture(scope="module")
def package():  # type: ignore[no-untyped-def]
    return load_package_or_raise(REAL)


@pytest.fixture
def ops(package) -> OperatorenDatei:  # type: ignore[no-untyped-def]
    assert package.operatoren is not None
    return package.operatoren


def test_all_operators_from_the_requirement_are_present(ops: OperatorenDatei) -> None:
    # ZI-02 nennt sechs Operatoren; „beurteilen“ kommt in den Aufgaben des Pakets vor
    required = {"nennen", "beschreiben", "erläutern", "begründen", "berechnen", "vergleichen", "beurteilen"}
    assert required <= set(ops.by_id())


def test_every_generated_task_is_solvable_with_its_model_answer(ops: OperatorenDatei) -> None:
    tasks = all_tasks(ops)
    assert len(tasks) == 1 + 2 * len(ops.operatoren) * len(ops.beispiele)
    assert len({t.id for t in tasks}) == len(tasks)
    for task in tasks:
        if isinstance(task, Freitext):
            continue
        assert evaluate(task, model_answer(task)).richtig, task.id


def test_recognize_task_has_exactly_the_target_operator_as_answer(ops: OperatorenDatei) -> None:
    for task in all_tasks(ops):
        if isinstance(task, MultipleChoice):
            correct = [o.text for o in task.optionen if o.richtig]
            assert len(correct) == 1 and correct[0] in task.id.replace("ae", "ä").replace("ue", "ü")


def test_training_round_goes_from_matching_to_writing(ops: OperatorenDatei) -> None:
    for seed in range(50):
        tasks = training_round(ops, random.Random(seed))
        assert isinstance(tasks[0], Zuordnung)
        recognize = tasks[1 : 1 + RECOGNIZE_COUNT]
        write = tasks[1 + RECOGNIZE_COUNT :]
        assert all(isinstance(t, MultipleChoice) for t in recognize)
        assert len(write) == WRITE_COUNT and all(isinstance(t, Freitext) for t in write)
        # Verschiedene Operatoren beim Erkennen, keine Aufgabe doppelt
        assert len({t.id.split("-")[-2] for t in recognize}) == RECOGNIZE_COUNT
        assert len({t.id for t in tasks}) == len(tasks)


def test_example_must_cover_every_operator(ops: OperatorenDatei) -> None:
    data = ops.model_dump()
    del data["beispiele"][0]["antworten"]["nennen"]
    with pytest.raises(ValidationError, match="fehlend"):
        OperatorenDatei.model_validate(data)


def test_checking_a_training_task_stores_no_attempt(package, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    trainer = Trainer(package, Store(tmp_path / "db.sqlite"))
    tasks = trainer.operator_training(random.Random(1))
    task = tasks[1]
    submission = trainer.check_operator_task(task, model_answer(task), seconds=40)
    assert submission.ergebnis.richtig and not submission.fehlerkarte
    # Kein Versuch, keine Fehlerkarte – nur Lernzeit
    assert trainer.store.attempts() == []
    wrong = trainer.check_operator_task(task, frozenset(), seconds=10)
    assert not wrong.ergebnis.richtig and trainer.due_cards() == []
