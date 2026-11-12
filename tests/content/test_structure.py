"""Tests für die Gliederung in Lernschritte und die Stilprüfung gegen Textüberladung."""

from __future__ import annotations

from pathlib import Path

from ap_trainer.content.checks import check_style
from ap_trainer.content.loader import load_package
from ap_trainer.content.structure import long_paragraphs, split_steps, visible_text, word_count

REPO_CONTENT = Path(__file__).resolve().parents[2] / "content" / "ap1"


def test_section_without_subheadings_is_one_step() -> None:
    (step,) = split_steps({"Worum geht es?": "Kurzer Text."})
    assert (step.abschnitt, step.titel, step.text) == ("Worum geht es?", "Worum geht es?", "Kurzer Text.")


def test_subheadings_become_own_steps_with_intro() -> None:
    text = "Einleitung.\n\n### Erster Schritt\nA\n\n### Zweiter Schritt\nB\n"
    steps = split_steps({"Wie funktioniert es?": text})
    assert [s.titel for s in steps] == ["Wie funktioniert es?", "Erster Schritt", "Zweiter Schritt"]
    assert [s.text for s in steps] == ["Einleitung.", "A", "B"]
    assert all(s.abschnitt == "Wie funktioniert es?" for s in steps)


def test_subheadings_without_intro() -> None:
    steps = split_steps({"Wie?": "### Nur Teil\nInhalt"})
    assert [s.titel for s in steps] == ["Nur Teil"]


def test_visible_text_drops_details() -> None:
    text = "Sichtbar.\n<details><summary>Warum?</summary>\nVersteckt\n</details>\nAuch sichtbar."
    shown = visible_text(text)
    assert "Versteckt" not in shown and "Auch sichtbar" in shown


def test_word_count_ignores_code_and_markup() -> None:
    assert word_count("**Fett** und `x` | Tabelle |\n```mermaid\ngraph TD; A-->B\n```") == 4


def test_long_paragraphs_only_prose() -> None:
    prose = " ".join(["Wort"] * 45)
    table = "| " + " | ".join(["Zelle"] * 50) + " |"
    listing = "- " + " ".join(["Punkt"] * 50)
    found = long_paragraphs(f"{prose}\n\n{table}\n\n{listing}\n\nKurz.")
    assert len(found) == 1 and found[0][0] == 45


def test_real_lessons_have_no_style_warnings() -> None:
    package, errors = load_package(REPO_CONTENT)
    assert package is not None, errors
    assert check_style(package) == []
