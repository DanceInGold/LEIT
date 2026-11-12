"""Anwendungsschicht: verbindet Inhaltspaket, Lernlogik und Speicher für die Oberfläche.

Die Oberfläche ruft nur diese Klasse auf. So bleibt ``core/`` frei von Speicher und
Oberfläche, und die Abläufe (Lektion gelesen → Karten anlegen → Plan neu rechnen) sind
ohne Browser testbar.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

from ap_trainer.content.loader import ContentPackage
from ap_trainer.content.models import Lektion
from ap_trainer.core import scheduler
from ap_trainer.core.cards import Flashcard, card_index, cards_for_topics
from ap_trainer.core.models import BudgetPeriod, LearningPlan, PlanSettings, ScheduleStatus, TopicProgress
from ap_trainer.core.planner import build_plan, schedule_status
from ap_trainer.core.stats import (
    AreaProgress,
    Kpis,
    TimeSeries,
    area_progress,
    daily_minutes,
    kpis,
    review_forecast,
    study_curve,
)
from ap_trainer.core.today import DailyRation, build_ration, minutes_for_day
from ap_trainer.core.weighting import compute_weights
from ap_trainer.storage.db import Store

DEFAULT_MAX_REVIEWS = 60


class Trainer:
    """Alle Abläufe des Lernbegleiters für eine Lernstand-Datei."""

    def __init__(self, package: ContentPackage, store: Store) -> None:
        self.package = package
        self.store = store
        self.weights = compute_weights(package.katalog)
        self._cards = card_index(package.begriffe)

    # --- Einstellungen -----------------------------------------------------------
    def default_settings(self, today: dt.date) -> PlanSettings:
        """Vorbelegung beim ersten Start: Termin aus dem Paket, 15 Std./Woche, Mo–Fr."""
        future = [t.datum for t in self.package.paket.pruefungstermine if t.datum > today]
        exam = future[0] if future else today + dt.timedelta(weeks=12)
        return PlanSettings(
            pruefungsdatum=exam,
            lernbeginn=today,
            budget=[BudgetPeriod(ab=today, stunden_pro_woche=15)],
        )

    def settings(self, today: dt.date | None = None) -> PlanSettings:
        """Gespeicherte Plan-Einstellungen oder die Vorbelegung."""
        return self.store.load_plan_settings() or self.default_settings(today or dt.date.today())

    def is_configured(self) -> bool:
        """True, wenn der Nutzer seine Einstellungen schon gespeichert hat."""
        return self.store.load_plan_settings() is not None

    def save_settings(self, settings: PlanSettings) -> None:
        """Speichert neue Einstellungen; der Plan rechnet sich beim nächsten Abruf neu."""
        self.store.save_plan_settings(settings)

    @property
    def max_reviews(self) -> int:
        """Obergrenze für Wiederholungen pro Tag (WH-02)."""
        value: int = self.store.get_setting("max_wiederholungen", DEFAULT_MAX_REVIEWS)
        return value

    # --- Plan und Tagesration ----------------------------------------------------
    def done_topics(self) -> set[str]:
        """IDs aller abgeschlossenen Themen."""
        return {tid for tid, p in self.store.progress().items() if p.zustand == "fertig"}

    def plan(self, today: dt.date | None = None) -> LearningPlan:
        """Aktueller Lernplan ab heute."""
        day = today or dt.date.today()
        return build_plan(self.package.katalog, self.settings(day), self.store.progress(), day)

    def status(self, today: dt.date | None = None) -> ScheduleStatus:
        """Zeitplan-Ampel (LP-10)."""
        day = today or dt.date.today()
        return schedule_status(self.package.katalog, self.settings(day), self.store.progress(), day)

    def ration(self, now: dt.datetime | None = None) -> DailyRation:
        """Tagesration für die Startseite (LP-05)."""
        moment = now or dt.datetime.now(dt.UTC)
        day = moment.date()
        settings = self.settings(day)
        lessons = {t.id: self.package.lessons_for_topic(t.id) for t in self.package.katalog.themen}
        return build_ration(
            plan=self.plan(day),
            today=day,
            due_count=self.store.count_due(moment),
            max_reviews=self.max_reviews,
            done_topics=self.done_topics(),
            read_lessons=self.store.read_lessons(),
            lessons_by_topic=lessons,
            minutes_today=minutes_for_day(settings.hours_per_week(day), settings.lerntage, day),
        )

    # --- Lektionen und Themen ----------------------------------------------------
    def mark_lesson_read(self, lesson: Lektion, minutes: int, now: dt.datetime | None = None) -> int:
        """Lektion als gelesen markieren, Thema auf „laufend“, Karten anlegen.

        Gibt die Zahl neu angelegter Lernkarten zurück.
        """
        self.store.mark_lesson_read(lesson.id)
        self.store.log_study(minutes, "lektion", lesson.id)
        progress = self.store.progress()
        share = max(minutes // len(lesson.themen), 1)
        for topic_id in lesson.themen:
            current = progress.get(topic_id, TopicProgress(topic_id=topic_id))
            zustand = "laufend" if current.zustand == "offen" else current.zustand
            self.store.set_progress(
                current.model_copy(update={"zustand": zustand, "minuten": current.minuten + share})
            )
        return self._introduce_cards(set(lesson.themen), now)

    def set_topic_done(self, topic_id: str, done: bool = True) -> None:
        """Thema als abgeschlossen markieren (oder zurücksetzen)."""
        current = self.store.progress().get(topic_id, TopicProgress(topic_id=topic_id))
        self.store.set_progress(current.model_copy(update={"zustand": "fertig" if done else "laufend"}))

    def _introduce_cards(self, topic_ids: set[str], now: dt.datetime | None) -> int:
        existing = self.store.card_ids()
        new = [c for c in cards_for_topics(self.package.begriffe, topic_ids) if c.card_id not in existing]
        for card in new:
            state = scheduler.new_card(now)
            self.store.put_card(card.card_id, state.due, state.data)
        return len(new)

    # --- Wiederholung ------------------------------------------------------------
    def due_cards(self, now: dt.datetime | None = None) -> list[Flashcard]:
        """Fällige Karten für die heutige Sitzung, höchstens ``max_reviews``."""
        moment = now or dt.datetime.now(dt.UTC)
        ids = self.store.due_cards(moment, self.max_reviews)
        return [self._cards[i] for i in ids if i in self._cards]

    def grade(
        self, card_id: str, grade: scheduler.Grade, now: dt.datetime | None = None, seconds: float = 0
    ) -> dt.datetime:
        """Bewertet eine Karte und gibt den nächsten Fälligkeitstermin zurück.

        ``seconds`` ist die Zeit, die die Karte auf dem Bildschirm war (höchstens 3 Minuten
        werden gezählt, damit eine offen gelassene Karte die Statistik nicht verfälscht).
        """
        moment = now or dt.datetime.now(dt.UTC)
        if seconds > 0:
            self.store.log_study(
                0, "wiederholung", card_id, day=moment.date(), sekunden=round(min(seconds, 180))
            )
        stored = self.store.get_card(card_id)
        if stored is None:
            raise KeyError(card_id)
        state = scheduler.review(scheduler.CardState(*stored), grade, moment)
        self.store.put_card(card_id, state.due, state.data)
        self.store.log_review(card_id, grade, moment)
        return state.due

    # --- Überblick ---------------------------------------------------------------
    def kpis(self, now: dt.datetime | None = None) -> Kpis:
        """Kennzahlen für die Startseite."""
        moment = now or dt.datetime.now(dt.UTC)
        day = moment.date()
        return kpis(
            self.package.katalog,
            self.settings(day),
            self.store.progress(),
            self.store.minutes_by_day(),
            self.store.count_due(moment),
            day,
        )

    def study_curve(self, today: dt.date | None = None) -> TimeSeries:
        """Kumulierte Soll- und Ist-Lernzeit seit Lernbeginn."""
        day = today or dt.date.today()
        return study_curve(self.settings(day), self.store.minutes_by_day(), day)

    def area_progress(self) -> list[AreaProgress]:
        """Fortschritt je Prüfungsbereich."""
        return area_progress(self.package.katalog, self.store.progress(), self.settings().kalibrierung)

    def daily_target_minutes(self, today: dt.date | None = None) -> int:
        """Geplante Minuten an einem Lerntag der laufenden Woche (Ziellinie im Diagramm)."""
        day = today or dt.date.today()
        settings = self.settings(day)
        return round(settings.hours_per_week(day) / len(settings.lerntage) * 60)

    def daily_minutes(self, today: dt.date | None = None) -> list[tuple[dt.date, float]]:
        """Lernminuten der letzten 14 Tage."""
        return daily_minutes(self.store.minutes_by_day(), today or dt.date.today())

    def review_forecast(self, now: dt.datetime | None = None) -> list[tuple[dt.date, int]]:
        """Fällige Karten der nächsten 7 Tage."""
        return review_forecast(self.store.card_due_dates(), now or dt.datetime.now(dt.UTC))

    # --- Export ------------------------------------------------------------------
    def export(self) -> dict[str, Any]:
        """Lernstand als JSON-fähiges Wörterbuch."""
        return self.store.export_json()

    def import_(self, data: dict[str, Any]) -> None:
        """Lernstand aus einem Export übernehmen."""
        self.store.import_json(data)
