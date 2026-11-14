"""Tests für das Fehlerprotokoll (FT-04)."""

from __future__ import annotations

import datetime as dt

from ap_trainer.core.mistakes import mistake_log
from ap_trainer.core.models import Attempt

START = dt.datetime(2027, 1, 10, 12, 0, tzinfo=dt.UTC)


def _attempt(task_id: str, richtig: bool, ursache: str | None = None, minute: int = 0) -> Attempt:
    return Attempt(
        aufgabe_id=task_id,
        thema="t",
        stufe=2,
        typ="rechnung",
        richtig=richtig,
        anteil=float(richtig),
        ursache=ursache,
        am=START + dt.timedelta(minutes=minute),
    )


HISTORY = [
    _attempt("a", False, "rechenfehler", 0),
    _attempt("b", False, "begriff", 1),
    _attempt("a", False, "rechenfehler", 2),
    _attempt("c", True, None, 3),
    _attempt("d", False, None, 4),
    _attempt("b", True, None, 5),
    _attempt("e", False, "rechenfehler", 6),
]


def test_groups_by_cause_in_fixed_order() -> None:
    groups = mistake_log(HISTORY)
    assert [g.ursache for g in groups] == ["rechenfehler", "begriff", "unbekannt"]
    assert groups[-1].titel == "Ursache nicht erkannt"


def test_one_entry_per_task_newest_first_with_counts() -> None:
    rechen = mistake_log(HISTORY)[0]
    assert [e.aufgabe_id for e in rechen.eintraege] == ["e", "a"]
    assert rechen.eintraege[1].fehlversuche == 2
    assert rechen.offen == 2


def test_later_correct_answer_marks_mistake_fixed() -> None:
    begriff = mistake_log(HISTORY)[1]
    assert begriff.eintraege[0].behoben and begriff.offen == 0
    open_only = mistake_log(HISTORY, include_fixed=False)
    assert "begriff" not in [g.ursache for g in open_only]


def test_new_mistake_after_fix_is_open_again() -> None:
    log = mistake_log([*HISTORY, _attempt("b", False, "konzept", 7)])
    konzept = next(g for g in log if g.ursache == "konzept")
    assert konzept.eintraege[0].aufgabe_id == "b" and not konzept.eintraege[0].behoben
    assert konzept.eintraege[0].fehlversuche == 2


def test_no_attempts_no_groups() -> None:
    assert mistake_log([]) == []
