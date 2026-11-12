"""Wiederholung nach FSRS für Lernkarten (WH-01, WH-02).

Dünne Hülle um das Paket ``fsrs``: Der Kartenzustand wird als JSON-Wörterbuch
gespeichert, damit Speicher und Oberfläche das Paket nicht kennen müssen.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Any, Literal, cast

from fsrs import Card, Rating, Scheduler

# Bewertung aus Sicht des Lernenden; Zahl = Taste in der Oberfläche (NF-05).
Grade = Literal[1, 2, 3, 4]
GRADE_LABELS: dict[int, str] = {1: "Nochmal", 2: "Schwer", 3: "Gut", 4: "Leicht"}

_RATINGS = {1: Rating.Again, 2: Rating.Hard, 3: Rating.Good, 4: Rating.Easy}


@dataclass(frozen=True)
class CardState:
    """Gespeicherter Zustand einer Karte: fällig ab ``due``, FSRS-Daten in ``data``."""

    due: dt.datetime
    data: dict[str, Any]


def _scheduler() -> Scheduler:
    # Standardparameter von FSRS; Zielbehaltensrate 90 % (Paketvorgabe).
    return Scheduler()


def new_card(now: dt.datetime | None = None) -> CardState:
    """Neue Karte, sofort fällig."""
    card = Card()
    if now is not None:
        card.due = now
    return CardState(due=card.due, data=dict(card.to_dict()))


def review(state: CardState, grade: Grade, now: dt.datetime | None = None) -> CardState:
    """Bewertet eine Karte und liefert den neuen Zustand mit nächstem Fälligkeitstermin."""
    card = Card.from_dict(cast(Any, state.data))
    moment = now or dt.datetime.now(dt.UTC)
    updated, _log = _scheduler().review_card(card, _RATINGS[grade], review_datetime=moment)
    return CardState(due=updated.due, data=dict(updated.to_dict()))
