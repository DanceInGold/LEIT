"""Aufbereitung einer Aufgabe für die Anzeige – ohne NiceGUI, deshalb testbar.

Mischt Antwortmöglichkeiten reproduzierbar (dieselbe Aufgabe sieht nach einem Neuladen gleich
aus), setzt Lücken als Nummern in den Text und liefert Eingabehilfen je Antwortformat.
"""

from __future__ import annotations

import random

from ap_trainer.content.aufgaben import LUECKE, Antwortformat, Aufgabe, Reihenfolge
from ap_trainer.tasks.check import Antwort, FreitextAntwort

PLATZHALTER: dict[Antwortformat, str] = {
    "zahl": "z. B. 62 oder 4,5",
    "dual": "z. B. 1010 0110",
    "hex": "z. B. 3F",
    "ipv4": "z. B. 192.168.10.0",
    "ipv6": "z. B. 2001:db8:abcd:12::/64",
    "text": "",
}


def shuffled_indices(task: Aufgabe, count: int, salt: str = "") -> list[int]:
    """Indizes 0 … count−1 in einer festen, von der Aufgabe abhängigen Zufallsreihenfolge."""
    order = list(range(count))
    random.Random(f"{task.id}{salt}").shuffle(order)
    return order


def initial_order(task: Aufgabe, count: int) -> list[int]:
    """Startreihenfolge für Reihenfolge-Aufgaben – nie schon die Lösung."""
    order = shuffled_indices(task, count, "reihenfolge")
    if order == sorted(order):
        order = order[1:] + order[:1]
    return order


def gap_markdown(text: str) -> str:
    """Ersetzt ``{{n}}`` durch eine gut sichtbare Lückennummer, z. B. ``**[1] …**``."""
    return LUECKE.sub(lambda match: f"**[{match.group(1)}] …**", text)


def percent(share: float) -> str:
    """Punkteanteil als ganze Prozentzahl."""
    return f"{round(share * 100)} %"


def is_blank(task: Aufgabe, answer: Antwort) -> bool:
    """True, wenn noch gar nichts eingegeben wurde – dann wird nicht bewertet."""
    if isinstance(task, Reihenfolge):
        return False
    if isinstance(answer, FreitextAntwort):
        return not answer.text.strip()
    if isinstance(answer, frozenset):
        return not answer
    return all(item is None or not str(item).strip() for item in answer)
