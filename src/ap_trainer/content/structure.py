"""Gliedert Lektionen in Lernschritte und misst die Textmenge (gegen Textüberladung).

Ein Lernschritt ist das, was die Oberfläche auf einmal zeigt: ein Abschnitt des Rasters
LI-01 oder – wenn ein Abschnitt Unterüberschriften (``###``) hat – je Unterabschnitt
ein eigener Schritt. Die Stilprüfung meldet zu lange Absätze und zu volle Schritte.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_SUBHEADING = re.compile(r"^### (.+?)\s*$", re.MULTILINE)
_DETAILS = re.compile(r"<details>.*?</details>", re.DOTALL)
_NON_PROSE = ("-", "|", "```", ">", "<", "#")
_NUMBERED = re.compile(r"^\d+\.\s")

# Grenzwerte der Stilprüfung (siehe CLAUDE.md, Abschnitt „Schreibregeln für Lektionen“)
MAX_PARAGRAPH_WORDS = 40
MAX_STEP_WORDS = 220


@dataclass(frozen=True)
class Step:
    """Ein Lernschritt: Abschnitt des Rasters, eigene Überschrift, Markdown-Text."""

    abschnitt: str
    titel: str
    text: str


def split_steps(abschnitte: dict[str, str]) -> list[Step]:
    """Zerlegt die Abschnitte einer Lektion in Lernschritte."""
    steps: list[Step] = []
    for title, text in abschnitte.items():
        matches = list(_SUBHEADING.finditer(text))
        if not matches:
            steps.append(Step(title, title, text.strip()))
            continue
        intro = text[: matches[0].start()].strip()
        if intro:
            steps.append(Step(title, title, intro))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            steps.append(Step(title, match.group(1), text[match.end() : end].strip()))
    return steps


def visible_text(text: str) -> str:
    """Text ohne aufklappbare Vertiefungen – das, was man sofort sieht."""
    return _DETAILS.sub("", text)


def word_count(text: str) -> int:
    """Wörter ohne Markdown-Zeichen, Tabellenstriche und Diagrammcode."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return len(re.findall(r"[0-9A-Za-zÄÖÜäöüß]+", text))


def long_paragraphs(text: str, limit: int = MAX_PARAGRAPH_WORDS) -> list[tuple[int, str]]:
    """Fließtext-Absätze über ``limit`` Wörtern als (Wortzahl, Anfang des Absatzes)."""
    found = []
    for block in re.split(r"\n\s*\n", re.sub(r"```.*?```", "", text, flags=re.DOTALL)):
        block = block.strip()
        if not block or block.startswith(_NON_PROSE) or _NUMBERED.match(block):
            continue
        words = word_count(block)
        if words > limit:
            found.append((words, block[:50].replace("\n", " ")))
    return found
