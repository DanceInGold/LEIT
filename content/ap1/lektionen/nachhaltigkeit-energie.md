---
id: nachhaltigkeit-energie
titel: "Nachhaltige IT: Energieverbrauch, Stromkosten, Recycling"
themen: [nachhaltigkeit-energie]
reihenfolge: 1
voraussetzungen: []
dauer_min: 25
quelle: "Neu erstellt (Claude). Energierechnung E = P × t; Kennzahl PUE nach The Green Grid; Entsorgung nach ElektroG und Richtlinie 2012/19/EU (WEEE); Strompreis als Annahme; alle Zahlen nachgerechnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkte 03.01/07.02: Nutzungsdauer, Energieverbrauch, Recyclingfähigkeit (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "Richtlinie 2012/19/EU über Elektro- und Elektronik-Altgeräte (WEEE)", url: "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32012L0019"}
  - {titel: "Elektro- und Elektronikgerätegesetz (ElektroG)", url: "https://www.gesetze-im-internet.de/elektrog_2015/"}
status: ungeprüft
---

## Worum geht es?

IT verbraucht Strom, Rohstoffe und erzeugt Elektroschrott. Nachhaltige IT spart dabei oft auch Geld.
Die Prüfung fragt typischerweise:

- **Stromkosten berechnen** und Geräte vergleichen
- **ökologische Kriterien** bei der Beschaffung nennen
- **richtig entsorgen**

## Wie funktioniert es?

### Stromkosten berechnen

**Energie (kWh) = Leistung (kW) × Zeit (h)**, **Kosten = Energie × Preis pro kWh**

Beispiel: Ein Archivserver nimmt **400 W** auf und läuft **rund um die Uhr**, Strompreis **0,30 €/kWh**.

1. Leistung: 400 W = **0,4 kW**
2. Zeit: 365 × 24 = **8.760 h**
3. Energie: 0,4 × 8.760 = **3.504 kWh**
4. Kosten: 3.504 × 0,30 = **1.051,20 € pro Jahr**

### Rechenbeispiel: PC oder Thin Client?

50 Arbeitsplätze, je **220 Tage × 8 h = 1.760 h** im Jahr:

| | Leistung | Energie je Platz | Kosten je Platz |
| --- | ---: | ---: | ---: |
| PC | 80 W | 0,08 × 1.760 = 140,8 kWh | 42,24 € |
| Thin Client | 15 W | 0,015 × 1.760 = 26,4 kWh | 7,92 € |

Ersparnis: 34,32 € je Platz, bei 50 Plätzen **1.716 € pro Jahr** – abzüglich des Stroms für die Server,
auf denen die Desktops laufen.

### Ökologische Kriterien bei der Beschaffung

| Kriterium | Beispiel |
| --- | --- |
| Energieverbrauch im Betrieb und Standby | Datenblatt, Effizienz des Netzteils (80 PLUS) |
| Nutzungsdauer | lange Updates, Reparierbarkeit, Ersatzteile |
| Recyclingfähigkeit | Materialien, modularer Aufbau |
| Umweltzeichen | Blauer Engel, TCO Certified, EPEAT, Energy Star |
| Verpackung und Transport | Mehrweg, Sammellieferung |
| Gebrauchtgeräte | aufbereitete Geräte (Refurbished) |

### Im Rechenzentrum: PUE

**PUE** (Power Usage Effectiveness) = Gesamtenergie des Rechenzentrums ÷ Energie der IT-Geräte.

Beispiel: 150 kW gesamt, 100 kW für die IT → PUE = **1,5**. Jedes Watt IT braucht 0,5 W zusätzlich für
Kühlung, USV-Verluste, Licht. Ideal wäre 1,0.

### Entsorgung

- Elektroaltgeräte gehören **nicht in den Hausmüll** (ElektroG, WEEE-Richtlinie).
- Rücknahme über Hersteller, Händler oder zertifizierte Entsorger.
- **Vorher Daten sicher löschen** oder Datenträger zertifiziert vernichten – mit Nachweis.

> **Halten wir kurz fest:**
>
> 1. kWh = kW × h, Kosten = kWh × Preis; ein Jahr hat 8.760 h.
> 2. Beschaffung: Verbrauch, Nutzungsdauer, Reparierbarkeit, Umweltzeichen.
> 3. Entsorgung über zertifizierte Wege, vorher Daten vernichten.

## Warum ist es so?

Der größte Teil der Umweltbelastung vieler Geräte entsteht schon bei der **Herstellung**. Wer ein Gerät
länger nutzt, spart deshalb oft mehr als mit einem etwas sparsameren Neugerät.

<details>
<summary>Warum lohnt sich ein sparsames Netzteil im Server so stark?</summary>

Ein Server läuft 8.760 Stunden im Jahr. Jedes eingesparte Watt spart 8,76 kWh – im Rechenzentrum mit
PUE 1,5 sogar 13,14 kWh, weil auch weniger gekühlt werden muss. Über Jahre und viele Server summiert
sich das erheblich.

</details>

## Praxisbezug im Betrieb

- **Virtualisierung und Konsolidierung:** weniger, besser ausgelastete Server sparen Strom.
- **Energiesparrichtlinien** für Clients: Standby nach Inaktivität, Monitore aus.
- **Altgeräte-Prozess:** Inventar, Datenlöschung mit Protokoll, Entsorgungsnachweis.

## Typische Prüfungsfalle

- **Watt nicht in Kilowatt umgerechnet:** 400 W = 0,4 kW.
- **Jahresstunden falsch:** 365 × 24 = 8.760 h, Arbeitstage nur bei Bürogeräten.
- **Nur Strom betrachtet:** Herstellung, Nutzungsdauer und Entsorgung gehören dazu.
- **Datenträger einfach entsorgt:** Datenschutzverstoß.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Leistung (W) | Momentanverbrauch |
| Energie (kWh) | Leistung über die Zeit |
| PUE | Effizienz eines Rechenzentrums, ideal 1,0 |
| Refurbished | aufbereitetes Gebrauchtgerät |
| WEEE / ElektroG | Regeln für Elektroaltgeräte |

## Merksatz

**Kilowatt mal Stunden mal Preis – und das grünste Gerät ist oft das, das man länger benutzt.**
