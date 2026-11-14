"""Wöchentlicher Mischtest (WH-03): zehn Aufgaben quer durch alle gelernten Themen.

Die Aufgaben werden wie beim normalen Üben bewertet und zählen für Stufe und Beherrschung.
Am Ende stehen das Ergebnis und die Themen, bei denen es gehakt hat.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from nicegui import ui

from ap_trainer.content.aufgaben import Aufgabe
from ap_trainer.core.mixed import MIN_TOPICS, MIXED_SIZE
from ap_trainer.service import Submission, Trainer
from ap_trainer.ui.exercise import ExerciseState, Runner, run_tasks
from ap_trainer.ui.layout import frame


@dataclass
class MixedSession:
    """Ablauf eines Mischtests im Browser."""

    tasks: list[Aufgabe]
    index: int = 0
    results: list[tuple[str, bool]] = field(default_factory=list)
    finished: bool = False

    def advance(self) -> Aufgabe | None:
        """Nächste Aufgabe oder ``None`` am Ende."""
        self.index += 1
        return self.tasks[self.index] if self.index < len(self.tasks) else None


def _summary(trainer: Trainer, session: MixedSession) -> None:
    """Ergebnis am Ende; beim ersten Anzeigen wird der Test als erledigt gespeichert."""
    correct = sum(ok for _topic, ok in session.results)
    total = len(session.results)
    if not session.finished:
        trainer.finish_mixed_test(correct, total)
        session.finished = True
    by_id = trainer.package.katalog.by_id()
    with ui.card().classes("w-full gap-2"):
        ui.label(f"Mischtest geschafft: {correct} von {total} richtig").classes("text-xl font-semibold")
        ui.linear_progress(value=correct / total if total else 0, show_value=False)
        weak = sorted({topic for topic, ok in session.results if not ok})
        if weak:
            ui.label("Hier lohnt sich noch Übung:").classes("font-medium")
            for topic_id in weak:
                title = by_id[topic_id].titel if topic_id in by_id else topic_id
                ui.link(f"→ {title}", f"/ueben/{topic_id}")
        else:
            ui.label("Alles richtig – stark!")
        ui.label("Falsch gelöste Aufgaben liegen jetzt als Fehlerkarten in der Wiederholung.").classes(
            "text-sm opacity-70"
        )
        with ui.row().classes("gap-2"):
            ui.button("Zum Fortschritt", on_click=lambda: ui.navigate.to("/fortschritt"))
            ui.button("Zu Heute", on_click=lambda: ui.navigate.to("/")).props("flat")


def register(trainer: Trainer) -> None:
    """Registriert die Mischtest-Seite."""

    @ui.page("/mischtest")
    def mixed_page() -> None:
        learned = trainer.learned_topics()
        with frame("Mischtest"):
            last = trainer.mixed_test_last()
            ui.label(
                f"{MIXED_SIZE} Aufgaben quer durch alle Themen, die du schon begonnen hast – schwache Themen "
                "kommen öfter dran. Einmal pro Woche festigt das Wissen besser als Üben am Stück."
            ).classes("text-sm opacity-80")
            if last is not None:
                ui.label(f"Letzter Mischtest: {last:%d.%m.%Y}").classes("text-sm opacity-70")
            if len(learned) < MIN_TOPICS:
                ui.label(
                    f"Der Mischtest lohnt sich ab {MIN_TOPICS} begonnenen Themen. Lies ein Kapitel oder "
                    "übe ein weiteres Thema."
                )
                return
            session = MixedSession(tasks=trainer.mixed_test())
            if not session.tasks:
                ui.label("Für deine Themen gibt es gerade keine Aufgaben.")
                return
            state = ExerciseState(task=session.tasks[0] if session.tasks else None)
            by_id = trainer.package.katalog.by_id()

            def on_submit(submission: Submission) -> None:
                task = session.tasks[session.index]
                session.results.append((task.thema, submission.ergebnis.richtig))

            runner = Runner(
                advance=session.advance,
                topic_title=lambda t: by_id[t.thema].titel if t.thema in by_id else t.thema,
                empty=lambda: _summary(trainer, session),
                on_submit=on_submit,
                next_label="Weiter",
                position=lambda: f"Aufgabe {session.index + 1} von {len(session.tasks)}",
            )
            run_tasks(trainer, state, runner)
