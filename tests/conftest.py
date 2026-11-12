"""Gemeinsame Test-Hilfen: Mini-Inhaltspaket und Ersatz für ``fsrs``, falls nicht installiert.

In der CI ist das echte ``fsrs`` installiert und wird getestet; der Ersatz greift nur in
schlanken Umgebungen, damit die Abläufe der Anwendung trotzdem prüfbar bleiben.
"""

from __future__ import annotations

import datetime as dt
import enum
import importlib.util
import sys
import types
from pathlib import Path
from typing import Any

import pytest

if (
    "fsrs" not in sys.modules and importlib.util.find_spec("fsrs") is None
):  # pragma: no cover - nur ohne echtes Paket
    stub = types.ModuleType("fsrs")

    class Rating(enum.IntEnum):
        Again = 1
        Hard = 2
        Good = 3
        Easy = 4

    class Card:
        def __init__(self) -> None:
            self.due = dt.datetime.now(dt.UTC)
            self.reps = 0

        def to_dict(self) -> dict[str, Any]:
            return {"due": self.due.isoformat(), "reps": self.reps}

        @classmethod
        def from_dict(cls, data: dict[str, Any]) -> Card:
            card = cls()
            card.due = dt.datetime.fromisoformat(data["due"])
            card.reps = data["reps"]
            return card

    class Scheduler:
        def review_card(self, card: Card, rating: Rating, review_datetime: dt.datetime) -> tuple[Card, None]:
            card.reps += 1
            card.due = review_datetime + dt.timedelta(days=[0, 0, 1, 3, 7][int(rating)])
            return card, None

    stub.Card = Card  # type: ignore[attr-defined]
    stub.Rating = Rating  # type: ignore[attr-defined]
    stub.Scheduler = Scheduler  # type: ignore[attr-defined]
    sys.modules["fsrs"] = stub

PAKET = """
id: test
name: Testpaket
pruefungsteil: AP1
berufe: [alle]
katalogversion: "2025"
paketversion: "0.0.1"
status: entwurf
pruefungsbereiche:
  - {id: a, name: A, dauer_minuten: 90, gewichtung_prozent: 20, aufgabenart: ungebunden, punkte: 100}
pruefungstermine:
  - {datum: 2027-02-24, bezeichnung: Frühjahr 2027}
"""

KATALOG = """
version: test
status: entwurf
gewichtung:
  methode: test
  cluster_punkte: {Netz: 60, Hardware: 40}
  einzelthemen_punkte: {subnetting: 30}
  mindestgewicht: 0.5
  wiederholungszuschlag: 0.2
bereiche:
  - {id: b1, name: Bereich}
themen:
  - {id: zahlen, titel: Zahlensysteme, bereich: b1, cluster: Netz, stand_2025: aktiv, aufwand_h: 2}
  - {id: subnetting, titel: Subnetting, bereich: b1, cluster: Netz, stand_2025: neu,
     voraussetzungen: [zahlen], aufwand_h: 5}
  - {id: hardware, titel: Hardware, bereich: b1, cluster: Hardware, stand_2025: aktiv, aufwand_h: 4}
  - {id: extra, titel: Zusatz, bereich: b1, stand_2025: ausserhalb, gewicht: 0.3, aufwand_h: 1}
  - {id: raid, titel: RAID, bereich: b1, cluster: Hardware, stand_2025: entfallen, gewicht: 0}
"""

LEKTION = """---
id: zahlen-1
titel: Zahlensysteme
themen: [zahlen]
dauer_min: 30
quelle: neu erstellt
belege:
  - {titel: Testbeleg}
status: ungeprüft
---
## Worum geht es?
Zahlen.
## Wie funktioniert es?
Stellenwerte. Siehe [Bit](glossar:bit).
## Warum ist es so?
Weil Strom an oder aus ist.
## Praxisbezug im Betrieb
Rechte in Linux.
## Typische Prüfungsfalle
Bit und Byte verwechseln.
## Merksatz
Acht Bit sind ein Byte.
"""

BEGRIFF = """
id: bit
begriff: Bit
langform: Binary Digit
kurz: Kleinste Informationseinheit mit den Werten 0 oder 1.
erklaerung: Ein Bit unterscheidet genau zwei Zustände.
beispiel: Ein Byte besteht aus acht Bit.
verwandt: []
thema: zahlen
quelle: neu erstellt
status: ungeprüft
"""


def write_package(root: Path) -> Path:
    """Schreibt ein gültiges Mini-Paket nach ``root`` und gibt den Pfad zurück."""
    (root / "lektionen").mkdir(parents=True)
    (root / "glossar").mkdir()
    (root / "paket.yaml").write_text(PAKET, encoding="utf-8")
    (root / "katalog.yaml").write_text(KATALOG, encoding="utf-8")
    (root / "lektionen" / "zahlen-1.md").write_text(LEKTION, encoding="utf-8")
    (root / "glossar" / "bit.yaml").write_text(BEGRIFF, encoding="utf-8")
    return root


@pytest.fixture
def package_dir(tmp_path: Path) -> Path:
    """Pfad zu einem frischen, gültigen Mini-Inhaltspaket."""
    return write_package(tmp_path / "paket")
