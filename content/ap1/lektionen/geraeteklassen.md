---
id: geraeteklassen
titel: "Geräteklassen auswählen: Auslastung, Erweiterbarkeit, Zukunftssicherheit"
themen: [geraeteklassen, auslastung-erweiterbarkeit]
reihenfolge: 1
voraussetzungen: []
dauer_min: 25
quelle: "Neu erstellt (Claude). Geräteklassen nach Katalogwortlaut; Auslastungsrechnung mit fiktiven Messwerten nachgerechnet; Reserve als Faustregel gekennzeichnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkte 04.02 (Geräteklassen, z. B. Desktops, Notebooks, All-in-One, Thin Clients, Tablets, Smartphones) und 03.04 (Auslastung, Erweiterbarkeit, Zukunftssicherheit) (laut Änderungsliste IT-Berufe-Podcast #190 bzw. katalog.yaml)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
status: ungeprüft
---

## Worum geht es?

„Welches Gerät empfehlen Sie für diesen Arbeitsplatz?“ ist eine typische Beratungsaufgabe. Die Antwort
hängt von der **Tätigkeit** ab – und davon, ob das Gerät auch in drei Jahren noch reicht.

- sechs Geräteklassen und ihr Einsatz
- **Auslastung** messen und Reserven planen
- **Erweiterbarkeit** und **Zukunftssicherheit** bewerten

## Wie funktioniert es?

### Geräteklassen

| Klasse | Stärken | Schwächen | typischer Einsatz |
| --- | --- | --- | --- |
| **Desktop-PC** | leistungsstark, erweiterbar, günstig je Leistung | nicht mobil | Entwicklung, CAD, feste Arbeitsplätze |
| **Notebook** | mobil, Akku | teurer, kaum erweiterbar | Außendienst, Homeoffice |
| **All-in-One** | platzsparend, wenige Kabel | Reparatur und Aufrüstung schwierig | Empfang, Besprechungsraum |
| **Thin Client** | günstig, sparsam, zentral verwaltet | braucht Server/VDI und Netz | Callcenter, Schulung, VDI |
| **Tablet** | Touch, leicht, lange Laufzeit | wenig Eingabe, eingeschränkte Software | Lager, Präsentation, Unterschriften |
| **Smartphone** | immer dabei, erreichbar | kleiner Bildschirm | Bereitschaft, 2FA, Kommunikation |

### Auslastung messen

Bevor du aufrüstest, miss die Auslastung über eine typische Arbeitswoche:

| Ressource | gemessen (Spitze) | vorhanden | Auslastung |
| --- | ---: | ---: | ---: |
| RAM | 14,2 GB | 16 GB | 14,2 ÷ 16 = **89 %** |
| CPU | 35 % | 8 Kerne | **35 %** |
| SSD | 410 GB | 512 GB | 410 ÷ 512 = **80 %** |

Ergebnis: Der **Arbeitsspeicher** ist der Engpass, nicht die CPU. Eine neue CPU brächte nichts.

Faustregel: Dauerhaft über **70–80 %** wird es eng; Reserve für Spitzen und Wachstum einplanen.

### Erweiterbarkeit prüfen

| Frage | Beispiel |
| --- | --- |
| Freie RAM-Steckplätze? | 2 von 4 belegt → auf 32 GB erweiterbar |
| RAM verlötet? | bei vielen Notebooks: nicht erweiterbar |
| Freie M.2- oder SATA-Plätze? | zweite SSD möglich |
| Freie PCIe-Steckplätze? | 10-Gbit-Netzwerkkarte nachrüsten |
| Netzteil-Reserve? | Grafikkarte nachrüstbar |

### Zukunftssicherheit

- **Laufzeit der Updates:** Wie lange liefert der Hersteller Sicherheitsupdates?
- **Aktuelle Schnittstellen:** USB-C, Wi-Fi 6/7, TPM 2.0 für aktuelle Betriebssysteme
- **Wachstum:** Datenmenge und Nutzerzahl in 3 Jahren
- **Ersatzteile und Garantie:** Verfügbarkeit, Vor-Ort-Service

> **Halten wir kurz fest:**
>
> 1. Gerät nach Tätigkeit wählen: stationär, mobil, zentral verwaltet.
> 2. Erst messen: Der Engpass bestimmt, was aufgerüstet wird.
> 3. Erweiterbarkeit (Steckplätze, verlötete Teile) und Update-Laufzeit gehören zur Bewertung.

## Warum ist es so?

Ein Gerät ist nur so schnell wie sein schwächster Teil. Wer die CPU tauscht, obwohl der RAM voll ist,
gibt Geld aus, ohne dass sich etwas verbessert.

<details>
<summary>Warum ein Thin Client, wenn ein PC doch mehr kann?</summary>

Der Thin Client zeigt nur an, gerechnet wird auf dem Server oder in der Cloud (VDI/DaaS). Er braucht
wenig Strom, hat keine lokalen Daten und ist in Minuten ausgetauscht. Für gleichförmige Arbeitsplätze
spart das Verwaltung, Energie und Sicherheitsrisiken.

</details>

## Praxisbezug im Betrieb

- **Monitoring** liefert die Auslastungswerte für Server – bei Clients helfen Task-Manager oder `top`.
- **Hardwarestandard** pro Arbeitsplatztyp (Büro, Entwicklung, mobil) vereinfacht Einkauf und Support.
- **Reserve einplanen:** Lieber einmal 32 GB RAM als nach einem Jahr nachrüsten.

## Typische Prüfungsfalle

- **Gerät ohne Begründung:** Immer mit der Tätigkeit begründen.
- **Falsche Komponente aufgerüstet:** Erst den Engpass bestimmen.
- **Notebook als erweiterbar:** RAM und SSD sind oft verlötet.
- **Thin Client ohne Server:** Er braucht eine zentrale Infrastruktur.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Thin Client | schlankes Endgerät, Rechenleistung zentral |
| Fat Client | vollwertiger PC mit lokalen Programmen |
| All-in-One | Rechner im Monitor eingebaut |
| Auslastung | Anteil der genutzten Kapazität |
| Erweiterbarkeit | Möglichkeit, Komponenten nachzurüsten |

## Merksatz

**Erst fragen, was getan wird, dann messen, wo es klemmt – und nur kaufen, was sich später noch
erweitern und aktualisieren lässt.**
