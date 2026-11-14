"""Markdown mit Mermaid-Diagrammen und aufklappbaren Vertiefungen für Aufgaben und Lernkarten.

Dieselbe Darstellung wie in der Lektionsansicht, aber ohne Schritt-Navigation.
"""

from __future__ import annotations

from nicegui import ui

from ap_trainer.ui.lesson import MARKDOWN_EXTRAS
from ap_trainer.ui.render import Block, parse_blocks


def markdown(text: str) -> None:
    """Zeichnet Markdown samt Mermaid-Diagrammen und ``<details>``-Vertiefungen."""
    _render(parse_blocks(text))


def _render(blocks: list[Block]) -> None:
    for block in blocks:
        if block.kind == "mermaid":
            ui.mermaid(block.text).classes("w-full")
        elif block.kind == "details":
            with ui.expansion(block.summary, icon="psychology_alt").classes("w-full border rounded"):
                _render(block.children)
        else:
            ui.markdown(block.text, extras=MARKDOWN_EXTRAS).classes("w-full")
