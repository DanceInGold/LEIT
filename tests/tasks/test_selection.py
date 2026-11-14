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


def test_single_task_on_level_is_not_repeated() -> None:
    """Fehler aus dem Test von PR #16: Stufe 1 hatte nur eine Aufgabe, sie kam immer wieder."""
    pool = TopicPool("t", [_task("a", 1), _task("b", 2), _task("c", 2), _task("d", 3)])
    rng = random.Random(3)
    for _ in range(50):
        task = pick_task(pool, 1, ["a"], rng)
        assert task is not None and task.id in {"b", "c"}  # nächste Stufe mit Neuem


def test_neighbour_level_prefers_closer_and_higher() -> None:
    pool = TopicPool("t", [_task("a", 1), _task("b", 2), _task("c", 3), _task("d", 4)])
    rng = random.Random(4)
    assert pick_task(pool, 2, ["b"], rng).id == "c"  # type: ignore[union-attr]
    assert pick_task(pool, 2, ["b", "c"], rng).id == "a"  # type: ignore[union-attr]


def test_everything_seen_never_repeats_last_task() -> None:
    pool = TopicPool("t", [_task("a", 1), _task("b", 2)])
    rng = random.Random(5)
    assert pick_task(pool, 1, ["b", "a"], rng).id == "b"  # type: ignore[union-attr]
    # Nur eine Aufgabe im ganzen Thema: Wiederholung unvermeidbar
    single = TopicPool("t", [_task("a", 1)])
    assert pick_task(single, 1, ["a"], rng).id == "a"  # type: ignore[union-attr]


def test_small_topic_rotates_instead_of_ping_pong() -> None:
    """Fehler aus dem Test von PR #20: SMART pendelte zwischen Stufe-1-Aufgabe und den anderen."""
    pool = TopicPool("t", [_task("a", 1), _task("b", 2), _task("c", 3), _task("d", 4)])
    rng = random.Random(1)
    recent: list[str] = []
    for _ in range(12):
        task = pick_task(pool, 1, recent, rng)
        assert task is not None
        recent.append(task.id)
    assert recent == ["a", "b", "c", "d"] * 3


def test_no_recent_repeat_in_real_package() -> None:
    """Für jedes Thema des Pakets: keine der letzten drei (bzw. n − 1) Aufgaben kommt sofort wieder.

    Die Stufe springt dabei zufällig, wie beim echten Üben mit Auf- und Abstieg.
    """
    from pathlib import Path

    from ap_trainer.content.loader import load_package_or_raise

    package = load_package_or_raise(Path(__file__).parents[2] / "content" / "ap1")
    pools = [
        TopicPool(t.id, package.tasks_for_topic(t.id), package.generatoren.get(t.id, []))
        for t in package.katalog.themen
    ]
    rng = random.Random(6)
    for pool in pools:
        if len(pool.aufgaben) < 2 or pool.generatoren:
            continue
        block = min(3, len(pool.aufgaben) - 1)
        recent: list[str] = []
        for _ in range(40):
            task = pick_task(pool, rng.choice(pool.levels()), recent, rng)
            assert task is not None
            distinct: list[str] = []
            for task_id in reversed(recent):
                if task_id not in distinct:
                    distinct.append(task_id)
            assert task.id not in distinct[:block], (pool.thema, task.id, recent[-4:])
            recent.append(task.id)
