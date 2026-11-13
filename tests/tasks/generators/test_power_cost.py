"""Generator „stromkosten“ gegen eine unabhängige Nachrechnung mit ``Decimal`` (NF-07)."""

from __future__ import annotations

import re
from decimal import Decimal, getcontext

from ap_trainer.content.aufgaben import Rechenschritt, Rechnung
from ap_trainer.tasks.answers import same_answer
from ap_trainer.tasks.generators import make
from tests.tasks.random_cases import random_cases

getcontext().prec = 50
YEAR = Decimal(8760)


def _close(step: Rechenschritt, value: Decimal) -> None:
    assert same_answer("zahl", step.antwort, format(value.normalize(), "f"), step.toleranz), (
        step.frage,
        step.antwort,
        value,
    )


def _num(text: str) -> Decimal:
    return Decimal(text.replace(".", "").replace(",", "."))


def _find(pattern: str, text: str) -> Decimal:
    return _num(re.search(pattern, text).group(1))  # type: ignore[union-attr]


def _steps(task: Rechnung) -> dict[str, Rechenschritt]:
    return {step.frage: step for step in task.schritte}


@random_cases()
def test_energy_and_yearly_cost(seed: int) -> None:
    energy = make("stromkosten", 1, seed, "x")
    assert isinstance(energy, Rechnung)
    watts, hours = _find(r"\*\*(\d+) W\*\*", energy.frage), _find(r"\*\*(\d+) Stunden\*\*", energy.frage)
    _close(_steps(energy)["Energie in kWh"], watts / 1000 * hours)

    yearly = make("stromkosten", 2, seed, "x")
    assert isinstance(yearly, Rechnung)
    watts = _find(r"\*\*(\d+) W\*\*", yearly.frage)
    price = _find(r"\*\*([\d,]+) €/kWh\*\*", yearly.frage)
    _close(_steps(yearly)["Stromkosten pro Jahr in Euro"], watts / 1000 * YEAR * price)


@random_cases()
def test_thin_client_comparison(seed: int) -> None:
    task = make("stromkosten", 3, seed, "x")
    assert isinstance(task, Rechnung) and task.situation
    text = task.situation
    seats = _find(r"\*\*(\d+) Arbeitsplatz-PCs\*\* \((\d+) W\)", text)
    old_w = _find(r"PCs\*\* \((\d+) W\)", text)
    new_w = _find(r"Clients\*\* \((\d+) W\)", text)
    days, per_day = (Decimal(x) for x in re.search(r"\*\*(\d+) Tagen je (\d+) Stunden\*\*", text).groups())  # type: ignore[union-attr]
    price = _find(r"\*\*([\d,]+) €/kWh\*\*", text)
    hours = days * per_day
    steps = _steps(task)
    _close(steps["Kosten je PC in Euro"], old_w / 1000 * hours * price)
    _close(
        steps["Ersparnis pro Jahr für alle Plätze in Euro"], (old_w - new_w) / 1000 * hours * price * seats
    )


@random_cases()
def test_efficiency_situations(seed: int) -> None:
    task = make("stromkosten", 4, seed, "x")
    assert isinstance(task, Rechnung) and task.situation
    text = task.situation
    price = _find(r"\*\*([\d,]+) €/kWh\*\*", text)
    steps = _steps(task)
    if task.titel == "Netzteil und Stromkosten":
        output = _find(r"\*\*(\d+) W\*\*", text)
        eta = _find(r"\*\*(\d+) %\*\*", text) / 100
        hours = YEAR if "rund um die Uhr" in text else Decimal(220 * 8)
        intake = output / eta
        _close(steps["Aufgenommene Leistung in W"], intake)
        _close(steps["Stromkosten pro Jahr in Euro"], intake / 1000 * hours * price)
    else:
        it_kw = _find(r"\*\*(\d+) kW\*\*", text)
        pue = _find(r"PUE von ([\d,]+)\*\*", text)
        _close(steps["Gesamtleistung des Rechenzentrums in kW"], it_kw * pue)
        _close(
            steps["Kosten für Kühlung und Verluste pro Jahr in Euro"], (it_kw * pue - it_kw) * YEAR * price
        )


def test_examples_from_lessons() -> None:
    # Lektion nachhaltigkeit-energie: 400 W rund um die Uhr bei 0,30 €/kWh = 1.051,20 €
    # und PC 80 W, 1.760 h = 42,24 €
    assert Decimal("0.4") * YEAR * Decimal("0.30") == Decimal("1051.200")
    assert Decimal("0.08") * 1760 * Decimal("0.30") == Decimal("42.2400")
    # Lektion Netzteil: 300 W ÷ 0,90 = 333,3 W
    assert round(Decimal(300) / Decimal("0.9"), 1) == Decimal("333.3")
