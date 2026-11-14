"""Lernkarten-Sitzung mit Wiederholung nach FSRS (GL-02, WH-01, WH-02), auch für Fehlerkarten (ZI-05).

Bedienung auch per Tastatur (NF-05): Leertaste oder Enter deckt auf, 1–4 bewertet.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from urllib.parse import quote

from nicegui import events, ui

from ap_trainer.core.cards import Flashcard
from ap_trainer.core.scheduler import GRADE_LABELS, Grade
from ap_trainer.service import Trainer
from ap_trainer.ui.layout import frame
from ap_trainer.ui.rich import markdown

GRADE_COLORS = {1: "negative", 2: "warning", 3: "positive", 4: "info"}


@dataclass
class Session:
    """Zustand einer Wiederholungssitzung im Browser."""

    cards: list[Flashcard]
    index: int = 0
    revealed: bool = False
    graded: list[int] = field(default_factory=list)
    # Zeitpunkt, seit dem die aktuelle Karte zu sehen ist (für die Lernzeit-Statistik)
    shown_at: float = field(default_factory=time.monotonic)

    @property
    def current(self) -> Flashcard | None:
        """Aktuelle Karte oder ``None``, wenn die Sitzung fertig ist."""
        return self.cards[self.index] if self.index < len(self.cards) else None


def _mistake_card(card: Flashcard, revealed: bool) -> None:
    """Fehlerkarte (ZI-05): Aufgabe vorne, Lösungsweg hinten, beides mit Tabellen und Diagrammen."""
    with ui.card().classes("w-full gap-2"):
        with ui.row().classes("items-center gap-1 text-sm opacity-70"):
            ui.icon("report")
            ui.label("Fehlerkarte – diese Aufgabe hattest du falsch. Überleg dir den Lösungsweg.")
        markdown(card.vorne)
        if revealed:
            ui.separator()
            ui.label("Lösungsweg").classes("text-xs uppercase tracking-wide opacity-70")
            markdown(card.hinten)
            target = f"/ueben/{card.thema}?aufgabe={quote(card.aufgabe_id, safe='')}"
            ui.link("Aufgabe noch einmal selbst lösen →", target, new_tab=True)


def register(trainer: Trainer) -> None:
    """Registriert die Lernkartenseite."""

    @ui.page("/lernkarten")
    def practice_page() -> None:
        session = Session(cards=trainer.due_cards())

        def grade(value: Grade) -> None:
            card = session.current
            if card is None or not session.revealed:
                return
            trainer.grade(card.card_id, value, seconds=time.monotonic() - session.shown_at)
            session.shown_at = time.monotonic()
            session.graded.append(value)
            session.index, session.revealed = session.index + 1, False
            view.refresh()

        def reveal() -> None:
            if session.current is not None:
                session.revealed = True
                view.refresh()

        def on_key(event: events.KeyEventArguments) -> None:
            if not event.action.keydown or event.action.repeat:
                return
            if event.key.name in (" ", "Enter", "Space"):
                reveal()
            elif event.key.name in ("1", "2", "3", "4"):
                grade(int(event.key.name))  # type: ignore[arg-type]

        @ui.refreshable
        def view() -> None:
            card = session.current
            if card is None:
                done = len(session.graded)
                ui.label("Für heute ist nichts mehr fällig." if done else "Keine Karten fällig.").classes(
                    "text-lg"
                )
                if done:
                    ui.label(f"{done} Karten wiederholt. Stark!")
                ui.button("Zurück zu Heute", on_click=lambda: ui.navigate.to("/"))
                return
            ui.linear_progress(value=session.index / len(session.cards), show_value=False)
            ui.label(f"Karte {session.index + 1} von {len(session.cards)}").classes("text-sm opacity-70")
            if card.art == "fehler":
                _mistake_card(card, session.revealed)
            else:
                with ui.card().classes("w-full min-h-[10rem] items-center justify-center text-center"):
                    ui.label(card.vorne).classes("text-xl font-medium")
                    if session.revealed:
                        ui.separator()
                        ui.label(card.hinten).classes("text-lg")
            if not session.revealed:
                ui.button("Aufdecken (Leertaste)", on_click=reveal).classes("w-full")
                return
            with ui.row().classes("w-full gap-2 flex-wrap justify-center"):
                for value, label in GRADE_LABELS.items():
                    ui.button(
                        f"{value} · {label}", color=GRADE_COLORS[value], on_click=lambda v=value: grade(v)
                    ).classes("grow")

        with frame("Lernkarten"):
            ui.keyboard(on_key=on_key)
            view()
