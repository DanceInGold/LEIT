"""Schema- und Verweisprüfung aller Inhalte eines Pakets (``ap-tools check``, NF-08).

Läuft lokal und in der CI. Gibt jede Fehlerzeile aus und endet mit Code 1, wenn etwas
nicht stimmt – so fällt ein Tippfehler in einer Lektion vor dem Merge auf.
"""

from __future__ import annotations

from pathlib import Path

from ap_trainer.content.checks import check_references, check_style
from ap_trainer.content.loader import load_package
from ap_trainer.tasks.validate import check_tasks


def run_check(root: Path, strict: bool = False) -> int:
    """Prüft das Paket unter ``root`` und gibt den Exit-Code zurück.

    Stilwarnungen (zu viel Text) brechen nur mit ``strict`` ab.
    """
    package, errors = load_package(root)
    warnings = []
    if package is not None:
        errors += check_references(package)
        errors += check_tasks(package)
        warnings = check_style(package)
    for warning in warnings:
        print(f"WARNUNG {warning}")
    if strict:
        errors += warnings
    for error in errors:
        print(f"FEHLER {error}")
    if errors:
        print(f"{len(errors)} Fehler gefunden.")
        return 1
    assert package is not None
    print(
        f"Inhalte in Ordnung: {len(package.katalog.themen)} Themen, "
        f"{len(package.lektionen)} Lektionen, {len(package.begriffe)} Begriffe, "
        f"{len(package.aufgaben)} Aufgaben, {sum(map(len, package.generatoren.values()))} Generatoren, "
        f"{len(warnings)} Stilwarnungen."
    )
    return 0
