---
id: netzwerk-standards
titel: "Ethernet, Glasfaser und WLAN: Standards und Kenngrößen"
themen: [netzwerk-standards]
reihenfolge: 1
voraussetzungen: []
dauer_min: 30
quelle: "Neu erstellt (Claude). Ethernet nach IEEE 802.3, WLAN nach IEEE 802.11 und Wi-Fi-Alliance-Bezeichnungen; Datenraten als theoretische Bruttowerte gekennzeichnet; Rechnung nachgerechnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 03.03: LWL, Ethernet-Standards, WLAN-Standards (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "IEEE 802.3 Ethernet Working Group", url: "https://www.ieee802.org/3/"}
  - {titel: "IEEE 802.11 Wireless LAN Working Group", url: "https://www.ieee802.org/11/"}
  - {titel: "Wi-Fi Alliance: Wi-Fi 6, Wi-Fi 6E, Wi-Fi 7", url: "https://www.wi-fi.org/discover-wi-fi"}
status: geprüft
---

## Worum geht es?

Kabel, Glasfaser oder Funk – jede Technik hat eigene Standards mit Namen wie **1000BASE-T** oder
**Wi-Fi 6**. In der Prüfung musst du sie **zuordnen** und **begründet auswählen**.

## Wie funktioniert es?

### Ethernet über Kupfer (IEEE 802.3)

| Standard | Datenrate | Kabel (mindestens) | max. Länge |
| --- | ---: | --- | ---: |
| 100BASE-TX (Fast Ethernet) | 100 Mbit/s | Cat 5 | 100 m |
| 1000BASE-T (Gigabit) | 1 Gbit/s | Cat 5e | 100 m |
| 10GBASE-T | 10 Gbit/s | Cat 6A (Cat 6 nur bis ca. 55 m) | 100 m |

So liest du den Namen: **Datenrate** (1000 = 1.000 Mbit/s) – **BASE** = Basisband – **T** = Twisted
Pair (verdrilltes Kupferkabel).

### Glasfaser (LWL)

| | Multimode | Singlemode |
| --- | --- | --- |
| Kerndurchmesser | 50 µm (oder 62,5 µm) | ca. 9 µm |
| Reichweite | bis einige Hundert Meter | viele Kilometer |
| Einsatz | im Gebäude, Rechenzentrum | zwischen Gebäuden, Standorten |
| Kosten | günstigere Optik | teurere Optik |

Vorteile von LWL gegenüber Kupfer: **große Reichweite**, **hohe Datenraten**, **unempfindlich gegen
elektromagnetische Störungen**, **kein Potentialausgleich nötig** zwischen Gebäuden, schwer abzuhören.

### WLAN (IEEE 802.11)

| IEEE | Wi-Fi-Name | Frequenzbänder | max. Bruttorate (theoretisch) |
| --- | --- | --- | ---: |
| 802.11n | Wi-Fi 4 | 2,4 und 5 GHz | 600 Mbit/s |
| 802.11ac | Wi-Fi 5 | 5 GHz | ca. 6,9 Gbit/s |
| 802.11ax | Wi-Fi 6 / 6E | 2,4 und 5 GHz / zusätzlich 6 GHz | ca. 9,6 Gbit/s |
| 802.11be | Wi-Fi 7 | 2,4, 5 und 6 GHz | ca. 46 Gbit/s |

Die Maximalwerte gelten nur unter Idealbedingungen mit vielen Antennen. Praktisch erreicht ein
einzelnes Gerät meist einen Bruchteil, und alle Geräte an einem Accesspoint **teilen** sich die Rate.

### 2,4 GHz oder 5/6 GHz?

| | 2,4 GHz | 5 GHz / 6 GHz |
| --- | --- | --- |
| Reichweite, Wände | besser | schlechter |
| Datenrate | geringer | höher |
| Störungen | viele (Nachbarnetze, Bluetooth) | weniger, mehr Kanäle |

### Rechenbeispiel: Reicht Gigabit für das Backup?

Ein Archivserver soll nachts **2 TB** sichern, über **1 Gbit/s**:

1. 2 × 10¹² Byte × 8 = 1,6 × 10¹³ Bit
2. ÷ 10⁹ bit/s = 16.000 s ≈ **4,4 Stunden**

Bei einem Zeitfenster von 4 Stunden reicht das nicht – 10GBASE-T oder LWL mit 10 Gbit/s schaffen es
in etwa 27 Minuten.

> **Halten wir kurz fest:**
>
> 1. Kupfer: bis 100 m; Gigabit ab Cat 5e, 10 Gigabit mit Cat 6A.
> 2. LWL: Multimode im Gebäude, Singlemode über Kilometer; störfest.
> 3. WLAN: Wi-Fi 4/5/6/7 = 802.11n/ac/ax/be; 2,4 GHz weit, 5/6 GHz schnell.

## Warum ist es so?

Elektrische Signale werden im Kupfer mit der Länge schwächer und anfälliger für Störungen – deshalb
die 100-m-Grenze. Licht in der Glasfaser verliert viel weniger und wird nicht von Stromleitungen
gestört.

<details>
<summary>Warum ist WLAN langsamer als die Zahl auf der Verpackung?</summary>

Funk ist ein **geteiltes Medium**: Immer nur ein Gerät sendet zur selben Zeit auf einem Kanal. Dazu
kommen Protokoll-Overhead, Abstand, Wände und Nachbarnetze. Die Angabe auf der Verpackung ist die
Summe aller Antennen unter Laborbedingungen.

</details>

## Praxisbezug im Betrieb

- **Server und Speicher** per Kabel oder LWL anbinden, nie per WLAN.
- **Zwischen Gebäuden** LWL verlegen: keine Probleme mit unterschiedlichem Erdpotential.
- **WLAN-Planung:** Accesspoints so verteilen, dass sich nicht zu viele Geräte einen teilen.

## Typische Prüfungsfalle

- **Cat 5 für Gigabit:** Mindestens Cat 5e.
- **WLAN-Bruttorate als Nutzrate:** Real deutlich weniger.
- **Multimode für 5 km:** Dafür braucht es Singlemode.
- **Wi-Fi-Namen und IEEE-Bezeichnung vertauscht:** Wi-Fi 6 = 802.11ax.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| 1000BASE-T | Gigabit-Ethernet über Kupfer |
| Cat 5e / 6A | Kabelkategorien mit steigender Übertragungsqualität |
| Multimode | LWL für kurze Strecken |
| Singlemode | LWL für lange Strecken |
| Wi-Fi 6E | Wi-Fi 6 zusätzlich im 6-GHz-Band |
| Bruttorate | theoretische Rate inkl. Overhead |

## Merksatz

**Kupfer bis hundert Meter, Glas für alles Weitere. Wi-Fi 4-5-6-7 heißt n-ac-ax-be – und WLAN teilen
sich alle.**
