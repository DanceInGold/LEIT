"""Lektionsansicht im Raster LI-01 mit aufklappbaren Vertiefungen (LI-02 bis LI-04, LI-06)."""

from __future__ import annotations

from nicegui import ui

from ap_trainer.content.models import Lektion
from ap_trainer.service import Trainer
from ap_trainer.ui.layout import frame
from ap_trainer.ui.render import Block, link_glossary, parse_blocks

STATUS_COLORS = {"geprüft": "positive", "korrigiert": "info", "ungeprüft": "warning"}
MARKDOWN_EXTRAS = ["fenced-code-blocks", "tables", "cuddled-lists"]


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


def _header(lesson: Lektion, trainer: Trainer) -> None:
    topics = trainer.package.katalog.by_id()
    with ui.row().classes("items-center gap-2 flex-wrap"):
        ui.badge(lesson.status, color=STATUS_COLORS[lesson.status]).tooltip("Prüfstatus (LI-06)")
        ui.label(f"ca. {lesson.dauer_min} Min.").classes("text-sm opacity-80")
        for topic_id in lesson.themen:
            ui.chip(topics[topic_id].titel, icon="topic").props("dense outline")
    if lesson.voraussetzungen:
        with ui.row().classes("items-center gap-2 flex-wrap text-sm"):
            ui.label("Voraussetzungen:")
            for topic_id in lesson.voraussetzungen:
                found = trainer.package.lessons_for_topic(topic_id)
                title = topics[topic_id].titel
                if found:
                    ui.link(title, f"/lektion/{found[0].id}")
                else:
                    ui.label(f"{title} (Lektion folgt)").classes("opacity-70")


def _footer(lesson: Lektion, trainer: Trainer) -> None:
    ui.separator()
    with ui.expansion("Quellen und Belege", icon="fact_check").classes("w-full"):
        ui.label(lesson.quelle).classes("text-sm")
        for beleg in lesson.belege:
            if beleg.url:
                ui.link(beleg.titel, beleg.url, new_tab=True).classes("text-sm block")
            else:
                ui.label(beleg.titel).classes("text-sm")
    read = lesson.id in trainer.store.read_lessons()
    with ui.card().classes("w-full"), ui.row().classes("items-end gap-3 flex-wrap"):
        minutes = ui.number("Gelernte Minuten", value=lesson.dauer_min, min=1, max=240, step=5).classes(
            "w-40"
        )

        def mark() -> None:
            created = trainer.mark_lesson_read(lesson, int(minutes.value or lesson.dauer_min))
            ui.notify(f"Gespeichert. {created} neue Lernkarten angelegt.", type="positive")

        ui.button("Wieder gelesen" if read else "Als gelesen markieren", icon="done", on_click=mark)
        for topic_id in lesson.themen:
            done = topic_id in trainer.done_topics()
            ui.checkbox(
                f"Thema „{trainer.package.katalog.by_id()[topic_id].titel}“ abgeschlossen",
                value=done,
                on_change=lambda e, t=topic_id: trainer.set_topic_done(t, bool(e.value)),
            )


def register(trainer: Trainer) -> None:
    """Registriert die Lektionsseite."""

    @ui.page("/lektion/{lesson_id}")
    def lesson_page(lesson_id: str) -> None:
        lesson = trainer.package.lektionen.get(lesson_id)
        if lesson is None:
            with frame("Lektion nicht gefunden"):
                ui.link("Zur Themenübersicht", "/themen")
            return
        with frame(lesson.titel):
            _header(lesson, trainer)
            with ui.column().classes("lesson w-full gap-2"):
                for title, text in lesson.abschnitte.items():
                    ui.label(title).classes("text-xl font-semibold mt-3")
                    render_blocks(parse_blocks(text), trainer)
            _footer(lesson, trainer)
