---
id: hdd-ssd
titel: "HDD und SSD: Aufbau, Kenngrößen und Einsatz"
themen: [speicher-hdd-ssd]
reihenfolge: 1
voraussetzungen: []
dauer_min: 30
quelle: "Neu erstellt (Claude). Funktionsweise nach Herstellerdokumentation und Fachliteratur; Löschen nach BSI-Empfehlung; Rechnungen (Rotationslatenz, TBW) nachgerechnet; typische Werte als Größenordnungen gekennzeichnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 03.03: Datenspeicher (SSD/HDD); HDD und SSD werden namentlich aufgeführt, Vor- und Nachteile kennen (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "BSI, Cyber-Sicherheitsempfehlungen für Verbraucher: Daten endgültig löschen (bei SSDs reicht Überschreiben nicht zuverlässig)"}
status: ungeprüft
---

## Worum geht es?

Ob Notebook, Server oder Archiv: Daten landen entweder auf einer **HDD** (Festplatte mit drehenden
Scheiben) oder einer **[SSD](glossar:ssd)** (Flash-Speicher ohne bewegliche Teile). Der Katalog 2025
nennt beide ausdrücklich – du sollst sie **unterscheiden** und **begründet auswählen** können.

## Wie funktioniert es?

### Aufbau im Vergleich

| | HDD | SSD |
| --- | --- | --- |
| Speichermedium | magnetisch beschichtete Scheiben (Platter) | NAND-Flash-Zellen |
| Lesen/Schreiben | Schreib-Lese-Kopf fährt zur Spur, Scheibe dreht | Controller adressiert Zellen elektronisch |
| bewegliche Teile | ja: Motor, Kopfarm | nein |
| Formfaktor | 3,5" (Desktop/Server), 2,5" | 2,5", M.2, U.2 |
| Schnittstelle | SATA, SAS | SATA, NVMe über PCIe |

### Kenngrößen

| Kenngröße | Bedeutung | HDD (Größenordnung) | SSD (Größenordnung) |
| --- | --- | --- | --- |
| Kapazität | Speicherplatz | bis über 20 TB | bis mehrere TB, teurer je TB |
| Zugriffszeit | Zeit bis zum ersten Byte | einige Millisekunden | unter 0,1 ms |
| Datenrate | MB/s beim Lesen am Stück | ca. 150–280 MB/s | SATA bis ca. 550 MB/s, NVMe mehrere GB/s |
| IOPS | Zugriffe pro Sekunde | wenige Hundert | Zehntausende und mehr |
| Haltbarkeit | | Mechanik verschleißt | begrenzte Schreibzyklen (TBW) |

### Rechenbeispiel: Warum HDDs langsam beim Zugriff sind

Eine HDD mit **7.200 Umdrehungen pro Minute**. Im Mittel muss die Scheibe eine **halbe** Umdrehung
drehen, bis der gesuchte Sektor unter dem Kopf ist:

1. Umdrehungen pro Sekunde: 7.200 ÷ 60 = **120**
2. Zeit für eine Umdrehung: 1 ÷ 120 s = **8,33 ms**
3. mittlere Wartezeit: 8,33 ÷ 2 = **4,17 ms**

Dazu kommt noch die Zeit, bis der Kopf die Spur erreicht. Eine SSD braucht für den Zugriff nur
Bruchteile einer Millisekunde.

### Haltbarkeit einer SSD: TBW

Hersteller geben an, wie viele **Terabytes geschrieben** (TBW) eine SSD aushält. Beispiel: 600 TBW,
täglich 100 GB geschrieben:

600.000 GB ÷ 100 GB/Tag = 6.000 Tage ≈ **16,4 Jahre**

### Wann verwende ich was?

| Einsatz | Wahl | Grund |
| --- | --- | --- |
| Betriebssystem, Notebook | SSD | schneller Start, stoßfest, leise, sparsam |
| Datenbank, virtuelle Maschinen | SSD (NVMe) | viele kleine Zugriffe (IOPS) |
| große Archive, Backups | HDD (oder Band) | günstig pro TB |
| NAS für Dateifreigaben | HDD, oft mit SSD-Cache | Kapazität und Preis |

> **Halten wir kurz fest:**
>
> 1. HDD = Mechanik, günstig und groß; SSD = Flash, schnell, stoßfest, teurer je TB.
> 2. Mittlere Rotationswartezeit = halbe Umdrehungszeit (7.200 U/min → 4,17 ms).
> 3. SSD-Lebensdauer über TBW abschätzen.

## Warum ist es so?

Bei der HDD muss sich physisch etwas bewegen – das dauert Millisekunden. Die SSD schaltet nur Strom
in Zellen: Dafür reichen Mikrosekunden. Die Mechanik macht die HDD dafür einfach und günstig zu bauen.

<details>
<summary>Warum reicht Überschreiben bei SSDs zum Löschen nicht?</summary>

Der SSD-Controller verteilt Schreibzugriffe gleichmäßig auf alle Zellen (Wear Leveling). Überschreibst
du eine Datei, landen die neuen Daten oft in **anderen** Zellen – die alten bleiben unsichtbar
erhalten. Sicher sind die Löschfunktion des Herstellers (Secure Erase), durchgehende Verschlüsselung
mit Schlüsselvernichtung oder die physische Zerstörung.

</details>

## Praxisbezug im Betrieb

- **Archivspeicher** kombiniert oft schnelle SSDs für aktuelle Daten und HDDs oder Band für Altes.
- **SMART-Werte** (Self-Monitoring) überwachen: `smartctl -a /dev/sda` zeigt Fehler und Verschleiß.
- **Ausgemusterte Datenträger** datenschutzgerecht vernichten und dokumentieren.

## Typische Prüfungsfalle

- **SSD = immer besser:** Für große Archive ist die HDD pro TB deutlich günstiger.
- **Datenrate und IOPS verwechselt:** IOPS = Anzahl Zugriffe, Datenrate = Menge pro Sekunde.
- **Ganze statt halbe Umdrehung:** Die mittlere Wartezeit ist die **halbe** Umdrehung.
- **SSD wie HDD überschrieben:** Löschen braucht andere Verfahren.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| HDD | magnetische Festplatte mit drehenden Scheiben |
| SSD | Flash-Speicher ohne bewegliche Teile |
| NVMe | schnelles Protokoll für SSDs über PCIe |
| M.2 | Formfaktor (Steckplatz), nicht automatisch NVMe |
| IOPS | Ein-/Ausgabe-Operationen pro Sekunde |
| TBW | Terabytes Written, garantierte Schreibmenge |

## Merksatz

**Die HDD dreht und wartet, die SSD schaltet und liefert. Für viel Platz die HDD, für viel Tempo die
SSD – und gelöscht wird eine SSD nicht durch Überschreiben.**
