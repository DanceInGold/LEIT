---
id: relationale-tabellen
titel: "Relationale Tabellen: Redundanz, Anomalien und Normalisierung"
themen: [erm-relational]
reihenfolge: 2
voraussetzungen: []
dauer_min: 40
quelle: "Neu erstellt (Claude). Relationales Modell nach Codd; Anomalien und Normalformen (1NF–3NF) nach gängiger Datenbank-Fachliteratur; Beispiel setzt das Archiv-Modell aus Kapitel 1 fort."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 04.08: Grundlagen von relationalen Datenbanken kennen und anwenden können (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "Codd, E. F.: A Relational Model of Data for Large Shared Data Banks. Communications of the ACM 13 (6), 1970, S. 377–387"}
  - {titel: "Codd, E. F.: Further Normalization of the Data Base Relational Model. In: Rustin (Hrsg.), Data Base Systems, Prentice-Hall 1972 (2. und 3. Normalform)"}
status: ungeprüft
---

## Worum geht es?

Im ersten Kapitel hast du aus einem ERM Tabellen abgeleitet. Oft ist es in der Praxis umgekehrt:
Es gibt schon **eine große Liste** – und sie macht Ärger.

- Warum verteilt man Daten auf **mehrere Tabellen**?
- Welche Fehler (Anomalien) entstehen, wenn man es nicht tut?
- Wie zerlegt man eine Liste sauber? Das heißt **[Normalisierung](glossar:normalisierung)**.

Am Ende landen wir genau bei den Tabellen aus Kapitel 1.

## Wie funktioniert es?

### Die Fachbegriffe

| Begriff | Bedeutung | Im Alltag |
| --- | --- | --- |
| Relation | Tabelle | „die Kundentabelle“ |
| Tupel | Datensatz, eine Zeile | „der Kunde K1“ |
| Attribut | Spalte | „Ort“ |
| Wertebereich (Domäne) | erlaubte Werte einer Spalte | Postleitzahl: 5 Ziffern |
| Primärschlüssel | identifiziert jede Zeile eindeutig | KundenNr |
| Fremdschlüssel | verweist auf den Primärschlüssel einer anderen Tabelle | KundenNr im Projekt |

### Die Ausgangsliste

Bisher pflegt die ArchivTech ihre Dokumente in einer einzigen Liste:

| DokNr | Titel | ProjektNr | Projekt | KundenNr | Kunde | Schlagworte |
| --- | --- | --- | --- | --- | --- | --- |
| 101 | Rechnung März | P1 | Buchhaltung | K1 | Kunde Nord GmbH | Rechnung, 2024 |
| 102 | Rechnung April | P1 | Buchhaltung | K1 | Kunde Nord GmbH | Rechnung, 2024 |
| 103 | Bauplan Halle | P2 | Bauakten | K2 | Kunde Süd KG | Plan |

„Kunde Nord GmbH“ und „Buchhaltung“ stehen mehrfach da. Das ist **[Redundanz](glossar:redundanz)**.

### Drei Anomalien

Redundanz führt zu Fehlern beim Ändern der Daten:

| Anomalie | Was passiert | Im Beispiel |
| --- | --- | --- |
| Änderungsanomalie | Eine Änderung muss in vielen Zeilen passieren – eine wird vergessen | Kunde Nord benennt sich um; Zeile 102 bleibt alt |
| Einfügeanomalie | Etwas lässt sich nicht speichern, solange etwas anderes fehlt | Neuer Kunde ohne Dokument passt nicht in die Liste |
| Löschanomalie | Beim Löschen verschwindet mehr als gewollt | Dokument 103 löschen – Kunde Süd ist weg |

### 1. Normalform: nur atomare Werte

Regel: In jeder Zelle steht **genau ein Wert**.

„Rechnung, 2024“ verletzt das. Lösung: eine eigene Zeile je Schlagwort. Der Primärschlüssel ist jetzt
**(DokNr, Schlagwort)**.

| <u>DokNr</u> | <u>Schlagwort</u> | Titel | ProjektNr | Projekt | KundenNr | Kunde |
| --- | --- | --- | --- | --- | --- | --- |
| 101 | Rechnung | Rechnung März | P1 | Buchhaltung | K1 | Kunde Nord GmbH |
| 101 | 2024 | Rechnung März | P1 | Buchhaltung | K1 | Kunde Nord GmbH |
| … | | | | | | |

Die Redundanz ist sogar gewachsen. Die nächsten Schritte bauen sie ab.

### 2. Normalform: ganzer Schlüssel

Regel: 1NF, und jedes Nicht-Schlüssel-Attribut hängt vom **ganzen** Primärschlüssel ab.

Titel, Projekt und Kunde hängen nur von **DokNr** ab, nicht vom Schlagwort. Also trennen:

- Dokument (<u>DokNr</u>, Titel, ProjektNr, Projekt, KundenNr, Kunde)
- Verschlagwortung (<u>DokNr, Schlagwort</u>)

Hat eine Tabelle einen Schlüssel aus **nur einer** Spalte, ist sie in 1NF automatisch auch in 2NF.

### 3. Normalform: keine Umwege

Regel: 2NF, und kein Nicht-Schlüssel-Attribut hängt von einem anderen Nicht-Schlüssel-Attribut ab
(keine **transitive Abhängigkeit**).

In „Dokument“ gilt: DokNr → ProjektNr → Projekt und ProjektNr → KundenNr → Kunde.
Projekt und Kunde hängen also nur **über einen Umweg** von DokNr ab. Trennen:

- Kunde (<u>KundenNr</u>, Kunde)
- Projekt (<u>ProjektNr</u>, Projekt, ↑KundenNr)
- Dokument (<u>DokNr</u>, Titel, ↑ProjektNr)
- Verschlagwortung (<u>↑DokNr, Schlagwort</u>)

Das ist im Kern der Entwurf aus Kapitel 1. Jeder Kundenname steht jetzt **genau einmal** in der
Datenbank.

> **Halten wir kurz fest:**
>
> 1. Redundanz → Änderungs-, Einfüge- und Löschanomalie.
> 2. 1NF atomar · 2NF ganzer Schlüssel · 3NF keine Umwege über andere Spalten.
> 3. Ein sauberes ERM führt meist direkt zu Tabellen in 3NF.

### Referentielle Integrität

Fremdschlüssel sind ein Versprechen: Jeder Wert muss in der anderen Tabelle **existieren**.

- Ein Projekt mit KundenNr K9 ist unzulässig, wenn es K9 nicht gibt.
- Ein Kunde mit Projekten darf nicht einfach gelöscht werden.

Die Datenbank kann das selbst überwachen: Sie verweigert die Aktion oder löscht abhängige Zeilen
mit („Löschweitergabe“).

## Warum ist es so?

Jede Information soll **an genau einer Stelle** stehen. Dann gibt es beim Ändern nur eine Stelle,
die stimmen muss.

<details>
<summary>Warum nicht einfach alles in einer Tabelle wie in Excel?</summary>

Bei 20 Zeilen geht das. Bei 2 Millionen Dokumenten heißt jeder Tippfehler im Kundennamen: Suchen
und Auswerten liefern falsche Ergebnisse. Außerdem kostet jede Wiederholung Speicher. Getrennte
Tabellen mit Schlüsseln lösen beides.

</details>

<details>
<summary>Warum hört man meist bei der 3. Normalform auf?</summary>

Ab der 3NF sind die Anomalien des Alltags beseitigt. Es gibt weitere Normalformen (BCNF, 4NF, 5NF),
die nur seltene Sonderfälle betreffen. Manchmal wird bewusst sogar wieder zusammengelegt
(Denormalisierung), damit Auswertungen schneller laufen.

</details>

## Praxisbezug im Betrieb

- **Excel-Listen ablösen:** Viele Fachabteilungen starten mit einer Tabelle. Wächst sie, hilft genau
  dieses Vorgehen beim Umzug in eine Datenbank.
- **Stammdaten:** Kunden und Projekte als eigene Tabellen sind die Grundlage für jedes Ticket- und
  Archivsystem.
- **Fehlersuche:** Taucht ein Kunde in Auswertungen doppelt auf, steckt oft Redundanz dahinter.

## Typische Prüfungsfalle

- **Anomalien vertauscht:** Ändern – Einfügen – Löschen, jeweils mit eigenem Beispiel.
- **1NF übersehen:** Listen in einer Zelle („Rechnung, 2024“) verletzen die erste Normalform.
- **2NF und 3NF verwechselt:** 2NF = Teil des Schlüssels reicht; 3NF = Umweg über eine andere
  Spalte. 2NF ist nur bei zusammengesetztem Schlüssel ein Thema.
- **Fremdschlüssel vergessen:** Nach dem Zerlegen braucht jede Tabelle die Verbindung zur anderen.
- **Normalformen nicht namentlich im Katalog:** Der Katalog nennt „Grundlagen relationaler
  Datenbanken“. Redundanz und Anomalien erklären können ist sicher gefragt, die Normalformen sind
  das Werkzeug dafür.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Redundanz | dieselbe Information mehrfach gespeichert |
| Anomalie | Fehler beim Ändern, Einfügen oder Löschen als Folge von Redundanz |
| 1NF | jede Zelle atomar |
| 2NF | kein Attribut hängt nur von einem Teil des Schlüssels ab |
| 3NF | kein Attribut hängt von einem anderen Nicht-Schlüssel-Attribut ab |
| Referentielle Integrität | jeder Fremdschlüssel verweist auf einen vorhandenen Datensatz |

## Merksatz

**Jede Information an genau eine Stelle: atomar (1NF), am ganzen Schlüssel (2NF), ohne Umweg (3NF) –
und jeder Fremdschlüssel zeigt auf etwas, das es wirklich gibt.**
