"""Generator „datenmengen“ gegen eine unabhängige Nachrechnung mit ``Decimal`` (NF-07).

Die Parameter werden aus dem Aufgabentext gelesen und mit den Formeln der Lektionen neu
gerechnet; verglichen wird mit der Toleranz, die die Aufgabe selbst angibt.
"""

from __future__ import annotations

import math
import re
from decimal import ROUND_HALF_UP, Decimal, getcontext

from ap_trainer.content.aufgaben import Rechenschritt, Rechnung
from ap_trainer.tasks.answers import same_answer
from ap_trainer.tasks.generators import make
from tests.tasks.random_cases import random_cases

getcontext().prec = 50
MB, GB = Decimal(10**6), Decimal(10**9)


def _close(step: Rechenschritt, value: Decimal) -> None:
    """Die Musterlösung muss dem exakten Wert entsprechen – exakt oder innerhalb ihrer Toleranz."""
    exact = format(value.normalize(), "f")
    assert same_answer("zahl", step.antwort, exact, step.toleranz), (step.frage, step.antwort, value)


def _num(text: str) -> Decimal:
    return Decimal(text.replace(".", "").replace(",", "."))


def _rate(text: str) -> Decimal:
    value, unit = re.search(r"\*\*([\d.,]+) (Mbit/s|Gbit/s)\*\*", text).groups()  # type: ignore[union-attr]
    return _num(value) * (MB if unit == "Mbit/s" else GB)


def _steps(task: Rechnung) -> dict[str, Rechenschritt]:
    return {step.frage: step for step in task.schritte}


@random_cases()
def test_image_and_transfer_levels(seed: int) -> None:
    image = make("datenmengen", 1, seed, "x")
    assert isinstance(image, Rechnung)
    width, height, depth = map(
        int, re.search(r"(\d+) × (\d+) Pixeln\*\* und \*\*(\d+) Bit", image.frage).groups()
    )  # type: ignore[union-attr]
    _close(_steps(image)["Datenmenge in MB"], Decimal(width * height * depth) / 8 / MB)

    transfer = make("datenmengen", 2, seed, "x")
    assert isinstance(transfer, Rechnung)
    amount = Decimal(re.search(r"\*\*(\d+) GB\*\*", transfer.frage).group(1)) * GB  # type: ignore[union-attr]
    seconds = amount * 8 / _rate(transfer.frage)
    steps = _steps(transfer)
    _close(steps["Übertragungszeit in Sekunden"], seconds)
    if "Übertragungszeit in Minuten" in steps:
        _close(steps["Übertragungszeit in Minuten"], seconds / 60)


def _check_scan(task: Rechnung) -> None:
    width_mm, height_mm, dpi = map(
        int, re.search(r"\((\d+) × (\d+) mm\) mit \*\*(\d+) dpi", task.frage).groups()
    )  # type: ignore[union-attr]
    pixels = [
        (Decimal(mm) / Decimal("25.4") * dpi).quantize(Decimal(1), rounding=ROUND_HALF_UP)
        for mm in (width_mm, height_mm)
    ]
    steps = _steps(task)
    assert Decimal(steps["Breite in Pixel"].antwort) == pixels[0]
    assert Decimal(steps["Höhe in Pixel"].antwort) == pixels[1]
    _close(steps["Datenmenge in MB"], pixels[0] * pixels[1] * 3 / MB)


def _check_audio(task: Rechnung) -> None:
    minutes, rate, depth = re.search(
        r"\*\*(\d+) Minuten\*\* mit \*\*([\d.]+) Hz\*\*, \*\*(\d+) Bit", task.frage
    ).groups()  # type: ignore[union-attr]
    channels = 2 if "Stereo" in task.frage else 1
    size = _num(rate) * int(depth) * channels * int(minutes) * 60 / 8
    _close(_steps(task)["Datenmenge in MB"], size / MB)


def _check_video(task: Rechnung) -> None:
    match = re.search(
        r"(\d+) × (\d+)\*\* Pixeln.*\*\*(\d+) Bildern pro Sekunde\*\* und \*\*(\d+) Sekunden", task.frage
    )
    width, height, fps, seconds = map(int, match.groups())  # type: ignore[union-attr]
    _close(_steps(task)["Datenmenge in GB"], Decimal(width * height * 3 * fps * seconds) / GB)


@random_cases()
def test_media_level(seed: int) -> None:
    task = make("datenmengen", 3, seed, "x")
    assert isinstance(task, Rechnung)
    {"Scan berechnen": _check_scan, "Audio berechnen": _check_audio, "Video berechnen": _check_video}[
        task.titel
    ](task)


@random_cases()
def test_situation_level(seed: int) -> None:
    task = make("datenmengen", 4, seed, "x")
    assert isinstance(task, Rechnung) and task.situation
    steps = _steps(task)
    text = task.situation
    if task.titel == "Nachtsicherung planen":
        tb, hours = map(int, re.search(r"\*\*(\d+) TB\*\*.*\*\*(\d+) Stunden\*\*", text).groups())  # type: ignore[union-attr]
        needed = Decimal(tb) * 10**12 * 8 / (hours * 3600) / GB
        _close(steps["Benötigte Datenrate in Gbit/s"], needed)
        line = min(s for s in (1, 10, 25, 40, 100) if s >= needed)
        assert int(steps["Kleinste ausreichende Leitung in Gbit/s"].antwort) == line
    elif task.titel == "Übertragung mit Overhead":
        amount = Decimal(re.search(r"\*\*(\d+) GB\*\*", text).group(1)) * GB  # type: ignore[union-attr]
        share = Decimal(re.search(r"\*\*(\d+) %\*\*", text).group(1)) / 100  # type: ignore[union-attr]
        seconds = amount * 8 / (_rate(text) * share)
        _close(steps["Übertragungszeit in Sekunden"], seconds)
        _close(steps["Übertragungszeit in Minuten"], seconds / 60)
    else:
        width, height = map(int, re.search(r"\*\*(\d+) × (\d+) Pixeln\*\*", text).groups())  # type: ignore[union-attr]
        minutes = int(re.search(r"\*\*(\d+) Minuten?\*\*", task.frage).group(1))  # type: ignore[union-attr]
        transferable = _rate(text) * minutes * 60 / 8
        assert int(steps["Vollständig übertragene Fotos"].antwort) == math.floor(
            transferable / (width * height * 3)
        )


def test_examples_from_lessons() -> None:
    # Lektion datenmengen-berechnen: 4000 × 3000 × 24 Bit = 36 MB; A4 mit 300 dpi = 2480 × 3508 Pixel
    assert Decimal(4000 * 3000 * 3) / MB == 36
    assert (Decimal(210) / Decimal("25.4") * 300).quantize(Decimal(1), rounding=ROUND_HALF_UP) == 2480
    # Lektion uebertragungszeit: 50 GB über 1 Gbit/s = 400 s
    assert 50 * GB * 8 / GB == 400
