"""Einstieg des Programms: ``uv run ap-trainer`` startet den Lernbegleiter im Browser.

Mit ``--lan`` ist er auch vom Smartphone im selben WLAN erreichbar (NF-01).
"""

from __future__ import annotations

import argparse
import socket
import sys

from ap_trainer import __version__
from ap_trainer.config import load_config
from ap_trainer.content.loader import ContentLoadError, load_package_or_raise
from ap_trainer.tasks.validate import check_tasks


def _lan_address() -> str:
    """Eigene IP-Adresse im lokalen Netz (ohne dass Daten gesendet werden)."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
        try:
            probe.connect(("192.0.2.1", 9))  # Dokumentationsadresse, nur zur Routenwahl
            address: str = probe.getsockname()[0]
            return address
        except OSError:
            return "127.0.0.1"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Kommandozeilenoptionen."""
    parser = argparse.ArgumentParser(prog="ap-trainer", description="AP1-Lernbegleiter im Browser starten.")
    parser.add_argument("--port", type=int, default=8080, help="Port (Vorgabe: 8080)")
    parser.add_argument(
        "--lan", action="store_true", help="auch im WLAN erreichbar machen (für das Smartphone)"
    )
    parser.add_argument("--kein-browser", action="store_true", help="Browser nicht automatisch öffnen")
    parser.add_argument("--version", action="version", version=f"ap-trainer {__version__}")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Lädt Inhalte und Lernstand und startet die Oberfläche."""
    args = parse_args(argv)
    config = load_config()
    try:
        package = load_package_or_raise(config.content_dir)
        task_errors = check_tasks(package)
        if task_errors:
            raise ContentLoadError(task_errors)
    except ContentLoadError as exc:
        print("Die Inhalte enthalten Fehler und können nicht geladen werden:", file=sys.stderr)
        for error in exc.errors:
            print(f"  {error}", file=sys.stderr)
        return 2

    from nicegui import app, ui

    from ap_trainer.service import Trainer
    from ap_trainer.storage.db import Store
    from ap_trainer.ui.app import build

    store = Store(config.data_file)
    app.on_shutdown(store.close)
    build(Trainer(package, store))
    host = "0.0.0.0" if args.lan else "127.0.0.1"
    if args.lan:
        print(f"Im WLAN erreichbar unter http://{_lan_address()}:{args.port}")
    print(f"Lernstand: {config.data_file}")
    ui.run(
        host=host,
        port=args.port,
        title="AP1-Lernbegleiter",
        favicon="📘",
        reload=False,
        show=not args.kein_browser,
        language="de",
    )
    return 0


if __name__ in {"__main__", "__mp_main__"}:
    raise SystemExit(main())
