"""Generator „kostenvergleich“ gegen eine unabhängige Nachrechnung mit ``Decimal`` (NF-07)."""

from __future__ import annotations

import re
from decimal import Decimal, getcontext

from ap_trainer.content.aufgaben import Rechenschritt, Rechnung
from ap_trainer.tasks.answers import same_answer
from ap_trainer.tasks.generators import make
from tests.tasks.random_cases import random_cases

getcontext().prec = 50


def _close(step: Rechenschritt, value: Decimal) -> None:
    assert same_answer("zahl", step.antwort, format(value.normalize(), "f"), step.toleranz), (
        step.frage,
        step.antwort,
        value,
    )


def _amounts(text: str) -> list[Decimal]:
    """Alle fett gedruckten Zahlen eines Textes in Reihenfolge."""
    return [Decimal(x.replace(".", "").replace(",", ".")) for x in re.findall(r"\*\*(\d[\d.,]*)", text)]


def _steps(task: Rechnung) -> dict[str, Rechenschritt]:
    return {step.frage: step for step in task.schritte}


@random_cases()
def test_amortisation_levels(seed: int) -> None:
    simple = make("kostenvergleich", 1, seed, "x")
    assert isinstance(simple, Rechnung)
    investment, reflux = _amounts(simple.frage)
    _close(simple.schritte[0], investment / reflux)

    detailed = make("kostenvergleich", 2, seed, "x")
    assert isinstance(detailed, Rechnung) and detailed.situation
    investment, hours, rate, running = _amounts(detailed.situation)
    reflux = hours * rate - running
    assert reflux > 0
    steps = _steps(detailed)
    _close(steps["Rückfluss in € pro Monat"], reflux)
    _close(steps["Amortisationsdauer in Monaten"], investment / reflux)


@random_cases()
def test_break_even(seed: int) -> None:
    task = make("kostenvergleich", 3, seed, "x")
    assert isinstance(task, Rechnung)
    fix, var_a, var_b, need = _amounts(task.frage)
    point = fix / (var_b - var_a)
    # Probe: am Break-even sind beide Lösungen gleich teuer
    assert fix + var_a * point == var_b * point
    _close(task.schritte[0], point)
    _close(task.schritte[1], fix + var_a * need)
    _close(task.schritte[2], var_b * need)


@random_cases()
def test_nas_or_cloud(seed: int) -> None:
    task = make("kostenvergleich", 4, seed, "x")
    assert isinstance(task, Rechnung) and task.situation
    purchase, years, maintenance, var_a, var_b, need = _amounts(task.situation)
    fix = purchase / years + maintenance
    steps = _steps(task)
    _close(steps["Fixe Kosten des NAS pro Jahr in €"], fix)
    _close(steps["Break-even in TB"], fix / (var_b - var_a))
    nas, cloud = fix + var_a * need, var_b * need
    _close(steps["Ersparnis der günstigeren Lösung pro Jahr in €"], abs(nas - cloud))
    assert purchase > 0


def test_examples_from_lesson() -> None:
    # Lektion wirtschaftlichkeit: 24.000 € ÷ 1.000 €/Monat = 24 Monate; NAS/Cloud-Break-even 40 TB
    assert Decimal(24000) / (20 * 60 - 200) == 24
    assert Decimal(2000) / (60 - 10) == 40
