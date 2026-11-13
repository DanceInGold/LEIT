"""Gestufte Hilfen (HI-01) und wie stark eine Lösung durch Hilfe gestützt war (HI-02).

Reihenfolge: Hinweis 1 (Richtung) → Hinweis 2 (Ansatz/Formel) → Hinweis 3 (erster Schritt)
→ vollständiger Lösungsweg. Eine Aufgabe darf weniger als drei Hinweise haben; der
Lösungsweg ist immer die letzte Stufe.
"""

from __future__ import annotations

from dataclasses import dataclass

from ap_trainer.content.aufgaben import Aufgabe

HINWEIS_NAMEN = ("Richtung", "Ansatz", "Erster Schritt")

# Gespeicherter Wert, wenn der Lösungsweg vor dem Prüfen geöffnet wurde
LOESUNGSWEG_GEOEFFNET = 4


@dataclass(frozen=True)
class Hilfe:
    """Eine Hilfestufe mit Beschriftung und Text (Markdown)."""

    stufe: int
    titel: str
    text: str


def help_steps(task: Aufgabe) -> list[Hilfe]:
    """Alle Hilfestufen einer Aufgabe in der Reihenfolge, in der sie aufgedeckt werden."""
    steps = [
        Hilfe(index + 1, f"Hinweis {index + 1} · {HINWEIS_NAMEN[index]}", text)
        for index, text in enumerate(task.hinweise)
    ]
    steps.append(Hilfe(LOESUNGSWEG_GEOEFFNET, "Lösungsweg", task.loesungsweg))
    return steps


def help_level(task: Aufgabe, opened: int) -> int:
    """Hilfestufe für den Lernstand aus der Zahl geöffneter Hilfen.

    0 = ohne Hilfe, 1–3 = so viele Hinweise, 4 = Lösungsweg gesehen. Bei Aufgaben mit weniger
    als drei Hinweisen ist die letzte geöffnete Hilfe immer der Lösungsweg.
    """
    if opened <= 0:
        return 0
    if opened > len(task.hinweise):
        return LOESUNGSWEG_GEOEFFNET
    return opened
