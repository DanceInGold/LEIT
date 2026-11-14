"""Schema des Operatoren-Trainings (ZI-02): Operatoren mit Erwartung und Musterantworten.

Ein Operator ist das Verb einer Prüfungsaufgabe („nennen“, „erläutern“ …). Er legt fest, wie tief
die Antwort gehen muss. Die Datei ``operatoren.yaml`` beschreibt jeden Operator und enthält
Beispiele: eine Situation, zu der es für **jeden** Operator eine Frage mit Musterantwort gibt.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ap_trainer.content.aufgaben import _ID, Operator
from ap_trainer.content.models import Beleg, Status

# Anforderungsbereich: I Wiedergeben, II Anwenden/Erklären, III Urteilen/Begründen
Bereich = Literal["I", "II", "III"]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class OperatorInfo(_Strict):
    """Was ein Operator verlangt und woran man eine gute Antwort erkennt."""

    id: Operator
    bereich: Bereich
    # Was erwartet der Prüfer? (ein Satz)
    verlangt: str
    # Antwortform, z. B. „Stichworte“, „ganze Sätze mit weil“, „Tabelle“
    form: str
    # Typischer Fehler, der Punkte kostet
    falle: str
    satzanfaenge: list[str] = Field(default_factory=list)
    # Prüfpunkte für die Selbstbewertung eigener Antworten
    kriterien: list[str] = Field(min_length=2, max_length=4)


class OperatorAntwort(_Strict):
    """Frage mit diesem Operator und Musterantwort (Markdown)."""

    frage: str
    antwort: str


class OperatorBeispiel(_Strict):
    """Eine Situation mit derselben Sache, gefragt mit jedem Operator."""

    id: str
    thema: str
    titel: str
    situation: str
    antworten: dict[Operator, OperatorAntwort]

    @field_validator("id")
    @classmethod
    def _check_id(cls, value: str) -> str:
        if not _ID.match(value):
            raise ValueError("id nur aus Kleinbuchstaben, Ziffern und Bindestrichen")
        return value


class OperatorenDatei(_Strict):
    """Inhalt von ``operatoren.yaml``."""

    quelle: str
    status: Status
    belege: list[Beleg] = Field(min_length=1)
    operatoren: list[OperatorInfo] = Field(min_length=2)
    beispiele: list[OperatorBeispiel] = Field(min_length=1)

    @model_validator(mode="after")
    def _complete(self) -> OperatorenDatei:
        ids = [op.id for op in self.operatoren]
        if len(set(ids)) != len(ids):
            raise ValueError("Operator doppelt")
        for example in self.beispiele:
            missing = set(ids) - set(example.antworten)
            extra = set(example.antworten) - set(ids)
            if missing or extra:
                raise ValueError(
                    f"Beispiel {example.id}: fehlend {sorted(missing)}, unbekannt {sorted(extra)}"
                )
        return self

    def by_id(self) -> dict[str, OperatorInfo]:
        """Operatoren nach ID, in der Reihenfolge der Datei."""
        return {op.id: op for op in self.operatoren}
