"""Übungsaufgaben für das Operatoren-Training (ZI-02), gebaut aus ``operatoren.yaml``.

Drei Arten, vom Erkennen zum Selbermachen:

1. **Zuordnen:** Welche Erwartung gehört zu welchem Operator?
2. **Erkennen:** Zu welchem Operator passt diese Musterantwort? (Antworttiefe sehen lernen)
3. **Schreiben:** Eine Frage mit Operator selbst beantworten, dann mit der Musterantwort vergleichen
   und anhand der Prüfpunkte des Operators selbst bewerten.

Die Aufgaben sind normale :mod:`ap_trainer.content.aufgaben`-Modelle, damit die Übungsansicht sie
ohne Sonderfälle anzeigen und prüfen kann.
"""

from __future__ import annotations

import random

from ap_trainer.content.aufgaben import AUFGABE, Aufgabe
from ap_trainer.content.operatoren import OperatorBeispiel, OperatorenDatei, OperatorInfo

# Stufe der Übungsaufgaben: Operatoren richtig zu treffen ist Prüfungshandwerk (Anwenden)
STUFE = 3
# Aufbau einer Trainingsrunde: 1 Zuordnung, dann Erkennen, dann Schreiben
RECOGNIZE_COUNT = 4
WRITE_COUNT = 2


def _slug(operator: str) -> str:
    """Operator für Aufgaben-IDs ohne Umlaute, z. B. „erläutern“ → „erlaeutern“."""
    return operator.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")


def _base(ops: OperatorenDatei, task_id: str, thema: str, titel: str) -> dict[str, object]:
    """Gemeinsame Felder aller Trainingsaufgaben; Quelle und Status kommen aus der Datei."""
    return {
        "id": task_id,
        "thema": thema,
        "stufe": STUFE,
        "titel": titel,
        "quelle": ops.quelle,
        "status": ops.status,
        "belege": [b.model_dump(exclude_none=True) for b in ops.belege],
    }


def definition_task(ops: OperatorenDatei, thema: str) -> Aufgabe:
    """Zuordnung: Erwartung → Operator. ``thema`` dient nur der Anzeige (Aufgaben brauchen eins)."""
    data = _base(ops, "op-zuordnen", thema, "Was verlangt welcher Operator?")
    data.update(
        typ="zuordnung",
        frage="Ordne jeder Erwartung den Operator zu, der sie verlangt.",
        paare=[{"links": op.verlangt, "rechts": op.id} for op in ops.operatoren],
        hinweise=[
            "Achte auf die Antwortform: Stichworte, Sätze, Tabelle oder Rechnung?",
            "Nur darstellen – oder auch erklären, begründen oder urteilen?",
        ],
        loesungsweg="\n".join(f"- **{op.id}** (AB {op.bereich}): {op.verlangt}" for op in ops.operatoren),
    )
    return AUFGABE.validate_python(data)


def _option_reason(op: OperatorInfo) -> str:
    return f"„{op.id}“ verlangt: {op.verlangt}"


def recognize_task(ops: OperatorenDatei, example: OperatorBeispiel, target: str) -> Aufgabe:
    """Multiple Choice: Zu welchem Operator passt die gezeigte Musterantwort?"""
    info = ops.by_id()
    answer = example.antworten[target]  # type: ignore[index]
    data = _base(
        ops,
        f"op-{example.id}-{_slug(target)}-erkennen",
        example.thema,
        f"Welcher Operator? – {example.titel}",
    )
    data.update(
        typ="multiple_choice",
        situation=example.situation,
        frage=(
            f"Diese Antwort holt die volle Punktzahl:\n\n{answer.antwort}\n\n"
            "**Mit welchem Operator war die Aufgabe gestellt?**"
        ),
        optionen=[
            {"text": op.id, "richtig": op.id == target, "warum": _option_reason(op)} for op in ops.operatoren
        ],
        hinweise=[
            "Schau auf die Form: Stichworte, Sätze, Tabelle, Rechnung oder ein Fazit am Ende?",
            f"Diese Antwort hat die Form: {info[target].form}",
        ],
        loesungsweg=f"Die Aufgabe lautete: {answer.frage}\n\n**{target}** – {info[target].verlangt}",
    )
    return AUFGABE.validate_python(data)


def write_task(ops: OperatorenDatei, example: OperatorBeispiel, target: str) -> Aufgabe:
    """Freitext: Frage mit Operator selbst beantworten, dann mit den Prüfpunkten selbst bewerten."""
    op = ops.by_id()[target]
    answer = example.antworten[target]  # type: ignore[index]
    data = _base(
        ops,
        f"op-{example.id}-{_slug(target)}-schreiben",
        example.thema,
        f"Selbst antworten – {example.titel}",
    )
    data.update(
        typ="freitext",
        operator=target,
        situation=example.situation,
        frage=answer.frage,
        musterloesung=answer.antwort,
        # Allgemeine Prüfpunkte des Operators – es geht um die Antworttiefe, nicht um Stichwortsuche
        bewertungspunkte=[{"punkt": k, "punkte": 1} for k in op.kriterien],
        hinweise=[f"Antwortform: {op.form}", f"Typischer Fehler: {op.falle}"],
        loesungsweg=f"**{target}** (AB {op.bereich}): {op.verlangt}\n\n{answer.antwort}",
    )
    return AUFGABE.validate_python(data)


def all_tasks(ops: OperatorenDatei) -> list[Aufgabe]:
    """Alle möglichen Trainingsaufgaben (für Prüfungen und die Aufgabensuche)."""
    thema = ops.beispiele[0].thema
    tasks = [definition_task(ops, thema)]
    for example in ops.beispiele:
        for op in ops.operatoren:
            tasks.append(recognize_task(ops, example, op.id))
            tasks.append(write_task(ops, example, op.id))
    return tasks


def training_round(ops: OperatorenDatei, rng: random.Random) -> list[Aufgabe]:
    """Eine Runde: Zuordnen, dann verschiedene Operatoren erkennen, dann selbst schreiben.

    Erkennen und Schreiben ziehen ohne Wiederholung aus allen Paaren (Beispiel, Operator), damit
    in einer Runde möglichst verschiedene Operatoren und Beispiele drankommen.
    """
    pairs: list[tuple[OperatorBeispiel, str]] = [(e, op.id) for e in ops.beispiele for op in ops.operatoren]
    rng.shuffle(pairs)
    recognize = _spread(pairs, RECOGNIZE_COUNT)
    rest = [p for p in pairs if p not in recognize]
    write = _spread(rest, WRITE_COUNT)
    tasks = [definition_task(ops, ops.beispiele[0].thema)]
    tasks += [recognize_task(ops, example, op) for example, op in recognize]
    tasks += [write_task(ops, example, op) for example, op in write]
    return tasks


def _spread(pairs: list[tuple[OperatorBeispiel, str]], count: int) -> list[tuple[OperatorBeispiel, str]]:
    """Wählt ``count`` Paare, möglichst jeder Operator nur einmal (Reihenfolge wie übergeben)."""
    chosen: list[tuple[OperatorBeispiel, str]] = []
    used: set[str] = set()
    for pair in pairs:
        if len(chosen) == count:
            break
        if pair[1] not in used:
            chosen.append(pair)
            used.add(pair[1])
    for pair in pairs:  # weniger Operatoren als verlangt: auffüllen
        if len(chosen) == count:
            break
        if pair not in chosen:
            chosen.append(pair)
    return chosen
