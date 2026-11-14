"""Prüfungssimulation (PS-01, PS-02, PS-04): Übersicht, Prüfung mit Timer, Auswertung.

Während der Simulation gibt es keine Hilfen und kein Feedback. Nach der Abgabe zeigt die
Auswertung Punkte je Teilaufgabe, die IHK-Note, Musterlösungen und die Schwachstellen;
Freitexte werden dort selbst bewertet.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

from nicegui import ui

from ap_trainer.content.aufgaben import Freitext, Rechnung
from ap_trainer.content.simulation import Simulation
from ap_trainer.core.simulation import GOAL_COUNT, GOAL_POINTS, SimRun, grade
from ap_trainer.service import Trainer
from ap_trainer.tasks.check import FreitextAntwort
from ap_trainer.ui.exercise import AnswerGetter, ExerciseState, render_inputs
from ap_trainer.ui.layout import frame
from ap_trainer.ui.rich import markdown


def _points(value: float) -> str:
    """Punkte deutsch, halbe Punkte mit Komma."""
    return f"{value:g}".replace(".", ",")


def _goal_banner(trainer: Trainer) -> None:
    reached = trainer.sim_goal()
    with ui.row().classes("items-center gap-2"):
        ui.icon("flag", color="positive" if len(reached) >= GOAL_COUNT else None)
        ui.label(
            f"Ziel: {GOAL_COUNT} verschiedene Simulationen mit mindestens {GOAL_POINTS} Punkten – "
            f"erreicht: {len(reached)} von {GOAL_COUNT}"
        ).classes("font-medium")


# --- Übersicht -----------------------------------------------------------------------
def _overview(trainer: Trainer) -> None:
    ui.label(
        "Wie die echte AP1: eine Ausgangssituation, vier Aufgaben, 100 Punkte, 90 Minuten. Keine Hilfen, "
        "kein Feedback – erst nach der Abgabe kommt die Auswertung. Ein nicht programmierbarer "
        "Taschenrechner ist erlaubt."
    ).classes("text-sm opacity-80")
    _goal_banner(trainer)
    if not trainer.package.simulationen:
        ui.label("Noch keine Simulation im Inhaltspaket.")
    for sim in trainer.package.simulationen.values():
        runs = trainer.sim_runs(sim.id)
        with ui.card().classes("w-full gap-2"):
            ui.label(sim.titel).classes("text-lg font-semibold")
            ui.label(
                f"{len(sim.aufgaben)} Aufgaben · {sim.punkte} Punkte · {sim.dauer_minuten} Minuten"
            ).classes("text-sm opacity-70")
            for run in runs[-3:]:
                note, label = grade(run.punkte)
                status = "" if run.vollstaendig else " · Freitext noch bewerten"
                day = f"{run.beendet.astimezone():%d.%m.%Y}"
                text = f"{day}: {_points(run.punkte)} Punkte, Note {note} ({label})"
                ui.link(text + status, f"/simulation/ergebnis/{run.id}").classes("text-sm")
            ui.button(
                "Simulation starten" if not runs else "Noch einmal",
                icon="timer",
                on_click=lambda s=sim.id: ui.navigate.to(f"/simulation/{s}"),
            )


# --- Prüfung -------------------------------------------------------------------------
@dataclass
class ExamState:
    """Laufende Simulation im Browser."""

    sim: Simulation
    started: dt.datetime = field(default_factory=lambda: dt.datetime.now(dt.UTC))
    getters: dict[str, AnswerGetter] = field(default_factory=dict)
    states: dict[str, ExerciseState] = field(default_factory=dict)
    submitted: bool = False

    def remaining(self) -> int:
        """Restzeit in Sekunden (nicht negativ)."""
        elapsed = (dt.datetime.now(dt.UTC) - self.started).total_seconds()
        return max(0, round(self.sim.dauer_minuten * 60 - elapsed))


def _free_text_input(task: Freitext) -> AnswerGetter:
    """Während der Simulation nur schreiben; bewertet wird nach der Abgabe."""
    if task.operator:
        ui.label(f"Operator: {task.operator}").classes("text-sm opacity-70")
    area = ui.textarea("Deine Antwort").classes("w-full").props("autogrow")
    return lambda: FreitextAntwort(area.value or "", [])


def _exam_body(trainer: Trainer, exam: ExamState) -> None:
    sim = exam.sim
    with ui.card().classes("w-full"):
        ui.label("Ausgangssituation").classes("text-xs uppercase tracking-wide opacity-70")
        markdown(sim.ausgangssituation)
    for task in sim.aufgaben:
        with ui.card().classes("w-full gap-3"):
            ui.label(f"Aufgabe {task.nr}: {task.titel} ({task.punkte} Punkte)").classes(
                "text-lg font-semibold"
            )
            if task.situation:
                markdown(task.situation)
            for part in task.teilaufgaben:
                inner = part.aufgabe
                with ui.column().classes("w-full gap-1 border-t border-gray-500/20 pt-2"):
                    ui.label(f"{part.nr}) {_points(part.punkte)} Punkte").classes("font-medium")
                    if inner.situation:
                        markdown(inner.situation)
                    markdown(inner.frage)
                    state = ExerciseState(task=inner)
                    exam.states[inner.id] = state
                    if isinstance(inner, Freitext):
                        exam.getters[inner.id] = _free_text_input(inner)
                    else:
                        exam.getters[inner.id] = render_inputs(inner, state, lambda: None)


def _submit(trainer: Trainer, exam: ExamState) -> None:
    if exam.submitted:
        return
    exam.submitted = True
    answers = {task_id: getter() for task_id, getter in exam.getters.items()}
    run = trainer.submit_simulation(exam.sim.id, answers, exam.started)
    ui.navigate.to(f"/simulation/ergebnis/{run.id}")


def _exam(trainer: Trainer, sim: Simulation) -> None:
    exam = ExamState(sim=sim)
    with ui.row().classes("items-center gap-3 w-full sticky top-14 z-10 seiten-hintergrund py-2"):
        clock = ui.label().classes("text-xl font-mono font-semibold")
        ui.space()
        confirm = ui.dialog()
        with confirm, ui.card():
            ui.label("Simulation jetzt abgeben? Danach lassen sich die Antworten nicht mehr ändern.")

            def hand_in() -> None:
                confirm.close()
                _submit(trainer, exam)

            with ui.row():
                ui.button("Abgeben", on_click=hand_in)
                ui.button("Weiterarbeiten", on_click=confirm.close).props("flat")
        ui.button("Abgeben", icon="send", on_click=confirm.open)

    def tick() -> None:
        seconds = exam.remaining()
        clock.set_text(f"⏱ {seconds // 60:02d}:{seconds % 60:02d}")
        if seconds <= 300:
            clock.classes("text-negative")
        if seconds == 0:
            ui.notify("Die Zeit ist um – die Simulation wird abgegeben.", type="warning")
            _submit(trainer, exam)

    tick()
    ui.timer(1.0, tick)
    ui.label("Hinweis: Neu laden der Seite verwirft die Antworten.").classes("text-xs opacity-60")
    _exam_body(trainer, exam)


# --- Auswertung ----------------------------------------------------------------------
def _rating(trainer: Trainer, run: SimRun, task: Freitext) -> None:
    """Selbstbewertung eines Freitexts nach der Simulation."""
    ui.label("Hake ehrlich ab, was in deiner Antwort steckt:").classes("font-medium")
    boxes = [
        ui.checkbox(p.punkt + (f" ({p.punkte} P.)" if p.punkte > 1 else "")) for p in task.bewertungspunkte
    ]

    def save() -> None:
        trainer.rate_simulation_text(run.id, task.id, [b.value for b in boxes])
        ui.navigate.reload()

    ui.button("Bewertung speichern", icon="check", on_click=save)


def _part_result(trainer: Trainer, run: SimRun, nr: str, part_id: str) -> None:
    entry = next(t for t in run.teile if t.aufgabe_id == part_id)
    task = trainer.find_task(part_id, entry.thema)
    if task is None:
        return
    share = entry.punkte / entry.max_punkte if entry.max_punkte else 0
    icon, colour = ("check_circle", "positive") if share >= 1 else ("remove_circle", "warning")
    if share == 0:
        icon, colour = "cancel", "negative"
    caption = f"{nr}) {_points(entry.punkte)} von {entry.max_punkte} Punkten"
    if not entry.bewertet:
        caption, icon, colour = (
            f"{nr}) noch selbst bewerten – {entry.max_punkte} Punkte möglich",
            "rate_review",
            "info",
        )
    with (
        ui.expansion(caption, icon=icon, value=not entry.bewertet)
        .classes("w-full border rounded")
        .props(f"header-class=text-{colour}" if colour else "")
    ):
        markdown(task.frage)
        ui.label("Deine Antwort").classes("text-xs uppercase opacity-60")
        markdown(entry.antwort)
        for hint in entry.hinweise:
            with ui.row().classes("items-start gap-1 text-sm"):
                ui.icon("lightbulb", color="warning")
                ui.label(hint)
        if isinstance(task, Freitext):
            ui.label("Musterlösung").classes("text-xs uppercase opacity-60")
            markdown(task.musterloesung)
            if not entry.bewertet:
                _rating(trainer, run, task)
        ui.label("Lösungsweg").classes("text-xs uppercase opacity-60")
        markdown(task.loesungsweg)
        if isinstance(task, Rechnung):
            ui.label(
                "Musterlösung: " + " · ".join(f"{s.antwort} {s.einheit or ''}".strip() for s in task.schritte)
            )


def _result(trainer: Trainer, run: SimRun) -> None:
    sim = trainer.package.simulationen.get(run.sim_id)
    note, label = grade(run.punkte)
    with ui.card().classes("w-full gap-1"):
        ui.label(sim.titel if sim else run.sim_id).classes("text-sm opacity-70")
        ui.label(f"{_points(run.punkte)} von {run.max_punkte} Punkten – Note {note} ({label})").classes(
            "text-2xl font-semibold"
        )
        ui.linear_progress(value=run.punkte / run.max_punkte if run.max_punkte else 0, show_value=False)
        ui.label(f"Bearbeitungszeit: {run.minuten} Minuten").classes("text-sm opacity-70")
        if not run.vollstaendig:
            ui.label("Freitext-Teilaufgaben sind noch nicht bewertet – die Punkte fehlen noch.").classes(
                "text-warning"
            )
    _goal_banner(trainer)
    weak = trainer.sim_weak_topics() if run.vollstaendig else []
    if weak:
        by_id = trainer.package.katalog.by_id()
        with ui.card().classes("w-full gap-1"):
            ui.label("Schwachstellen – kommen auf „Heute“ und in die Wiederholung").classes("font-medium")
            for topic_id in weak:
                ui.link(f"→ {by_id[topic_id].titel}", f"/ueben/{topic_id}")
    if sim is None:
        return
    for task in sim.aufgaben:
        got = sum(t.punkte for t in run.teile if t.aufgabe_id in {p.aufgabe.id for p in task.teilaufgaben})
        ui.label(f"Aufgabe {task.nr}: {task.titel} – {_points(got)} von {task.punkte} Punkten").classes(
            "text-lg font-semibold mt-2"
        )
        for part in task.teilaufgaben:
            _part_result(trainer, run, part.nr, part.aufgabe.id)


def register(trainer: Trainer) -> None:
    """Registriert Übersicht, Prüfung und Auswertung."""

    @ui.page("/simulation")
    def overview_page() -> None:
        with frame("Prüfungssimulation"):
            _overview(trainer)

    @ui.page("/simulation/{sim_id}")
    def exam_page(sim_id: str) -> None:
        sim = trainer.package.simulationen.get(sim_id)
        with frame(sim.titel if sim else "Prüfungssimulation"):
            if sim is None:
                ui.label("Diese Simulation gibt es nicht.")
                ui.link("Zur Übersicht", "/simulation")
                return
            _exam(trainer, sim)

    @ui.page("/simulation/ergebnis/{run_id}")
    def result_page(run_id: int) -> None:
        with frame("Auswertung"):
            try:
                run = trainer.sim_run(int(run_id))
            except KeyError:
                ui.label("Diesen Durchlauf gibt es nicht.")
                ui.link("Zur Übersicht", "/simulation")
                return
            ui.link("← Alle Simulationen", "/simulation")
            _result(trainer, run)
