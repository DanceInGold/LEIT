"""Welche Aufgabe kommt als Nächstes? Auswahl aus festen Aufgaben und Generatoren eines Themas.

Gesucht wird auf der aktuellen Stufe; gibt es dort nichts, auf der nächstniedrigeren, sonst
auf der nächsthöheren. Feste Aufgaben, die zuletzt dran waren, kommen ans Ende; Generatoren
liefern immer neue Varianten und mischen sich mit den festen Aufgaben. Sind auf der Stufe alle
festen Aufgaben schon zuletzt dran gewesen, kommt eine noch nicht gesehene Aufgabe einer
Nachbarstufe – dieselbe Aufgabe direkt zweimal hintereinander gibt es nur, wenn das Thema nur
eine einzige hat.
"""

from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass, field

from ap_trainer.content.aufgaben import Aufgabe
from ap_trainer.tasks.generators import make, registry

# So viele zuletzt gelöste Aufgaben werden bei der Auswahl gemieden
RECENT_WINDOW = 15
SEED_MAX = 2**31 - 1


@dataclass(frozen=True)
class TopicPool:
    """Alle Aufgabenquellen eines Themas."""

    thema: str
    aufgaben: list[Aufgabe] = field(default_factory=list)
    generatoren: list[str] = field(default_factory=list)

    def levels(self) -> list[int]:
        """Stufen, auf denen es Aufgaben gibt, aufsteigend."""
        found = {task.stufe for task in self.aufgaben}
        for generator_id in self.generatoren:
            found.update(registry()[generator_id].stufen)
        return sorted(found)

    def is_empty(self) -> bool:
        """True, wenn es zu diesem Thema weder feste Aufgaben noch Generatoren gibt."""
        return not self.aufgaben and not self.generatoren

    def sources_at(self, stufe: int) -> tuple[list[Aufgabe], list[str]]:
        """Feste Aufgaben und Generatoren genau dieser Stufe."""
        tasks = [task for task in self.aufgaben if task.stufe == stufe]
        generators = [g for g in self.generatoren if stufe in registry()[g].stufen]
        return tasks, generators


def target_level(levels: Sequence[int], wanted: int) -> int | None:
    """Die Stufe, aus der gezogen wird: ``wanted``, sonst darunter, sonst darüber."""
    if not levels:
        return None
    lower = [s for s in levels if s <= wanted]
    return max(lower) if lower else min(levels)


def pick_task(pool: TopicPool, stufe: int, recent_ids: Sequence[str], rng: random.Random) -> Aufgabe | None:
    """Zieht die nächste Aufgabe für ``stufe``; ``recent_ids`` sind die zuletzt gelösten Aufgaben-IDs."""
    level = target_level(pool.levels(), stufe)
    if level is None:
        return None
    recent = list(recent_ids)[-RECENT_WINDOW:]
    picked = _pick_at(pool, level, recent, rng)
    if picked is not None:
        return picked
    # Auf dieser Stufe ist alles zuletzt dran gewesen: erst Nachbarstufen mit Neuem probieren
    for other in _by_distance(pool.levels(), level):
        picked = _pick_at(pool, other, recent, rng)
        if picked is not None:
            return picked
    return _least_recent(pool, level, recent)


def _pick_at(pool: TopicPool, level: int, recent: list[str], rng: random.Random) -> Aufgabe | None:
    """Eine noch nicht zuletzt gesehene feste Aufgabe oder eine Generatorvariante dieser Stufe."""
    tasks, generators = pool.sources_at(level)
    fresh = [task for task in tasks if task.id not in recent]
    # Feste, länger nicht gesehene Aufgaben und Generatorvarianten wechseln sich zufällig ab
    if fresh and (not generators or rng.random() < 0.5):
        return rng.choice(fresh)
    if generators:
        return make(rng.choice(generators), level, rng.randint(0, SEED_MAX), pool.thema)
    return None


def _by_distance(levels: Sequence[int], level: int) -> list[int]:
    """Die anderen Stufen, nächstgelegene zuerst; bei Gleichstand die höhere (dort gibt es Neues)."""
    return sorted((s for s in levels if s != level), key=lambda s: (abs(s - level), -s))


def _least_recent(pool: TopicPool, level: int, recent: list[str]) -> Aufgabe:
    """Alles zuletzt gesehen: die am längsten zurückliegende Aufgabe, möglichst nicht die letzte."""
    last = recent[-1] if recent else None
    candidates = [t for t in pool.aufgaben if t.stufe == level and t.id != last]
    if not candidates:
        candidates = [t for t in pool.aufgaben if t.id != last] or list(pool.aufgaben)
    return min(candidates, key=lambda t: (_last_seen(recent, t.id), abs(t.stufe - level)))


def _last_seen(recent: list[str], task_id: str) -> int:
    """Position des letzten Vorkommens (kleiner = länger her)."""
    return max((i for i, value in enumerate(recent) if value == task_id), default=-1)
