"""Zerlegt Lektionstext in Bausteine für die Oberfläche – ohne NiceGUI, deshalb testbar.

Bausteine: normaler Markdown-Text, Mermaid-Diagramme und aufklappbare Vertiefungen
(``<details><summary>Warum?</summary> … </details>``, beliebig verschachtelt, LI-02).
Glossar-Verweise ``[Text](glossar:id)`` werden zu Links mit Tooltip (LI-04).
"""

from __future__ import annotations

import html
import re
from collections.abc import Callable
from dataclasses import dataclass, field

_DETAILS_OPEN = re.compile(r"<details>\s*<summary>(.*?)</summary>", re.DOTALL)
_DETAILS_CLOSE = "</details>"
_MERMAID = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
_GLOSSARY = re.compile(r"\[([^\]]+)\]\(glossar:([a-z0-9-]+)\)")


@dataclass
class Block:
    """Ein Baustein: ``markdown``, ``mermaid`` oder ``details`` (mit Kindern)."""

    kind: str
    text: str = ""
    summary: str = ""
    children: list[Block] = field(default_factory=list)


def _split_mermaid(text: str) -> list[Block]:
    blocks: list[Block] = []
    pos = 0
    for match in _MERMAID.finditer(text):
        if text[pos : match.start()].strip():
            blocks.append(Block("markdown", text[pos : match.start()].strip()))
        blocks.append(Block("mermaid", match.group(1).strip()))
        pos = match.end()
    if text[pos:].strip():
        blocks.append(Block("markdown", text[pos:].strip()))
    return blocks


def _matching_close(text: str, start: int) -> int:
    """Index des zu ``start`` passenden ``</details>`` (berücksichtigt Verschachtelung)."""
    depth, pos = 1, start
    while depth:
        nxt_open = _DETAILS_OPEN.search(text, pos)
        nxt_close = text.find(_DETAILS_CLOSE, pos)
        if nxt_close == -1:
            raise ValueError("<details> ohne passendes </details>")
        if nxt_open and nxt_open.start() < nxt_close:
            depth, pos = depth + 1, nxt_open.end()
        else:
            depth, pos = depth - 1, nxt_close + len(_DETAILS_CLOSE)
    return pos - len(_DETAILS_CLOSE)


def parse_blocks(text: str) -> list[Block]:
    """Zerlegt einen Abschnitt in Bausteine, Vertiefungen rekursiv."""
    blocks: list[Block] = []
    pos = 0
    while (match := _DETAILS_OPEN.search(text, pos)) is not None:
        blocks.extend(_split_mermaid(text[pos : match.start()]))
        close = _matching_close(text, match.end())
        inner = text[match.end() : close]
        blocks.append(Block("details", summary=match.group(1).strip(), children=parse_blocks(inner)))
        pos = close + len(_DETAILS_CLOSE)
    blocks.extend(_split_mermaid(text[pos:]))
    return blocks


def link_glossary(text: str, tooltip: Callable[[str], str | None]) -> str:
    """Ersetzt Glossar-Verweise durch HTML-Links mit Kurzdefinition als Tooltip."""

    def replace(match: re.Match[str]) -> str:
        label, term_id = match.group(1), match.group(2)
        title = html.escape(tooltip(term_id) or "", quote=True)
        return f'<a href="/glossar?begriff={term_id}" title="{title}" class="glossar-link">{label}</a>'

    return _GLOSSARY.sub(replace, text)
