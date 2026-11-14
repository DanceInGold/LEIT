"""Generator „Verfügbarkeit“: Ausfallzeit, Reihen- und Parallelschaltung, SLA prüfen (AU-03).

Stufen: 1 Verfügbarkeit in Ausfallzeit pro Jahr umrechnen, 2 Komponenten in Reihe, 3 redundante
Komponenten parallel, 4 Handlungssituation: redundantes Serverpaar hinter einem Switch gegen eine
SLA-Zusage prüfen. Formeln aus der Lektion „Verfügbarkeit sichern“: Ausfallzeit = (1 − V) × 8.760 h,
Reihe = Produkt der Verfügbarkeiten, parallel = 1 − Produkt der Ausfallwahrscheinlichkeiten.
"""

from __future__ import annotations

import random
from fractions import Fraction

from ap_trainer.content.aufgaben import Aufgabe, Fehlerbild, Rechenschritt, Rechnung, Stufe
from ap_trainer.content.models import Beleg
from ap_trainer.tasks.generators import Generator, register
from ap_trainer.tasks.generators._numbers import de, number_step

type _Parts = tuple[list[Rechenschritt], str, str, str | None, list[str]]

HOURS_PER_YEAR = 8760
# Prozentangaben werden auf vier Nachkommastellen erwartet (bei 99,99 % zählt jede Stelle);
# relative Toleranz 0,00001 ≈ 0,001 Prozentpunkte
PERCENT_PLACES = 4
PERCENT_TOLERANCE = 0.00001
COMPONENTS = ["Server", "Switch", "Firewall", "Router", "Storage", "Internetanschluss"]
SERIES_VALUES = [Fraction(v) / 100 for v in ("99", "99.5", "99.8", "99.9", "99.95")]
SINGLE_VALUES = [Fraction(v) / 100 for v in ("99", "99.5", "99.9", "99.95", "99.99")]
PARALLEL_VALUES = [Fraction(v) / 100 for v in ("95", "97", "98", "99", "99.5")]


def downtime_hours(availability: Fraction) -> Fraction:
    """Ausfallzeit pro Jahr in Stunden: (1 − V) × 8.760 h."""
    return (1 - availability) * HOURS_PER_YEAR


def series(values: list[Fraction]) -> Fraction:
    """Gesamtverfügbarkeit hintereinander geschalteter Komponenten: Produkt."""
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def parallel(values: list[Fraction]) -> Fraction:
    """Gesamtverfügbarkeit redundanter Komponenten: 1 − Produkt der Ausfallwahrscheinlichkeiten."""
    failure = Fraction(1)
    for value in values:
        failure *= 1 - value
    return 1 - failure


def pct(value: Fraction) -> str:
    """Verfügbarkeit als Prozent mit bis zu vier Nachkommastellen, z. B. ``99,95 %``."""
    return f"{de(value * 100, max_places=4)} %"


def _percent_step(
    frage: str, value: Fraction, erklaerung: str, falsch: list[tuple[Fraction, str, str]] | None = None
) -> Rechenschritt:
    """Schritt mit Prozentwert auf vier Nachkommastellen und enger Toleranz."""
    step = number_step(frage, value * 100, erklaerung, "%", places=PERCENT_PLACES, toleranz=PERCENT_TOLERANCE)
    errors: list[Fehlerbild] = []
    for wrong, why, cause in falsch or []:
        candidate = number_step("x", wrong * 100, "x", places=PERCENT_PLACES).antwort
        # „100“ entsteht nur durch Rundung (z. B. Parallel-Fehlwert 99,99995 %) und wäre irreführend
        if candidate not in {step.antwort, "100"} and candidate not in {e.antwort for e in errors}:
            errors.append(Fehlerbild(antwort=candidate, warum=why, ursache=cause))  # type: ignore[arg-type]
    return step.model_copy(update={"falsch": errors})


def _downtime_steps(availability: Fraction, label: str = "pro Jahr") -> list[Rechenschritt]:
    hours = downtime_hours(availability)
    # Kleine Ausfallzeiten brauchen mehr Stellen, sonst trägt die Rundung in die Minuten weiter
    places = 2 if hours >= 10 else 4 if hours >= Fraction(1, 100) else 6
    steps = [
        number_step(
            f"Ausfallzeit {label} in Stunden",
            hours,
            f"(1 − {de(availability, max_places=12)}) × 8.760 h = {de(hours, max_places=places)} h.",
            "h",
            [
                (
                    availability * HOURS_PER_YEAR,
                    "Mit der Verfügbarkeit statt mit dem Ausfallanteil (1 − V) gerechnet.",
                    "konzept",
                ),
                (
                    (1 - availability) * 365,
                    "Das sind Tage (× 365), gefragt sind Stunden (× 8.760).",
                    "rechenfehler",
                ),
            ],
            places=places,
        )
    ]
    if hours < 10:
        steps.append(
            number_step(
                f"Ausfallzeit {label} in Minuten",
                hours * 60,
                f"{de(hours, max_places=places)} h × 60 = {de(hours * 60, max_places=4)} min.",
                "min",
                [(hours * 100, "Eine Stunde hat 60 Minuten, nicht 100.", "rechenfehler")],
            )
        )
    return steps


BELEGE = (
    Beleg(titel="Lektion „Verfügbarkeit sichern“ (Ausfallzeit, Reihen- und Parallelschaltung)"),
    Beleg(titel="BSI IT-Grundschutz-Kompendium, Baustein CON.3 Datensicherungskonzept und Hochverfügbarkeit"),
    Beleg(
        titel="Prüfungskatalog AP1 2025, Unterpunkt 06.04: Sicherung der Verfügbarkeit (laut "
        "IT-Berufe-Podcast #190)",
        url="https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/",
    ),
)


@register
class Availability(Generator):
    """Verfügbarkeit und Ausfallzeit in vier Stufen."""

    id = "verfuegbarkeit"
    titel = "Verfügbarkeit berechnen"
    stufen = (1, 2, 3, 4)
    status = "geprüft"
    quelle = "Generator „verfuegbarkeit“; jede Variante mit exakter Bruchrechnung unabhängig nachgerechnet."
    belege = BELEGE

    def generate(self, rng: random.Random, stufe: Stufe, task_id: str, thema: str) -> Aufgabe:
        """Erzeugt eine Verfügbarkeitsaufgabe der gewünschten Stufe."""
        builders = {1: self._downtime, 2: self._series, 3: self._parallel, 4: self._sla}
        steps, title, question, situation, hints = builders[stufe](rng)
        return Rechnung(
            typ="rechnung",
            id=task_id,
            thema=thema,
            stufe=stufe,
            titel=title,
            situation=situation,
            frage=question,
            hinweise=hints,
            loesungsweg="\n".join(f"{i + 1}. **{s.frage}:** {s.erklaerung}" for i, s in enumerate(steps)),
            schritte=steps,
            quelle=self.quelle,
            belege=list(self.belege),
            status=self.status,
        )

    def _downtime(self, rng: random.Random) -> _Parts:
        availability = rng.choice(SINGLE_VALUES)
        name = rng.choice(COMPONENTS)
        steps = [
            _percent_step(
                "Ausfallanteil in %",
                1 - availability,
                f"100 % − {pct(availability)} = {pct(1 - availability)}.",
                [
                    (
                        availability,
                        "Das ist die Verfügbarkeit selbst. Gesucht ist der Rest bis 100 %.",
                        "konzept",
                    )
                ],
            ),
            *_downtime_steps(availability),
        ]
        question = (
            f"Ein Hersteller garantiert für einen {name} eine Verfügbarkeit von **{pct(availability)}**. "
            "Wie lange darf er pro Jahr höchstens ausfallen? (1 Jahr = 8.760 h)"
        )
        hints = [
            "Gesucht ist der Anteil der Zeit, in der der Dienst **nicht** läuft.",
            "Ausfallzeit = (1 − Verfügbarkeit) × 8.760 h.",
            f"Ausfallanteil: 100 % − {pct(availability)}.",
        ]
        return steps, "Verfügbarkeit in Ausfallzeit", question, None, hints

    def _series(self, rng: random.Random) -> _Parts:
        count = rng.choice([2, 3])
        names = rng.sample(COMPONENTS, count)
        values = [rng.choice(SERIES_VALUES) for _ in names]
        total = series(values)
        product = " × ".join(de(v, max_places=4) for v in values)
        listing = ", ".join(f"{n} **{pct(v)}**" for n, v in zip(names, values, strict=True))
        steps = [
            _percent_step(
                "Gesamtverfügbarkeit in %",
                total,
                f"Reihe = Produkt: {product} = {de(total, max_places=8)} ≈ {pct(total)}.",
                [
                    (
                        min(values),
                        "Das ist nur das schwächste Glied. In Reihe sinkt die Verfügbarkeit weiter.",
                        "konzept",
                    ),
                    (
                        sum(values, Fraction(0)) / count,
                        "Der Durchschnitt gilt nicht – in Reihe wird multipliziert.",
                        "konzept",
                    ),
                    (
                        parallel(values),
                        "Das wäre Redundanz. Hier braucht der Dienst **alle** Komponenten.",
                        "konzept",
                    ),
                ],
            ),
            *_downtime_steps(total),
        ]
        question = (
            f"Ein Dienst funktioniert nur, wenn **alle** Komponenten laufen: {listing}. "
            "Berechne die Gesamtverfügbarkeit (in % auf vier Nachkommastellen) und die Ausfallzeit pro Jahr."
        )
        hints = [
            "Fällt eine Komponente aus, ist der Dienst weg – das ist eine Reihenschaltung.",
            "Reihe: Verfügbarkeiten als Dezimalzahl multiplizieren.",
            f"{product} = ?",
        ]
        return steps, "Komponenten in Reihe", question, None, hints

    def _parallel(self, rng: random.Random) -> _Parts:
        count = rng.choice([2, 2, 3])
        # Drei Server mit 99,5 % ergäben 99,99999 % – auf vier Stellen nicht mehr von 100 % zu trennen
        value = rng.choice(PARALLEL_VALUES if count == 2 else PARALLEL_VALUES[:4])
        failure = 1 - value
        both = failure**count
        total = 1 - both
        steps = [
            _percent_step(
                "Ausfallwahrscheinlichkeit eines Servers in %",
                failure,
                f"1 − {de(value, max_places=4)} = {de(failure, max_places=4)} = {pct(failure)}.",
                [(value, "Das ist die Verfügbarkeit. Ausfallwahrscheinlichkeit = 1 − V.", "konzept")],
            ),
            number_step(
                f"Wahrscheinlichkeit, dass alle {count} gleichzeitig ausfallen (Dezimalzahl)",
                both,
                f"{de(failure, max_places=4)}^{count} = {de(both, max_places=8)}.",
                places=8,
            ),
            _percent_step(
                "Gesamtverfügbarkeit in %",
                total,
                f"1 − {de(both, max_places=8)} = {de(total, max_places=8)} ≈ {pct(total)}.",
                [
                    (
                        value**count,
                        "Das wäre eine Reihenschaltung. Redundant fällt der Dienst nur aus, "
                        "wenn **alle** ausfallen.",
                        "konzept",
                    )
                ],
            ),
            *_downtime_steps(total),
        ]
        question = (
            f"**{count} Server** mit je **{pct(value)}** Verfügbarkeit arbeiten redundant – einer "
            "reicht für den "
            "Dienst. Berechne die Gesamtverfügbarkeit (in % auf vier Nachkommastellen) und die "
            "Ausfallzeit pro Jahr."
        )
        hints = [
            "Der Dienst fällt nur aus, wenn **alle** Server gleichzeitig ausfallen.",
            "Parallel: 1 − (Ausfallwahrscheinlichkeit)^Anzahl.",
            f"Ausfallwahrscheinlichkeit je Server: 1 − {de(value, max_places=4)}.",
        ]
        return steps, "Redundante Server", question, None, hints

    def _sla(self, rng: random.Random) -> _Parts:
        server = rng.choice(PARALLEL_VALUES[2:])
        switch = rng.choice(SERIES_VALUES)
        target = rng.choice([Fraction(v) / 100 for v in ("99", "99.5", "99.8", "99.9")])
        pair = parallel([server, server])
        total = pair * switch
        meets = total >= target
        steps = [
            _percent_step(
                "Verfügbarkeit des Serverpaars in %",
                pair,
                f"1 − ({de(1 - server, max_places=4)})² = {de(pair, max_places=8)} ≈ {pct(pair)}.",
                [(server * server, "Das Paar ist redundant: 1 − (1 − V)², nicht V².", "konzept")],
            ),
            _percent_step(
                "Gesamtverfügbarkeit mit Switch in %",
                total,
                f"Paar und Switch in Reihe: {de(pair, max_places=8)} × {de(switch, max_places=4)} = "
                f"{de(total, max_places=8)} ≈ {pct(total)}.",
                [(pair, "Der Switch fehlt. Er ist ein einzelner Ausfallpunkt in Reihe.", "konzept")],
            ),
            *_downtime_steps(total),
            Rechenschritt(
                frage=f"Wird die Zusage von {pct(target)} eingehalten? (ja/nein)",
                antwort="ja" if meets else "nein",
                format="text",
                erklaerung=f"{pct(total)} {'≥' if meets else '<'} {pct(target)} → "
                f"{'ja' if meets else 'nein'}."
                + ("" if meets else " Der Switch ist der Engpass – ein zweiter Switch würde helfen."),
                falsch=[
                    Fehlerbild(
                        antwort="nein" if meets else "ja",
                        warum="Vergleiche die **Gesamt**verfügbarkeit inklusive Switch mit der Zusage.",
                        ursache="konzept",
                    )
                ],
            ),
        ]
        situation = (
            "Das Kundenportal der ArchivTech GmbH läuft auf **zwei redundanten Servern** mit je "
            f"**{pct(server)}** "
            f"Verfügbarkeit. Beide hängen an **einem Switch** mit **{pct(switch)}**. Im Vertrag ist eine "
            f"Verfügbarkeit von **{pct(target)}** zugesagt."
        )
        question = (
            "Berechne die Gesamtverfügbarkeit (in % auf vier Nachkommastellen) und prüfe, ob die Zusage hält."
        )
        hints = [
            "Erst das redundante Paar berechnen, dann mit dem Switch in Reihe schalten.",
            "Paar: 1 − (1 − V)². Reihe: multiplizieren.",
            f"Ausfallwahrscheinlichkeit je Server: {de(1 - server, max_places=4)}.",
        ]
        return steps, "SLA des Kundenportals prüfen", question, situation, hints
