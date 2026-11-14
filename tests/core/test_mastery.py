"""Tests für den Beherrschungsgrad (FT-01) und die Ampel (FT-02)."""

from __future__ import annotations

import datetime as dt

import pytest

from ap_trainer.core.mastery import Mastery, attempt_score, mastery, quality, reach, recency
from ap_trainer.core.models import Attempt

NOW = dt.datetime(2027, 1, 10, 12, 0, tzinfo=dt.UTC)


def _attempt(
    stufe: int, richtig: bool, hilfen: int = 0, anteil: float | None = None, days_ago: float = 0
) -> Attempt:
    return Attempt(
        aufgabe_id=f"a{stufe}",
        thema="t",
        stufe=stufe,
        typ="rechnung",
        richtig=richtig,
        anteil=anteil if anteil is not None else float(richtig),
        hilfen=hilfen,
        am=NOW - dt.timedelta(days=days_ago),
    )


def test_not_practised_is_grey() -> None:
    value = mastery([], 4, NOW)
    assert value.grad is None and value.ampel == "grau"


def test_help_and_partial_credit_reduce_score() -> None:
    assert attempt_score(_attempt(1, True)) == 1.0
    assert attempt_score(_attempt(1, True, hilfen=2)) == 0.7
    assert attempt_score(_attempt(1, True, hilfen=4)) == 0.2
    assert attempt_score(_attempt(1, False, anteil=0.5)) == 0.5


def test_quality_weights_by_level_and_uses_recent_attempts() -> None:
    # Stufe 1 richtig, Stufe 3 falsch: (1·1 + 3·0) / 4 = 0,25
    assert quality([_attempt(1, True), _attempt(3, False)]) == pytest.approx(0.25)
    # Alte Fehler fallen aus dem Fenster der letzten zehn Versuche
    history = [_attempt(2, False)] * 5 + [_attempt(2, True)] * 10
    assert quality(history) == 1.0


def test_reach_needs_secure_success_on_high_levels() -> None:
    assert reach([_attempt(4, True, hilfen=3)], 4) == 0.5  # mit viel Hilfe: nicht sicher
    assert reach([_attempt(1, True)], 4) == pytest.approx(0.625)
    assert reach([_attempt(4, True, hilfen=1)], 4) == 1.0


def test_recency_decays_after_a_week() -> None:
    assert recency([_attempt(1, True, days_ago=3)], NOW) == 1.0
    assert recency([_attempt(1, True, days_ago=37)], NOW) == pytest.approx(0.8)
    assert recency([_attempt(1, False)], NOW) == 0.6
    naive = _attempt(1, True).model_copy(update={"am": NOW.replace(tzinfo=None)})
    assert recency([naive], NOW) == 1.0


@pytest.mark.parametrize(
    ("attempts", "grad", "ampel"),
    [
        ([_attempt(4, True)] * 3, 100, "grün"),
        ([_attempt(1, True)] * 3, 62, "gelb"),  # 1 × 0,625 × 1 = 62,5 → 62 (Banker's Rounding)
        ([_attempt(2, False)] * 3, 0, "rot"),
        ([_attempt(4, True, days_ago=67)], 70, "gelb"),  # Frische 0,7 nach 60 Tagen über der Schonfrist
    ],
)
def test_mastery_combines_components(attempts: list[Attempt], grad: int, ampel: str) -> None:
    value = mastery(attempts, 4, NOW)
    assert value.grad == grad and value.ampel == ampel
    assert value.versuche == len(attempts)


def test_ampel_thresholds() -> None:
    assert Mastery(grad=80).ampel == "grün"
    assert Mastery(grad=79).ampel == "gelb"
    assert Mastery(grad=50).ampel == "gelb"
    assert Mastery(grad=49).ampel == "rot"
