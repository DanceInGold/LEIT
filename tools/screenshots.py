"""Bildschirmfotos aller wichtigen Seiten mit einem befüllten Beispiel-Lernstand (Design-Prüfung).

Startet den Lernbegleiter mit einem frischen Lernstand in einem Temp-Ordner, befüllt ihn
(Einstellungen, gelesene Kapitel, Versuche, Lernzeit, eine Simulation) und fotografiert die Seiten
mit Playwright: dunkel und hell am Desktop, dazu einige Seiten in Smartphone-Breite. Läuft in der CI
(Workflow „Screenshots“); lokal braucht es NiceGUI und ``playwright`` mit Chromium.
"""

from __future__ import annotations

import datetime as dt
import os
import random
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT = REPO_ROOT / "content" / "ap1"

# (Dateiname, Pfad) – je Bereich der Navigation mindestens eine Seite
PAGES = [
    ("01-heute", "/"),
    ("02-plan", "/plan"),
    ("03-themen", "/themen"),
    ("04-thema", "/thema/hardware-komponenten"),
    ("05-lektion", "/lektion/hardware-pc-aufbau"),
    ("06-glossar", "/glossar"),
    ("07-ueben", "/ueben"),
    ("08-aufgabe-rechnung", "/ueben/ipv4-subnetting?aufgabe=gen:ipv4-subnetting:4:7"),
    ("09-aufgabe-zuordnung", "/ueben/zahlensysteme?aufgabe=zahlen-praefixe-zuordnen"),
    ("10-lernkarten", "/lernkarten"),
    ("11-simulation", "/simulation"),
    ("12-simulation-pruefung", "/simulation/sim-02"),
    ("13-simulation-ergebnis", "/simulation/ergebnis/1"),
    ("14-operatoren", "/operatoren"),
    ("15-fortschritt", "/fortschritt"),
    ("16-fehler", "/fehler"),
    ("17-einstellungen", "/einstellungen"),
]
LIGHT_PAGES = {"01-heute", "05-lektion", "08-aufgabe-rechnung", "15-fortschritt"}
MOBILE_PAGES = {"01-heute", "05-lektion", "08-aufgabe-rechnung", "12-simulation-pruefung"}
DESKTOP = (1440, 900)
MOBILE = (390, 844)


def seed(data_file: Path) -> None:
    """Befüllt einen Lernstand, der nach vier Wochen Lernen aussieht."""
    from ap_trainer.content.aufgaben import Freitext
    from ap_trainer.content.loader import load_package_or_raise
    from ap_trainer.core.models import BudgetPeriod, PlanSettings
    from ap_trainer.service import Trainer
    from ap_trainer.storage.db import Store
    from ap_trainer.tasks.check import blank_answer
    from ap_trainer.tasks.validate import model_answer

    store = Store(data_file)
    trainer = Trainer(load_package_or_raise(CONTENT), store)
    today = dt.date.today()
    start = today - dt.timedelta(days=28)
    exam = max(dt.date(2027, 2, 24), today + dt.timedelta(days=60))
    trainer.save_settings(
        PlanSettings(
            pruefungsdatum=exam, lernbeginn=start, budget=[BudgetPeriod(ab=start, stunden_pro_woche=15)]
        )
    )
    rng = random.Random(7)
    for lesson_id in ("hardware-pc-aufbau", "zahlensysteme-umrechnen", "projekt-merkmale"):
        if lesson_id in trainer.package.lektionen:
            trainer.mark_lesson_read(trainer.package.lektionen[lesson_id], 30)
    for days_ago in range(14):
        if rng.random() < 0.7:
            store.log_study(rng.randint(25, 80), "lektion", "seed", today - dt.timedelta(days=days_ago))
    for topic_id in ("hardware-komponenten", "zahlensysteme", "projektplanung", "schutzziele"):
        for task in trainer.package.tasks_for_topic(topic_id)[:4]:
            if isinstance(task, Freitext):
                continue
            answer = model_answer(task) if rng.random() < 0.7 else blank_answer(task)
            now = dt.datetime.now(dt.UTC) - dt.timedelta(days=rng.randint(0, 10))
            trainer.submit(task, answer, seconds=90, now=now)
    sim = trainer.package.simulationen["sim-01"]
    answers = {
        t.id: model_answer(t) for t in sim.tasks() if not isinstance(t, Freitext) and rng.random() < 0.8
    }
    started = dt.datetime.now(dt.UTC) - dt.timedelta(days=2, minutes=85)
    trainer.submit_simulation("sim-01", answers, started, started + dt.timedelta(minutes=84))
    store.close()


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port: int = probe.getsockname()[1]
        return port


def _wait(base: str, process: subprocess.Popen[bytes]) -> None:
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Der Lernbegleiter hat sich beim Start beendet")
        try:
            urllib.request.urlopen(base + "/glossar", timeout=2)
            return
        except (urllib.error.URLError, ConnectionError):
            time.sleep(0.3)
    raise RuntimeError("Der Lernbegleiter ist nicht rechtzeitig gestartet")


def _set_light(data_file: Path, light: bool) -> None:
    from ap_trainer.storage.db import Store
    from ap_trainer.ui.app import LIGHT_KEY

    store = Store(data_file)
    store.set_setting(LIGHT_KEY, light)
    store.close()


def _shoot(base: str, out: Path, data_file: Path) -> list[Path]:
    from playwright.sync_api import sync_playwright

    files: list[Path] = []
    runs = [
        ("dunkel", DESKTOP, False, None),
        ("hell", DESKTOP, True, LIGHT_PAGES),
        ("handy", MOBILE, False, MOBILE_PAGES),
    ]
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for suffix, viewport, light, only in runs:
            _set_light(data_file, light)
            page = browser.new_page(
                viewport={"width": viewport[0], "height": viewport[1]},
                device_scale_factor=2 if suffix == "handy" else 1,
            )
            for name, path in PAGES:
                if only is not None and name not in only:
                    continue
                page.goto(base + path, wait_until="networkidle")
                page.wait_for_timeout(1200)  # Diagramme und Schrift fertig zeichnen lassen
                target = out / f"{name}-{suffix}.png"
                page.screenshot(path=str(target), full_page=True)
                files.append(target)
            page.close()
        browser.close()
    return files


def run_screenshots(out: Path, port: int | None = None) -> int:
    """Startet den Lernbegleiter mit Beispiel-Lernstand und fotografiert die Seiten nach ``out``."""
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("Playwright fehlt: uv run --with playwright ap-tools screenshots", file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "lernstand.sqlite"
        seed(data_file)
        port = port or _free_port()
        env = {**os.environ, "AP_TRAINER_CONTENT": str(CONTENT), "AP_TRAINER_DATA": str(data_file)}
        process = subprocess.Popen(
            [sys.executable, "-m", "ap_trainer", "--kein-browser", "--port", str(port)],
            cwd=tmp,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        base = f"http://127.0.0.1:{port}"
        try:
            _wait(base, process)
            files = _shoot(base, out, data_file)
        finally:
            process.terminate()
            output, _ = process.communicate(timeout=20)
            if process.returncode not in (0, -15):
                print(output.decode(errors="replace"), file=sys.stderr)
    print(f"{len(files)} Bildschirmfotos in {out}")
    return 0
