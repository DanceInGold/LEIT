"""Auswertung von Prüfungssimulationen (PS-02, PS-04): Punkte, Note, Schwachstellen, Ziel.

Rein rechnerisch: Welche Teilaufgabe wie viele Punkte bringt, entscheidet die normale
Aufgabenbewertung (Anteil 0–1); hier werden daraus Punkte, die IHK-Note, die Schwachstellen
je Thema und der Stand des Ziels „zwei Simulationen mit mindestens 92 Punkten“.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Sequence

from pydantic import BaseModel, Field

# IHK-Notenschlüssel für 100 Punkte (z. B. IHK Pfalz): ab 92 sehr gut, ab 81 gut, …
GRADE_SCALE: tuple[tuple[float, int, str], ...] = (
    (92, 1, "sehr gut"),
    (81, 2, "gut"),
    (67, 3, "befriedigend"),
    (50, 4, "ausreichend"),
    (30, 5, "mangelhaft"),
    (0, 6, "ungenügend"),
)
# Ziel aus dem Anforderungsdokument (Kap. 1): zwei verschiedene Simulationen mit mindestens 92 Punkten
GOAL_POINTS = 92
GOAL_COUNT = 2
# Ein Thema gilt in einer Simulation als Schwachstelle unter 70 % der möglichen Punkte
WEAK_SHARE = 0.7


class TeilErgebnis(BaseModel):
    """Ergebnis einer Teilaufgabe in einem Simulationsdurchlauf."""

    aufgabe_id: str
    thema: str
    max_punkte: int
    punkte: float = 0.0
    # Freitext wird erst nach der Simulation selbst bewertet (AU-05)
    bewertet: bool = True
    antwort: str = ""
    # Erklärungen erkannter Falschantworten (HI-03), für die Auswertung
    hinweise: list[str] = Field(default_factory=list)


class SimRun(BaseModel):
    """Ein abgeschlossener Simulationsdurchlauf."""

    id: int = 0
    sim_id: str
    gestartet: dt.datetime
    beendet: dt.datetime
    teile: list[TeilErgebnis]

    @property
    def punkte(self) -> float:
        """Erreichte Punkte (nur bewertete Teilaufgaben zählen)."""
        return sum(t.punkte for t in self.teile)

    @property
    def max_punkte(self) -> int:
        return sum(t.max_punkte for t in self.teile)

    @property
    def vollstaendig(self) -> bool:
        """Alle Teilaufgaben bewertet (auch die Freitexte)?"""
        return all(t.bewertet for t in self.teile)

    @property
    def minuten(self) -> int:
        """Gebrauchte Zeit in ganzen Minuten."""
        return int((self.beendet - self.gestartet).total_seconds() // 60)


def points(max_points: int, share: float) -> float:
    """Punkte einer Teilaufgabe aus dem Anteil 0–1, auf halbe Punkte gerundet."""
    return round(max(0.0, min(1.0, share)) * max_points * 2) / 2


def grade(total: float) -> tuple[int, str]:
    """IHK-Note und Bezeichnung zu einer Punktzahl von 0–100."""
    for threshold, note, label in GRADE_SCALE:
        if total >= threshold:
            return note, label
    return 6, "ungenügend"


def weak_topics(run: SimRun, share: float = WEAK_SHARE) -> list[str]:
    """Themen unter ``share`` der möglichen Punkte, die meisten verlorenen Punkte zuerst (PS-04)."""
    got: dict[str, float] = {}
    possible: dict[str, int] = {}
    for part in run.teile:
        if not part.bewertet:
            continue
        got[part.thema] = got.get(part.thema, 0.0) + part.punkte
        possible[part.thema] = possible.get(part.thema, 0) + part.max_punkte
    weak = [t for t in possible if got[t] < share * possible[t]]
    return sorted(weak, key=lambda t: (got[t] - possible[t], t))


def goal_reached(runs: Sequence[SimRun], target: float = GOAL_POINTS) -> list[str]:
    """IDs verschiedener Simulationen, die einmal vollständig mit ``target`` Punkten bestanden wurden."""
    return sorted({r.sim_id for r in runs if r.vollstaendig and r.punkte >= target})
