"""Wochenplan rückwärts von der Prüfung, Machbarkeitsprüfung und Zeitplan-Ampel.

Umsetzung von LP-01, LP-03, LP-04, LP-06 bis LP-10. Der Plan wird bei jedem Aufruf aus
Einstellungen und Fortschritt neu berechnet; verpasste Tage oder ein geändertes Budget
(z. B. Wechsel von 15 auf 30 Stunden) verschieben ihn deshalb automatisch, ohne Neustart.
"""

from __future__ import annotations

import datetime as dt
import heapq
from collections.abc import Iterable

from ap_trainer.content.models import Katalog, Thema
from ap_trainer.core.models import (
    Ampel,
    Feasibility,
    LearningPlan,
    Phase,
    PlannedTopic,
    PlanSettings,
    PlanWeek,
    ScheduleStatus,
    TopicProgress,
)
from ap_trainer.core.weighting import compute_weights

# Anteile der Phasen an der verfügbaren Zeit (LP-04)
PHASE_SHARES: dict[Phase, float] = {"aufbau": 0.60, "vertiefung": 0.25, "pruefung": 0.15}
# Bekannte Themen (Einstufungstest) brauchen nur noch diesen Anteil der Zeit (LP-02)
KNOWN_FACTOR = 0.3


def daily_hours(settings: PlanSettings, start: dt.date) -> list[tuple[dt.date, float]]:
    """Lernstunden je Tag von ``start`` bis zum Vortag der Prüfung."""
    days = []
    day = start
    while day < settings.pruefungsdatum:
        hours = 0.0
        if day.weekday() in settings.lerntage and not any(r.contains(day) for r in settings.lernfrei):
            hours = settings.hours_per_week(day) / len(settings.lerntage)
        days.append((day, hours))
        day += dt.timedelta(days=1)
    return days


def phase_starts(days: list[tuple[dt.date, float]], fallback: dt.date) -> dict[Phase, dt.date]:
    """Erster Tag jeder Phase, gemessen an den kumulierten verfügbaren Stunden."""
    total = sum(h for _, h in days)
    starts: dict[Phase, dt.date] = {"aufbau": days[0][0] if days else fallback}
    limits: list[tuple[Phase, float]] = [
        ("vertiefung", PHASE_SHARES["aufbau"]),
        ("pruefung", PHASE_SHARES["aufbau"] + PHASE_SHARES["vertiefung"]),
    ]
    cumulative = 0.0
    for day, hours in days:
        for phase, share in limits:
            if phase not in starts and total and cumulative >= share * total:
                starts[phase] = day
        cumulative += hours
    for phase, _ in limits:
        starts.setdefault(phase, fallback)
    return starts


def effective_priority(topics: Iterable[Thema], weights: dict[str, float]) -> dict[str, float]:
    """Priorität je Thema: eigenes Gewicht oder das höchste Gewicht eines Themas, das darauf aufbaut.

    So wird eine leichte Voraussetzung (Zahlensysteme) früh gelernt, wenn ein schweres
    Thema (Dateigrößen berechnen) auf ihr aufbaut.
    """
    pool = {t.id: t for t in topics}
    dependents: dict[str, set[str]] = {tid: set() for tid in pool}
    for topic in pool.values():
        for req in topic.voraussetzungen:
            if req in pool:
                dependents[req].add(topic.id)
    priority: dict[str, float] = {}

    def resolve(tid: str) -> float:
        if tid not in priority:
            priority[tid] = weights.get(tid, 0.0)  # Schutz vor Zyklen
            priority[tid] = max([weights.get(tid, 0.0), *(resolve(d) for d in dependents[tid])])
        return priority[tid]

    for tid in pool:
        resolve(tid)
    return priority


def order_topics(topics: Iterable[Thema], weights: dict[str, float]) -> list[Thema]:
    """Sortiert Themen so, dass Voraussetzungen zuerst kommen (LP-03).

    Unter den jeweils lernbaren Themen gewinnt die höhere Priorität (LP-07), damit
    punktstarke Themen früh gelernt und öfter wiederholt werden.
    """
    pool = {t.id: t for t in topics}
    priority = effective_priority(pool.values(), weights)
    missing = {t.id: {r for r in t.voraussetzungen if r in pool} for t in pool.values()}
    heap = [(-priority[tid], tid) for tid, reqs in missing.items() if not reqs]
    heapq.heapify(heap)
    ordered: list[Thema] = []
    while heap:
        _, tid = heapq.heappop(heap)
        ordered.append(pool[tid])
        for other, reqs in missing.items():
            if tid in reqs:
                reqs.discard(tid)
                if not reqs:
                    heapq.heappush(heap, (-priority[other], other))
    return ordered


def needed_hours(topic: Thema, progress: TopicProgress | None, katalog: Katalog, factor: float) -> float:
    """Restbedarf eines Themas in Stunden inklusive Wiederholungszuschlag (LP-08)."""
    hours = (topic.aufwand_h or 0.0) * (1 + katalog.gewichtung.wiederholungszuschlag) * factor
    if progress and progress.bekannt:
        hours *= KNOWN_FACTOR
    if progress:
        hours = max(hours - progress.minuten / 60, 0.25)
    return round(hours, 2)


def _allocate(
    queue: list[PlannedTopic], days: list[tuple[dt.date, float]], until: dt.date
) -> list[PlannedTopic]:
    """Verteilt die Themen der Reihe nach auf die Lerntage der Aufbauphase.

    Ein Thema darf sich über mehrere Tage erstrecken; ein Tag kann mehrere Themen
    enthalten. Was bis zum Beginn der Vertiefung nicht passt, bleibt ohne Zeitraum.
    """
    slot_days = [day for day, hours in days if day < until and hours > 0]
    free = [hours for day, hours in days if day < until and hours > 0]
    cursor = 0
    result: list[PlannedTopic] = []
    for item in queue:
        need = item.stunden
        begin: dt.date | None = None
        end: dt.date | None = None
        while need > 1e-9 and cursor < len(slot_days):
            used = min(need, free[cursor])
            begin, end = begin or slot_days[cursor], slot_days[cursor]
            need -= used
            free[cursor] -= used
            if free[cursor] <= 1e-9:
                cursor += 1
        if need > 1e-9:
            begin = end = None
        result.append(item.model_copy(update={"beginn": begin, "ende": end}))
    return result


def _feasibility(
    topics: list[PlannedTopic], days: list[tuple[dt.date, float]], starts: dict[Phase, dt.date]
) -> Feasibility:
    """Vergleicht Bedarf und Aufbau-Kapazität und schlägt Ausgleich vor (LP-09)."""
    need = sum(t.stunden for t in topics)
    capacity = sum(h for d, h in days if d < starts["vertiefung"])
    total = sum(h for _, h in days)
    buffer = round(capacity - need, 1)
    extra, cut = 0.0, []
    if buffer < 0:
        weeks = max(len(days) / 7, 1)
        extra = round(-buffer / PHASE_SHARES["aufbau"] / weeks, 1)
        missing = -buffer
        for topic in sorted(topics, key=lambda t: (not t.optional, t.gewicht)):
            if missing <= 0:
                break
            cut.append(topic.topic_id)
            missing -= topic.stunden
    return Feasibility(
        benoetigt_h=round(need, 1),
        verfuegbar_aufbau_h=round(capacity, 1),
        verfuegbar_gesamt_h=round(total, 1),
        puffer_h=buffer,
        zusaetzlich_pro_woche_h=extra,
        kuerzung=cut,
    )


def _weeks(
    days: list[tuple[dt.date, float]], topics: list[PlannedTopic], starts: dict[Phase, dt.date]
) -> list[PlanWeek]:
    """Fasst die Tage zu Kalenderwochen (Montag bis Sonntag) zusammen."""
    if not days:
        return []
    monday = days[0][0] - dt.timedelta(days=days[0][0].weekday())
    weeks, number = [], 1
    while monday < days[-1][0] + dt.timedelta(days=1):
        sunday = monday + dt.timedelta(days=6)
        hours = sum(h for d, h in days if monday <= d <= sunday)
        names = [
            t.topic_id for t in topics if t.beginn and t.ende and t.beginn <= sunday and t.ende >= monday
        ]
        anchor = max(monday, days[0][0])
        phase: Phase = "aufbau"
        if anchor >= starts["pruefung"]:
            phase = "pruefung"
        elif anchor >= starts["vertiefung"]:
            phase = "vertiefung"
        weeks.append(
            PlanWeek(nummer=number, montag=monday, phase=phase, verfuegbar_h=round(hours, 1), themen=names)
        )
        monday, number = monday + dt.timedelta(days=7), number + 1
    return weeks


def build_plan(
    katalog: Katalog,
    settings: PlanSettings,
    progress: dict[str, TopicProgress],
    today: dt.date,
) -> LearningPlan:
    """Berechnet den Lernplan ab ``today`` für alle noch nicht fertigen Themen."""
    weights = compute_weights(katalog)
    start = max(today, settings.lernbeginn)
    days = daily_hours(settings, start)
    starts = phase_starts(days, settings.pruefungsdatum)
    done = {tid for tid, p in progress.items() if p.zustand == "fertig"}
    open_topics = [t for t in katalog.themen if t.is_relevant and t.id not in done]
    queue = [
        PlannedTopic(
            topic_id=t.id,
            titel=t.titel,
            gewicht=weights.get(t.id, 0.0),
            stunden=needed_hours(t, progress.get(t.id), katalog, settings.kalibrierung),
            optional=t.stand_2025 == "ausserhalb",
        )
        for t in order_topics(open_topics, weights)
    ]
    planned = _allocate(queue, days, starts["vertiefung"])
    return LearningPlan(
        erstellt_am=today,
        pruefungsdatum=settings.pruefungsdatum,
        phasenbeginn=starts,
        themen=planned,
        wochen=_weeks(days, planned, starts),
        machbarkeit=_feasibility(queue, days, starts),
    )


def schedule_status(
    katalog: Katalog, settings: PlanSettings, progress: dict[str, TopicProgress], today: dt.date
) -> ScheduleStatus:
    """Soll-Ist-Vergleich seit Lernbeginn mit Prognose (LP-10).

    Soll: Anteil der Aufbau-Kapazität, der bis heute verstrichen ist.
    Ist: Anteil des gesamten Themenbedarfs, der erledigt ist.
    """
    all_days = daily_hours(settings, settings.lernbeginn)
    starts = phase_starts(all_days, settings.pruefungsdatum)
    capacity = sum(h for d, h in all_days if d < starts["vertiefung"]) or 1.0
    elapsed = sum(h for d, h in all_days if d < min(today, starts["vertiefung"]))
    relevant = [t for t in katalog.themen if t.is_relevant]
    total = sum(needed_hours(t, None, katalog, settings.kalibrierung) for t in relevant) or 1.0
    done = sum(
        needed_hours(t, None, katalog, settings.kalibrierung)
        for t in relevant
        if progress.get(t.id, TopicProgress(topic_id=t.id)).zustand == "fertig"
    )
    soll, ist = min(elapsed / capacity, 1.0), done / total
    gap = soll - ist
    ampel: Ampel = "im Plan" if gap <= 0.05 else ("knapp" if gap <= 0.15 else "im Verzug")
    if soll <= 0:
        prognose = "Lernzeit hat noch nicht begonnen."
    elif ist == 0:
        prognose = "Noch kein Thema abgeschlossen – markiere erledigte Themen, damit die Prognose greift."
    elif ist / soll >= 0.95:
        prognose = "Das aktuelle Tempo reicht bis zur Prüfung."
    else:
        prognose = (
            f"Bei diesem Tempo schaffst du bis zum Ende der Aufbauphase etwa {ist / soll:.0%} des Stoffs."
        )
    return ScheduleStatus(
        ampel=ampel, soll_anteil=round(soll, 3), ist_anteil=round(ist, 3), prognose=prognose
    )
