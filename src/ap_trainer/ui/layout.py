"""Gemeinsamer Seitenrahmen: Kopfzeile mit Navigation, Dunkelmodus, schmale Bildschirme.

Alle Seiten rufen :func:`frame` auf; der Inhalt landet in einer mittigen Spalte, die
auf dem Smartphone die volle Breite nutzt (NF-01, NF-05).
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from nicegui import ui

NAV = [
    ("Heute", "/", "today"),
    ("Plan", "/plan", "event_note"),
    ("Themen", "/themen", "topic"),
    ("Glossar", "/glossar", "menu_book"),
    ("Lernkarten", "/lernkarten", "style"),
    ("Einstellungen", "/einstellungen", "settings"),
]

AMPEL_COLORS = {"im Plan": "positive", "knapp": "warning", "im Verzug": "negative"}

_CSS = """
.glossar-link { text-decoration: underline dotted; cursor: help; }
.lesson .nicegui-markdown { line-height: 1.65; font-size: 1.02rem; }
.lesson .nicegui-markdown p { margin: 0.6rem 0; }
.lesson .nicegui-markdown li { margin: 0.25rem 0; }
.nicegui-markdown table { border-collapse: collapse; margin: 0.75rem 0; font-size: 0.95rem; }
.nicegui-markdown th, .nicegui-markdown td { border: 1px solid #8884; padding: 0.3rem 0.6rem; }
.nicegui-markdown th { background: #8881; }
/* Zwischenfazit „Halten wir kurz fest“ als Merkkasten */
.nicegui-markdown blockquote {
  margin: 1rem 0; padding: 0.6rem 1rem; border-left: 4px solid #2a78d6;
  background: #2a78d61a; border-radius: 0 8px 8px 0;
}
.body--dark .nicegui-markdown blockquote { border-left-color: #3987e5; background: #3987e526; }
.nicegui-markdown blockquote p:first-child { margin-top: 0; }
.kpi-value { font-size: 1.8rem; font-weight: 600; line-height: 1.1; }
"""

# Farben der Diagramme nach der Referenzpalette: Ist = Blau, Soll = Grau, Abstufungen = Blau hell
CHART_BLUE = "#2a78d6"
CHART_BLUE_LIGHT = "#86b6ef"
CHART_GREY = "#8a8984"
CHART_TRACK = "#8a898433"


@contextmanager
def frame(title: str) -> Iterator[None]:
    """Seitenrahmen mit Navigation; der ``with``-Block füllt den Inhalt."""
    ui.add_css(_CSS)
    dark = ui.dark_mode(None)  # None = folgt der Systemeinstellung
    with ui.header().classes("items-center gap-1 flex-wrap py-1"):
        ui.label("AP1-Lernbegleiter").classes("text-lg font-bold mr-4")
        for label, target, icon in NAV:
            ui.button(label, icon=icon, on_click=lambda t=target: ui.navigate.to(t)).props(
                "flat color=white dense"
            )
        ui.space()
        ui.button(icon="dark_mode", on_click=lambda: dark.set_value(not dark.value)).props(
            "flat color=white round dense"
        ).tooltip("Hell/Dunkel umschalten")
    with ui.column().classes("w-full max-w-3xl mx-auto p-3 gap-3"):
        ui.label(title).classes("text-2xl font-semibold")
        yield
