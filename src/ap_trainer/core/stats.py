"""Auswertungen für den analytischen Überblick auf der Startseite.

Reine Funktionen: Sie bekommen Plan-Einstellungen, Katalog, Fortschritt und Rohdaten
(Lernzeit je Tag, Fälligkeiten) und liefern fertige Zahlenreihen für die Diagramme.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from ap_trainer.content.models import Katalog
from ap_trainer.core.models import PlanSettings, TopicProgress
from ap_trainer.core.planner import daily_hours, needed_hours


@dataclass(frozen=True)
class TimeSeries:
    """Kumulierte Soll- und Ist-Lernstunden je Tag."""

    tage: list[dt.date]
    soll: list[float]
    ist: list[float | None]  # None für Tage in der Zukunft


@dataclass(frozen=True)
class AreaProgress:
    """Lernstand eines Prüfungsbereichs in Stunden."""

    bereich_id: str
    bereich: str
    erledigt_h: float
    begonnen_h: float
    offen_h: float

    @property
    def anteil(self) -> float:
        """Erledigter Anteil 0…1 (begonnene Themen zählen anteilig über die gelernte Zeit)."""
        total = self.erledigt_h + self.begonnen_h + self.offen_h
        return self.erledigt_h / total if total else 0.0


@dataclass(frozen=True)
class Kpis:
    """Kennzahlen für die obere Leiste der Startseite."""

    tage_bis_pruefung: int
    fortschritt: float  # Anteil des gesamten Themenbedarfs, der erledigt ist
    woche_ist_h: float
    woche_soll_h: float
    karten_faellig: int


def study_curve(settings: PlanSettings, minutes: dict[dt.date, float], today: dt.date) -> TimeSeries:
    """Kumulierte geplante Lernzeit (laut Budget) gegen tatsächlich gelernte Zeit."""
    days = daily_hours(settings, settings.lernbeginn)
    tage, soll, ist = [], [], []
    plan_sum = done_sum = 0.0
    for day, hours in days:
        plan_sum += hours
        done_sum += minutes.get(day, 0.0) / 60
        tage.append(day)
        soll.append(round(plan_sum, 1))
        ist.append(round(done_sum, 1) if day <= today else None)
    return TimeSeries(tage, soll, ist)


def area_progress(
    katalog: Katalog, progress: dict[str, TopicProgress], factor: float = 1.0
) -> list[AreaProgress]:
    """Erledigte, begonnene und offene Stunden je Prüfungsbereich."""
    result = []
    for bereich in katalog.bereiche:
        done = started = open_ = 0.0
        for topic in katalog.themen:
            if topic.bereich != bereich.id or topic.stand_2025 in ("entfallen", "ausserhalb"):
                continue
            need = needed_hours(topic, None, katalog, factor)
            state = progress.get(topic.id, TopicProgress(topic_id=topic.id))
            if state.zustand == "fertig":
                done += need
            else:
                learned = min(state.minuten / 60, need)
                started += learned
                open_ += need - learned
        result.append(
            AreaProgress(bereich.id, bereich.name, round(done, 1), round(started, 1), round(open_, 1))
        )
    return result


def daily_minutes(
    minutes: dict[dt.date, float], today: dt.date, days: int = 14
) -> list[tuple[dt.date, float]]:
    """Lernminuten der letzten ``days`` Tage, heute zuletzt."""
    start = today - dt.timedelta(days=days - 1)
    return [(start + dt.timedelta(n), round(minutes.get(start + dt.timedelta(n), 0.0))) for n in range(days)]


def review_forecast(due: list[dt.datetime], now: dt.datetime, days: int = 7) -> list[tuple[dt.date, int]]:
    """Fällige Karten je Tag für die nächsten ``days`` Tage; Überfälliges zählt zu heute."""
    today = now.date()
    counts = {today + dt.timedelta(n): 0 for n in range(days)}
    for moment in due:
        day = max(moment.date(), today)
        if day in counts:
            counts[day] += 1
    return sorted(counts.items())


def kpis(
    katalog: Katalog,
    settings: PlanSettings,
    progress: dict[str, TopicProgress],
    minutes: dict[dt.date, float],
    due_now: int,
    today: dt.date,
) -> Kpis:
    """Kennzahlen: Countdown, Gesamtfortschritt, Lernzeit dieser Woche, fällige Karten."""
    areas = area_progress(katalog, progress, settings.kalibrierung)
    total = sum(a.erledigt_h + a.begonnen_h + a.offen_h for a in areas) or 1.0
    monday = today - dt.timedelta(days=today.weekday())
    week_done = sum(m for d, m in minutes.items() if monday <= d <= today) / 60
    return Kpis(
        tage_bis_pruefung=(settings.pruefungsdatum - today).days,
        fortschritt=round(sum(a.erledigt_h for a in areas) / total, 3),
        woche_ist_h=round(week_done, 1),
        woche_soll_h=settings.hours_per_week(today),
        karten_faellig=due_now,
    )
