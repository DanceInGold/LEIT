"""Antworten bewerten: je Aufgabentyp eine Funktion, gemeinsames Ergebnisformat.

Rechenaufgaben werden Schritt für Schritt geprüft; das Ergebnis nennt den ersten falschen
Schritt (AU-04). Typische Falschantworten bekommen ihre eigene Erklärung (HI-03), und jeder
Fehler trägt eine Ursache für das Fehlerprotokoll (FT-04).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from ap_trainer.content.aufgaben import (
    Antwortformat,
    Aufgabe,
    Fehlerbild,
    Fehlerursache,
    Freitext,
    Lueckentext,
    MultipleChoice,
    Rechenschritt,
    Rechnung,
    Reihenfolge,
    Zuordnung,
)
from ap_trainer.tasks.answers import normalize_text, same_answer

# Freitext gilt als gelöst, wenn mindestens drei Viertel der Punkte erreicht sind
FREITEXT_SCHWELLE = 0.75


@dataclass(frozen=True)
class Rueckmeldung:
    """Feedback zu einem Teil der Antwort (Option, Lücke, Schritt, Paar …)."""

    teil: str
    richtig: bool
    text: str
    ursache: Fehlerursache | None = None


@dataclass(frozen=True)
class Ergebnis:
    """Bewertung einer Antwort.

    ``anteil`` ist der Punkteanteil zwischen 0 und 1, ``fehlerschritt`` der erste falsche
    Rechenschritt (0-basiert) und ``ursache`` die Ursache des ersten Fehlers.
    """

    richtig: bool
    anteil: float
    rueckmeldungen: list[Rueckmeldung] = field(default_factory=list)
    fehlerschritt: int | None = None
    ursache: Fehlerursache | None = None


@dataclass(frozen=True)
class FreitextAntwort:
    """Freitext plus Selbstbewertung: je Bewertungspunkt, ob er in der Antwort steckt."""

    text: str
    erfuellt: Sequence[bool]


Antwort = frozenset[int] | Sequence[str | None] | Sequence[int] | FreitextAntwort


def _first_cause(feedback: list[Rueckmeldung]) -> Fehlerursache | None:
    return next((f.ursache for f in feedback if not f.richtig), None)


def _match_error(
    errors: list[Fehlerbild], given: str, fmt: Antwortformat = "text", tolerance: float = 0.0
) -> Fehlerbild | None:
    """Sucht eine bekannte Falschantwort, die zur Eingabe passt."""
    return next((e for e in errors if same_answer(fmt, given, e.antwort, tolerance)), None)


def check_multiple_choice(task: MultipleChoice, chosen: frozenset[int]) -> Ergebnis:
    """Richtig nur bei genau der richtigen Auswahl; Teilpunkte für richtige Kreuze."""
    feedback: list[Rueckmeldung] = []
    hits = wrong = 0
    for index, option in enumerate(task.optionen):
        picked = index in chosen
        if picked and option.richtig:
            hits += 1
            feedback.append(Rueckmeldung(option.text, True, option.warum or "Richtig angekreuzt."))
        elif picked:
            wrong += 1
            reason = option.warum or "Diese Option trifft nicht zu."
            feedback.append(Rueckmeldung(option.text, False, reason, option.ursache))
        elif option.richtig:
            text = "Diese Option hätte angekreuzt werden müssen."
            if option.warum:
                text += f" {option.warum}"
            feedback.append(Rueckmeldung(option.text, False, text, option.ursache))
    share = max(hits - wrong, 0) / task.anzahl_richtig
    correct = hits == task.anzahl_richtig and wrong == 0
    # Ein falsches Kreuz sagt mehr über die Fehlerursache als ein fehlendes
    picked_wrong = [o.ursache for i, o in enumerate(task.optionen) if i in chosen and not o.richtig]
    cause = picked_wrong[0] if picked_wrong else _first_cause(feedback)
    return Ergebnis(correct, share, feedback, ursache=cause)


def check_assignment(task: Zuordnung, chosen: Sequence[str | None]) -> Ergebnis:
    """Je Paar ein Teilpunkt; ``chosen[i]`` ist das rechte Element für ``paare[i]``."""
    feedback: list[Rueckmeldung] = []
    for index, pair in enumerate(task.paare):
        answer = chosen[index] if index < len(chosen) else None
        if answer is not None and normalize_text(answer) == normalize_text(pair.rechts):
            feedback.append(Rueckmeldung(pair.links, True, f"→ {pair.rechts}"))
        else:
            given = answer or "nichts gewählt"
            feedback.append(
                Rueckmeldung(pair.links, False, f"Gewählt: {given}. Richtig: {pair.rechts}.", "begriff")
            )
    hits = sum(f.richtig for f in feedback)
    return Ergebnis(hits == len(task.paare), hits / len(task.paare), feedback, ursache=_first_cause(feedback))


def check_gap_text(task: Lueckentext, answers: Sequence[str | None]) -> Ergebnis:
    """Je Lücke ein Teilpunkt; bekannte Falschantworten bekommen ihre Erklärung."""
    feedback: list[Rueckmeldung] = []
    for index, gap in enumerate(task.luecken):
        given = (answers[index] if index < len(answers) else None) or ""
        label = f"Lücke {index + 1}"
        if any(normalize_text(given) == normalize_text(a) for a in gap.antworten):
            feedback.append(Rueckmeldung(label, True, gap.antworten[0]))
            continue
        known = _match_error(gap.falsch, given)
        text = f"Richtig: {gap.antworten[0]}."
        if known:
            feedback.append(Rueckmeldung(label, False, f"{known.warum} {text}", known.ursache))
        else:
            feedback.append(Rueckmeldung(label, False, f"„{given or '–'}“ passt nicht. {text}", "begriff"))
    hits = sum(f.richtig for f in feedback)
    return Ergebnis(
        hits == len(task.luecken), hits / len(task.luecken), feedback, ursache=_first_cause(feedback)
    )


def check_order(task: Reihenfolge, order: Sequence[int]) -> Ergebnis:
    """``order`` enthält die Indizes von ``elemente`` in der Reihenfolge des Lernenden."""
    feedback: list[Rueckmeldung] = []
    for position, element_index in enumerate(order):
        element = task.elemente[element_index]
        if element_index == position:
            feedback.append(Rueckmeldung(element, True, f"Platz {position + 1} stimmt."))
        else:
            text = f"Steht auf Platz {position + 1}, gehört auf Platz {element_index + 1}."
            feedback.append(Rueckmeldung(element, False, text, "konzept"))
    hits = sum(f.richtig for f in feedback)
    complete = sorted(order) == list(range(len(task.elemente)))
    correct = complete and hits == len(task.elemente)
    return Ergebnis(correct, hits / len(task.elemente), feedback, ursache=_first_cause(feedback))


def _check_step(step: Rechenschritt, given: str) -> Rueckmeldung:
    unit = f" {step.einheit}" if step.einheit else ""
    if given.strip() and same_answer(step.format, given, step.antwort, step.toleranz):
        return Rueckmeldung(step.frage, True, f"{step.antwort}{unit}")
    known = _match_error(step.falsch, given, step.format, step.toleranz) if given.strip() else None
    expected = f"Richtig: {step.antwort}{unit}. {step.erklaerung}"
    if known:
        return Rueckmeldung(step.frage, False, f"{known.warum} {expected}", known.ursache)
    if not given.strip():
        return Rueckmeldung(step.frage, False, f"Keine Eingabe. {expected}", "konzept")
    return Rueckmeldung(step.frage, False, f"„{given}“ stimmt nicht. {expected}", "rechenfehler")


def check_calculation(task: Rechnung, inputs: Sequence[str | None]) -> Ergebnis:
    """Prüft jeden Zwischenschritt einzeln und meldet den ersten falschen (AU-04).

    Spätere Schritte werden trotzdem gegen die richtigen Werte geprüft; ein Fehler am Anfang
    führt deshalb oft zu Folgefehlern, auf die das Feedback hinweist.
    """
    feedback = [
        _check_step(step, (inputs[i] if i < len(inputs) else None) or "")
        for i, step in enumerate(task.schritte)
    ]
    first_wrong = next((i for i, f in enumerate(feedback) if not f.richtig), None)
    if first_wrong is not None and first_wrong < len(feedback) - 1:
        later = feedback[first_wrong + 1 :]
        if any(not f.richtig for f in later):
            note = Rueckmeldung(
                "Hinweis",
                False,
                f"Der erste Fehler steckt in Schritt {first_wrong + 1}; "
                "spätere Fehler können Folgefehler sein.",
            )
            feedback.append(note)
    hits = sum(f.richtig for f in feedback[: len(task.schritte)])
    share = hits / len(task.schritte)
    return Ergebnis(first_wrong is None, share, feedback, first_wrong, _first_cause(feedback))


def missing_terms(task: Freitext, text: str) -> list[tuple[str, list[str]]]:
    """Bewertungspunkte, deren Kernbegriffe in ``text`` nicht vorkommen (AU-05).

    Liefert je Punkt die Liste seiner Kernbegriffe; leer, wenn ein Punkt keine hat oder einer
    davon im Text steht.
    """
    haystack = normalize_text(text)
    result: list[tuple[str, list[str]]] = []
    for point in task.bewertungspunkte:
        terms = point.kernbegriffe
        if terms and not any(normalize_text(term) in haystack for term in terms):
            result.append((point.punkt, terms))
    return result


def check_free_text(task: Freitext, answer: FreitextAntwort) -> Ergebnis:
    """Punkte aus der Selbstbewertung; fehlende Kernbegriffe werden zusätzlich gemeldet."""
    total = sum(p.punkte for p in task.bewertungspunkte)
    feedback: list[Rueckmeldung] = []
    reached = 0
    missing = {point for point, _ in missing_terms(task, answer.text)}
    for index, point in enumerate(task.bewertungspunkte):
        claimed = index < len(answer.erfuellt) and bool(answer.erfuellt[index])
        if claimed:
            reached += point.punkte
            text = "Genannt."
            if point.punkt in missing:
                text = (
                    f"Genannt – aber keiner der Kernbegriffe steht im Text ({', '.join(point.kernbegriffe)})."
                )
            feedback.append(Rueckmeldung(point.punkt, True, text))
        else:
            feedback.append(Rueckmeldung(point.punkt, False, "Fehlt in der Antwort.", "konzept"))
    share = reached / total
    return Ergebnis(share >= FREITEXT_SCHWELLE, share, feedback, ursache=_first_cause(feedback))


def evaluate(task: Aufgabe, answer: Antwort) -> Ergebnis:
    """Bewertet eine Antwort passend zum Aufgabentyp.

    Erwartete Antwortform je Typ: Multiple Choice ``frozenset`` der Optionsindizes,
    Zuordnung und Lückentext je eine Zeichenkette pro Paar/Lücke, Reihenfolge die Indizes in
    gewählter Reihenfolge, Rechnung je eine Eingabe pro Schritt, Freitext :class:`FreitextAntwort`.
    """
    if isinstance(task, MultipleChoice) and isinstance(answer, frozenset):
        return check_multiple_choice(task, answer)
    if isinstance(task, Freitext) and isinstance(answer, FreitextAntwort):
        return check_free_text(task, answer)
    if isinstance(answer, frozenset | FreitextAntwort):
        raise TypeError(f"Antwortform passt nicht zum Aufgabentyp {task.typ}")
    if isinstance(task, Reihenfolge):
        return check_order(task, [int(i) for i in answer if i is not None])
    texts = [None if a is None else str(a) for a in answer]
    if isinstance(task, Zuordnung):
        return check_assignment(task, texts)
    if isinstance(task, Lueckentext):
        return check_gap_text(task, texts)
    if isinstance(task, Rechnung):
        return check_calculation(task, texts)
    raise TypeError(f"Antwortform passt nicht zum Aufgabentyp {task.typ}")
