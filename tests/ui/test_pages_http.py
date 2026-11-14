"""Ende-zu-Ende-Rauchtest: Programm starten und jede Seite einmal per HTTP abrufen.

Läuft nur mit installiertem NiceGUI (CI). Ein Fehler beim Aufbau einer Seite liefert bei
NiceGUI den Statuscode 500 – so fallen Laufzeitfehler auf, die reine Unit-Tests nicht sehen.
Der Lernstand wird vorher befüllt, damit auch Diagramme mit echten Daten gezeichnet werden.
"""

from __future__ import annotations

import datetime as dt
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from pathlib import Path

import pytest

REPO_CONTENT = Path(__file__).resolve().parents[2] / "content" / "ap1"
PAGES = [
    "/",
    "/themen",
    "/thema/hardware-komponenten",
    "/thema/ipv4-subnetting",  # Thema ohne Kapitel
    "/lektion/hardware-pc-aufbau",
    "/lernkarten",
    "/ueben",
    "/ueben/zahlensysteme",
    "/ueben/ipv4-subnetting",
    # Jede feste Aufgabe einmal öffnen, damit jeder Aufgabentyp gezeichnet wird
    "/ueben/zahlensysteme?aufgabe=zahlen-hexziffer-bits",
    "/ueben/zahlensysteme?aufgabe=zahlen-praefixe-zuordnen",
    "/ueben/zahlensysteme?aufgabe=zahlen-nibble-byte-luecke",
    "/ueben/zahlensysteme?aufgabe=zahlen-groessen-ordnen",
    "/ueben/zahlensysteme?aufgabe=zahlen-warum-hex",
    "/ueben/ipv4-subnetting?aufgabe=gen:ipv4-subnetting:4:7",
    "/ueben/ipv6?aufgabe=gen:ipv6:3:5",
    "/ueben/ipv6?aufgabe=gen:ipv6:4:3",
    "/ueben/datenmengen-uebertragung?aufgabe=gen:datenmengen:4:1",
    "/ueben/nachhaltigkeit-energie?aufgabe=gen:stromkosten:4:2",
    "/ueben/wirtschaftlichkeit?aufgabe=gen:kostenvergleich:4:5",
    "/ueben/projektplanung?aufgabe=plan-netzplan-rechnen",
    "/ueben/hardware-komponenten?aufgabe=hw-bestellung-pruefen",
    "/ueben/osi-protokolle?aufgabe=osi-ports-zuordnen",
    "/ueben/verschluesselung?aufgabe=krypto-schluesselanzahl",
    "/ueben/englische-texte?aufgabe=englisch-mail-zusammenfassen",
    "/ueben/oop-grundlagen?aufgabe=oop-objekte-verfolgen",
    "/ueben/unbekannt",
    "/glossar",
    "/plan",
    "/einstellungen",
]


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port: int = probe.getsockname()[1]
        return port


def _seed(data_file: Path) -> None:
    """Befüllt den Lernstand: ein gelesenes Kapitel, Lernzeit an zwei Tagen."""
    from ap_trainer.content.loader import load_package_or_raise
    from ap_trainer.service import Trainer
    from ap_trainer.storage.db import Store

    store = Store(data_file)
    trainer = Trainer(load_package_or_raise(REPO_CONTENT), store)
    trainer.mark_lesson_read(trainer.package.lektionen["hardware-pc-aufbau"], 35)
    store.log_study(20, "wiederholung", "test", dt.date.today() - dt.timedelta(days=1))
    # Ein falsch gelöster Versuch, damit die Übungsübersicht Zahlen zeigt
    task = trainer.find_task("gen:zahlensysteme:2:1", "zahlensysteme")
    assert task is not None
    trainer.submit(task, ["0"], seconds=30)
    store.close()


@pytest.fixture(scope="module")
def server(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    pytest.importorskip("nicegui")
    workdir = tmp_path_factory.mktemp("app")
    data_file = workdir / "lernstand.sqlite"
    _seed(data_file)
    port = _free_port()
    env = {**os.environ, "AP_TRAINER_CONTENT": str(REPO_CONTENT), "AP_TRAINER_DATA": str(data_file)}
    process = subprocess.Popen(
        [sys.executable, "-m", "ap_trainer", "--kein-browser", "--port", str(port)],
        cwd=workdir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    base = f"http://127.0.0.1:{port}"
    try:
        _wait_until_up(base, process)
        yield base
    finally:
        process.terminate()
        output, _ = process.communicate(timeout=20)
        print(output.decode(errors="replace"))


def _wait_until_up(base: str, process: subprocess.Popen[bytes]) -> None:
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if process.poll() is not None:
            pytest.fail("Programm hat sich beim Start beendet")
        try:
            urllib.request.urlopen(base + "/glossar", timeout=2)
            return
        except (urllib.error.URLError, ConnectionError):
            time.sleep(0.3)
    pytest.fail("Programm ist nicht rechtzeitig gestartet")


@pytest.mark.parametrize("path", PAGES)
def test_page_renders_without_error(server: str, path: str) -> None:
    try:
        with urllib.request.urlopen(server + path, timeout=15) as response:
            assert response.status == 200
            html = response.read().decode()
    except urllib.error.HTTPError as exc:  # pragma: no cover - nur im Fehlerfall
        pytest.fail(f"{path} liefert {exc.code}")
    assert "Traceback" not in html
