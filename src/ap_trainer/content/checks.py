"""Verweisprüfung über ein geladenes Paket: IDs, Voraussetzungen, Zyklen.

Ergänzt die Schemaprüfung der Modelle um alles, was nur im Zusammenhang prüfbar ist.
"""

from __future__ import annotations

import re
from collections import Counter

from ap_trainer.content.loader import ContentError, ContentPackage

# Glossar-Verweis in Lektionen: [Text](glossar:begriff-id)  (LI-04)
GLOSSARY_LINK = re.compile(r"\]\(glossar:([a-z0-9-]+)\)")


def _duplicates(ids: list[str]) -> set[str]:
    return {item for item, count in Counter(ids).items() if count > 1}


def _find_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    """Sucht einen Zyklus per Tiefensuche und gibt ihn als Pfad zurück."""
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        state[node] = 1
        stack.append(node)
        for nxt in graph.get(node, []):
            if state.get(nxt) == 1:
                return [*stack[stack.index(nxt) :], nxt]
            if nxt not in state and (cycle := visit(nxt)):
                return cycle
        state[node] = 2
        stack.pop()
        return None

    for node in graph:
        if node not in state and (cycle := visit(node)):
            return cycle
    return None


def _check_catalog(pkg: ContentPackage) -> list[ContentError]:
    file = str(pkg.root / "katalog.yaml")
    errors = []
    topics = pkg.katalog.by_id()
    bereiche = {b.id for b in pkg.katalog.bereiche}
    for dup in sorted(_duplicates([t.id for t in pkg.katalog.themen])):
        errors.append(ContentError(file, f"Thema '{dup}' ist doppelt"))
    for topic in pkg.katalog.themen:
        if topic.bereich not in bereiche:
            errors.append(ContentError(file, f"{topic.id}: unbekannter Bereich '{topic.bereich}'"))
        for req in topic.voraussetzungen:
            if req not in topics:
                errors.append(ContentError(file, f"{topic.id}: unbekannte Voraussetzung '{req}'"))
        if topic.is_relevant and topic.aufwand_h is None:
            errors.append(ContentError(file, f"{topic.id}: aufwand_h fehlt (LP-08)"))
    for topic_id in pkg.katalog.gewichtung.einzelthemen_punkte:
        if topic_id not in topics:
            errors.append(ContentError(file, f"gewichtung: unbekanntes Thema '{topic_id}'"))
    cycle = _find_cycle({t.id: list(t.voraussetzungen) for t in pkg.katalog.themen})
    if cycle:
        errors.append(ContentError(file, f"Zyklus in den Voraussetzungen: {' → '.join(cycle)}"))
    return errors


def _check_lessons(pkg: ContentPackage) -> list[ContentError]:
    errors = []
    topics = pkg.katalog.by_id()
    for lesson in pkg.lektionen.values():
        file = str(pkg.root / "lektionen" / f"{lesson.id}.md")
        for ref in [*lesson.themen, *lesson.voraussetzungen]:
            if ref not in topics:
                errors.append(ContentError(file, f"unbekanntes Thema '{ref}'"))
        text = "\n".join(lesson.abschnitte.values())
        for term_id in sorted(set(GLOSSARY_LINK.findall(text))):
            if term_id not in pkg.begriffe:
                errors.append(ContentError(file, f"Glossar-Verweis '{term_id}' existiert nicht"))
    return errors


def _check_terms(pkg: ContentPackage) -> list[ContentError]:
    errors = []
    topics = pkg.katalog.by_id()
    for term in pkg.begriffe.values():
        file = str(pkg.root / "glossar" / f"{term.id}.yaml")
        if term.thema not in topics:
            errors.append(ContentError(file, f"unbekanntes Thema '{term.thema}'"))
        for ref in term.verwandt:
            if ref not in pkg.begriffe:
                errors.append(ContentError(file, f"verwandter Begriff '{ref}' existiert nicht"))
    return errors


def check_references(pkg: ContentPackage) -> list[ContentError]:
    """Alle Verweisfehler eines Pakets."""
    return _check_catalog(pkg) + _check_lessons(pkg) + _check_terms(pkg)
