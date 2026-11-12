"""Lektionsansicht Schritt für Schritt: ein Lernschritt pro Bildschirm statt einer Textwand.

Raster LI-01, aufklappbare Vertiefungen (LI-02), Voraussetzungen (LI-03), Glossar-Tooltips
(LI-04), Prüfstatus und Belege (LI-06). Mit „Alles auf einer Seite“ lässt sich die ganze
Lektion zum Nachschlagen oder Drucken anzeigen; Pfeiltasten blättern (NF-05).
"""

from __future__ import annotations

from dataclasses import dataclass

from nicegui import events, ui

from ap_trainer.content.models import Lektion
from ap_trainer.content.structure import Step, split_steps
from ap_trainer.service import Trainer
from ap_trainer.ui.layout import frame
from ap_trainer.ui.render import Block, link_glossary, parse_blocks

STATUS_COLORS = {"geprüft": "positive", "korrigiert": "info", "ungeprüft": "warning"}
MARKDOWN_EXTRAS = ["fenced-code-blocks", "tables", "cuddled-lists"]


@dataclass
class ViewState:
    """Zustand der Ansicht im Browser."""

    index: int = 0
    all_on_one_page: bool = False


def render_blocks(blocks: list[Block], trainer: Trainer) -> None:
    """Zeichnet Bausteine: Markdown, Mermaid-Diagramme, verschachtelte Vertiefungen."""

    def tooltip(term_id: str) -> str | None:
        term = trainer.package.begriffe.get(term_id)
        return term.kurz if term else None

    for block in blocks:
        if block.kind == "markdown":
            ui.markdown(link_glossary(block.text, tooltip), extras=MARKDOWN_EXTRAS).classes("w-full")
        elif block.kind == "mermaid":
            ui.mermaid(block.text).classes("w-full")
        else:
            with ui.expansion(block.summary, icon="psychology_alt").classes("w-full border rounded"):
                render_blocks(block.children, trainer)


def chapter_position(lesson: Lektion, trainer: Trainer) -> tuple[str, int, int, Lektion | None]:
    """Hauptthema, Kapitelnummer, Kapitelanzahl und das nächste Kapitel einer Lektion."""
    topic_id = lesson.themen[0]
    chapters = trainer.package.lessons_for_topic(topic_id)
    number = chapters.index(lesson) + 1
    following = chapters[number] if number < len(chapters) else None
    return topic_id, number, len(chapters), following


def _header(lesson: Lektion, trainer: Trainer) -> None:
    topics = trainer.package.katalog.by_id()
    topic_id, number, total, _ = chapter_position(lesson, trainer)
    with ui.row().classes("items-center gap-2 flex-wrap text-sm"):
        ui.link(f"← {topics[topic_id].titel}", f"/thema/{topic_id}")
        ui.label(f"· Kapitel {number} von {total}").classes("opacity-70")
        ui.badge(lesson.status, color=STATUS_COLORS[lesson.status]).tooltip("Prüfstatus (LI-06)")
        ui.label(f"ca. {lesson.dauer_min} Min.").classes("opacity-70")
    missing = [t for t in lesson.voraussetzungen if t not in trainer.done_topics()]
    if missing:
        names = ", ".join(topics[t].titel for t in missing)
        ui.label(f"Baut auf: {names}").classes("text-sm opacity-70")


def _step_card(step: Step, trainer: Trainer) -> None:
    with ui.card().classes("w-full lesson"):
        if step.titel != step.abschnitt:
            ui.label(step.abschnitt).classes("text-xs uppercase tracking-wide opacity-60")
        ui.label(step.titel).classes("text-xl font-semibold")
        render_blocks(parse_blocks(step.text), trainer)


def _sources(lesson: Lektion) -> None:
    with ui.expansion("Quellen und Belege", icon="fact_check").classes("w-full"):
        ui.label(lesson.quelle).classes("text-sm")
        for beleg in lesson.belege:
            if beleg.url:
                ui.link(beleg.titel, beleg.url, new_tab=True).classes("text-sm block")
            else:
                ui.label(beleg.titel).classes("text-sm")


def _finish(lesson: Lektion, trainer: Trainer) -> None:
    """Abschluss des Kapitels: Lernzeit speichern, Karten anlegen, weiter zum nächsten Kapitel."""
    topic_id, _, _, following = chapter_position(lesson, trainer)
    with ui.card().classes("w-full"):
        ui.label("Kapitel geschafft?").classes("text-lg font-medium")
        with ui.row().classes("items-end gap-3 flex-wrap"):
            minutes = ui.number("Gelernte Minuten", value=lesson.dauer_min, min=1, max=240, step=5).classes(
                "w-40"
            )

            def mark() -> None:
                created = trainer.mark_lesson_read(lesson, int(minutes.value or lesson.dauer_min))
                ui.notify(f"Gespeichert. {created} neue Lernkarten.", type="positive")

            read = lesson.id in trainer.store.read_lessons()
            ui.button("Wieder gelesen" if read else "Als gelesen markieren", icon="done", on_click=mark)
        if following:
            ui.button(
                f"Weiter: Kapitel „{following.titel}“",
                icon="arrow_forward",
                on_click=lambda: ui.navigate.to(f"/lektion/{following.id}"),
            ).props("flat")
        else:
            ui.button(
                "Zurück zum Thema", icon="topic", on_click=lambda: ui.navigate.to(f"/thema/{topic_id}")
            ).props("flat")


def register(trainer: Trainer) -> None:
    """Registriert die Lektionsseite."""

    @ui.page("/lektion/{lesson_id}")
    def lesson_page(lesson_id: str) -> None:
        lesson = trainer.package.lektionen.get(lesson_id)
        if lesson is None:
            with frame("Lektion nicht gefunden"):
                ui.link("Zur Themenübersicht", "/themen")
            return
        steps = split_steps(lesson.abschnitte)
        state = ViewState()

        def go(index: int) -> None:
            state.index = max(0, min(index, len(steps)))
            body.refresh()

        def on_key(event: events.KeyEventArguments) -> None:
            if not event.action.keydown or state.all_on_one_page:
                return
            if event.key.name == "ArrowRight":
                go(state.index + 1)
            elif event.key.name == "ArrowLeft":
                go(state.index - 1)

        @ui.refreshable
        def body() -> None:
            if state.all_on_one_page:
                for step in steps:
                    _step_card(step, trainer)
                _finish(lesson, trainer)
                _sources(lesson)
                return
            done = state.index >= len(steps)
            ui.linear_progress(value=min(state.index + 1, len(steps)) / len(steps), show_value=False)
            with ui.row().classes("w-full gap-1 flex-nowrap overflow-x-auto pb-1"):
                for number, step in enumerate(steps):
                    color = (
                        "primary"
                        if number == state.index
                        else ("grey-6" if number > state.index else "grey-8")
                    )
                    ui.button(str(number + 1), on_click=lambda n=number: go(n)).props(
                        f"dense round unelevated size=sm color={color}"
                    ).tooltip(step.titel)
            if done:
                _finish(lesson, trainer)
                _sources(lesson)
            else:
                ui.label(f"Schritt {state.index + 1} von {len(steps)}").classes("text-sm opacity-70")
                _step_card(steps[state.index], trainer)
            with ui.row().classes("w-full justify-between"):
                ui.button("Zurück", icon="arrow_back", on_click=lambda: go(state.index - 1)).props(
                    "flat" + (" disable" if state.index == 0 else "")
                )
                if not done:
                    last = state.index == len(steps) - 1
                    ui.button(
                        "Abschließen" if last else "Weiter",
                        icon_right="arrow_forward",
                        on_click=lambda: go(state.index + 1),
                    )

        def toggle(event: events.ValueChangeEventArguments) -> None:
            state.all_on_one_page = bool(event.value)
            body.refresh()

        with frame(lesson.titel):
            ui.keyboard(on_key=on_key)
            _header(lesson, trainer)
            ui.switch("Alles auf einer Seite", on_change=toggle).props("dense")
            body()
