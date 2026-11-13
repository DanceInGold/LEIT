"""Tests für die Stufensteuerung beim Üben (AU-06, HI-02)."""

from __future__ import annotations

from ap_trainer.core.levels import LevelState, apply_attempt, is_secure, replay

LEVELS = [1, 2, 3, 4]


def test_three_secure_in_a_row_raise_level() -> None:
    assert replay([(True, 0), (True, 1), (True, 0)], LEVELS).stufe == 2
    assert replay([(True, 0), (True, 0)], LEVELS) == LevelState(1, 2, 0)


def test_two_errors_in_a_row_lower_level() -> None:
    attempts = [(True, 0)] * 6 + [(False, 0), (False, 0)]
    assert replay(attempts, LEVELS).stufe == 2
    # Ein Fehler zwischendurch senkt nicht
    assert replay([(True, 0)] * 3 + [(False, 0), (True, 0), (False, 0)], LEVELS).stufe == 2


def test_help_breaks_the_streak_but_is_no_error() -> None:
    assert not is_secure(True, 2)
    assert replay([(True, 0), (True, 0), (True, 4), (True, 0)], LEVELS).stufe == 1
    assert replay([(False, 0), (True, 3), (False, 0)], LEVELS) == LevelState(1, 0, 1)


def test_bounds_and_missing_levels() -> None:
    assert replay([(False, 0)] * 4, LEVELS).stufe == 1
    assert replay([(True, 0)] * 30, LEVELS).stufe == 4
    # Stufe 2 gibt es nicht: von 1 direkt auf 3
    assert replay([(True, 0)] * 3, [1, 3]).stufe == 3
    assert replay([], []).stufe == 1
    assert apply_attempt(LevelState(3), False, 0, [3]).stufe == 3
