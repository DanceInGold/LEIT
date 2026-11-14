"""Beherrschungsgrad je Thema (FT-01) und Ampel für die Themenkarte (FT-02).

Der Grad (0–100 %) verbindet vier Größen aus den Übungsversuchen eines Themas:
Trefferquote, Schwierigkeitsstufe, Hilfenutzung und Abstand seit dem letzten Erfolg.
Die Formel und ihre Konstanten sind in docs/entscheidungen.md (E-34) begründet.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from ap_trainer.core.models import Attempt

# Nur die letzten Versuche zählen: Wer sich verbessert hat, soll das schnell sehen
RECENT_ATTEMPTS = 10
# Wie viel eine Lösung mit Hilfe noch zählt, je Hilfestufe (0 = ohne, 4 = Lösungsweg gesehen)
HELP_FACTOR = {0: 1.0, 1: 0.9, 2: 0.7, 3: 0.5, 4: 0.2}
# Ohne einen einzigen sicheren Erfolg erreicht der Grad höchstens diesen Anteil der Qualität
REACH_BASE = 0.5
# Vergessen: bis 7 Tage nach dem letzten Erfolg kein Abzug, danach Halbwertszeit 30 Tage bis 60 %
FRESH_DAYS = 7
HALF_LIFE_DAYS = 30
RECENCY_FLOOR = 0.6
# Ampelgrenzen; 80 % ist auch die Schwelle für Themen-Abzeichen (ZI-12)
GREEN_FROM = 80
YELLOW_FROM = 50

Ampel = Literal["grün", "gelb", "rot", "grau"]
AMPEL_LABELS: dict[Ampel, str] = {
    "grün": "sicher",
    "gelb": "unsicher",
    "rot": "Lücke",
    "grau": "noch nicht geübt",
}


@dataclass(frozen=True)
class Mastery:
    """Beherrschungsgrad eines Themas mit seinen Bestandteilen (jeweils 0–1)."""

    grad: int | None
    qualitaet: float = 0.0
    reichweite: float = 0.0
    frische: float = 0.0
    versuche: int = 0

    @property
    def ampel(self) -> Ampel:
        """Ampelfarbe für die Themenkarte; grau, solange nicht geübt wurde."""
        if self.grad is None:
            return "grau"
        if self.grad >= GREEN_FROM:
            return "grün"
        return "gelb" if self.grad >= YELLOW_FROM else "rot"


def attempt_score(attempt: Attempt) -> float:
    """Wert eines Versuchs: Anteil richtiger Teile, gemindert durch genutzte Hilfen.

    Ein falscher Versuch zählt mit seinem Teilanteil (z. B. 2 von 3 Lücken), damit knappe
    Fehler nicht wie völlige Unkenntnis wirken.
    """
    share = 1.0 if attempt.richtig else attempt.anteil
    return share * HELP_FACTOR.get(attempt.hilfen, HELP_FACTOR[4])


def quality(attempts: Sequence[Attempt]) -> float:
    """Trefferquote der letzten Versuche, nach Stufe gewichtet (Stufe 4 zählt viermal so viel wie 1)."""
    recent = list(attempts)[-RECENT_ATTEMPTS:]
    total = sum(a.stufe for a in recent)
    return sum(a.stufe * attempt_score(a) for a in recent) / total if total else 0.0


def reach(attempts: Sequence[Attempt], max_level: int) -> float:
    """Wie hoch hinauf das Thema sicher gelöst wurde (richtig, höchstens Hinweis 1).

    Ohne sicheren Erfolg 0,5; wer die höchste Stufe sicher löst, erreicht 1,0.
    """
    secure = [a.stufe for a in attempts if a.richtig and a.hilfen <= 1]
    if not secure or max_level <= 0:
        return REACH_BASE
    return REACH_BASE + (1 - REACH_BASE) * min(max(secure), max_level) / max_level


def _aware(moment: dt.datetime) -> dt.datetime:
    """Zeitpunkte ohne Zeitzone gelten als UTC (ältere Exporte)."""
    return moment if moment.tzinfo else moment.replace(tzinfo=dt.UTC)


def recency(attempts: Sequence[Attempt], now: dt.datetime) -> float:
    """Abzug für lange zurückliegende Erfolge; ohne jeden Erfolg die Untergrenze."""
    successes = [_aware(a.am) for a in attempts if a.richtig]
    if not successes:
        return RECENCY_FLOOR
    days = max(0.0, (_aware(now) - max(successes)).total_seconds() / 86_400 - FRESH_DAYS)
    decay: float = 0.5 ** (days / HALF_LIFE_DAYS)
    return RECENCY_FLOOR + (1 - RECENCY_FLOOR) * decay


def mastery(attempts: Sequence[Attempt], max_level: int, now: dt.datetime) -> Mastery:
    """Beherrschungsgrad aus allen Versuchen eines Themas (zeitlich sortiert)."""
    if not attempts:
        return Mastery(grad=None)
    q, r, f = quality(attempts), reach(attempts, max_level), recency(attempts, now)
    return Mastery(grad=round(100 * q * r * f), qualitaet=q, reichweite=r, frische=f, versuche=len(attempts))
