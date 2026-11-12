---
id: wirtschaftlichkeit
titel: "Machbarkeit und Wirtschaftlichkeit: Amortisation und Kostenvergleich"
themen: [wirtschaftlichkeit]
reihenfolge: 1
voraussetzungen: [kalkulation]
dauer_min: 35
quelle: "Neu erstellt (Claude). Statische Investitionsrechnung (Amortisations- und Kostenvergleichsrechnung) nach betriebswirtschaftlicher Standardliteratur; alle Zahlen fiktiv und nachgerechnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 01.02: Machbarkeit von Projekten beurteilen, Wirtschaftlichkeit (z. B. Amortisation) (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "Statische Investitionsrechnung (Kostenvergleich, Amortisation): Standardinhalt der kaufmännischen Ausbildung, Rahmenlehrplan IT-Berufe LF 2"}
status: geprüft
---

## Worum geht es?

Bevor ein Projekt startet, stellt die Geschäftsleitung zwei Fragen:

1. **Machbarkeit:** Können wir das überhaupt?
2. **Wirtschaftlichkeit:** Lohnt es sich?

Für die zweite Frage gibt es zwei einfache Rechnungen: die **[Amortisationsrechnung](glossar:amortisation)**
und den **Kostenvergleich** mit Break-even.

## Wie funktioniert es?

### Machbarkeit aus fünf Blickwinkeln

| Blickwinkel | Frage | Beispiel Archiv-Automatisierung |
| --- | --- | --- |
| technisch | Gibt es die Technik, passt sie zu uns? | Schnittstelle zum Archiv vorhanden |
| wirtschaftlich | Rechnet es sich? | Amortisation in 24 Monaten |
| rechtlich | Dürfen wir das? | Aufbewahrungsfristen, DSGVO |
| personell | Haben wir die Leute und das Wissen? | Python-Kenntnisse im Team |
| zeitlich / organisatorisch | Passt es in den Zeitplan und die Abläufe? | vor dem Jahresabschluss fertig |

### Amortisation: Wann ist das Geld wieder drin?

**Amortisationsdauer = Investition ÷ jährlicher (oder monatlicher) Rückfluss**

Die ArchivTech will das manuelle Umlagern von Daten automatisieren:

| Posten | Betrag |
| --- | ---: |
| Investition (Software, Einrichtung) | 24.000 € |
| eingesparte Arbeit: 20 h/Monat × 60 €/h | 1.200 €/Monat |
| − neue laufende Kosten (Wartung) | 200 €/Monat |
| = Rückfluss | 1.000 €/Monat |

Amortisationsdauer = 24.000 € ÷ 1.000 €/Monat = **24 Monate**

Nach zwei Jahren hat sich die Automatisierung bezahlt gemacht; danach spart sie jeden Monat 1.000 €.

### Kostenvergleich mit Break-even

Speicher für das Archiv: eigenes **NAS** oder **Cloud-Speicher**?

| | NAS | Cloud |
| --- | ---: | ---: |
| fixe Kosten pro Jahr (Abschreibung 6.000 € über 3 Jahre) | 2.000 € | 0 € |
| variable Kosten pro TB und Jahr | 10 € | 60 € |

Kostenfunktionen (x = TB):

- NAS: K = 2.000 + 10 · x
- Cloud: K = 60 · x

**Break-even** – beide gleich teuer:

1. 2.000 + 10x = 60x
2. 2.000 = 50x
3. x = **40 TB**

Unter 40 TB ist die Cloud günstiger, darüber das NAS. Probe: 40 TB → NAS 2.400 €, Cloud 2.400 € ✔

### Welche Lösung wann?

| Bedarf | günstiger |
| --- | --- |
| 20 TB | Cloud: 1.200 € statt 2.200 € |
| 40 TB | gleich: je 2.400 € |
| 100 TB | NAS: 3.000 € statt 6.000 € |

> **Halten wir kurz fest:**
>
> 1. Machbarkeit: technisch, wirtschaftlich, rechtlich, personell, zeitlich.
> 2. Amortisation = Investition ÷ Rückfluss pro Zeiteinheit.
> 3. Break-even: Kostenfunktionen gleichsetzen und nach der Menge auflösen.

## Warum ist es so?

Geld lässt sich nur einmal ausgeben. Die Rechnungen machen Vorhaben **vergleichbar** – auch mit
ganz anderen Projekten, die um dasselbe Budget konkurrieren.

<details>
<summary>Warum heißen diese Rechnungen „statisch“?</summary>

Sie rechnen so, als wäre ein Euro heute genauso viel wert wie ein Euro in drei Jahren. Zinsen und
Inflation bleiben außen vor. Für kurze IT-Projekte reicht das meist; bei großen, langen Investitionen
nutzt man dynamische Verfahren, die genau diesen Unterschied einrechnen.

</details>

<details>
<summary>Warum zählen nicht nur die Kosten?</summary>

Qualitative Punkte entscheiden oft mit: Abhängigkeit von einem Anbieter, Datenschutz in der Cloud,
eigenes Know-how, Skalierbarkeit. Dafür eignet sich die **Nutzwertanalyse** aus dem Kapitel
Angebotsvergleich.

</details>

## Praxisbezug im Betrieb

- **Automatisierung begründen:** Eingesparte Stunden × Stundensatz ist das stärkste Argument für ein
  neues Skript oder eine Pipeline.
- **Cloud oder eigener Betrieb:** Mit dem Break-even lässt sich zeigen, ab welcher Datenmenge sich
  eigene Hardware lohnt.
- **Annahmen offenlegen:** Jede Rechnung steht und fällt mit den geschätzten Werten.

## Typische Prüfungsfalle

- **Laufende Kosten vergessen:** Der Rückfluss ist die **Einsparung minus neue Kosten**.
- **Einheiten gemischt:** Monatlicher Rückfluss ergibt Monate, jährlicher Jahre.
- **Fixe Kosten nicht pro Jahr:** Anschaffung auf die Nutzungsdauer verteilen (Abschreibung).
- **Ergebnis nicht gedeutet:** Sag dazu, welche Lösung wann günstiger ist.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Amortisationsdauer | Zeit, bis die Investition durch Rückflüsse gedeckt ist |
| Break-even | Menge, bei der zwei Alternativen gleich viel kosten |
| fixe Kosten | unabhängig von der Menge (Abschreibung, Miete) |
| variable Kosten | steigen mit der Menge (pro TB, pro Stunde) |
| Machbarkeit | Können wir es? |
| Wirtschaftlichkeit | Lohnt es sich? |

## Merksatz

**Erst prüfen, ob es geht, dann, ob es sich lohnt: Investition durch Rückfluss gibt die
Amortisation, gleichgesetzte Kosten geben den Break-even.**
