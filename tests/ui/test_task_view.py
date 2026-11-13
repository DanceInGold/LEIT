"""Tests für die Aufbereitung einer Aufgabe zur Anzeige."""

from __future__ import annotations

from ap_trainer.content.aufgaben import AUFGABE
from ap_trainer.tasks.check import FreitextAntwort
from ap_trainer.ui.task_view import gap_markdown, initial_order, is_blank, percent, shuffled_indices

TASK = AUFGABE.validate_python(
    {
        "id": "ordnen",
        "typ": "reihenfolge",
        "thema": "t",
        "stufe": 1,
        "titel": "x",
        "frage": "x",
        "elemente": ["a", "b", "c", "d"],
        "loesungsweg": "x",
        "quelle": "x",
        "status": "ungeprüft",
    }
)


def test_shuffle_is_reproducible_and_complete() -> None:
    order = shuffled_indices(TASK, 4)
    assert sorted(order) == [0, 1, 2, 3]
    assert shuffled_indices(TASK, 4) == order


def test_initial_order_is_never_the_solution() -> None:
    for name in ("a", "b", "c", "d", "e", "f", "g"):
        task = TASK.model_copy(update={"id": name})
        assert initial_order(task, 4) != [0, 1, 2, 3]
        assert initial_order(task, 3) != [0, 1, 2]


def test_gap_markdown_and_percent() -> None:
    assert gap_markdown("Ein Byte hat {{1}} Bit und {{2}} Nibbles.") == (
        "Ein Byte hat **[1] …** Bit und **[2] …** Nibbles."
    )
    assert percent(0.666) == "67 %"


def test_blank_answers_are_not_graded() -> None:
    other = AUFGABE.validate_python(
        {
            **TASK.model_dump(exclude={"typ", "elemente"}),
            "typ": "rechnung",
            "schritte": [{"frage": "a", "antwort": "1", "erklaerung": "b"}],
        }
    )
    assert not is_blank(TASK, [])  # Reihenfolge hat immer eine Antwort
    assert is_blank(other, ["", None, "  "])
    assert not is_blank(other, ["", "4"])
    assert is_blank(other, frozenset())
    assert is_blank(other, FreitextAntwort(" ", []))
