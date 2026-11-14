"""Operatoren-Training (ZI-02): Was verlangt „nennen“, „erläutern“, „beurteilen“ …?

Die Übersichtsseite zeigt alle Operatoren und je Beispiel dieselbe Sache mit jedem Operator
gefragt – mit Musterantwort. Die Trainingsseite übt das Erkennen und Schreiben; sie speichert
keine Versuche, weil sie Prüfungshandwerk übt und nicht das Thema des Beispiels.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from nicegui import ui

from ap_trainer.content.aufgaben import Aufgabe
from ap_trainer.content.operatoren import OperatorenDatei
from ap_trainer.service import Submission, Trainer
from ap_trainer.tasks.check import Antwort
from ap_trainer.ui.exercise import ExerciseState, Runner, run_tasks
from ap_trainer.ui.layout import frame
from ap_trainer.ui.rich import markdown

INTRO = (
    "Der Operator ist das Verb einer Aufgabe. Er bestimmt, wie tief deine Antwort gehen muss: "
    "Wer bei „erläutern“ nur Stichworte liefert, verschenkt Punkte – wer bei „nennen“ einen Aufsatz "
    "schreibt, verschenkt Zeit. In der Prüfung steht die Sie-Form („Nennen Sie …“)."
)


def _overview_table(ops: OperatorenDatei) -> str:
    """Merktabelle aller Operatoren als Markdown."""
    rows = ["| Operator | AB | Was wird verlangt? | Antwortform |", "| --- | :---: | --- | --- |"]
    rows += [f"| **{op.id}** | {op.bereich} | {op.verlangt} | {op.form} |" for op in ops.operatoren]
    return "\n".join(rows)


def _operator_details(ops: OperatorenDatei) -> None:
    """Je Operator aufklappbar: typischer Fehler, Satzanfänge, Prüfpunkte."""
    for op in ops.operatoren:
        with ui.expansion(f"{op.id} – worauf achten?", icon="checklist").classes("w-full"):
            ui.label(f"Typischer Fehler: {op.falle}")
            if op.satzanfaenge:
                ui.label("Satzanfänge: " + " · ".join(op.satzanfaenge)).classes("text-sm opacity-80")
            ui.label("Prüfe deine Antwort:").classes("font-medium mt-1")
            for point in op.kriterien:
                ui.label(f"✓ {point}").classes("text-sm")


def _examples(ops: OperatorenDatei) -> None:
    """Auswahl eines Beispiels; darunter jede Frage mit aufklappbarer Musterantwort."""
    titles = {example.id: example.titel for example in ops.beispiele}
    selected = {"id": ops.beispiele[0].id}

    @ui.refreshable
    def show() -> None:
        example = next(e for e in ops.beispiele if e.id == selected["id"])
        markdown(f"> {example.situation}")
        for op in ops.operatoren:
            item = example.antworten[op.id]
            with ui.card().classes("w-full gap-1"):
                ui.label(f"{op.id} · AB {op.bereich}").classes("leit-meta")
                markdown(item.frage)
                with ui.expansion("Musterantwort", icon="visibility").classes("w-full"):
                    markdown(item.antwort)

    def choose(event: object) -> None:
        selected["id"] = getattr(event, "value", selected["id"])
        show.refresh()

    ui.select(titles, value=selected["id"], label="Beispiel", on_change=choose).classes("w-full")
    show()


@dataclass
class TrainingSession:
    """Ablauf einer Trainingsrunde im Browser."""

    tasks: list[Aufgabe]
    index: int = 0
    results: list[bool] = field(default_factory=list)

    def advance(self) -> Aufgabe | None:
        """Nächste Aufgabe oder ``None`` am Ende."""
        self.index += 1
        return self.tasks[self.index] if self.index < len(self.tasks) else None


def _summary(session: TrainingSession) -> None:
    correct = sum(session.results)
    with ui.card().classes("w-full gap-2"):
        ui.label(f"Runde geschafft: {correct} von {len(session.results)} gelöst").classes(
            "text-xl font-semibold"
        )
        ui.label(
            "Tipp: Lies in Prüfungsaufgaben zuerst den Operator und markiere ihn – er sagt dir, "
            "wie viel du schreiben musst."
        ).classes("text-sm opacity-80")
        with ui.row().classes("gap-2"):
            ui.button("Noch eine Runde", on_click=lambda: ui.navigate.to("/operatoren/training"))
            ui.button("Zur Übersicht", on_click=lambda: ui.navigate.to("/operatoren")).props("flat")


def register(trainer: Trainer) -> None:
    """Registriert Übersicht und Training."""

    @ui.page("/operatoren")
    def operators_page() -> None:
        ops = trainer.package.operatoren
        with frame("Operatoren-Training"):
            if ops is None:
                ui.label("Dieses Inhaltspaket enthält kein Operatoren-Training.")
                return
            ui.label(INTRO).classes("text-sm opacity-80")
            ui.button(
                "Training starten",
                icon="play_arrow",
                on_click=lambda: ui.navigate.to("/operatoren/training"),
            )
            ui.label("Die Operatoren auf einen Blick").classes("leit-section")
            markdown(_overview_table(ops))
            _operator_details(ops)
            ui.label("Eine Situation – jeder Operator").classes("leit-section")
            ui.label(
                "Dieselbe Sache, unterschiedlich gefragt: Vergleiche, wie lang und wie tief die "
                "Musterantworten sind."
            ).classes("text-sm opacity-80")
            _examples(ops)

    @ui.page("/operatoren/training")
    def training_page() -> None:
        with frame("Operatoren-Training"):
            session = TrainingSession(tasks=trainer.operator_training())
            if not session.tasks:
                ui.label("Dieses Inhaltspaket enthält kein Operatoren-Training.")
                return
            state = ExerciseState(task=session.tasks[0])
            state.started = time.monotonic()

            def check(task: Aufgabe, answer: Antwort, _hints: int, seconds: float) -> Submission:
                return trainer.check_operator_task(task, answer, seconds)

            def on_submit(submission: Submission) -> None:
                session.results.append(submission.ergebnis.richtig)

            runner = Runner(
                advance=session.advance,
                topic_title=lambda _task: "Operatoren-Training",
                empty=lambda: _summary(session),
                on_submit=on_submit,
                next_label="Weiter",
                position=lambda: f"Aufgabe {session.index + 1} von {len(session.tasks)}",
                submit=check,
            )
            run_tasks(trainer, state, runner)
