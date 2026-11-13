"""Datenmodelle der Lernlogik: Einstellungen, Fortschritt und der berechnete Lernplan.

Die Lernlogik bekommt diese Modelle hinein und gibt sie heraus; sie kennt weder
Oberfläche noch Datenbank (Konvention aus Kap. 8 der Anforderungen).
"""

from __future__ import annotations

import datetime as dt
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Phase = Literal["aufbau", "vertiefung", "pruefung"]
TopicState = Literal["offen", "laufend", "fertig"]
Ampel = Literal["im Plan", "knapp", "im Verzug"]

PHASE_NAMES: dict[Phase, str] = {
    "aufbau": "Aufbau",
    "vertiefung": "Vertiefung und Mischtraining",
    "pruefung": "Prüfungsmodus",
}


class _Model(BaseModel):
    model_config = ConfigDict(frozen=True)


class BudgetPeriod(_Model):
    """Ab ``ab`` gilt ein Wochenbudget von ``stunden_pro_woche`` (LP-01)."""

    ab: dt.date
    stunden_pro_woche: float = Field(gt=0, le=80)


class DateRange(_Model):
    """Lernfreier Zeitraum, beide Tage eingeschlossen (Urlaub, Feiertage)."""

    von: dt.date
    bis: dt.date
    bezeichnung: str = ""

    @model_validator(mode="after")
    def _ordered(self) -> DateRange:
        if self.bis < self.von:
            raise ValueError("Ende liegt vor dem Beginn")
        return self

    def contains(self, day: dt.date) -> bool:
        """True, wenn ``day`` im Zeitraum liegt."""
        return self.von <= day <= self.bis


class PlanSettings(_Model):
    """Alles, was der Nutzer für den Lernplan einstellt (LP-01)."""

    pruefungsdatum: dt.date
    lernbeginn: dt.date
    budget: list[BudgetPeriod] = Field(min_length=1)
    # Wochentage mit Lernzeit, 0 = Montag … 6 = Sonntag
    lerntage: list[int] = Field(default=[0, 1, 2, 3, 4], min_length=1)
    lernfrei: list[DateRange] = Field(default_factory=list)
    # LP-11: Faktor > 1, wenn Themen dauerhaft länger dauern als geschätzt
    kalibrierung: float = Field(default=1.0, gt=0.2, lt=5)

    @model_validator(mode="after")
    def _valid(self) -> PlanSettings:
        if any(day not in range(7) for day in self.lerntage):
            raise ValueError("Lerntage müssen zwischen 0 (Montag) und 6 (Sonntag) liegen")
        if self.pruefungsdatum <= self.lernbeginn:
            raise ValueError("Prüfungsdatum muss nach dem Lernbeginn liegen")
        return self

    def hours_per_week(self, day: dt.date) -> float:
        """Wochenbudget, das an ``day`` gilt (letzte Periode mit ``ab <= day``)."""
        valid = [p for p in sorted(self.budget, key=lambda p: p.ab) if p.ab <= day]
        return (valid[-1] if valid else min(self.budget, key=lambda p: p.ab)).stunden_pro_woche


class TopicProgress(_Model):
    """Lernstand eines Themas aus Sicht des Plans."""

    topic_id: str
    zustand: TopicState = "offen"
    # Aus dem Einstufungstest bekannt: Erarbeiten wird verkürzt (LP-02)
    bekannt: bool = False
    minuten: int = Field(default=0, ge=0)


class PlannedTopic(_Model):
    """Ein Thema im Plan mit Zeitbedarf und Zeitraum."""

    topic_id: str
    titel: str
    gewicht: float
    stunden: float
    beginn: dt.date | None = None
    ende: dt.date | None = None
    optional: bool = False

    @property
    def eingeplant(self) -> bool:
        """True, wenn das Thema in der Aufbauphase Platz gefunden hat."""
        return self.beginn is not None


class PlanWeek(_Model):
    """Eine Kalenderwoche des Plans."""

    nummer: int
    montag: dt.date
    phase: Phase
    verfuegbar_h: float
    themen: list[str]


class Feasibility(_Model):
    """Ergebnis der Machbarkeitsprüfung (LP-09)."""

    benoetigt_h: float
    verfuegbar_aufbau_h: float
    verfuegbar_gesamt_h: float
    puffer_h: float
    zusaetzlich_pro_woche_h: float = 0.0
    kuerzung: list[str] = Field(default_factory=list)

    @property
    def machbar(self) -> bool:
        """True, wenn alle offenen Themen in die Aufbauphase passen."""
        return self.puffer_h >= 0


class LearningPlan(_Model):
    """Der vollständige, aus Einstellungen und Fortschritt berechnete Lernplan."""

    erstellt_am: dt.date
    pruefungsdatum: dt.date
    phasenbeginn: dict[Phase, dt.date]
    themen: list[PlannedTopic]
    wochen: list[PlanWeek]
    machbarkeit: Feasibility

    def current_topic(self, done: set[str]) -> PlannedTopic | None:
        """Erstes eingeplantes Thema, das noch nicht fertig ist."""
        return next((t for t in self.themen if t.eingeplant and t.topic_id not in done), None)

    def phase_on(self, day: dt.date) -> Phase:
        """Phase, in der ``day`` liegt."""
        if day >= self.phasenbeginn["pruefung"]:
            return "pruefung"
        if day >= self.phasenbeginn["vertiefung"]:
            return "vertiefung"
        return "aufbau"


class ScheduleStatus(_Model):
    """Wöchentlicher Soll-Ist-Vergleich mit Prognose (LP-10)."""

    ampel: Ampel
    soll_anteil: float
    ist_anteil: float
    prognose: str


class Attempt(_Model):
    """Ein gespeicherter Lösungsversuch einer Aufgabe (Grundlage für AU-06, HI-02, FT-01, FT-04)."""

    aufgabe_id: str
    thema: str
    stufe: int = Field(ge=1, le=5)
    typ: str
    richtig: bool
    anteil: float = Field(ge=0, le=1)
    # 0 = ohne Hilfe, 1–3 = so viele Hinweise, 4 = Lösungsweg vor dem Prüfen geöffnet (HI-02)
    hilfen: int = Field(default=0, ge=0, le=4)
    ursache: str | None = None
    fehlerschritt: int | None = None
    # Eingabe als JSON-Text, damit eine falsche Antwort im Fehlerprotokoll wieder sichtbar ist
    antwort: str = ""
    sekunden: int = Field(default=0, ge=0)
    am: dt.datetime
