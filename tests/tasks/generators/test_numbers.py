"""Tests für die Zahlenhilfen der Generatoren (Rundung, deutsche Schreibweise, Musterlösung)."""

from __future__ import annotations

from fractions import Fraction

from ap_trainer.tasks.answers import same_answer
from ap_trainer.tasks.generators._numbers import answer, de, number_step, rounded


def test_rounding_is_commercial() -> None:
    assert rounded(Fraction(5, 1000)) == Fraction(1, 100)
    assert rounded(Fraction(-5, 1000)) == Fraction(-1, 100)
    assert rounded(Fraction(2480_3, 10), 0) == 2480


def test_german_display_and_unambiguous_answer() -> None:
    assert de(Fraction(10512, 10)) == "1.051,2"
    assert de(Fraction(10512, 10), 2) == "1.051,20"
    assert de(Fraction(18, 1000), max_places=4) == "0,018"
    assert answer(1500) == "1500"  # ohne Tausenderpunkt, sonst wäre „1.500“ zweideutig
    assert answer(Fraction(10512, 10)) == "1051,2"
    assert answer(Fraction(1, 3)) == "0,33"


def test_number_step_tolerance_and_errors() -> None:
    exact = number_step(
        "a", 520, "x", falsch=[(521, "aufgerundet", "rechenfehler"), (520, "gleich", "konzept")]
    )
    assert exact.toleranz == 0 and [f.antwort for f in exact.falsch] == ["521"]
    third = number_step("b", Fraction(100, 3), "x", falsch=[(Fraction(1001, 30), "zu nah", "rechenfehler")])
    assert third.toleranz > 0 and third.falsch == []
    assert same_answer("zahl", "33,3", third.antwort, third.toleranz)
    small = number_step("c", Fraction(18, 1000), "x")
    assert small.antwort == "0,018" and small.toleranz == 0
