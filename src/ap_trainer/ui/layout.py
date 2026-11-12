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
.lesson h3 { font-size: 1.15rem; font-weight: 600; margin-top: 0.5rem; }
.nicegui-markdown table { border-collapse: collapse; margin: 0.5rem 0; }
.nicegui-markdown th, .nicegui-markdown td { border: 1px solid #8884; padding: 0.25rem 0.5rem; }
"""


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
