"""Fachwort-Kompendium mit Volltextsuche und Filter nach Themengebiet (GL-01, GL-04)."""

from __future__ import annotations

from nicegui import ui

from ap_trainer.content.models import Begriff
from ap_trainer.service import Trainer
from ap_trainer.ui.layout import frame


def matches(term: Begriff, query: str, topic: str | None) -> bool:
    """True, wenn der Begriff zu Suchtext und Themenfilter passt."""
    if topic and term.thema != topic:
        return False
    if not query:
        return True
    haystack = " ".join(
        [term.begriff, term.langform or "", term.kurz, term.erklaerung, term.beispiel]
    ).lower()
    return query.lower() in haystack


def _term_card(term: Begriff, trainer: Trainer, opened: bool) -> None:
    title = term.begriff + (f" – {term.langform}" if term.langform else "")
    with ui.expansion(title, value=opened).classes("w-full border rounded"):
        ui.label(term.kurz).classes("font-medium")
        ui.markdown(term.erklaerung)
        if term.warum:
            ui.markdown(f"**Warum?** {term.warum}")
        ui.markdown(f"**Beispiel:** {term.beispiel}")
        topic = trainer.package.katalog.by_id()[term.thema].titel
        with ui.row().classes("items-center gap-2 flex-wrap text-sm"):
            ui.chip(topic, icon="topic").props("dense outline")
            for ref in term.verwandt:
                other = trainer.package.begriffe[ref]
                ui.link(other.begriff, f"/glossar?begriff={ref}")
            ui.badge(term.status).props("outline")


def register(trainer: Trainer) -> None:
    """Registriert die Glossarseite."""

    @ui.page("/glossar")
    def glossary_page(begriff: str = "") -> None:
        topics = trainer.package.katalog.by_id()
        used = sorted({t.thema for t in trainer.package.begriffe.values()}, key=lambda tid: topics[tid].titel)
        with frame("Glossar"):
            with ui.row().classes("w-full gap-2 flex-wrap"):
                search = ui.input("Suchen", value="").props("clearable").classes("grow")
                topic = ui.select(
                    {tid: topics[tid].titel for tid in used}, label="Themengebiet", clearable=True
                )
                topic.classes("min-w-[14rem]")

            @ui.refreshable
            def results() -> None:
                terms = sorted(trainer.package.begriffe.values(), key=lambda t: t.begriff.lower())
                shown = [t for t in terms if matches(t, search.value or "", topic.value)]
                ui.label(f"{len(shown)} von {len(terms)} Begriffen").classes("text-sm opacity-70")
                for term in shown:
                    _term_card(term, trainer, opened=term.id == begriff)

            search.on_value_change(lambda _: results.refresh())
            topic.on_value_change(lambda _: results.refresh())
            results()
