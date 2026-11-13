"""Generator „zahlensysteme“ gegen Pythons ``int()`` und ``format()`` als unabhängige Referenz (NF-07)."""

from __future__ import annotations

import random
import re

from ap_trainer.content.aufgaben import Rechnung
from ap_trainer.tasks.answers import parse_dual, parse_hex
from ap_trainer.tasks.generators import make
from ap_trainer.tasks.generators.number_systems import dual_value, group, hex_value, to_dual, to_hex
from tests.tasks.random_cases import random_cases

_SOURCE = re.compile(r"(?:`([0-9A-F ]+)`|\*\*(\d+)\*\*)")


@random_cases()
def test_conversion_helpers_match_python(seed: int) -> None:
    value = random.Random(seed).randint(0, 2**20)
    assert to_dual(value) == format(value, "b")
    assert to_hex(value) == format(value, "X")
    assert dual_value(format(value, "b")) == value
    assert hex_value(format(value, "x")) == value
    assert group(format(value, "b")).replace(" ", "").lstrip("0") == format(value, "b").lstrip("0")


def _source_value(task: Rechnung) -> int:
    """Liest die Ausgangszahl aus der Aufgabenstellung und rechnet sie mit Python um."""
    match = _SOURCE.search(task.frage)
    assert match, task.frage
    if match.group(2):
        return int(match.group(2))
    text = match.group(1).replace(" ", "")
    is_dual = set(text) <= {"0", "1"} and ("Dualzahl `" in task.frage)
    return int(text, 2) if is_dual else int(text, 16)


@random_cases()
def test_every_step_matches_reference(seed: int) -> None:
    for level in (1, 2, 3, 4):
        task = make("zahlensysteme", level, seed, "zahlensysteme")
        assert isinstance(task, Rechnung)
        value = _source_value(task)
        for step in task.schritte:
            if step.format == "dual":
                assert parse_dual(step.antwort) == value
                width = int(re.search(r"\((\d+) Bit\)", step.frage).group(1))  # type: ignore[union-attr]
                assert len(step.antwort.replace(" ", "")) == width
            elif step.format == "hex":
                assert parse_hex(step.antwort) == value
            else:
                assert int(step.antwort) == value


def test_known_example_from_lesson() -> None:
    # 183 = 1011 0111 = B7 (Beispiel in der Lektion zahlensysteme-umrechnen)
    assert to_dual(183, 8) == "10110111"
    assert to_hex(183) == "B7"
    assert group("10110111") == "1011 0111"
