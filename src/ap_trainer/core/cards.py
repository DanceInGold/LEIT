"""Lernkarten aus dem Glossar ableiten (GL-02).

Je Begriff entsteht eine Karte „Begriff → Kurzdefinition“; hat der Begriff eine
Langform, zusätzlich „Abkürzung → Langform“. Karten werden erst angelegt, wenn eine
Lektion zum Thema gelesen wurde – so wiederholt man nur, was man schon gelernt hat.
"""

from __future__ import annotations

from dataclasses import dataclass

from ap_trainer.content.models import Begriff


@dataclass(frozen=True)
class Flashcard:
    """Vorder- und Rückseite einer Lernkarte."""

    card_id: str
    begriff_id: str
    vorne: str
    hinten: str


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
