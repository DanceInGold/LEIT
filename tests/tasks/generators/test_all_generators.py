"""Gemeinsame Eigenschaften aller registrierten Generatoren (AU-03, AU-04, HI-01, HI-03).

Für jeden Generator und jede Stufe: Die Aufgabe ist schemagültig und reproduzierbar, die eigene
Musterlösung wird als richtig erkannt, jede typische Falschantwort als falsch – mit ihrer Erklärung.
"""

from __future__ import annotations

import random

import pytest

from ap_trainer.content.aufgaben import AUFGABE, Rechnung
from ap_trainer.tasks.answers import is_valid
from ap_trainer.tasks.check import evaluate
from ap_trainer.tasks.generators import make, nearest_level, parse_task_id, registry, task_id
from tests.tasks.random_cases import random_cases

GENERATORS = sorted(registry())


def _all_levels(seed: int) -> list[tuple[str, int]]:
    rng = random.Random(seed)
    return [(gid, rng.choice(registry()[gid].stufen)) for gid in GENERATORS]


@pytest.mark.parametrize("generator_id", GENERATORS)
def test_generator_metadata(generator_id: str) -> None:
    generator = registry()[generator_id]
    assert generator.id == generator_id
    assert generator.stufen and all(1 <= s <= 5 for s in generator.stufen)
    assert generator.quelle and generator.titel


@random_cases()
def test_tasks_are_valid_and_reproducible(seed: int) -> None:
    for generator_id, level in _all_levels(seed):
        task = make(generator_id, level, seed, "thema-x")
        assert task.id == task_id(generator_id, level, seed)
        assert parse_task_id(task.id) == (generator_id, level, seed)
        assert task.thema == "thema-x" and task.stufe == level
        assert AUFGABE.validate_python(task.model_dump()) == task
        assert make(generator_id, level, seed, "thema-x") == task
        assert task.loesungsweg.strip()


@random_cases()
def test_model_answer_is_correct_and_errors_are_recognised(seed: int) -> None:
    for generator_id, level in _all_levels(seed):
        task = make(generator_id, level, seed, "thema-x")
        assert isinstance(task, Rechnung)
        answers = [step.antwort for step in task.schritte]
        result = evaluate(task, answers)
        assert result.richtig and result.anteil == 1, task.id
        for index, step in enumerate(task.schritte):
            assert is_valid(step.format, step.antwort), (task.id, step.frage)
            for error in step.falsch:
                wrong = list(answers)
                wrong[index] = error.antwort
                checked = evaluate(task, wrong)
                assert not checked.richtig, (task.id, step.frage, error.antwort)
                assert checked.fehlerschritt == index
                assert checked.ursache == error.ursache
                assert error.warum in checked.rueckmeldungen[index].text


def test_unknown_level_falls_back_to_nearest() -> None:
    assert nearest_level((1, 2, 3), 5) == 3
    assert nearest_level((2, 3), 1) == 2
    assert parse_task_id("zahlen-1") is None
