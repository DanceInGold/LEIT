"""Die Tagesration für die Startseite „Heute“ (LP-05, WH-02).

Reihenfolge: zuerst fällige Wiederholungen (mit Tagesobergrenze), dann die nächste
Lektion aus dem Plan, dann ein Übungsblock (Aufgaben folgen in Phase 2).
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from ap_trainer.content.models import Lektion
from ap_trainer.core.models import LearningPlan, Phase, PlannedTopic


@dataclass(frozen=True)
class DailyRation:
    """Was heute ansteht."""

    datum: dt.date
    tage_bis_pruefung: int
    phase: Phase
    wiederholungen: int
    thema: PlannedTopic | None
    lektion: Lektion | None
    lektion_fehlt: bool
    minuten_budget: int


def build_ration(
    plan: LearningPlan,
    today: dt.date,
    due_count: int,
    max_reviews: int,
    done_topics: set[str],
    read_lessons: set[str],
    lessons_by_topic: dict[str, list[Lektion]],
    minutes_today: int,
) -> DailyRation:
    """Stellt die Tagesration zusammen.

    ``lektion_fehlt`` ist True, wenn das nächste Thema geplant ist, aber noch keine
    Lektion dafür geschrieben wurde – dann zeigt die Startseite einen Hinweis.
    """
    topic = plan.current_topic(done_topics)
    lesson = None
    if topic:
        candidates = lessons_by_topic.get(topic.topic_id, [])
        lesson = next((les for les in candidates if les.id not in read_lessons), None)
        if lesson is None and candidates:
            lesson = candidates[-1]
    return DailyRation(
        datum=today,
        tage_bis_pruefung=(plan.pruefungsdatum - today).days,
        phase=plan.phase_on(today),
        wiederholungen=min(due_count, max_reviews),
        thema=topic,
        lektion=lesson,
        lektion_fehlt=topic is not None and not lessons_by_topic.get(topic.topic_id),
        minuten_budget=minutes_today,
    )


def minutes_for_day(hours_per_week: float, study_days: list[int], day: dt.date) -> int:
    """Lernminuten für einen Tag aus Wochenbudget und Lerntagen."""
    if day.weekday() not in study_days:
        return 0
    return round(hours_per_week / len(study_days) * 60)
