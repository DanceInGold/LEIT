"""Themenübersicht nach Bereichen mit Gewicht, Lernstand und Lektionen (Vorstufe zu FT-02)."""

from __future__ import annotations

from nicegui import ui

from ap_trainer.service import Trainer
from ap_trainer.ui.layout import frame

STATE_ICONS = {"offen": "radio_button_unchecked", "laufend": "timelapse", "fertig": "check_circle"}
STAND_LABELS = {"neu": "neu 2025", "ausserhalb": "Zusatz", "entfallen": "entfallen"}


def register(trainer: Trainer) -> None:
    """Registriert die Themenseite."""

    @ui.page("/themen")
    def topics_page() -> None:
        progress = trainer.store.progress()
        katalog = trainer.package.katalog
        with frame("Themen"):
            ui.label("Gewicht = Anteil an den Prüfungspunkten (vorläufig, bis der Katalog da ist).").classes(
                "text-sm opacity-70"
            )
            for bereich in katalog.bereiche:
                topics = [t for t in katalog.themen if t.bereich == bereich.id and t.is_relevant]
                with ui.expansion(f"{bereich.name} ({len(topics)})", icon="folder").classes(
                    "w-full border rounded"
                ):
                    for topic in sorted(topics, key=lambda t: -trainer.weights[t.id]):
                        state = progress[topic.id].zustand if topic.id in progress else "offen"
                        with ui.row().classes("items-center gap-2 w-full flex-wrap"):
                            ui.icon(STATE_ICONS[state]).tooltip(state)
                            ui.label(topic.titel).classes("grow")
                            if topic.stand_2025 in STAND_LABELS:
                                ui.badge(STAND_LABELS[topic.stand_2025]).props("outline")
                            ui.label(f"{trainer.weights[topic.id]:.1f} %").classes("text-sm opacity-70 w-14")
                            for lesson in trainer.package.lessons_for_topic(topic.id):
                                ui.link(lesson.titel, f"/lektion/{lesson.id}").classes("text-sm")
