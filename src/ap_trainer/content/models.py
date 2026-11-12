"""Pydantic-Modelle für Inhaltspakete: Paket, Katalog, Thema, Lektion, Glossarbegriff.

Die Modelle sind das Schema, gegen das jede Inhaltsdatei beim Start und in der CI geprüft
wird (NF-08). Feldnamen entsprechen den Schlüsseln in den YAML- bzw. Frontmatter-Dateien.
"""

from __future__ import annotations

import datetime as dt
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Prüfstatus jeder Lektion und jedes Begriffs (LI-06).
Status = Literal["ungeprüft", "korrigiert", "geprüft"]

# Stand eines Themas im Prüfungskatalog 2025.
Stand = Literal["aktiv", "neu", "entfallen", "ausserhalb"]

# Pflichtabschnitte einer Lektion in genau dieser Reihenfolge (Raster LI-01).
LESSON_SECTIONS: tuple[str, ...] = (
    "Worum geht es?",
    "Wie funktioniert es?",
    "Warum ist es so?",
    "Praxisbezug im Betrieb",
    "Typische Prüfungsfalle",
    "Merksatz",
)


class _Strict(BaseModel):
    """Basis: unbekannte Felder sind ein Fehler, damit Tippfehler auffallen."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class Pruefungsbereich(_Strict):
    """Ein Prüfungsbereich mit Dauer, Gewichtung und Aufgabenart (ER-05)."""

    id: str
    name: str
    rechtsgrundlage: str | None = None
    dauer_minuten: int = Field(gt=0)
    gewichtung_prozent: float = Field(gt=0, le=100)
    aufgabenart: Literal["ungebunden", "gebunden", "gemischt"]
    punkte: int = Field(gt=0)


class Pruefungstermin(_Strict):
    """Vorbelegter Prüfungstermin für die Terminauswahl (LP-01)."""

    datum: dt.date
    bezeichnung: str
    quelle: str | None = None


class Paket(_Strict):
    """Selbstbeschreibung eines Inhaltspakets (ER-01)."""

    id: str
    name: str
    pruefungsteil: str
    berufe: list[str]
    katalogversion: str
    paketversion: str
    status: Literal["entwurf", "freigegeben"]
    pruefungsbereiche: list[Pruefungsbereich] = Field(min_length=1)
    pruefungstermine: list[Pruefungstermin] = Field(default_factory=list)


class Bereich(_Strict):
    """Oberster Gliederungspunkt des Katalogs."""

    id: str
    name: str


class Thema(_Strict):
    """Ein Thema des Prüfungskatalogs mit Abhängigkeiten, Gewicht und Aufwand."""

    id: str
    titel: str
    bereich: str
    katalog: list[str] = Field(default_factory=list)
    cluster: str | None = None
    stand_2025: Stand
    voraussetzungen: list[str] = Field(default_factory=list)
    gewicht: float | None = Field(default=None, ge=0)
    aufwand_h: float | None = Field(default=None, gt=0)
    hinweis: str | None = None

    @property
    def is_relevant(self) -> bool:
        """True, wenn das Thema geplant und gelernt wird (alles außer entfallen)."""
        return self.stand_2025 != "entfallen"


class Gewichtung(_Strict):
    """Eingangsdaten für die vorläufige Themengewichtung (LP-07, Kap. 2)."""

    methode: str
    cluster_punkte: dict[str, float]
    einzelthemen_punkte: dict[str, float] = Field(default_factory=dict)
    mindestgewicht: float = Field(default=0.5, ge=0)
    wiederholungszuschlag: float = Field(default=0.2, ge=0, le=1)


class Katalog(_Strict):
    """Themenbaum eines Pakets."""

    version: str
    status: Literal["entwurf", "freigegeben"]
    gewichtung: Gewichtung
    bereiche: list[Bereich]
    themen: list[Thema]

    def by_id(self) -> dict[str, Thema]:
        """Themen als Wörterbuch nach ID."""
        return {t.id: t for t in self.themen}


class Beleg(_Strict):
    """Quelle, gegen die eine Aussage geprüft wurde."""

    titel: str
    url: str | None = None


class Lektion(_Strict):
    """Eine Lektion: Kopfdaten aus dem Frontmatter plus Markdown-Abschnitte."""

    id: str
    titel: str
    themen: list[str] = Field(min_length=1)
    voraussetzungen: list[str] = Field(default_factory=list)
    dauer_min: int = Field(gt=0, le=180)
    quelle: str
    belege: list[Beleg] = Field(min_length=1)
    status: Status
    # Abschnittsüberschrift → Markdown-Text; vom Loader befüllt.
    abschnitte: dict[str, str]

    @field_validator("abschnitte")
    @classmethod
    def _check_sections(cls, value: dict[str, str]) -> dict[str, str]:
        present = [title for title in value if title in LESSON_SECTIONS]
        missing = [title for title in LESSON_SECTIONS if title not in value]
        if missing:
            raise ValueError(f"Pflichtabschnitte fehlen: {', '.join(missing)}")
        if present != list(LESSON_SECTIONS):
            raise ValueError("Pflichtabschnitte stehen nicht in der Reihenfolge des Rasters LI-01")
        empty = [title for title in LESSON_SECTIONS if not value[title].strip()]
        if empty:
            raise ValueError(f"Abschnitte ohne Inhalt: {', '.join(empty)}")
        return value


class Begriff(_Strict):
    """Ein Eintrag im Fachwort-Kompendium (GL-01)."""

    id: str
    begriff: str
    langform: str | None = None
    kurz: str = Field(min_length=10, max_length=200)
    erklaerung: str
    warum: str | None = None
    beispiel: str
    verwandt: list[str] = Field(default_factory=list)
    thema: str
    quelle: str
    status: Status
