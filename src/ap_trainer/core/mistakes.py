"""Fehlerprotokoll (FT-04): falsch gelöste Aufgaben, gruppiert nach Fehlerursache.

Je Aufgabe gibt es einen Eintrag mit dem letzten Fehlversuch. Wird dieselbe Aufgabe später
richtig gelöst, gilt der Fehler als behoben – er bleibt sichtbar, aber nicht mehr als offen.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Sequence
from dataclasses import dataclass

from ap_trainer.core.models import Attempt

# Reihenfolge und Beschriftung der Gruppen; Fehler ohne erkanntes Fehlerbild landen zuletzt
CAUSE_LABELS: dict[str, str] = {
    "rechenfehler": "Rechenfehler",
    "begriff": "Begriff verwechselt",
    "konzept": "Konzept nicht verstanden",
    "unbekannt": "Ursache nicht erkannt",
}


@dataclass(frozen=True)
class MistakeEntry:
    """Eine falsch gelöste Aufgabe mit ihrem letzten Fehlversuch."""

    aufgabe_id: str
    thema: str
    ursache: str
    zuletzt_falsch: dt.datetime
    fehlversuche: int
    behoben: bool
    antwort: str
    fehlerschritt: int | None


@dataclass(frozen=True)
class MistakeGroup:
    """Alle Einträge einer Fehlerursache, neueste zuerst."""

    ursache: str
    titel: str
    eintraege: list[MistakeEntry]

    @property
    def offen(self) -> int:
        """Zahl der noch nicht behobenen Fehler."""
        return sum(not e.behoben for e in self.eintraege)


def _entry(task_id: str, history: list[Attempt]) -> MistakeEntry | None:
    """Eintrag für eine Aufgabe aus ihren Versuchen; ``None``, wenn sie nie falsch war."""
    wrong = [i for i, a in enumerate(history) if not a.richtig]
    if not wrong:
        return None
    last = history[wrong[-1]]
    # Behoben, wenn nach dem letzten Fehlversuch ein richtiger kam (Versuche sind zeitlich sortiert)
    fixed = any(a.richtig for a in history[wrong[-1] + 1 :])
    return MistakeEntry(
        aufgabe_id=task_id,
        thema=last.thema,
        ursache=last.ursache if last.ursache in CAUSE_LABELS else "unbekannt",
        zuletzt_falsch=last.am,
        fehlversuche=len(wrong),
        behoben=fixed,
        antwort=last.antwort,
        fehlerschritt=last.fehlerschritt,
    )


def mistake_log(attempts: Sequence[Attempt], include_fixed: bool = True) -> list[MistakeGroup]:
    """Fehlerprotokoll aus allen Versuchen (zeitlich sortiert), gruppiert nach Ursache."""
    by_task: dict[str, list[Attempt]] = {}
    for attempt in attempts:
        by_task.setdefault(attempt.aufgabe_id, []).append(attempt)
    entries = [e for task_id, history in by_task.items() if (e := _entry(task_id, history)) is not None]
    if not include_fixed:
        entries = [e for e in entries if not e.behoben]
    # Neueste Fehler zuerst: Die Versuche sind zeitlich sortiert, also zählt die Position
    latest = {a.aufgabe_id: i for i, a in enumerate(attempts) if not a.richtig}
    entries.sort(key=lambda e: latest[e.aufgabe_id], reverse=True)
    groups = []
    for cause, title in CAUSE_LABELS.items():
        members = [e for e in entries if e.ursache == cause]
        if members:
            groups.append(MistakeGroup(cause, title, members))
    return groups
