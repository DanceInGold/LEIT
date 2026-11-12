---
id: urheberrecht-lizenzen
titel: "Urheberrecht und Softwarelizenzen"
themen: [urheberrecht-lizenzen]
reihenfolge: 1
voraussetzungen: []
dauer_min: 30
quelle: "Neu erstellt (Claude). Nach Urheberrechtsgesetz (§§ 2, 7, 64, 69a, 69c, 69d UrhG); Open-Source-Lizenzen nach Open Source Initiative und Free Software Foundation; Lizenzbeispiel fiktiv und nachgerechnet. Keine Rechtsberatung."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 04.04: Grundlagen des Schutzes der Urheber, Lizenzen – Themenzuordnung siehe content/ap1/katalog.yaml"}
  - {titel: "Urheberrechtsgesetz (UrhG), insbesondere § 64 (70 Jahre nach dem Tod) und §§ 69a ff. (Computerprogramme)", url: "https://www.gesetze-im-internet.de/urhg/"}
  - {titel: "Open Source Initiative: Licenses", url: "https://opensource.org/licenses"}
  - {titel: "GNU General Public License v3", url: "https://www.gnu.org/licenses/gpl-3.0.html"}
status: ungeprüft
---

## Worum geht es?

Software, Texte, Bilder und Fotos sind **geschützte Werke**. Wer sie nutzt, braucht eine Erlaubnis –
eine **[Lizenz](glossar:lizenz)**. Für die IT heißt das: Jede installierte Software muss richtig
lizenziert sein, und Bilder aus dem Internet darf man nicht einfach übernehmen.

## Wie funktioniert es?

### Grundlagen des Urheberrechts

| Regel | Inhalt |
| --- | --- |
| Was ist geschützt? | persönliche geistige Schöpfungen: Texte, Bilder, Musik, **Computerprogramme** (§ 2, § 69a UrhG) |
| Wer ist Urheber? | der Schöpfer des Werks (§ 7) |
| Wie entsteht der Schutz? | automatisch mit der Schöpfung, ohne Anmeldung |
| Wie lange? | bis **70 Jahre nach dem Tod** des Urhebers (§ 64) |
| Was darf der Urheber? | über Vervielfältigung, Verbreitung, Bearbeitung entscheiden |

Bei Software, die Angestellte im Job programmieren, liegen die wirtschaftlichen Nutzungsrechte in der
Regel beim **Arbeitgeber** (§ 69b UrhG).

### Lizenzarten

| Lizenz | Bedeutung |
| --- | --- |
| proprietär (kommerziell) | Nutzung gegen Entgelt, Quellcode nicht offen |
| OEM | an ein Gerät gebunden, mit Hardware verkauft |
| Volumenlizenz | viele Lizenzen für ein Unternehmen, zentral verwaltet |
| Abonnement (Subscription) | Nutzung, solange gezahlt wird |
| Freeware | kostenlos, aber Quellcode und Weitergabe nicht frei |
| Shareware | zum Testen kostenlos, danach Kauf |
| Open Source | Quellcode offen, Nutzung und Änderung erlaubt – unter Bedingungen |

### Open Source: Copyleft oder freizügig?

| | Copyleft (z. B. GPL) | freizügig (permissive, z. B. MIT, Apache 2.0) |
| --- | --- | --- |
| eigene Änderungen weitergeben | nur unter **derselben** Lizenz, mit Quellcode | auch in geschlossener Software erlaubt |
| Pflicht | Lizenztext, Quellcode bei Weitergabe | Lizenz- und Urhebervermerk beibehalten |

Open Source heißt **nicht** „ohne Regeln“.

### Lizenzmodelle und Rechenbeispiel

| Modell | gezählt wird |
| --- | --- |
| pro Gerät | jedes Gerät mit Installation |
| pro Benutzer (named user) | jede berechtigte Person |
| gleichzeitige Nutzer (concurrent) | höchstens so viele gleichzeitig |
| pro Prozessorkern | Kerne des Servers |

Beispiel: 40 Mitarbeitende, davon nutzen höchstens 12 gleichzeitig eine Software. Named User 80 € je
Person, Concurrent 220 € je gleichzeitigem Nutzer.

- Named User: 40 × 80 € = **3.200 €**
- Concurrent: 12 × 220 € = **2.640 €**

> **Halten wir kurz fest:**
>
> 1. Urheberrecht entsteht automatisch und gilt bis 70 Jahre nach dem Tod; Software ist geschützt.
> 2. Lizenz = Erlaubnis zur Nutzung, in vielen Formen von OEM bis Open Source.
> 3. Copyleft (GPL) verlangt gleiche Lizenz bei Weitergabe, permissive (MIT) nicht.

## Warum ist es so?

Wer etwas Neues schafft, soll darüber bestimmen und davon leben können. Lizenzen regeln genau, was
andere mit dem Werk tun dürfen – vom einfachen Nutzen bis zum Verändern und Weitergeben.

<details>
<summary>Warum darf man Software nicht einfach privat kopieren wie eine CD?</summary>

Für Computerprogramme gelten Sonderregeln (§§ 69a ff. UrhG). Eine Privatkopie wie bei Musik ist dort
nicht vorgesehen; erlaubt ist im Wesentlichen eine **Sicherungskopie**, wenn sie für die weitere
Nutzung nötig ist (§ 69d). Alles Weitere regelt der Lizenzvertrag.

</details>

## Praxisbezug im Betrieb

- **Lizenzmanagement:** Inventar, welche Software mit welcher Lizenz auf welchem Gerät läuft.
- **Open-Source-Bibliotheken** in eigener Software: Lizenzen prüfen, bevor ausgeliefert wird.
- **Bilder in Präsentationen:** eigene Diagramme oder Bilder mit klarer Lizenz verwenden.

## Typische Prüfungsfalle

- **Freeware = Open Source:** Freeware ist kostenlos, aber nicht offen.
- **Open Source ohne Pflichten:** Lizenzbedingungen gelten.
- **Urheberrecht muss angemeldet werden:** Es entsteht automatisch.
- **Named und Concurrent verwechselt:** Personen gegenüber gleichzeitigen Nutzern.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Urheberrecht | Schutz des Werks, automatisch |
| Lizenz | Erlaubnis zur Nutzung |
| Freeware | kostenlos, Quellcode geschlossen |
| Open Source | Quellcode offen, Lizenzbedingungen |
| Copyleft | Änderungen unter gleicher Lizenz weitergeben |
| OEM-Lizenz | an ein Gerät gebunden |

## Merksatz

**Geschützt ist, wer schafft – automatisch und bis 70 Jahre nach dem Tod. Genutzt wird nur mit Lizenz,
und auch Open Source hat Regeln.**
