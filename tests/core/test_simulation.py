"""Tests für die Auswertung der Prüfungssimulation (PS-02, PS-04)."""

from __future__ import annotations

import datetime as dt

import pytest

from ap_trainer.core.simulation import SimRun, TeilErgebnis, goal_reached, grade, points, weak_topics

START = dt.datetime(2027, 1, 20, 9, 0, tzinfo=dt.UTC)


def _run(sim_id: str, parts: list[tuple[str, int, float, bool]]) -> SimRun:
    return SimRun(
        sim_id=sim_id,
        gestartet=START,
        beendet=START + dt.timedelta(minutes=87),
        teile=[
            TeilErgebnis(aufgabe_id=f"t{i}", thema=t, max_punkte=m, punkte=p, bewertet=b)
            for i, (t, m, p, b) in enumerate(parts)
        ],
    )


@pytest.mark.parametrize(
    ("share", "expected"),
    [(1.0, 8.0), (0.75, 6.0), (2 / 3, 5.5), (1 / 3, 2.5), (0.0, 0.0), (1.5, 8.0), (-1, 0.0)],
)
def test_points_rounded_to_half_points(share: float, expected: float) -> None:
    assert points(8, share) == expected


@pytest.mark.parametrize(
    ("total", "note"),
    [
        (100, 1),
        (92, 1),
        (91.5, 2),
        (81, 2),
        (80.5, 3),
        (67, 3),
        (66.5, 4),
        (50, 4),
        (49.5, 5),
        (30, 5),
        (29.5, 6),
        (0, 6),
    ],
)
def test_ihk_grade_scale(total: float, note: int) -> None:
    assert grade(total)[0] == note


def test_run_totals_and_completeness() -> None:
    run = _run("s", [("a", 10, 8, True), ("b", 6, 0, False)])
    assert run.punkte == 8 and run.max_punkte == 16 and not run.vollstaendig and run.minuten == 87


def test_weak_topics_below_seventy_percent_most_lost_first() -> None:
    run = _run(
        "s",
        [("a", 10, 6.5, True), ("a", 4, 2, True), ("b", 6, 6, True), ("c", 8, 2, True), ("d", 4, 0, False)],
    )
    # a: 8,5 von 14 (61 %), b: 100 %, c: 25 %, d unbewertet
    assert weak_topics(run) == ["c", "a"]


def test_goal_counts_distinct_complete_simulations() -> None:
    runs = [
        _run("s1", [("a", 100, 93, True)]),
        _run("s1", [("a", 100, 95, True)]),
        _run("s2", [("a", 100, 91.5, True)]),
        _run("s3", [("a", 92, 92, True), ("b", 8, 0, False)]),
    ]
    assert goal_reached(runs) == ["s1"]
