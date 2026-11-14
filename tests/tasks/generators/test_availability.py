"""Generator „verfuegbarkeit“ gegen eine unabhängige Nachrechnung mit ``Decimal`` (NF-07).

Die Werte werden aus dem Aufgabentext gelesen und mit den Formeln der Lektion neu berechnet:
Ausfallzeit = (1 − V) × 8.760 h, Reihe = Produkt, parallel = 1 − Produkt der Ausfallanteile.
"""

from __future__ import annotations

import re
from decimal import Decimal, getcontext

from ap_trainer.content.aufgaben import Rechenschritt, Rechnung
from ap_trainer.tasks.answers import same_answer
from ap_trainer.tasks.generators import make
from tests.tasks.random_cases import random_cases

getcontext().prec = 50
YEAR = Decimal(8760)
PERCENT = r"\*\*([\d,]+) %\*\*"


def _close(step: Rechenschritt, value: Decimal) -> None:
    """Die Musterlösung muss mit dem nachgerechneten Wert (innerhalb der Toleranz) übereinstimmen."""
    assert same_answer("zahl", step.antwort, format(value.normalize(), "f"), step.toleranz), (
        step.frage,
        step.antwort,
        value,
    )


def _percents(text: str) -> list[Decimal]:
    """Alle fett gedruckten Prozentwerte als Dezimalzahl (99,5 % → 0,995)."""
    return [Decimal(v.replace(",", ".")) / 100 for v in re.findall(PERCENT, text)]


def _steps(task: Rechnung) -> dict[str, Rechenschritt]:
    return {step.frage: step for step in task.schritte}


def _check_downtime(steps: dict[str, Rechenschritt], availability: Decimal) -> None:
    hours = (1 - availability) * YEAR
    _close(steps["Ausfallzeit pro Jahr in Stunden"], hours)
    if "Ausfallzeit pro Jahr in Minuten" in steps:
        assert hours < 10
        _close(steps["Ausfallzeit pro Jahr in Minuten"], hours * 60)


@random_cases()
def test_downtime(seed: int) -> None:
    task = make("verfuegbarkeit", 1, seed, "x")
    assert isinstance(task, Rechnung)
    (availability,) = _percents(task.frage)
    steps = _steps(task)
    _close(steps["Ausfallanteil in %"], (1 - availability) * 100)
    _check_downtime(steps, availability)


@random_cases()
def test_series(seed: int) -> None:
    task = make("verfuegbarkeit", 2, seed, "x")
    assert isinstance(task, Rechnung)
    values = _percents(task.frage)
    assert len(values) in (2, 3)
    total = Decimal(1)
    for value in values:
        total *= value
    steps = _steps(task)
    _close(steps["Gesamtverfügbarkeit in %"], total * 100)
    _check_downtime(steps, total)


@random_cases()
def test_parallel(seed: int) -> None:
    task = make("verfuegbarkeit", 3, seed, "x")
    assert isinstance(task, Rechnung)
    count = int(re.search(r"\*\*(\d) Server\*\*", task.frage).group(1))  # type: ignore[union-attr]
    (value,) = _percents(task.frage)
    all_fail = (1 - value) ** count
    steps = _steps(task)
    _close(steps["Ausfallwahrscheinlichkeit eines Servers in %"], (1 - value) * 100)
    _close(steps[f"Wahrscheinlichkeit, dass alle {count} gleichzeitig ausfallen (Dezimalzahl)"], all_fail)
    _close(steps["Gesamtverfügbarkeit in %"], (1 - all_fail) * 100)
    # Auf vier Nachkommastellen muss sich das Ergebnis noch von 100 % unterscheiden
    assert steps["Gesamtverfügbarkeit in %"].antwort != "100"
    _check_downtime(steps, 1 - all_fail)


@random_cases()
def test_sla(seed: int) -> None:
    task = make("verfuegbarkeit", 4, seed, "x")
    assert isinstance(task, Rechnung) and task.situation
    server, switch, target = _percents(task.situation)
    pair = 1 - (1 - server) ** 2
    total = pair * switch
    steps = _steps(task)
    _close(steps["Verfügbarkeit des Serverpaars in %"], pair * 100)
    _close(steps["Gesamtverfügbarkeit mit Switch in %"], total * 100)
    _check_downtime(steps, total)
    verdict = next(s for s in task.schritte if s.frage.startswith("Wird die Zusage"))
    assert verdict.antwort == ("ja" if total >= target else "nein")


def test_examples_from_lesson() -> None:
    """Zahlen der Lektion „Verfügbarkeit sichern“ mit den Funktionen des Generators."""
    from fractions import Fraction

    from ap_trainer.tasks.generators.availability import downtime_hours, parallel, series

    assert downtime_hours(Fraction(99, 100)) == Fraction("87.6")
    assert downtime_hours(Fraction(999, 1000)) == Fraction("8.76")
    assert downtime_hours(Fraction(9999, 10000)) * 60 == Fraction("52.56")
    assert series([Fraction(99, 100), Fraction(995, 1000)]) == Fraction("0.98505")
    assert parallel([Fraction(99, 100), Fraction(99, 100)]) == Fraction("0.9999")
