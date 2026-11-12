"""Schema- und Verweisprüfung aller Inhalte eines Pakets (``ap-tools check``, NF-08).

Läuft lokal und in der CI. Gibt jede Fehlerzeile aus und endet mit Code 1, wenn etwas
nicht stimmt – so fällt ein Tippfehler in einer Lektion vor dem Merge auf.
"""

from __future__ import annotations

from pathlib import Path

from ap_trainer.content.checks import check_references
from ap_trainer.content.loader import load_package


def run_check(root: Path) -> int:
    """Prüft das Paket unter ``root`` und gibt den Exit-Code zurück."""
    package, errors = load_package(root)
    if package is not None:
        errors += check_references(package)
    for error in errors:
        print(f"FEHLER {error}")
    if errors:
        print(f"{len(errors)} Fehler gefunden.")
        return 1
    assert package is not None
    print(
        f"Inhalte in Ordnung: {len(package.katalog.themen)} Themen, "
        f"{len(package.lektionen)} Lektionen, {len(package.begriffe)} Begriffe."
    )
    return 0
