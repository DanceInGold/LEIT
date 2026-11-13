"""Tests für die Auswahl der nächsten Aufgabe."""

from __future__ import annotations

import random
from typing import Any

from ap_trainer.content.aufgaben import AUFGABE
from ap_trainer.tasks.selection import TopicPool, pick_task, target_level


def _task(task_id: str, stufe: int) -> Any:
    return AUFGABE.validate_python(
        {
            "id": task_id,
            "typ": "reihenfolge",
            "thema": "t",
            "stufe": stufe,
            "titel": "x",
            "frage": "x",
            "elemente": ["a", "b", "c"],
            "loesungsweg": "x",
            "quelle": "x",
            "status": "ungeprüft",
        }
    )


def test_target_level_prefers_lower() -> None:
    assert target_level([1, 3], 2) == 1
    assert target_level([3, 4], 1) == 3
    assert target_level([], 1) is None


def test_fixed_tasks_avoid_recent_ones() -> None:
    pool = TopicPool("t", [_task("a", 1), _task("b", 1)])
    rng = random.Random(1)
    assert all(pick_task(pool, 1, ["a"], rng).id == "b" for _ in range(20))  # type: ignore[union-attr]
    # Alle zuletzt gesehen: die am längsten zurückliegende kommt
    assert pick_task(pool, 1, ["b", "a"], rng).id == "b"  # type: ignore[union-attr]


def test_generators_mix_with_fixed_tasks() -> None:
    pool = TopicPool("t", [_task("a", 2)], ["zahlensysteme"])
    assert pool.levels() == [1, 2, 3, 4]
    rng = random.Random(3)
    picked = {pick_task(pool, 2, [], rng).id.startswith("gen:") for _ in range(40)}  # type: ignore[union-attr]
    assert picked == {True, False}
    generated = pick_task(pool, 4, ["a"], rng)
    assert generated is not None and generated.stufe == 4 and generated.thema == "t"
    assert pick_task(TopicPool("leer"), 1, [], rng) is None
