"""Welche Aufgabe kommt als Nächstes? Auswahl aus festen Aufgaben und Generatoren eines Themas.

Gesucht wird auf der aktuellen Stufe; gibt es dort nichts, auf der nächstniedrigeren, sonst
auf der nächsthöheren. Feste Aufgaben, die zuletzt dran waren, kommen ans Ende; Generatoren
liefern immer neue Varianten und mischen sich mit den festen Aufgaben.
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
    tasks, generators = pool.sources_at(level)
    recent = list(recent_ids)[-RECENT_WINDOW:]
    fresh = [task for task in tasks if task.id not in recent]
    # Feste, länger nicht gesehene Aufgaben und Generatorvarianten wechseln sich zufällig ab
    if fresh and (not generators or rng.random() < 0.5):
        return rng.choice(fresh)
    if generators:
        return make(rng.choice(generators), level, rng.randint(0, SEED_MAX), pool.thema)
    # Nur feste Aufgaben, alle zuletzt gesehen: die am längsten zurückliegende zuerst
    return min(tasks, key=lambda task: _last_seen(recent, task.id))


def _last_seen(recent: list[str], task_id: str) -> int:
    """Position des letzten Vorkommens (kleiner = länger her)."""
    return max((i for i, value in enumerate(recent) if value == task_id), default=-1)
