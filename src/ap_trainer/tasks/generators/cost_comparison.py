"""Generator „Kostenvergleich“: Amortisation und Break-even zweier Lösungen (AU-03).

Stufen: 1 Amortisationsdauer aus Investition und Rückfluss, 2 Rückfluss aus Einsparung minus
laufender Kosten, 3 Break-even zweier Kostenfunktionen, 4 Handlungssituation NAS oder Cloud mit
Abschreibung, Wartung und Entscheidung für einen konkreten Bedarf. Formeln aus der Lektion
„Machbarkeit und Wirtschaftlichkeit“.
"""

from __future__ import annotations

import random
from fractions import Fraction

from ap_trainer.content.aufgaben import Aufgabe, Rechenschritt, Rechnung, Stufe
from ap_trainer.content.models import Beleg
from ap_trainer.tasks.generators import Generator, register
from ap_trainer.tasks.generators._numbers import de, number_step

type _Parts = tuple[list[Rechenschritt], str, str, str | None, list[str]]

PROJECTS = [
    "das automatische Umlagern von Archivdaten",
    "ein Skript für die nächtliche Prüfung der Backups",
    "eine Self-Service-Seite für Passwort-Resets",
    "die automatische Benutzeranlage im Verzeichnisdienst",
]
# Zwei Lösungen: (Lösung A mit Fixkosten, Lösung B ohne, Einheit nach „bei“, Mengenwort nach „je“)
SCENARIOS = [
    ("eigenes NAS", "Cloud-Speicher", "TB", "TB Speicher"),
    ("Abteilungsdrucker kaufen", "Seitenpreis-Vertrag", "Tsd. Seiten", "Tausend Seiten"),
    ("eigener Ticket-Server", "Ticket-System als SaaS", "Nutzern", "Nutzer"),
]


def amortisation(investment: int | Fraction, reflux: int | Fraction) -> Fraction:
    """Amortisationsdauer = Investition ÷ Rückfluss pro Zeiteinheit."""
    return Fraction(investment) / Fraction(reflux)


def break_even(fix_a: int | Fraction, var_a: int | Fraction, var_b: int | Fraction) -> Fraction:
    """Menge, bei der fix_a + var_a · x = var_b · x gilt."""
    return Fraction(fix_a) / (Fraction(var_b) - Fraction(var_a))


BELEGE = (
    Beleg(titel="Lektion „Machbarkeit und Wirtschaftlichkeit“ (Amortisation, Break-even)"),
    Beleg(
        titel="Prüfungskatalog AP1 ab 2025, 01.02: Machbarkeit und Wirtschaftlichkeit (laut "
        "IT-Berufe-Podcast #190)",
        url="https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/",
    ),
)


@register
class CostComparison(Generator):
    """Amortisation und Kostenvergleich in vier Stufen."""

    id = "kostenvergleich"
    titel = "Amortisation und Kostenvergleich"
    stufen = (1, 2, 3, 4)
    status = "geprüft"
    quelle = "Generator „kostenvergleich“; jede Variante mit exakter Bruchrechnung unabhängig nachgerechnet."
    belege = BELEGE

    def generate(self, rng: random.Random, stufe: Stufe, task_id: str, thema: str) -> Aufgabe:
        """Erzeugt eine Wirtschaftlichkeitsaufgabe der gewünschten Stufe."""
        builders = {1: self._simple, 2: self._reflux, 3: self._break_even, 4: self._nas_or_cloud}
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

    def _simple(self, rng: random.Random) -> _Parts:
        months = rng.randint(6, 48)
        reflux = rng.choice(range(250, 3001, 50))
        investment = reflux * months
        steps = [
            number_step(
                "Amortisationsdauer in Monaten",
                amortisation(investment, reflux),
                f"{de(investment)} € ÷ {de(reflux)} €/Monat = {months} Monate.",
                "Monate",
                [
                    (
                        Fraction(months, 12),
                        "Das sind Jahre. Ein monatlicher Rückfluss ergibt Monate.",
                        "rechenfehler",
                    )
                ],
            )
        ]
        project = rng.choice(PROJECTS)
        question = (
            f"Die ArchivTech investiert **{de(investment)} €** in {project}. Dadurch fließen jeden Monat "
            f"**{de(reflux)} €** zurück. Nach wie vielen Monaten hat sich die Investition amortisiert?"
        )
        hints = [
            "Amortisation: Wann ist das investierte Geld wieder drin?",
            "Amortisationsdauer = Investition ÷ Rückfluss pro Zeiteinheit.",
            f"Rechne {de(investment)} ÷ {de(reflux)}.",
        ]
        return steps, "Amortisationsdauer", question, None, hints

    def _reflux(self, rng: random.Random) -> _Parts:
        hours = rng.choice([8, 10, 12, 15, 20, 25, 30, 40])
        rate = rng.choice([45, 50, 55, 60, 65, 70, 75, 80])
        saving = hours * rate
        running = rng.choice(range(50, saving // 2, 50)) if saving > 200 else 50
        reflux = saving - running
        months = rng.randint(6, 36)
        investment = reflux * months
        steps = [
            number_step(
                "Eingesparte Arbeit in € pro Monat",
                saving,
                f"{hours} h × {rate} €/h = {de(saving)} €.",
                "€",
            ),
            number_step(
                "Rückfluss in € pro Monat",
                reflux,
                f"Einsparung − laufende Kosten = {de(saving)} € − {de(running)} € = {de(reflux)} €.",
                "€",
                [(saving + running, "Laufende Kosten werden abgezogen, nicht addiert.", "rechenfehler")],
            ),
            number_step(
                "Amortisationsdauer in Monaten",
                amortisation(investment, reflux),
                f"{de(investment)} € ÷ {de(reflux)} €/Monat = {months} Monate.",
                "Monate",
                [
                    (
                        amortisation(investment, saving),
                        "Die laufenden Kosten fehlen – der Rückfluss ist Einsparung **minus** neue Kosten.",
                        "konzept",
                    )
                ],
            ),
        ]
        project = rng.choice(PROJECTS)
        situation = (
            f"Die ArchivTech GmbH plant {project}. Die Einführung kostet **{de(investment)} €**. "
            "Danach spart "
            f"das Team **{hours} Stunden pro Monat** zu je **{rate} €**; für Wartung und Lizenzen kommen "
            f"**{de(running)} € pro Monat** hinzu."
        )
        question = "Berechne den monatlichen Rückfluss und die Amortisationsdauer."
        hints = [
            "Rückfluss = eingesparte Kosten − neue laufende Kosten.",
            "Amortisationsdauer = Investition ÷ Rückfluss pro Monat.",
            f"Eingesparte Arbeit: {hours} h × {rate} €/h.",
        ]
        return steps, "Rückfluss und Amortisation", question, situation, hints

    def _break_even(self, rng: random.Random) -> _Parts:
        name_a, name_b, unit, words = rng.choice(SCENARIOS)
        var_a = rng.choice([2, 4, 5, 8, 10, 12, 15])
        diff = rng.choice([10, 15, 20, 25, 30, 40, 50])
        var_b = var_a + diff
        point = rng.choice(range(10, 201, 5))
        fix_a = point * diff
        need = rng.choice([q for q in range(5, 401, 5) if q != point])
        cost_a = fix_a + var_a * need
        cost_b = var_b * need
        steps = [
            number_step(
                "Break-even-Menge",
                break_even(fix_a, var_a, var_b),
                f"{de(fix_a)} + {var_a}x = {var_b}x → {de(fix_a)} = {diff}x → x = {point}.",
                None,
                [
                    (
                        Fraction(fix_a, var_b),
                        "Die variablen Kosten von A fehlen: beide Kostenfunktionen vollständig gleichsetzen.",
                        "konzept",
                    )
                ],
            ),
            number_step(
                f"Kosten „{name_a}“ bei {need} {unit} in €",
                cost_a,
                f"{de(fix_a)} + {var_a} × {need} = {de(cost_a)} €.",
                "€",
            ),
            number_step(
                f"Kosten „{name_b}“ bei {need} {unit} in €",
                cost_b,
                f"{var_b} × {need} = {de(cost_b)} €.",
                "€",
            ),
        ]
        question = (
            f"Vergleiche zwei Lösungen pro Jahr: **{name_a}** mit **{de(fix_a)} €** Fixkosten plus "
            f"**{var_a} €** "
            f"je {words}, oder **{name_b}** mit **{var_b} €** je {words}. Ab welcher Menge ist "
            f"„{name_a}“ günstiger (Break-even)? Was kosten beide bei **{need} {unit}**?"
        )
        hints = [
            "Break-even: beide Kostenfunktionen gleichsetzen und nach der Menge auflösen.",
            f"K_A = {de(fix_a)} + {var_a}x und K_B = {var_b}x.",
            f"{de(fix_a)} + {var_a}x = {var_b}x → {de(fix_a)} = {diff}x.",
        ]
        return steps, "Break-even zweier Lösungen", question, None, hints

    def _nas_or_cloud(self, rng: random.Random) -> _Parts:
        years = rng.choice([3, 4, 5])
        maintenance = rng.choice([200, 300, 400, 500, 600])
        var_a = rng.choice([5, 8, 10, 12])
        diff = rng.choice([20, 25, 30, 40, 50])
        var_b = var_a + diff
        # Break-even ab 40 TB: fixe Kosten ≥ 800 €, die Anschaffung bleibt also immer positiv
        point = rng.choice(range(40, 121, 5))
        fix_per_year = point * diff
        purchase = (fix_per_year - maintenance) * years
        need = rng.choice([q for q in range(10, 201, 10) if q != point])
        cost_a = fix_per_year + var_a * need
        cost_b = var_b * need
        steps = [
            number_step(
                "Fixe Kosten des NAS pro Jahr in €",
                fix_per_year,
                f"Abschreibung {de(purchase)} € ÷ {years} Jahre = {de(purchase // years)} € + Wartung "
                f"{de(maintenance)} € = {de(fix_per_year)} €.",
                "€",
                [
                    (
                        purchase + maintenance,
                        "Die Anschaffung wird auf die Nutzungsdauer verteilt (Abschreibung), nicht "
                        "in einem Jahr gezählt.",
                        "konzept",
                    ),
                    (
                        Fraction(purchase, years),
                        "Die Wartung gehört auch zu den fixen Kosten.",
                        "rechenfehler",
                    ),
                ],
            ),
            number_step(
                "Break-even in TB",
                break_even(fix_per_year, var_a, var_b),
                f"{de(fix_per_year)} + {var_a}x = {var_b}x → x = {de(fix_per_year)} ÷ {diff} = "
                f"{de(break_even(fix_per_year, var_a, var_b))} TB.",
                "TB",
            ),
            number_step(
                f"Kosten NAS bei {need} TB in €",
                cost_a,
                f"{de(fix_per_year)} + {var_a} × {need} = {de(cost_a)} €.",
                "€",
            ),
            number_step(
                f"Kosten Cloud bei {need} TB in €", cost_b, f"{var_b} × {need} = {de(cost_b)} €.", "€"
            ),
            number_step(
                "Ersparnis der günstigeren Lösung pro Jahr in €",
                abs(cost_a - cost_b),
                f"|{de(cost_a)} − {de(cost_b)}| = {de(abs(cost_a - cost_b))} € zugunsten "
                f"{'des NAS' if cost_a < cost_b else 'der Cloud'}.",
                "€",
            ),
        ]
        situation = (
            "Die ArchivTech GmbH braucht Speicher für das Archiv. **NAS:** Anschaffung "
            f"**{de(purchase)} €**, "
            f"Nutzungsdauer **{years} Jahre**, Wartung **{de(maintenance)} € pro Jahr**, dazu "
            f"**{var_a} €** je TB "
            f"und Jahr für Strom und Platten. **Cloud:** **{var_b} €** je TB und Jahr. Geplant sind "
            f"**{need} TB**."
        )
        question = "Ab wie vielen TB lohnt sich das NAS, und welche Lösung ist beim geplanten Bedarf "
        "um wie viel günstiger?"
        hints = [
            "Erst die fixen Kosten pro Jahr bestimmen: Anschaffung auf die Nutzungsdauer verteilen, "
            "Wartung dazu.",
            "Dann Break-even: K_NAS = fix + var · x, K_Cloud = var · x gleichsetzen.",
            f"Abschreibung pro Jahr = {de(purchase)} € ÷ {years}.",
        ]
        return steps, "NAS oder Cloud?", question, situation, hints
