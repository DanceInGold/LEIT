"""Wöchentlicher Mischtest über alle bisher gelernten Themen (WH-03, Interleaving).

Ausgewählt werden Themen, nicht Aufgaben: Schwache Themen mit hohem Prüfungsgewicht
kommen häufiger dran, und dasselbe Thema steht nie zweimal hintereinander. Welche Aufgabe
je Thema gezogen wird, entscheidet die normale Aufgabenauswahl auf der aktuellen Stufe.
"""

from __future__ import annotations

import datetime as dt
import random
from collections.abc import Mapping, Sequence

# Aufgaben pro Mischtest und Abstand zwischen zwei Tests
MIXED_SIZE = 10
MIXED_INTERVAL_DAYS = 7
# Erst ab so vielen gelernten Themen lohnt sich das Mischen
MIN_TOPICS = 2


def topic_weight(exam_weight: float, grad: int | None) -> float:
    """Ziehgewicht eines Themas: Prüfungsgewicht × (1,5 − Beherrschung).

    Nicht geübte Themen zählen wie 0 % Beherrschung; ein Thema mit 100 % behält ein Drittel
    seines Gewichts, damit auch Sicheres gelegentlich wiederkommt.
    """
    return max(exam_weight, 0.01) * (1.5 - (grad or 0) / 100)


def _draw(pool: dict[str, float], rng: random.Random, exclude: str | None) -> str:
    """Zieht ein Thema nach Gewicht, wenn möglich nicht ``exclude``."""
    choices = [t for t in pool if t != exclude] or list(pool)
    return rng.choices(choices, weights=[pool[t] for t in choices])[0]


def mixed_topics(
    weights: Mapping[str, float],
    grades: Mapping[str, int | None],
    rng: random.Random,
    size: int = MIXED_SIZE,
) -> list[str]:
    """Reihenfolge der Themen für einen Mischtest.

    Erst wird jedes Thema höchstens einmal gezogen (so viel Abwechslung wie möglich); reichen die
    Themen nicht, wird nachgezogen – nie dasselbe Thema direkt hintereinander.
    """
    pool = {t: topic_weight(w, grades.get(t)) for t, w in weights.items()}
    if not pool:
        return []
    remaining = dict(pool)
    order: list[str] = []
    while len(order) < size:
        source = remaining or pool
        topic = _draw(source, rng, order[-1] if order else None)
        order.append(topic)
        remaining.pop(topic, None)
    return order


def mixed_test_due(last: dt.date | None, today: dt.date, learned: Sequence[str]) -> bool:
    """Ist ein Mischtest fällig? Ab zwei gelernten Themen, danach alle sieben Tage."""
    if len(learned) < MIN_TOPICS:
        return False
    return last is None or (today - last).days >= MIXED_INTERVAL_DAYS
