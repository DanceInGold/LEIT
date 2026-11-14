"""Lernkarten aus dem Glossar (GL-02) und aus eigenen Fehlern (ZI-05).

Je Begriff entsteht eine Karte „Begriff → Kurzdefinition“; hat der Begriff eine
Langform, zusätzlich „Abkürzung → Langform“. Karten werden erst angelegt, wenn eine
Lektion zum Thema gelesen wurde – so wiederholt man nur, was man schon gelernt hat.
Jede falsch gelöste Aufgabe wird zur Fehlerkarte: vorne die Aufgabe, hinten der Lösungsweg.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ap_trainer.content.aufgaben import Aufgabe
from ap_trainer.content.models import Begriff

# Karten-IDs von Fehlerkarten: „fehler:<thema>:<aufgabe_id>“ (Aufgaben-IDs dürfen „:“ enthalten)
MISTAKE_PREFIX = "fehler:"


@dataclass(frozen=True)
class Flashcard:
    """Vorder- und Rückseite einer Lernkarte."""

    card_id: str
    begriff_id: str
    vorne: str
    hinten: str
    art: Literal["begriff", "fehler"] = "begriff"
    # Nur Fehlerkarten: Thema und Aufgabe, um sie erneut zu öffnen
    thema: str = ""
    aufgabe_id: str = ""


def cards_for_term(term: Begriff) -> list[Flashcard]:
    """Alle Karten eines Glossarbegriffs."""
    back = term.kurz if not term.langform else f"{term.langform} – {term.kurz}"
    cards = [Flashcard(f"{term.id}:def", term.id, f"Was ist {term.begriff}?", back)]
    if term.langform:
        cards.append(Flashcard(f"{term.id}:lang", term.id, f"Wofür steht „{term.begriff}“?", term.langform))
    return cards


def cards_for_topics(terms: dict[str, Begriff], topic_ids: set[str]) -> list[Flashcard]:
    """Karten aller Begriffe, deren Thema in ``topic_ids`` liegt."""
    result: list[Flashcard] = []
    for term in sorted(terms.values(), key=lambda t: t.begriff.lower()):
        if term.thema in topic_ids:
            result.extend(cards_for_term(term))
    return result


def card_index(terms: dict[str, Begriff]) -> dict[str, Flashcard]:
    """Alle möglichen Karten nach Karten-ID (zum Nachschlagen beim Wiederholen)."""
    return {card.card_id: card for term in terms.values() for card in cards_for_term(term)}


def mistake_card_id(topic_id: str, task_id: str) -> str:
    """Karten-ID der Fehlerkarte zu einer Aufgabe."""
    return f"{MISTAKE_PREFIX}{topic_id}:{task_id}"


def parse_mistake_card_id(card_id: str) -> tuple[str, str] | None:
    """(Thema, Aufgaben-ID) aus einer Fehlerkarten-ID; ``None`` bei anderen Karten."""
    if not card_id.startswith(MISTAKE_PREFIX):
        return None
    topic_id, sep, task_id = card_id.removeprefix(MISTAKE_PREFIX).partition(":")
    return (topic_id, task_id) if sep and topic_id and task_id else None


def mistake_card(task: Aufgabe) -> Flashcard:
    """Fehlerkarte: vorne Titel, Situation und Frage der Aufgabe, hinten der Lösungsweg (Markdown)."""
    front = f"**{task.titel}**\n\n"
    if task.situation:
        front += f"{task.situation}\n\n"
    front += task.frage
    return Flashcard(
        mistake_card_id(task.thema, task.id),
        "",
        front,
        task.loesungsweg,
        art="fehler",
        thema=task.thema,
        aufgabe_id=task.id,
    )
