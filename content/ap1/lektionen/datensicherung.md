---
id: datensicherung
titel: "Datensicherung: voll, inkrementell, differenziell und die 3-2-1-Regel"
themen: [verfuegbarkeit-backup]
reihenfolge: 1
voraussetzungen: []
dauer_min: 35
quelle: "Neu erstellt (Claude). Sicherungsarten und Generationenprinzip nach BSI IT-Grundschutz-Kompendium, Baustein CON.3 Datensicherungskonzept; 3-2-1-Regel als verbreitete Praxisregel; Rechenbeispiel nachgerechnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 06.04: Sicherung der Verfügbarkeit, z. B. NAS; RAID und SAN entfallen (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "BSI IT-Grundschutz-Kompendium, Baustein CON.3 Datensicherungskonzept"}
status: geprüft
---

## Worum geht es?

Festplatten fallen aus, Ransomware verschlüsselt, Menschen löschen aus Versehen. Gegen all das hilft
nur eine **[Datensicherung](glossar:datensicherung)** (Backup) – wenn sie richtig geplant ist.

- drei Sicherungsarten und ihr Speicher- und Wiederherstellungsaufwand
- die **3-2-1-Regel** und das **Generationenprinzip**
- Abgrenzung: Backup, Archiv, Spiegelung

## Wie funktioniert es?

### Drei Sicherungsarten

| Art | sichert … | Sicherung | Wiederherstellung |
| --- | --- | --- | --- |
| **Vollsicherung** | alles | langsam, viel Speicher | schnell: 1 Satz |
| **inkrementell** | Änderungen seit der **letzten Sicherung** (egal welcher) | schnell, wenig Speicher | langsam: Voll + **alle** Inkremente |
| **differenziell** | Änderungen seit der **letzten Vollsicherung** | wächst täglich | mittel: Voll + **letzte** Differenz |

### Rechenbeispiel: eine Woche Archivserver

Sonntag Vollsicherung **500 GB**. Montag bis Samstag kommen jeden Tag **20 GB** neue Daten dazu.

| Tag | inkrementell | differenziell |
| --- | ---: | ---: |
| So (voll) | 500 GB | 500 GB |
| Mo | 20 GB | 20 GB |
| Di | 20 GB | 40 GB |
| Mi | 20 GB | 60 GB |
| Do | 20 GB | 80 GB |
| Fr | 20 GB | 100 GB |
| Sa | 20 GB | 120 GB |
| **Summe** | **620 GB** | **920 GB** |

Am Freitagabend geht der Server kaputt. Was brauche ich zum Wiederherstellen?

- **inkrementell:** Voll (So) + Mo + Di + Mi + Do + Fr = **6 Sicherungen**
- **differenziell:** Voll (So) + Fr = **2 Sicherungen**

Inkrementell spart Speicher, differenziell spart Zeit beim Wiederherstellen.

### Die 3-2-1-Regel

- **3** Kopien der Daten (Original + 2 Sicherungen)
- auf **2** verschiedenen Medien (z. B. NAS und Band oder Cloud)
- davon **1** an einem anderen Ort (außer Haus)

Viele ergänzen heute: eine Kopie **offline oder unveränderbar** (immutable), damit Ransomware sie
nicht verschlüsseln kann.

### Das Generationenprinzip

Damit man auch ältere Stände zurückholen kann, werden Sicherungen nach dem
**Großvater-Vater-Sohn-Prinzip** aufbewahrt:

| Generation | Rhythmus | Beispiel Aufbewahrung |
| --- | --- | --- |
| Sohn | täglich | 1 Woche |
| Vater | wöchentlich | 1 Monat |
| Großvater | monatlich | 1 Jahr |

So bleibt eine Datei, die vor drei Wochen beschädigt wurde, wiederherstellbar.

> **Halten wir kurz fest:**
>
> 1. Inkrementell = seit letzter Sicherung, differenziell = seit letzter Vollsicherung.
> 2. 3 Kopien, 2 Medien, 1 außer Haus – plus eine offline.
> 3. Generationen: Sohn täglich, Vater wöchentlich, Großvater monatlich.

## Warum ist es so?

Eine Sicherung, die beim Wiederherstellen nicht funktioniert, ist keine. Deshalb geht es nicht nur
ums Sichern, sondern vor allem ums **Zurückholen** – schnell und vollständig.

<details>
<summary>Warum ist eine Spiegelung kein Backup?</summary>

Eine Spiegelung (z. B. zweite Festplatte, die alles sofort mitschreibt) schützt vor dem Ausfall
einer Platte. Löscht aber jemand eine Datei oder verschlüsselt Ransomware alles, passiert das auf
beiden Seiten gleichzeitig. Ein Backup ist ein **älterer** Stand, getrennt vom Original.

</details>

<details>
<summary>Und was ist der Unterschied zum Archiv?</summary>

Ein Backup ist eine **Kopie** für die Wiederherstellung und wird nach einiger Zeit überschrieben. Ein
Archiv ist der **langfristige, oft einzige** Aufbewahrungsort von Daten, die aus dem Alltag
herausgenommen werden – etwa für gesetzliche Fristen. Auch ein Archiv braucht deshalb ein Backup.

</details>

## Praxisbezug im Betrieb

- **Restore testen:** Regelmäßig eine Sicherung probeweise zurückspielen – erst dann weißt du, dass
  sie funktioniert.
- **Sicherungsfenster:** Mit der Formel aus „Übertragungszeit“ prüfen, ob die Nacht reicht.
- **NAS als Sicherungsziel:** praktisch, aber nicht der einzige Ort – sonst verletzt es die
  3-2-1-Regel.

## Typische Prüfungsfalle

- **Inkrementell und differenziell vertauscht:** inkrementell = seit **letzter** Sicherung.
- **Wiederherstellung inkrementell nur mit letztem Inkrement:** Es braucht **alle** seit der
  Vollsicherung.
- **RAID als Backup:** RAID ist seit 2025 nicht mehr AP1-Stoff – und ersetzt ohnehin keine Sicherung.
- **Backup im selben Raum:** Bei Brand oder Wasser ist alles weg.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Vollsicherung | alle Daten |
| inkrementelle Sicherung | Änderungen seit der letzten Sicherung jeder Art |
| differenzielle Sicherung | Änderungen seit der letzten Vollsicherung |
| Spiegelung | gleichzeitige Kopie, schützt vor Hardwareausfall, nicht vor Löschen |
| Archiv | langfristige Aufbewahrung von Daten außerhalb des Alltagsbetriebs |

## Merksatz

**Inkrementell spart Speicher, differenziell spart Zeit beim Zurückholen. Drei Kopien, zwei Medien,
eine außer Haus – und nur ein getesteter Restore ist ein echtes Backup.**
