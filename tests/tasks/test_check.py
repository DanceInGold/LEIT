"""Tests für die Bewertung je Aufgabentyp (AU-01, AU-04, AU-05, HI-01 bis HI-03)."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from ap_trainer.content.aufgaben import AUFGABE, Freitext, Lueckentext, MultipleChoice
from ap_trainer.tasks.check import FreitextAntwort, evaluate, missing_terms
from ap_trainer.tasks.hints import LOESUNGSWEG_GEOEFFNET, help_level, help_steps

BASE: dict[str, Any] = {
    "thema": "zahlen",
    "stufe": 1,
    "titel": "Test",
    "frage": "Frage?",
    "loesungsweg": "So geht es.",
    "quelle": "Test",
    "status": "ungeprüft",
}


def task(**fields: Any) -> Any:
    return AUFGABE.validate_python({**BASE, **fields})


MC = task(
    id="mc",
    typ="multiple_choice",
    hinweise=["Richtung"],
    optionen=[
        {"text": "4 Bit", "richtig": True},
        {"text": "8 Bit", "warum": "Das ist ein Byte.", "ursache": "begriff"},
        {"text": "2 Bit"},
    ],
)


def test_multiple_choice() -> None:
    assert evaluate(MC, frozenset({0})).richtig
    wrong = evaluate(MC, frozenset({1}))
    assert not wrong.richtig and wrong.anteil == 0
    assert wrong.ursache == "begriff"
    assert any("Das ist ein Byte." in r.text for r in wrong.rueckmeldungen)
    assert not evaluate(MC, frozenset({0, 1})).richtig


def test_multiple_choice_needs_right_and_wrong_option() -> None:
    with pytest.raises(ValidationError):
        task(id="x", typ="multiple_choice", optionen=[{"text": "a"}, {"text": "b"}])
    with pytest.raises(ValidationError):
        task(
            id="x",
            typ="multiple_choice",
            optionen=[{"text": "a", "richtig": True}, {"text": "b", "richtig": True}],
        )


def test_assignment() -> None:
    item = task(
        id="z",
        typ="zuordnung",
        paare=[{"links": "Ki", "rechts": "2^10"}, {"links": "k", "rechts": "10^3"}],
        ablenker=["2^8"],
    )
    assert item.auswahl == ["10^3", "2^10", "2^8"]
    assert evaluate(item, ["2^10", "10^3"]).richtig
    half = evaluate(item, ["2^10", "2^8"])
    assert half.anteil == 0.5 and half.ursache == "begriff"


def test_gap_text_with_known_error() -> None:
    item: Lueckentext = task(
        id="l",
        typ="lueckentext",
        text="Eine Hex-Ziffer hat {{1}} Bit.",
        luecken=[{"antworten": ["4", "vier"], "falsch": [{"antwort": "8", "warum": "Das ist ein Byte."}]}],
    )
    assert evaluate(item, ["Vier"]).richtig
    wrong = evaluate(item, ["8"])
    assert not wrong.richtig and "Das ist ein Byte." in wrong.rueckmeldungen[0].text


def test_gap_text_placeholders_must_match() -> None:
    with pytest.raises(ValidationError):
        task(
            id="l",
            typ="lueckentext",
            text="{{1}} und {{3}}",
            luecken=[{"antworten": ["a"]}, {"antworten": ["b"]}],
        )


def test_order() -> None:
    item = task(id="r", typ="reihenfolge", elemente=["KiB", "MB", "MiB", "GB"])
    assert evaluate(item, [0, 1, 2, 3]).richtig
    swapped = evaluate(item, [0, 2, 1, 3])
    assert not swapped.richtig and swapped.anteil == 0.5


def test_calculation_reports_first_wrong_step() -> None:
    item = task(
        id="c",
        typ="rechnung",
        schritte=[
            {"frage": "Hostbits", "antwort": "6", "erklaerung": "32 − 26."},
            {
                "frage": "Hosts",
                "antwort": "62",
                "erklaerung": "2^6 − 2.",
                "falsch": [{"antwort": "64", "warum": "Es fehlt − 2.", "ursache": "konzept"}],
            },
            {"frage": "Maske", "antwort": "255.255.255.192", "format": "ipv4", "erklaerung": "26 Einsen."},
        ],
    )
    assert evaluate(item, ["6", "62", "255.255.255.192"]).richtig
    result = evaluate(item, ["6", "64 Hosts", "255.255.255.192"])
    assert result.fehlerschritt == 1 and result.ursache == "konzept"
    assert "Es fehlt − 2." in result.rueckmeldungen[1].text
    unknown = evaluate(item, ["7", "62", "255.255.255.0"])
    assert unknown.fehlerschritt == 0 and unknown.ursache == "rechenfehler"
    assert "Folgefehler" in unknown.rueckmeldungen[-1].text
    assert evaluate(item, ["", "", ""]).ursache == "konzept"


def test_free_text_self_assessment_and_missing_terms() -> None:
    item: Freitext = task(
        id="f",
        typ="freitext",
        operator="erläutern",
        musterloesung="Kurz, weil 4 Bit eine Ziffer sind.",
        bewertungspunkte=[
            {"punkt": "4 Bit je Ziffer", "kernbegriffe": ["4 bit", "vier bit", "nibble"]},
            {"punkt": "kürzer als dual", "kernbegriffe": ["kürzer", "kompakt"]},
        ],
    )
    text = "Hex ist kompakter."
    assert missing_terms(item, text) == [("4 Bit je Ziffer", ["4 bit", "vier bit", "nibble"])]
    full = evaluate(item, FreitextAntwort(text, [True, True]))
    assert full.richtig and "Kernbegriffe" in full.rueckmeldungen[0].text
    half = evaluate(item, FreitextAntwort(text, [False, True]))
    assert not half.richtig and half.anteil == 0.5


def test_wrong_answer_form_raises() -> None:
    with pytest.raises(TypeError):
        evaluate(MC, ["a"])


def test_help_steps_and_level() -> None:
    steps = help_steps(MC)
    assert [s.titel for s in steps] == ["Hinweis 1 · Richtung", "Lösungsweg"]
    assert help_level(MC, 0) == 0
    assert help_level(MC, 1) == 1
    assert help_level(MC, 2) == LOESUNGSWEG_GEOEFFNET


def test_ids_are_checked() -> None:
    with pytest.raises(ValidationError):
        task(id="Groß Buchstaben", typ="reihenfolge", elemente=["a", "b", "c"])
    assert isinstance(MC, MultipleChoice)
