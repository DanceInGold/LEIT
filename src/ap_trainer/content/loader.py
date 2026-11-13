"""Liest ein Inhaltspaket von der Platte und meldet Schemafehler verständlich.

Der Loader sammelt alle Fehler, statt beim ersten abzubrechen, damit die Inhaltsprüfung
(``ap-tools check``) eine vollständige Liste liefert.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError

from ap_trainer.content.aufgaben import Aufgabe, AufgabenDatei
from ap_trainer.content.models import Begriff, Katalog, Lektion, Paket

_HEADING = re.compile(r"^## (.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class ContentError:
    """Ein Fehler in einer Inhaltsdatei, lesbar für Menschen."""

    datei: str
    meldung: str

    def __str__(self) -> str:
        return f"{self.datei}: {self.meldung}"


@dataclass
class ContentPackage:
    """Ein geladenes Inhaltspaket mit Lektionen, Begriffen und Aufgaben."""

    root: Path
    paket: Paket
    katalog: Katalog
    lektionen: dict[str, Lektion] = field(default_factory=dict)
    begriffe: dict[str, Begriff] = field(default_factory=dict)
    aufgaben: dict[str, Aufgabe] = field(default_factory=dict)
    # Thema → IDs der Aufgabengeneratoren, die dazu Varianten erzeugen (AU-03)
    generatoren: dict[str, list[str]] = field(default_factory=dict)

    def tasks_for_topic(self, topic_id: str) -> list[Aufgabe]:
        """Alle festen Aufgaben eines Themas, nach Stufe und ID sortiert."""
        found = [task for task in self.aufgaben.values() if task.thema == topic_id]
        return sorted(found, key=lambda task: (task.stufe, task.id))

    def lessons_for_topic(self, topic_id: str) -> list[Lektion]:
        """Alle Lektionen eines Themas in Lesereihenfolge (``reihenfolge``, dann Titel)."""
        found = [lesson for lesson in self.lektionen.values() if topic_id in lesson.themen]
        return sorted(found, key=lambda lesson: (lesson.reihenfolge, lesson.titel))


class ContentLoadError(Exception):
    """Das Paket ist nicht ladbar; ``errors`` enthält alle Einzelfehler."""

    def __init__(self, errors: list[ContentError]) -> None:
        super().__init__("\n".join(str(e) for e in errors))
        self.errors = errors


def _format_validation(exc: ValidationError) -> str:
    """Macht aus einer Pydantic-Meldung eine kurze deutsche Zeile je Fehler."""
    parts = []
    for err in exc.errors():
        location = ".".join(str(p) for p in err["loc"]) or "Datei"
        parts.append(f"{location}: {err['msg']}")
    return "; ".join(parts)


def _read_yaml(path: Path, errors: list[ContentError]) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(ContentError(str(path), f"YAML nicht lesbar ({exc})"))
        return None


def _validate[M: BaseModel](model: type[M], data: Any, path: Path, errors: list[ContentError]) -> M | None:
    if data is None:
        return None
    try:
        return model.model_validate(data)
    except ValidationError as exc:
        errors.append(ContentError(str(path), _format_validation(exc)))
        return None


def split_frontmatter(text: str) -> tuple[str, str]:
    """Trennt YAML-Frontmatter (zwischen ``---``-Zeilen) vom Markdown-Text."""
    if not text.startswith("---\n"):
        raise ValueError("Frontmatter fehlt (Datei muss mit '---' beginnen)")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Frontmatter wird nicht mit '---' geschlossen")
    return text[4:end], text[end + 5 :]


def split_sections(body: str) -> dict[str, str]:
    """Zerlegt Markdown an ``## ``-Überschriften in Abschnitt → Inhalt."""
    sections: dict[str, str] = {}
    matches = list(_HEADING.finditer(body))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[match.group(1)] = body[match.end() : end].strip()
    return sections


def _load_lesson(path: Path, errors: list[ContentError]) -> Lektion | None:
    try:
        head, body = split_frontmatter(path.read_text(encoding="utf-8"))
        data = yaml.safe_load(head) or {}
    except (ValueError, yaml.YAMLError) as exc:
        errors.append(ContentError(str(path), str(exc)))
        return None
    if not isinstance(data, dict):
        errors.append(ContentError(str(path), "Frontmatter ist kein YAML-Wörterbuch"))
        return None
    data["abschnitte"] = split_sections(body)
    lesson = _validate(Lektion, data, path, errors)
    if lesson and lesson.id != path.stem:
        errors.append(ContentError(str(path), f"id '{lesson.id}' passt nicht zum Dateinamen"))
    return lesson


def _load_terms(root: Path, errors: list[ContentError]) -> dict[str, Begriff]:
    terms: dict[str, Begriff] = {}
    for path in sorted((root / "glossar").glob("*.yaml")):
        term = _validate(Begriff, _read_yaml(path, errors), path, errors)
        if term is None:
            continue
        if term.id != path.stem:
            errors.append(ContentError(str(path), f"id '{term.id}' passt nicht zum Dateinamen"))
        terms[term.id] = term
    return terms


def _load_task_file(path: Path, errors: list[ContentError]) -> AufgabenDatei | None:
    """Liest ``aufgaben/<thema>.yaml``; das Thema ergibt sich aus dem Dateinamen."""
    data = _read_yaml(path, errors)
    if not isinstance(data, dict):
        if data is not None:
            errors.append(ContentError(str(path), "Datei ist kein YAML-Wörterbuch"))
        return None
    for index, item in enumerate(data.get("aufgaben") or []):
        if isinstance(item, dict) and item.setdefault("thema", path.stem) != path.stem:
            errors.append(ContentError(str(path), f"aufgaben.{index}: thema passt nicht zum Dateinamen"))
    return _validate(AufgabenDatei, data, path, errors)


def _load_tasks(root: Path, errors: list[ContentError]) -> tuple[dict[str, Aufgabe], dict[str, list[str]]]:
    tasks: dict[str, Aufgabe] = {}
    generators: dict[str, list[str]] = {}
    for path in sorted((root / "aufgaben").glob("*.yaml")):
        content = _load_task_file(path, errors)
        if content is None:
            continue
        if content.generatoren:
            generators[path.stem] = list(content.generatoren)
        for task in content.aufgaben:
            if task.id in tasks:
                errors.append(ContentError(str(path), f"Aufgaben-ID '{task.id}' ist doppelt"))
            tasks[task.id] = task
    return tasks, generators


def load_package(root: Path) -> tuple[ContentPackage | None, list[ContentError]]:
    """Lädt ein Paket und liefert es zusammen mit allen gefundenen Fehlern."""
    errors: list[ContentError] = []
    paket = _validate(Paket, _read_yaml(root / "paket.yaml", errors), root / "paket.yaml", errors)
    katalog = _validate(Katalog, _read_yaml(root / "katalog.yaml", errors), root / "katalog.yaml", errors)
    lessons = {}
    for path in sorted((root / "lektionen").glob("*.md")):
        lesson = _load_lesson(path, errors)
        if lesson:
            lessons[lesson.id] = lesson
    terms = _load_terms(root, errors)
    tasks, generators = _load_tasks(root, errors)
    if paket is None or katalog is None:
        return None, errors
    package = ContentPackage(root, paket, katalog, lessons, terms, tasks, generators)
    return package, errors


def load_package_or_raise(root: Path) -> ContentPackage:
    """Wie :func:`load_package`, wirft aber bei jedem Fehler (für den Programmstart)."""
    from ap_trainer.content.checks import check_references

    package, errors = load_package(root)
    if package is not None:
        errors += check_references(package)
    if package is None or errors:
        raise ContentLoadError(errors)
    return package
