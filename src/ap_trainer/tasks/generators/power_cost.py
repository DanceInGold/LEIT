"""Generator „Stromkosten“: Energie und Kosten, Gerätevergleich, Netzteil-Wirkungsgrad, PUE (AU-03).

Stufen: 1 Energie in kWh, 2 Jahreskosten im Dauerbetrieb, 3 Vergleich zweier Geräte für viele
Arbeitsplätze, 4 Handlungssituation mit Wirkungsgrad oder PUE. Formeln aus den Lektionen
„Nachhaltige IT“ (kWh = kW × h) und „Netzteil und Anschlüsse“ (P_auf = P_ab ÷ η).
"""

from __future__ import annotations

import random
from fractions import Fraction

from ap_trainer.content.aufgaben import Aufgabe, Rechenschritt, Rechnung, Stufe
from ap_trainer.content.models import Beleg
from ap_trainer.tasks.generators import Generator, register
from ap_trainer.tasks.generators._numbers import ROUNDED_TOLERANCE, de, number_step

type _Parts = tuple[list[Rechenschritt], str, str, str | None, list[str]]

HOURS_PER_YEAR = 365 * 24
# Strompreise in Cent pro kWh, als Annahme in der Aufgabe genannt
PRICES_CENT = [25, 28, 30, 32, 35, 40]
DEVICES = [
    ("Monitor", [18, 22, 25, 30]),
    ("Arbeitsplatz-PC", [60, 80, 95, 120]),
    ("Notebook", [15, 25, 35, 45]),
    ("Switch", [30, 45, 60, 90]),
    ("Archivserver", [250, 300, 400, 550]),
]


def kwh(watts: Fraction | int, hours: Fraction | int) -> Fraction:
    """Energie in kWh: Leistung in kW × Zeit in h."""
    return Fraction(watts) / 1000 * hours


def euro(cent: int) -> Fraction:
    """Cent in Euro."""
    return Fraction(cent, 100)


def _energy_step(watts: Fraction | int, hours: int, label: str = "Energie in kWh") -> Rechenschritt:
    energy = kwh(watts, hours)
    return number_step(
        label,
        energy,
        f"{de(Fraction(watts) / 1000, max_places=4)} kW × {de(hours)} h = {de(energy)} kWh.",
        "kWh",
        [
            (
                Fraction(watts) * hours,
                "Watt nicht in Kilowatt umgerechnet: erst durch 1.000 teilen.",
                "rechenfehler",
            )
        ],
    )


def _cost_step(energy: Fraction, cent: int, label: str = "Kosten in Euro") -> Rechenschritt:
    cost = energy * euro(cent)
    return number_step(
        label,
        cost,
        f"{de(energy)} kWh × {de(euro(cent), 2)} €/kWh = {de(cost, 2)} €.",
        "€",
        [
            (
                energy * cent,
                f"Mit Cent statt Euro gerechnet: der Preis ist {de(euro(cent), 2)} €/kWh.",
                "rechenfehler",
            )
        ],
    )


BELEGE = (
    Beleg(titel="Lektion „Nachhaltige IT und Energie“ (kWh = kW × h, PUE)"),
    Beleg(titel="Lektion „Netzteil und Anschlüsse“ (Wirkungsgrad η = P_ab ÷ P_auf)"),
    Beleg(titel="ISO/IEC 30134-2:2016 – Key performance indicators, Part 2: Power usage effectiveness (PUE)"),
    Beleg(
        titel="80 PLUS Programm (CLEAResult): Effizienzstufen für Netzteile",
        url="https://www.clearesult.com/80plus/",
    ),
)


@register
class PowerCost(Generator):
    """Energie, Stromkosten und Effizienz in vier Stufen."""

    id = "stromkosten"
    titel = "Stromverbrauch und Stromkosten"
    stufen = (1, 2, 3, 4)
    status = "ungeprüft"
    quelle = "Generator „stromkosten“; jede Variante mit exakter Bruchrechnung unabhängig nachgerechnet."
    belege = BELEGE

    def generate(self, rng: random.Random, stufe: Stufe, task_id: str, thema: str) -> Aufgabe:
        """Erzeugt eine Stromkosten-Aufgabe der gewünschten Stufe."""
        builders = {1: self._energy, 2: self._yearly, 3: self._compare, 4: self._efficiency}
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

    def _energy(self, rng: random.Random) -> _Parts:
        name, options = rng.choice(DEVICES)
        watts = rng.choice(options)
        hours = rng.choice([8, 10, 24, 40, 160, 200])
        steps = [
            number_step(
                "Leistung in kW",
                Fraction(watts, 1000),
                f"{watts} W ÷ 1.000 = {de(Fraction(watts, 1000), max_places=4)} kW.",
                "kW",
                [(Fraction(watts, 100), "1 kW sind 1.000 W, nicht 100 W.", "rechenfehler")],
            ),
            _energy_step(watts, hours),
        ]
        question = f"Ein {name} nimmt **{watts} W** auf und läuft **{hours} Stunden**. Wie viel "
        "Energie verbraucht er?"
        hints = [
            "Energie = Leistung × Zeit.",
            "Für kWh die Leistung in kW umrechnen: Watt ÷ 1.000.",
            f"{watts} W = {de(Fraction(watts, 1000), max_places=4)} kW.",
        ]
        return steps, "Energie berechnen", question, None, hints

    def _yearly(self, rng: random.Random) -> _Parts:
        name, options = rng.choice(DEVICES[3:])
        watts = rng.choice(options)
        cent = rng.choice(PRICES_CENT)
        energy = kwh(watts, HOURS_PER_YEAR)
        steps = [
            number_step(
                "Betriebsstunden pro Jahr",
                HOURS_PER_YEAR,
                "365 Tage × 24 h = 8.760 h.",
                "h",
                [(365 * 8, "Der Server läuft rund um die Uhr – 24 h pro Tag, nicht 8.", "konzept")],
            ),
            _energy_step(watts, HOURS_PER_YEAR, "Energie pro Jahr in kWh"),
            _cost_step(energy, cent, "Stromkosten pro Jahr in Euro"),
        ]
        question = (
            f"Ein {name} nimmt im Durchschnitt **{watts} W** auf und läuft **rund um die Uhr**. "
            f"Wie hoch sind die Stromkosten pro Jahr bei **{de(euro(cent), 2)} €/kWh**?"
        )
        hints = [
            "Kosten = Energie (kWh) × Preis pro kWh.",
            "Ein Jahr im Dauerbetrieb hat 365 × 24 Stunden.",
            f"Energie = {de(Fraction(watts, 1000), max_places=4)} kW × 8.760 h.",
        ]
        return steps, "Jahresstromkosten", question, None, hints

    def _compare(self, rng: random.Random) -> _Parts:
        old_w = rng.choice([65, 80, 95, 110])
        new_w = rng.choice([10, 12, 15, 20])
        seats = rng.choice([10, 20, 25, 40, 50])
        days = rng.choice([200, 210, 220])
        per_day = rng.choice([6, 8])
        cent = rng.choice(PRICES_CENT)
        hours = days * per_day
        old_cost = kwh(old_w, hours) * euro(cent)
        new_cost = kwh(new_w, hours) * euro(cent)
        saving = (old_cost - new_cost) * seats
        steps = [
            number_step(
                "Betriebsstunden pro Jahr",
                hours,
                f"{days} Tage × {per_day} h = {de(hours)} h.",
                "h",
                [(HOURS_PER_YEAR, "Bürogeräte laufen nur an Arbeitstagen – nicht 8.760 h.", "konzept")],
            ),
            _cost_step(kwh(old_w, hours), cent, "Kosten je PC in Euro"),
            _cost_step(kwh(new_w, hours), cent, "Kosten je Thin Client in Euro"),
            number_step(
                "Ersparnis pro Jahr für alle Plätze in Euro",
                saving,
                f"({old_w} − {new_w}) W = {de(Fraction(old_w - new_w, 1000), max_places=4)} kW "
                f"× {de(hours)} h × {de(euro(cent), 2)} € = {de(old_cost - new_cost, 2)} € je Platz "
                f"× {seats} = {de(saving, 2)} €.",
                "€",
                [
                    (
                        old_cost - new_cost,
                        "Das ist die Ersparnis je Platz – noch mal die Anzahl Plätze.",
                        "rechenfehler",
                    )
                ],
                # Wer die Kosten je Gerät erst auf Cent rundet, landet ein paar Cent daneben – das zählt
                toleranz=ROUNDED_TOLERANCE,
            ),
        ]
        situation = (
            f"Die ArchivTech GmbH überlegt, **{seats} Arbeitsplatz-PCs** ({old_w} W) durch **Thin Clients** "
            f"({new_w} W) zu ersetzen. Die Geräte laufen an **{days} Tagen je {per_day} Stunden**; "
            f"Strompreis **{de(euro(cent), 2)} €/kWh**."
        )
        question = "Wie viel Stromkosten spart die Umstellung pro Jahr? (Strom der Server bleibt außen vor.)"
        hints = [
            "Je Gerät: Leistung in kW × Stunden × Preis; dann die Differenz mal Anzahl Plätze.",
            "Betriebsstunden = Arbeitstage × Stunden pro Tag.",
            f"Ein PC braucht {de(Fraction(old_w, 1000), max_places=4)} kW × {de(hours)} h.",
        ]
        return steps, "PC oder Thin Client?", question, situation, hints

    def _efficiency(self, rng: random.Random) -> _Parts:
        return rng.choice([self._power_supply, self._pue])(rng)

    def _power_supply(self, rng: random.Random) -> _Parts:
        output = rng.choice([180, 240, 300, 360, 450])
        eta = rng.choice([80, 85, 87, 90, 92, 94])
        hours = rng.choice([HOURS_PER_YEAR, 220 * 8])
        cent = rng.choice(PRICES_CENT)
        intake = Fraction(output * 100, eta)
        energy = kwh(intake, hours)
        steps = [
            number_step(
                "Aufgenommene Leistung in W",
                intake,
                f"P_auf = P_ab ÷ η = {output} W ÷ {de(Fraction(eta, 100), 2)} = {de(intake)} W.",
                "W",
                [
                    (
                        Fraction(output * eta, 100),
                        "Wirkungsgrad falsch herum: aus der Steckdose kommt **mehr**, als im PC "
                        "ankommt – also teilen.",
                        "konzept",
                    )
                ],
            ),
            _energy_step(intake, hours, "Energie pro Jahr in kWh"),
            _cost_step(energy, cent, "Stromkosten pro Jahr in Euro"),
        ]
        runtime = "rund um die Uhr" if hours == HOURS_PER_YEAR else "an 220 Arbeitstagen je 8 Stunden"
        situation = (
            f"Die Komponenten eines Archivservers der ArchivTech GmbH brauchen zusammen **{output} W**. "
            f"Das Netzteil hat bei dieser Last einen Wirkungsgrad von **{eta} %**. Der Server läuft "
            f"{runtime}; "
            f"Strompreis **{de(euro(cent), 2)} €/kWh**."
        )
        question = "Welche Leistung nimmt der Server aus der Steckdose auf, und was kostet das pro Jahr?"
        hints = [
            "Wirkungsgrad η = abgegebene Leistung ÷ aufgenommene Leistung.",
            "Umgestellt: P_auf = P_ab ÷ η. Danach wie gewohnt kWh und Kosten.",
            f"η = {eta} % = {de(Fraction(eta, 100), 2)}.",
        ]
        return steps, "Netzteil und Stromkosten", question, situation, hints

    def _pue(self, rng: random.Random) -> _Parts:
        it_kw = rng.choice([20, 40, 50, 80, 120])
        pue = Fraction(rng.choice([12, 13, 14, 15, 16, 18]), 10)
        cent = rng.choice(PRICES_CENT)
        total_kw = it_kw * pue
        energy = total_kw * HOURS_PER_YEAR
        overhead = (total_kw - it_kw) * HOURS_PER_YEAR * euro(cent)
        steps = [
            number_step(
                "Gesamtleistung des Rechenzentrums in kW",
                total_kw,
                f"PUE = Gesamt ÷ IT → Gesamt = {it_kw} kW × {de(pue)} = {de(total_kw)} kW.",
                "kW",
                [
                    (
                        Fraction(it_kw) / pue,
                        "Umgestellt in die falsche Richtung: Gesamt = IT-Leistung × PUE.",
                        "konzept",
                    )
                ],
            ),
            number_step(
                "Energie pro Jahr in kWh",
                energy,
                f"{de(total_kw)} kW × 8.760 h = {de(energy)} kWh.",
                "kWh",
            ),
            number_step(
                "Kosten für Kühlung und Verluste pro Jahr in Euro",
                overhead,
                f"({de(total_kw)} − {it_kw}) kW × 8.760 h × {de(euro(cent), 2)} € = {de(overhead, 2)} €.",
                "€",
                [
                    (
                        energy * euro(cent),
                        "Das sind die Gesamtkosten; gefragt ist nur der Anteil über der IT-Last.",
                        "konzept",
                    )
                ],
            ),
        ]
        situation = (
            f"Die IT-Geräte im Rechenzentrum der ArchivTech GmbH nehmen dauerhaft **{it_kw} kW** auf. "
            f"Das Rechenzentrum hat eine **PUE von {de(pue)}**; Strompreis **{de(euro(cent), 2)} €/kWh**."
        )
        question = "Wie hoch sind Gesamtleistung, Jahresenergie und die jährlichen Kosten für "
        "Kühlung, USV und Licht?"
        hints = [
            "PUE = Gesamtenergie des Rechenzentrums ÷ Energie der IT-Geräte.",
            "Alles über der IT-Last (Gesamt − IT) ist Kühlung, USV-Verlust, Licht.",
            f"Gesamtleistung = {it_kw} kW × {de(pue)}.",
        ]
        return steps, "PUE im Rechenzentrum", question, situation, hints
