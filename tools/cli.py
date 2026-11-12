"""Gemeinsamer Einstieg für die Pipeline-Werkzeuge: ``uv run ap-tools <befehl>``.

Bewusst mit ``argparse`` statt Typer umgesetzt (siehe docs/entscheidungen.md):
keine zusätzliche Abhängigkeit, läuft in jeder Python-3.12-Umgebung.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tools import inventory
from tools.check_content import run_check

REPO_ROOT = Path(__file__).resolve().parent.parent


def _cmd_inventur(args: argparse.Namespace) -> int:
    root = Path(args.quellen)
    manifest_path = Path(args.manifest)
    if not root.is_dir():
        print(f"Ordner nicht gefunden: {root}", file=sys.stderr)
        return 2

    old = inventory.load_manifest(manifest_path)
    current = inventory.scan(root)
    changes = inventory.compare(old, current)
    report = inventory.render_report(changes, current)
    print(report)

    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as out:
            out.write(f"changed={'false' if changes.is_empty else 'true'}\n")
            out.write(f"summary={changes.summary()}\n")

    if args.check:
        return 0

    touched = changes.new + changes.changed + [new for _, new in changes.renamed]
    targets = [e.path for e in current] if args.alle else touched
    without_text = inventory.extract_all(root, Path(args.extrakte), targets)
    if not changes.is_empty or not manifest_path.exists():
        inventory.write_manifest(manifest_path, current)
    if without_text:
        print("Ohne Textebene (als Bild sichten):")
        for rel in without_text:
            print(f"  - {rel}")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    return run_check(Path(args.paket), strict=args.streng)


def build_parser() -> argparse.ArgumentParser:
    """Baut den Parser mit allen Unterbefehlen."""
    parser = argparse.ArgumentParser(prog="ap-tools", description="Werkzeuge der Content-Pipeline.")
    sub = parser.add_subparsers(dest="befehl", required=True)

    inv = sub.add_parser(
        "inventur",
        help="Dateien in quellen/ erfassen und mit dem Manifest vergleichen.",
        description=(
            "Listet alle Dateien in quellen/ mit Prüfsumme, erkennt neue, geänderte, "
            "umbenannte und gelöschte Dateien und legt Rohtext in build/extrakte/ ab. "
            "Bewertet und committet nichts."
        ),
    )
    inv.add_argument("--check", action="store_true", help="Nur anzeigen, nichts schreiben.")
    inv.add_argument("--alle", action="store_true", help="Rohtext für alle Dateien neu erzeugen.")
    inv.add_argument("--quellen", default=str(REPO_ROOT / "quellen"), help="Materialordner.")
    inv.add_argument(
        "--manifest", default=str(REPO_ROOT / "docs" / "inventur-manifest.json"), help="Manifest-Datei."
    )
    inv.add_argument(
        "--extrakte", default=str(REPO_ROOT / "build" / "extrakte"), help="Zielordner für Rohtext."
    )
    inv.add_argument("--report", help="Bericht zusätzlich als Markdown-Datei schreiben.")
    inv.add_argument("--github-output", help="Ergebnis für GitHub Actions ($GITHUB_OUTPUT).")
    inv.set_defaults(func=_cmd_inventur)

    chk = sub.add_parser(
        "check",
        help="Inhaltspaket gegen Schema und Verweise prüfen.",
        description="Prüft paket.yaml, katalog.yaml, alle Lektionen und Glossarbegriffe (NF-08).",
    )
    chk.add_argument("--paket", default=str(REPO_ROOT / "content" / "ap1"), help="Ordner des Inhaltspakets.")
    chk.add_argument("--streng", action="store_true", help="Stilwarnungen (zu viel Text) als Fehler werten.")
    chk.set_defaults(func=_cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Einstiegspunkt für ``ap-tools``."""
    args = build_parser().parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
