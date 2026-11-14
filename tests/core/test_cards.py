"""Tests für Lernkarten aus Glossar und Fehlern (GL-02, ZI-05)."""

from __future__ import annotations

from ap_trainer.content.aufgaben import AUFGABE
from ap_trainer.core.cards import mistake_card, mistake_card_id, parse_mistake_card_id


def test_mistake_card_ids_round_trip_with_colons_in_task_id() -> None:
    card_id = mistake_card_id("ipv6", "gen:ipv6:3:5")
    assert card_id == "fehler:ipv6:gen:ipv6:3:5"
    assert parse_mistake_card_id(card_id) == ("ipv6", "gen:ipv6:3:5")
    assert parse_mistake_card_id("osi:def") is None
    assert parse_mistake_card_id("fehler:nurthema") is None


def test_mistake_card_shows_task_and_solution() -> None:
    task = AUFGABE.validate_python(
        {
            "id": "x",
            "typ": "reihenfolge",
            "thema": "t",
            "stufe": 1,
            "titel": "Titel",
            "situation": "Lage",
            "frage": "Frage?",
            "elemente": ["a", "b", "c"],
            "loesungsweg": "erst a, dann b",
            "quelle": "q",
            "status": "geprüft",
        }
    )
    card = mistake_card(task)
    assert card.art == "fehler" and card.thema == "t" and card.aufgabe_id == "x"
    assert card.vorne == "**Titel**\n\nLage\n\nFrage?"
    assert card.hinten == "erst a, dann b"
