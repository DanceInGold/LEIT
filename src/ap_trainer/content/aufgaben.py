"""Schema der Aufgaben: sechs Aufgabentypen als Pydantic-Modelle (AU-01, AU-02, AU-05, HI-01, HI-03).

Dieselben Modelle beschreiben Aufgaben aus den YAML-Dateien eines Pakets
(``content/<paket>/aufgaben/<thema>.yaml``) und Aufgaben, die ein Generator erzeugt.
Die Bewertung einer Antwort steht nicht hier, sondern in ``ap_trainer.tasks.check``.
"""

from __future__ import annotations

import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, field_validator, model_validator

from ap_trainer.content.models import Beleg, Status

# Schwierigkeitsstufen nach AU-02
Stufe = Literal[1, 2, 3, 4, 5]
STUFEN_NAMEN: dict[int, str] = {
    1: "Erinnern",
    2: "Verstehen",
    3: "Anwenden",
    4: "Analysieren",
    5: "Prüfungsniveau",
}

# Fehlerursachen für das Fehlerprotokoll (FT-04)
Fehlerursache = Literal["rechenfehler", "begriff", "konzept"]
URSACHE_NAMEN: dict[str, str] = {
    "rechenfehler": "Rechenfehler",
    "begriff": "Begriff verwechselt",
    "konzept": "Konzept nicht verstanden",
}

# Wie eine Eingabe in einem Rechenschritt gelesen wird (siehe tasks/answers.py)
Antwortformat = Literal["zahl", "dual", "hex", "ipv4", "ipv6", "text"]

# Operatoren offener Prüfungsfragen (Vorbereitung auf ZI-02)
Operator = Literal["nennen", "beschreiben", "erläutern", "begründen", "vergleichen", "beurteilen"]

# Platzhalter für Lücken im Lückentext: {{1}}, {{2}}, …
LUECKE = re.compile(r"\{\{(\d+)\}\}")

# Erlaubte IDs: Kleinbuchstaben, Ziffern, Bindestriche (wie Lektionen und Begriffe)
_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class _Strict(BaseModel):
    """Basis: unbekannte Felder sind ein Fehler, damit Tippfehler auffallen."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class Fehlerbild(_Strict):
    """Typische Falschantwort mit eigener Erklärung, warum sie falsch ist (HI-03)."""

    antwort: str
    warum: str
    ursache: Fehlerursache = "konzept"


class _AufgabeBasis(_Strict):
    """Gemeinsame Felder aller Aufgabentypen."""

    id: str
    thema: str
    stufe: Stufe
    titel: str
    # Handlungssituation als Einstieg (Markdown), vor allem ab Stufe 4
    situation: str | None = None
    # Die eigentliche Aufgabenstellung (Markdown)
    frage: str
    # Gestufte Hilfen (HI-01): 1 Richtung, 2 Ansatz/Formel, 3 erster Schritt
    hinweise: list[str] = Field(default_factory=list, max_length=3)
    # Vollständiger Lösungsweg (HI-01, letzte Hilfestufe; nach dem Prüfen immer sichtbar)
    loesungsweg: str
    quelle: str
    belege: list[Beleg] = Field(default_factory=list)
    status: Status

    @field_validator("id")
    @classmethod
    def _check_id(cls, value: str) -> str:
        # Generierte Aufgaben tragen „gen:<generator>:<stufe>:<seed>“ und sind davon ausgenommen
        if not value.startswith("gen:") and not _ID.match(value):
            raise ValueError("id nur aus Kleinbuchstaben, Ziffern und Bindestrichen")
        return value


class Option(_Strict):
    """Antwortmöglichkeit einer Multiple-Choice-Aufgabe."""

    text: str
    richtig: bool = False
    # Warum diese Option (nicht) stimmt; bei falschen Optionen das Fehlerfeedback (HI-03)
    warum: str | None = None
    ursache: Fehlerursache = "konzept"


class MultipleChoice(_AufgabeBasis):
    """Eine oder mehrere richtige Optionen ankreuzen."""

    typ: Literal["multiple_choice"]
    optionen: list[Option] = Field(min_length=2)

    @model_validator(mode="after")
    def _check_options(self) -> MultipleChoice:
        if not any(o.richtig for o in self.optionen):
            raise ValueError("mindestens eine Option muss richtig sein")
        if all(o.richtig for o in self.optionen):
            raise ValueError("mindestens eine Option muss falsch sein")
        return self

    @property
    def anzahl_richtig(self) -> int:
        """Wie viele Optionen anzukreuzen sind (wird in der Aufgabe angezeigt)."""
        return sum(1 for o in self.optionen if o.richtig)


class Paar(_Strict):
    """Ein Element links und das, was rechts dazugehört."""

    links: str
    rechts: str


class Zuordnung(_AufgabeBasis):
    """Jedem Element links das passende Element rechts zuordnen."""

    typ: Literal["zuordnung"]
    paare: list[Paar] = Field(min_length=2)
    # Zusätzliche rechte Elemente, die zu nichts passen (erschweren Raten)
    ablenker: list[str] = Field(default_factory=list)

    @property
    def auswahl(self) -> list[str]:
        """Alle wählbaren rechten Elemente, alphabetisch und ohne Doppelte."""
        return sorted({p.rechts for p in self.paare} | set(self.ablenker), key=str.casefold)


class Luecke(_Strict):
    """Eine Lücke mit allen akzeptierten Antworten und typischen Falschantworten."""

    antworten: list[str] = Field(min_length=1)
    falsch: list[Fehlerbild] = Field(default_factory=list)


class Lueckentext(_AufgabeBasis):
    """Text mit Platzhaltern ``{{1}}``, ``{{2}}`` …, die ausgefüllt werden."""

    typ: Literal["lueckentext"]
    text: str
    luecken: list[Luecke] = Field(min_length=1)

    @model_validator(mode="after")
    def _check_gaps(self) -> Lueckentext:
        numbers = [int(n) for n in LUECKE.findall(self.text)]
        expected = list(range(1, len(self.luecken) + 1))
        if sorted(numbers) != expected:
            raise ValueError(f"Platzhalter im Text ({numbers}) passen nicht zu {len(self.luecken)} Lücken")
        return self


class Reihenfolge(_AufgabeBasis):
    """Elemente in die richtige Reihenfolge bringen; ``elemente`` steht in der Lösungsreihenfolge."""

    typ: Literal["reihenfolge"]
    elemente: list[str] = Field(min_length=3)

    @field_validator("elemente")
    @classmethod
    def _unique(cls, value: list[str]) -> list[str]:
        if len(set(value)) != len(value):
            raise ValueError("Elemente müssen verschieden sein")
        return value


class Rechenschritt(_Strict):
    """Ein Zwischenschritt einer Rechenaufgabe, der einzeln geprüft wird (AU-04)."""

    frage: str
    antwort: str
    format: Antwortformat = "zahl"
    einheit: str | None = None
    # Erlaubte relative Abweichung bei Zahlen, z. B. 0.01 = 1 % (für gerundete Ergebnisse)
    toleranz: float = Field(default=0.0, ge=0, lt=1)
    # Wie man auf diesen Schritt kommt; erscheint im Feedback, wenn er falsch ist
    erklaerung: str
    falsch: list[Fehlerbild] = Field(default_factory=list)


class Rechnung(_AufgabeBasis):
    """Rechenaufgabe mit Lösungsweg: jeder Zwischenschritt wird geprüft (AU-04)."""

    typ: Literal["rechnung"]
    schritte: list[Rechenschritt] = Field(min_length=1)


class Bewertungspunkt(_Strict):
    """Ein Punkt der Musterlösung, den eine gute Freitextantwort enthält (AU-05)."""

    punkt: str
    # Wörter, an denen man den Punkt in der Antwort erkennt (Teilwort, Groß/klein egal)
    kernbegriffe: list[str] = Field(default_factory=list)
    punkte: int = Field(default=1, ge=1)


class Freitext(_AufgabeBasis):
    """Offene Frage: Selbstbewertung anhand der Bewertungspunkte (AU-05)."""

    typ: Literal["freitext"]
    operator: Operator | None = None
    musterloesung: str
    bewertungspunkte: list[Bewertungspunkt] = Field(min_length=1)


Aufgabe = Annotated[
    MultipleChoice | Zuordnung | Lueckentext | Reihenfolge | Rechnung | Freitext,
    Field(discriminator="typ"),
]
AUFGABE: TypeAdapter[Aufgabe] = TypeAdapter(Aufgabe)

TYP_NAMEN: dict[str, str] = {
    "multiple_choice": "Multiple Choice",
    "zuordnung": "Zuordnung",
    "lueckentext": "Lückentext",
    "reihenfolge": "Reihenfolge",
    "rechnung": "Rechenaufgabe",
    "freitext": "Freitext",
}


class AufgabenDatei(_Strict):
    """Inhalt einer Datei ``aufgaben/<thema>.yaml``: Generatoren und feste Aufgaben eines Themas."""

    # IDs der Aufgabengeneratoren, die zu diesem Thema passen (AU-03)
    generatoren: list[str] = Field(default_factory=list)
    aufgaben: list[Aufgabe] = Field(default_factory=list)
