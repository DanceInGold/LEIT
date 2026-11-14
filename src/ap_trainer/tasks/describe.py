"""Antworten lesbar machen: „Was habe ich angegeben?“ für die Auswertung der Simulation (PS-02)."""

from __future__ import annotations

from ap_trainer.content.aufgaben import (
    Aufgabe,
    Freitext,
    Lueckentext,
    MultipleChoice,
    Rechnung,
    Reihenfolge,
    Zuordnung,
)
from ap_trainer.tasks.check import Antwort, FreitextAntwort

EMPTY = "–"


def _text(value: object) -> str:
    return str(value).strip() if value not in (None, "") else EMPTY


def describe_answer(task: Aufgabe, answer: Antwort) -> str:
    """Antwort als Markdown-Text, passend zum Aufgabentyp; leere Eingaben als „–“."""
    if isinstance(task, Freitext) and isinstance(answer, FreitextAntwort):
        return answer.text.strip() or EMPTY
    if isinstance(task, MultipleChoice) and isinstance(answer, frozenset):
        chosen = [task.optionen[i].text for i in sorted(answer) if 0 <= i < len(task.optionen)]
        return "; ".join(chosen) or EMPTY
    values = list(answer) if not isinstance(answer, frozenset | FreitextAntwort) else []
    if isinstance(task, Zuordnung):
        return "\n".join(f"- {pair.links} → {_text(v)}" for pair, v in zip(task.paare, values, strict=False))
    if isinstance(task, Lueckentext):
        return " · ".join(f"({i}) {_text(v)}" for i, v in enumerate(values, start=1)) or EMPTY
    if isinstance(task, Reihenfolge):
        order = [task.elemente[int(i)] for i in values if i is not None and 0 <= int(i) < len(task.elemente)]
        return " → ".join(order) or EMPTY
    if isinstance(task, Rechnung):
        return "\n".join(
            f"- {step.frage}: {_text(v)}" for step, v in zip(task.schritte, values, strict=False)
        )
    return EMPTY
