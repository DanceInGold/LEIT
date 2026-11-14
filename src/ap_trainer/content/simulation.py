"""Schema der Prüfungssimulationen (PS-01): ein kompletter AP1-Prüfungssatz je Datei.

Aufbau wie die echte AP1: eine Ausgangssituation, vier Aufgaben mit je 20–30 Punkten und
Teilaufgaben, zusammen 100 Punkte in 90 Minuten. Jede Teilaufgabe ist eine normale Aufgabe
(sechs Typen, siehe ``aufgaben.py``) auf Stufe 5 „Prüfungsniveau“ (AU-02).
"""

from __future__ import annotations

from collections.abc import Iterator

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ap_trainer.content.aufgaben import _ID, Aufgabe
from ap_trainer.content.models import Beleg, Status

# Rahmen der AP1 (U-Form-Prüfungstrainer: 100 Punkte, 90 Minuten, vier Aufgaben zu 20–30 Punkten)
TOTAL_POINTS = 100
POINTS_PER_TASK = (20, 30)


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Teilaufgabe(_Strict):
    """Teilaufgabe a), b), … mit Punktzahl; die Aufgabe selbst ist eine normale Aufgabe."""

    nr: str = Field(pattern=r"^[a-z]{1,2}$")
    punkte: int = Field(ge=1, le=30)
    aufgabe: Aufgabe


class SimAufgabe(_Strict):
    """Eine der vier Aufgaben einer Simulation mit eigenem Einstieg."""

    nr: int = Field(ge=1, le=6)
    titel: str
    situation: str | None = None
    teilaufgaben: list[Teilaufgabe] = Field(min_length=1)

    @property
    def punkte(self) -> int:
        """Summe der Teilaufgaben."""
        return sum(t.punkte for t in self.teilaufgaben)


class Simulation(_Strict):
    """Ein vollständiger Prüfungssatz (``simulationen/<id>.yaml``)."""

    id: str
    titel: str
    dauer_minuten: int = Field(default=90, ge=10, le=180)
    # Wer ist der Ausbildungsbetrieb, wer der Kunde, worum geht es? (Markdown)
    ausgangssituation: str
    aufgaben: list[SimAufgabe] = Field(min_length=1)
    quelle: str
    belege: list[Beleg] = Field(default_factory=list)
    status: Status

    @field_validator("id")
    @classmethod
    def _check_id(cls, value: str) -> str:
        if not _ID.match(value):
            raise ValueError("id nur aus Kleinbuchstaben, Ziffern und Bindestrichen")
        return value

    @model_validator(mode="after")
    def _check_points(self) -> Simulation:
        if self.punkte != TOTAL_POINTS:
            raise ValueError(f"Summe der Punkte ist {self.punkte}, erwartet {TOTAL_POINTS}")
        low, high = POINTS_PER_TASK
        for task in self.aufgaben:
            if not low <= task.punkte <= high:
                raise ValueError(f"Aufgabe {task.nr} hat {task.punkte} Punkte, erwartet {low}–{high}")
        return self

    @property
    def punkte(self) -> int:
        """Gesamtpunktzahl (immer 100, siehe Validierung)."""
        return sum(a.punkte for a in self.aufgaben)

    def teile(self) -> Iterator[tuple[SimAufgabe, Teilaufgabe]]:
        """Alle Teilaufgaben in Reihenfolge, jeweils mit ihrer Aufgabe."""
        for task in self.aufgaben:
            for part in task.teilaufgaben:
                yield task, part

    def tasks(self) -> list[Aufgabe]:
        """Alle Teilaufgaben als Aufgaben (für Prüfungen und die Aufgabensuche)."""
        return [part.aufgabe for _task, part in self.teile()]
