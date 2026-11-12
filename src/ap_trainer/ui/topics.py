"""Themenübersicht und Themenseite mit nummerierten Kapiteln (Vorstufe zu FT-02).

Die Übersicht zeigt Bereiche mit Fortschrittsbalken; die Themenseite listet die Kapitel
(Lektionen) eines Themas in Lesereihenfolge mit Dauer und Lesestand.
"""

from __future__ import annotations

from nicegui import ui

from ap_trainer.content.models import Thema
from ap_trainer.service import Trainer
from ap_trainer.ui.layout import frame

STATE_ICONS = {"offen": "radio_button_unchecked", "laufend": "timelapse", "fertig": "check_circle"}
STATE_LABELS = {"offen": "offen", "laufend": "begonnen", "fertig": "abgeschlossen"}
STAND_LABELS = {"neu": "neu 2025", "ausserhalb": "Zusatz", "entfallen": "entfallen"}


def _topic_row(topic: Thema, trainer: Trainer, state: str) -> None:
    chapters = trainer.package.lessons_for_topic(topic.id)
    read = trainer.store.read_lessons()
    with (
        ui.row()
        .classes("items-center gap-2 w-full flex-nowrap cursor-pointer hover:bg-gray-500/10 rounded p-1")
        .on("click", lambda: ui.navigate.to(f"/thema/{topic.id}"))
    ):
        ui.icon(STATE_ICONS[state]).tooltip(STATE_LABELS[state])
        ui.label(topic.titel).classes("grow")
        if topic.stand_2025 in STAND_LABELS:
            ui.badge(STAND_LABELS[topic.stand_2025]).props("outline")
        if chapters:
            done = sum(1 for c in chapters if c.id in read)
            ui.label(f"{done}/{len(chapters)} Kap.").classes("text-sm opacity-70 whitespace-nowrap")
        else:
            ui.label("Kapitel folgen").classes("text-sm opacity-50 whitespace-nowrap")
        ui.label(f"{trainer.weights[topic.id]:.1f} %").classes("text-sm opacity-70 w-12 text-right")


def _chapter_card(number: int, lesson_id: str, title: str, minutes: int, read: bool) -> None:
    with (
        ui.card()
        .classes("w-full cursor-pointer hover:shadow-md")
        .on("click", lambda: ui.navigate.to(f"/lektion/{lesson_id}")),
        ui.row().classes("items-center gap-3 w-full flex-nowrap"),
    ):
        ui.label(str(number)).classes("text-2xl font-semibold opacity-50 w-8 text-center")
        with ui.column().classes("grow gap-0"):
            ui.label(f"Kapitel {number}").classes("text-xs uppercase tracking-wide opacity-60")
            ui.label(title).classes("font-medium")
        ui.label(f"{minutes} Min.").classes("text-sm opacity-70 whitespace-nowrap")
        ui.icon("check_circle" if read else "chevron_right", color="positive" if read else None)


def register(trainer: Trainer) -> None:
    """Registriert Themenübersicht und Themenseite."""

    @ui.page("/themen")
    def topics_page() -> None:
        progress = trainer.store.progress()
        katalog = trainer.package.katalog
        areas = {a.bereich: a for a in trainer.area_progress()}
        with frame("Themen"):
            ui.label("Gewicht = Anteil an den Prüfungspunkten (vorläufig, bis der Katalog da ist).").classes(
                "text-sm opacity-70"
            )
            for bereich in katalog.bereiche:
                topics = [t for t in katalog.themen if t.bereich == bereich.id and t.is_relevant]
                share = areas[bereich.name].anteil if bereich.name in areas else 0.0
                with ui.expansion(f"{bereich.name} ({len(topics)})", icon="folder").classes(
                    "w-full border rounded"
                ):
                    ui.linear_progress(value=share, show_value=False).tooltip(f"{share:.0%} erledigt")
                    for topic in sorted(topics, key=lambda t: -trainer.weights[t.id]):
                        state = progress[topic.id].zustand if topic.id in progress else "offen"
                        _topic_row(topic, trainer, state)

    @ui.page("/thema/{topic_id}")
    def topic_page(topic_id: str) -> None:
        topic = trainer.package.katalog.by_id().get(topic_id)
        if topic is None:
            with frame("Thema nicht gefunden"):
                ui.link("Zur Themenübersicht", "/themen")
            return
        chapters = trainer.package.lessons_for_topic(topic_id)
        read = trainer.store.read_lessons()
        state = trainer.store.progress().get(topic_id)
        with frame(topic.titel):
            with ui.row().classes("items-center gap-2 flex-wrap text-sm"):
                ui.link("← Alle Themen", "/themen")
                ui.badge(f"Gewicht {trainer.weights[topic_id]:.1f} %").props("outline")
                if topic.katalog:
                    ui.badge("Katalog " + ", ".join(topic.katalog)).props("outline")
                if topic.stand_2025 in STAND_LABELS:
                    ui.badge(STAND_LABELS[topic.stand_2025])
            if not chapters:
                ui.label("Die Kapitel zu diesem Thema sind noch in Arbeit.").classes("opacity-70")
            done = sum(1 for c in chapters if c.id in read)
            if chapters:
                ui.linear_progress(value=done / len(chapters), show_value=False)
                ui.label(f"{done} von {len(chapters)} Kapiteln gelesen").classes("text-sm opacity-70")
            for number, lesson in enumerate(chapters, start=1):
                _chapter_card(number, lesson.id, lesson.titel, lesson.dauer_min, lesson.id in read)
            finished = state is not None and state.zustand == "fertig"
            ui.checkbox(
                "Thema abgeschlossen",
                value=finished,
                on_change=lambda e: trainer.set_topic_done(topic_id, bool(e.value)),
            ).classes("mt-2")
