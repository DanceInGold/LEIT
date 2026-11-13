"""Inhaltsprüfung der Aufgaben, die das Aufgabenmodul braucht (NF-08).

Ergänzt ``content/checks.py`` um alles, was die Aufgabenlogik kennen muss: Gibt es die genannten
Generatoren? Sind die Musterlösungen der Rechenschritte im angegebenen Format lesbar? Wird jede
eigene Musterlösung als richtig bewertet und jede typische Falschantwort als falsch?
"""

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
from ap_trainer.content.loader import ContentError, ContentPackage
from ap_trainer.tasks.answers import is_valid, same_answer
from ap_trainer.tasks.check import Antwort, FreitextAntwort, evaluate
from ap_trainer.tasks.generators import registry


def model_answer(task: Aufgabe) -> Antwort:
    """Die Antwort, die laut Aufgabe volle Punktzahl bekommt (für Prüfungen und Tests)."""
    if isinstance(task, MultipleChoice):
        return frozenset(i for i, option in enumerate(task.optionen) if option.richtig)
    if isinstance(task, Zuordnung):
        return [pair.rechts for pair in task.paare]
    if isinstance(task, Lueckentext):
        return [gap.antworten[0] for gap in task.luecken]
    if isinstance(task, Reihenfolge):
        return list(range(len(task.elemente)))
    if isinstance(task, Rechnung):
        return [step.antwort for step in task.schritte]
    assert isinstance(task, Freitext)
    return FreitextAntwort(task.musterloesung, [True] * len(task.bewertungspunkte))


def _check_task(task: Aufgabe) -> list[str]:
    problems: list[str] = []
    if isinstance(task, Rechnung):
        for number, step in enumerate(task.schritte, start=1):
            if not is_valid(step.format, step.antwort):
                problems.append(f"Schritt {number}: Antwort „{step.antwort}“ ist kein gültiges {step.format}")
            for error in step.falsch:
                if not is_valid(step.format, error.antwort):
                    problems.append(f"Schritt {number}: Falschantwort „{error.antwort}“ nicht lesbar")
                elif same_answer(step.format, error.antwort, step.antwort, step.toleranz):
                    problems.append(f"Schritt {number}: Falschantwort „{error.antwort}“ zählt als richtig")
    if not problems and not evaluate(task, model_answer(task)).richtig:
        problems.append("die eigene Musterlösung wird nicht als richtig bewertet")
    if isinstance(task, Lueckentext):
        for number, gap in enumerate(task.luecken, start=1):
            for error in gap.falsch:
                if error.antwort.casefold() in (a.casefold() for a in gap.antworten):
                    problems.append(f"Lücke {number}: „{error.antwort}“ ist zugleich richtig und falsch")
    return problems


def check_tasks(pkg: ContentPackage) -> list[ContentError]:
    """Alle Aufgabenfehler eines Pakets: unbekannte Generatoren, unlesbare oder falsche Lösungen."""
    errors: list[ContentError] = []
    known = registry()
    for topic_id, generator_ids in pkg.generatoren.items():
        file = str(pkg.root / "aufgaben" / f"{topic_id}.yaml")
        for generator_id in generator_ids:
            if generator_id not in known:
                errors.append(ContentError(file, f"unbekannter Generator '{generator_id}'"))
    for task in pkg.aufgaben.values():
        file = str(pkg.root / "aufgaben" / f"{task.thema}.yaml")
        errors.extend(ContentError(file, f"{task.id}: {problem}") for problem in _check_task(task))
    return errors
