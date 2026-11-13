"""Aufgabengeneratoren für Rechenthemen (AU-03) und ihre Registrierung.

Ein neuer Generator ist eine neue Datei in diesem Ordner mit einer Klasse, die von
:class:`Generator` erbt und mit ``@register`` markiert ist. Beim ersten Zugriff auf
:data:`REGISTRY` werden alle Dateien des Ordners importiert – sonst muss nichts geändert werden.

Welcher Generator zu welchem Thema gehört, steht im Inhaltspaket
(``aufgaben/<thema>.yaml``, Schlüssel ``generatoren``); die Generatoren selbst kennen keine Themen-IDs.
"""

from __future__ import annotations

import importlib
import pkgutil
import random
from abc import ABC, abstractmethod
from typing import ClassVar

from ap_trainer.content.aufgaben import Aufgabe, Stufe
from ap_trainer.content.models import Beleg, Status

_REGISTRY: dict[str, Generator] = {}
_LOADED = False


class Generator(ABC):
    """Erzeugt beliebig viele Varianten einer Rechenaufgabe aus einem Zufallsgenerator.

    Gleicher Seed und gleiche Stufe liefern immer dieselbe Aufgabe – so lässt sich eine
    falsch gelöste Aufgabe später genau so wiederholen.
    """

    id: ClassVar[str]
    titel: ClassVar[str]
    stufen: ClassVar[tuple[Stufe, ...]]
    # Prüfstatus der Texte wie bei Inhalten: „ungeprüft“ bis zum Merge, dann „geprüft“
    status: ClassVar[Status]
    quelle: ClassVar[str]
    belege: ClassVar[tuple[Beleg, ...]] = ()

    @abstractmethod
    def generate(self, rng: random.Random, stufe: Stufe, task_id: str, thema: str) -> Aufgabe:
        """Erzeugt eine Aufgabe der Stufe ``stufe`` mit der übergebenen ID und Themen-ID."""


def register[G: type[Generator]](cls: G) -> G:
    """Klassen-Dekorator: legt eine Instanz des Generators in der Registrierung ab."""
    if cls.id in _REGISTRY:
        raise ValueError(f"Generator-ID doppelt: {cls.id}")
    _REGISTRY[cls.id] = cls()
    return cls


def registry() -> dict[str, Generator]:
    """Alle Generatoren nach ID; importiert beim ersten Aufruf alle Module dieses Ordners."""
    global _LOADED
    if not _LOADED:
        for module in pkgutil.iter_modules(__path__):
            if not module.name.startswith("_"):
                importlib.import_module(f"{__name__}.{module.name}")
        _LOADED = True
    return _REGISTRY


def task_id(generator_id: str, stufe: int, seed: int) -> str:
    """ID einer generierten Aufgabe: ``gen:<generator>:<stufe>:<seed>``."""
    return f"gen:{generator_id}:{stufe}:{seed}"


def parse_task_id(value: str) -> tuple[str, int, int] | None:
    """Zerlegt eine generierte Aufgaben-ID in Generator, Stufe und Seed."""
    parts = value.split(":")
    if len(parts) != 4 or parts[0] != "gen" or not parts[2].isdigit() or not parts[3].isdigit():
        return None
    return parts[1], int(parts[2]), int(parts[3])


def nearest_level(levels: tuple[Stufe, ...], wanted: int) -> Stufe:
    """Die gewünschte Stufe, sonst die nächstniedrigere, sonst die kleinste vorhandene."""
    lower = [s for s in levels if s <= wanted]
    return max(lower) if lower else min(levels)


def make(generator_id: str, stufe: int, seed: int, thema: str) -> Aufgabe:
    """Erzeugt die Aufgabe ``gen:<generator>:<stufe>:<seed>`` für ein Thema."""
    generator = registry()[generator_id]
    level = nearest_level(generator.stufen, stufe)
    return generator.generate(random.Random(seed), level, task_id(generator_id, level, seed), thema)
