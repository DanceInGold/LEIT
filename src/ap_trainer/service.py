"""Anwendungsschicht: verbindet Inhaltspaket, Lernlogik und Speicher für die Oberfläche.

Die Oberfläche ruft nur diese Klasse auf. So bleibt ``core/`` frei von Speicher und
Oberfläche, und die Abläufe (Lektion gelesen → Karten anlegen → Plan neu rechnen) sind
ohne Browser testbar.
"""

from __future__ import annotations

import datetime as dt
import json
import random
from dataclasses import dataclass
from typing import Any

from ap_trainer.content.aufgaben import Aufgabe
from ap_trainer.content.loader import ContentPackage
from ap_trainer.content.models import Lektion, Thema
from ap_trainer.core import scheduler
from ap_trainer.core.cards import Flashcard, card_index, cards_for_topics
from ap_trainer.core.levels import LevelState, replay
from ap_trainer.core.mastery import Mastery, mastery
from ap_trainer.core.mistakes import MistakeGroup, mistake_log
from ap_trainer.core.models import (
    Attempt,
    BudgetPeriod,
    LearningPlan,
    PlanSettings,
    ScheduleStatus,
    TopicProgress,
)
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
from ap_trainer.tasks.check import Antwort, Ergebnis, FreitextAntwort, evaluate
from ap_trainer.tasks.generators import make, parse_task_id
from ap_trainer.tasks.hints import help_level
from ap_trainer.tasks.selection import TopicPool, pick_task

DEFAULT_MAX_REVIEWS = 60
# Höchstens so viele Sekunden einer Aufgabe zählen als Lernzeit (offen gelassene Aufgaben)
MAX_TASK_SECONDS = 15 * 60


@dataclass(frozen=True)
class PracticeTopic:
    """Ein Thema mit Aufgaben: aktuelle Stufe und bisherige Trefferquote."""

    thema: Thema
    stufe: int
    stufen: list[int]
    versuche: int
    richtig: int


@dataclass(frozen=True)
class Submission:
    """Ergebnis einer abgegebenen Aufgabe mit Stufe vorher und nachher (AU-06)."""

    ergebnis: Ergebnis
    stufe_vorher: int
    stufe_nachher: int


def _answer_json(answer: Antwort) -> str:
    """Antwort als JSON-Text für das Fehlerprotokoll."""
    if isinstance(answer, FreitextAntwort):
        return json.dumps({"text": answer.text, "erfuellt": list(answer.erfuellt)}, ensure_ascii=False)
    if isinstance(answer, frozenset):
        return json.dumps(sorted(answer))
    return json.dumps(list(answer), ensure_ascii=False)


class Trainer:
    """Alle Abläufe des Lernbegleiters für eine Lernstand-Datei."""

    def __init__(self, package: ContentPackage, store: Store) -> None:
        self.package = package
        self.store = store
        self.weights = compute_weights(package.katalog)
        self._cards = card_index(package.begriffe)
        self.pools = {
            topic.id: TopicPool(
                topic.id, package.tasks_for_topic(topic.id), package.generatoren.get(topic.id, [])
            )
            for topic in package.katalog.themen
        }

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

    # --- Üben (AU-01 bis AU-06, HI-01 bis HI-03) -----------------------------------
    def practice_topics(self) -> list[PracticeTopic]:
        """Alle prüfungsrelevanten Themen mit Aufgaben, in Katalogreihenfolge."""
        result = []
        for topic in self.package.katalog.themen:
            pool = self.pools[topic.id]
            if pool.is_empty() or not topic.is_relevant:
                continue
            attempts = self.store.attempts(topic.id)
            result.append(
                PracticeTopic(
                    thema=topic,
                    stufe=self.level(topic.id).stufe,
                    stufen=pool.levels(),
                    versuche=len(attempts),
                    richtig=sum(a.richtig for a in attempts),
                )
            )
        return result

    def level(self, topic_id: str) -> LevelState:
        """Aktuelle Stufe eines Themas, aus allen Versuchen nachgespielt (AU-06)."""
        attempts = self.store.attempts(topic_id)
        return replay(((a.richtig, a.hilfen) for a in attempts), self.pools[topic_id].levels())

    def next_task(self, topic_id: str, rng: random.Random | None = None) -> Aufgabe | None:
        """Nächste Aufgabe für ein Thema auf seiner aktuellen Stufe."""
        pool = self.pools.get(topic_id)
        if pool is None or pool.is_empty():
            return None
        recent = [a.aufgabe_id for a in self.store.attempts(topic_id)]
        return pick_task(pool, self.level(topic_id).stufe, recent, rng or random.Random())

    def find_task(self, task_id: str, topic_id: str) -> Aufgabe | None:
        """Eine bestimmte Aufgabe: fest aus dem Paket oder per Generator-ID nachgebaut."""
        if task_id in self.package.aufgaben:
            fixed = self.package.aufgaben[task_id]
            return fixed if fixed.thema == topic_id else None
        parsed = parse_task_id(task_id)
        pool = self.pools.get(topic_id)
        if parsed is None or pool is None or parsed[0] not in pool.generatoren:
            return None
        generator_id, stufe, seed = parsed
        return make(generator_id, stufe, seed, topic_id)

    def submit(
        self,
        task: Aufgabe,
        answer: Antwort,
        hints_opened: int = 0,
        seconds: float = 0,
        now: dt.datetime | None = None,
    ) -> Submission:
        """Bewertet eine Antwort, speichert den Versuch und die Lernzeit, liefert die neue Stufe."""
        moment = now or dt.datetime.now(dt.UTC)
        before = self.level(task.thema).stufe
        result = evaluate(task, answer)
        counted = round(min(max(seconds, 0), MAX_TASK_SECONDS))
        self.store.log_attempt(
            Attempt(
                aufgabe_id=task.id,
                thema=task.thema,
                stufe=task.stufe,
                typ=task.typ,
                richtig=result.richtig,
                anteil=round(result.anteil, 4),
                hilfen=help_level(task, hints_opened),
                ursache=result.ursache,
                fehlerschritt=result.fehlerschritt,
                antwort=_answer_json(answer),
                sekunden=counted,
                am=moment,
            )
        )
        if counted:
            self.store.log_study(0, "uebung", task.id, day=moment.date(), sekunden=counted)
        progress = self.store.progress().get(task.thema, TopicProgress(topic_id=task.thema))
        if progress.zustand == "offen":
            self.store.set_progress(progress.model_copy(update={"zustand": "laufend"}))
        return Submission(result, before, self.level(task.thema).stufe)

    # --- Fortschritt (FT-01, FT-02, FT-04) -----------------------------------------
    def masteries(self, now: dt.datetime | None = None) -> dict[str, Mastery]:
        """Beherrschungsgrad aller prüfungsrelevanten Themen mit Aufgaben (FT-01)."""
        moment = now or dt.datetime.now(dt.UTC)
        by_topic: dict[str, list[Attempt]] = {}
        for attempt in self.store.attempts():
            by_topic.setdefault(attempt.thema, []).append(attempt)
        result = {}
        for topic in self.package.katalog.themen:
            pool = self.pools[topic.id]
            if pool.is_empty() or not topic.is_relevant:
                continue
            result[topic.id] = mastery(by_topic.get(topic.id, []), max(pool.levels()), moment)
        return result

    def mastery(self, topic_id: str, now: dt.datetime | None = None) -> Mastery:
        """Beherrschungsgrad eines Themas; ohne Aufgaben „noch nicht geübt“."""
        pool = self.pools.get(topic_id)
        if pool is None or pool.is_empty():
            return Mastery(grad=None)
        return mastery(self.store.attempts(topic_id), max(pool.levels()), now or dt.datetime.now(dt.UTC))

    def mistakes(self, include_fixed: bool = True) -> list[MistakeGroup]:
        """Fehlerprotokoll, gruppiert nach Fehlerursache (FT-04)."""
        return mistake_log(self.store.attempts(), include_fixed)

    def task_title(self, task_id: str, topic_id: str) -> str:
        """Titel einer festen oder generierten Aufgabe; die ID, falls sie nicht mehr existiert."""
        task = self.find_task(task_id, topic_id)
        return task.titel if task is not None else task_id

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
