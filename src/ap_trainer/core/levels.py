"""Stufensteuerung beim Üben (AU-06) unter Berücksichtigung der Hilfen (HI-02).

Die Stufe eines Themas wird aus der Liste der bisherigen Versuche nachgespielt, statt sie
gesondert zu speichern – so bleibt sie nach einem Import oder einer Regeländerung stimmig.

Regeln:

- **Sicher gelöst** heißt: richtig und höchstens Hinweis 1 („Richtung“) genutzt.
- Drei sicher gelöste Aufgaben in Folge → eine Stufe höher.
- Zwei falsche Aufgaben in Folge → eine Stufe tiefer.
- Richtig, aber mit mehr Hilfe gelöst, zählt weder als Erfolg noch als Fehler; die Serie
  richtiger Antworten beginnt danach neu („gelöst mit Hilfe ≠ sicher“).
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

UP_AFTER = 3
DOWN_AFTER = 2
# Höchste Hilfestufe, bei der eine richtige Lösung noch als sicher gilt
MAX_HELP_FOR_SUCCESS = 1


@dataclass(frozen=True)
class LevelState:
    """Aktuelle Stufe und die laufenden Serien."""

    stufe: int
    richtig_in_folge: int = 0
    falsch_in_folge: int = 0


def is_secure(correct: bool, help_used: int) -> bool:
    """True, wenn eine Aufgabe ohne nennenswerte Hilfe richtig gelöst wurde."""
    return correct and help_used <= MAX_HELP_FOR_SUCCESS


def _neighbour(levels: Sequence[int], current: int, direction: int) -> int:
    """Nächste vorhandene Stufe nach oben (+1) oder unten (−1); sonst die aktuelle."""
    candidates = [s for s in levels if (s - current) * direction > 0]
    if not candidates:
        return current
    return min(candidates) if direction > 0 else max(candidates)


def apply_attempt(state: LevelState, correct: bool, help_used: int, levels: Sequence[int]) -> LevelState:
    """Neuer Zustand nach einem Versuch."""
    if is_secure(correct, help_used):
        streak = state.richtig_in_folge + 1
        if streak >= UP_AFTER:
            return LevelState(_neighbour(levels, state.stufe, +1))
        return LevelState(state.stufe, streak, 0)
    if correct:
        return LevelState(state.stufe, 0, 0)
    misses = state.falsch_in_folge + 1
    if misses >= DOWN_AFTER:
        return LevelState(_neighbour(levels, state.stufe, -1))
    return LevelState(state.stufe, 0, misses)


def replay(attempts: Iterable[tuple[bool, int]], levels: Sequence[int]) -> LevelState:
    """Stufe nach allen Versuchen ``(richtig, Hilfestufe)`` in zeitlicher Reihenfolge.

    ``levels`` sind die Stufen, für die es Aufgaben gibt; begonnen wird bei der kleinsten.
    """
    ordered = sorted(set(levels)) or [1]
    state = LevelState(ordered[0])
    for correct, help_used in attempts:
        state = apply_attempt(state, correct, help_used, ordered)
    return state
