---
id: qualitaet-testprotokoll
titel: "Qualität sichern: Maßnahmen und Testprotokoll für einen Arbeitsplatz"
themen: [qualitaet]
reihenfolge: 1
voraussetzungen: []
dauer_min: 25
quelle: "Neu erstellt (Claude). Qualitätsbegriff nach DIN EN ISO 9000:2015 (Hintergrund); PDCA nach Deming; Testprotokoll als Praxisbeispiel; Kennzahl nachgerechnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkte 05.01/05.02: Qualitätsmaßnahmen, Testprotokoll für das Einrichten eines Arbeitsplatzes – Themenzuordnung siehe content/ap1/katalog.yaml"}
  - {titel: "DIN EN ISO 9000:2015 Qualitätsmanagementsysteme – Grundlagen und Begriffe (Qualität: Grad, in dem ein Satz inhärenter Merkmale Anforderungen erfüllt)"}
status: ungeprüft
---

## Worum geht es?

**Qualität** heißt: Das Ergebnis erfüllt die **Anforderungen**. Ein neu eingerichteter Arbeitsplatz
ist gut, wenn alles funktioniert, was vereinbart war – und man das **nachweisen** kann.

- Maßnahmen, die Qualität sichern
- das **[Testprotokoll](glossar:testprotokoll)** als Nachweis
- Qualität messen und verbessern

## Wie funktioniert es?

### Qualitätsmaßnahmen

| Art | Beispiel |
| --- | --- |
| vorbeugend | Checklisten, Standard-Images, Schulungen, Vier-Augen-Prinzip |
| prüfend | Tests nach Testprotokoll, Abnahme, Stichproben |
| verbessernd | Fehler auswerten, Ursachen beheben, Checkliste anpassen |

Für Verbesserung nutzt man den **PDCA-Zyklus**: planen, umsetzen, prüfen, verbessern – wie beim ISMS.

### Das Testprotokoll

Ein Testprotokoll hält fest, **was** getestet wurde, **was** erwartet war und **was** herauskam.

| Kopfdaten | Beispiel |
| --- | --- |
| Gerät, Seriennummer, Benutzer | Notebook NB-0412, SN 5CD1234XYZ, Frau K. |
| Datum, Tester | 14.01.2027, Azubi |
| Grundlage | Checkliste Arbeitsplatz v3, Pflichtenheft |

### Testfälle für einen Arbeitsplatz

| Nr. | Testfall | erwartet | Ergebnis | Status |
| ---: | --- | --- | --- | --- |
| 1 | Anmeldung mit Domänenkonto | Desktop erscheint, Laufwerke verbunden | wie erwartet | ✔ |
| 2 | Netzwerk und Internet | Intranet und externe Seite erreichbar | wie erwartet | ✔ |
| 3 | Drucken auf Abteilungsdrucker | Testseite kommt | Treiberfehler | ✘ |
| 4 | Office und Archivportal starten | starten ohne Fehler | wie erwartet | ✔ |
| 5 | Festplattenverschlüsselung | aktiv | aktiv | ✔ |
| 6 | Updates | keine ausstehenden Updates | wie erwartet | ✔ |

Bei ✘: **Fehler beheben, erneut testen, dokumentieren**. Am Ende unterschreiben Tester und Nutzer.

### Qualität messen

Eine einfache Kennzahl: **Erstlösungsquote** des Rollouts.

48 von 60 Arbeitsplätzen bestanden alle Tests beim ersten Mal: 48 ÷ 60 × 100 = **80 %**.

Die Auswertung zeigt: 9 der 12 Fehler waren der Druckertreiber → Treiber ins Image aufnehmen.

> **Halten wir kurz fest:**
>
> 1. Qualität = Anforderungen erfüllt; vorbeugen, prüfen, verbessern.
> 2. Testprotokoll: Kopfdaten, Testfall, erwartet, Ergebnis, Status, Unterschrift.
> 3. Fehler auswerten und die Ursache beheben (PDCA).

## Warum ist es so?

Ohne Test fällt ein Fehler erst beim Nutzer auf – dann kostet er mehr Zeit und Ärger. Das Protokoll
beweist außerdem, dass ordentlich gearbeitet wurde, und ist Grundlage für die Abnahme.

<details>
<summary>Warum schreibt man das erwartete Ergebnis vorher auf?</summary>

Wer erst nach dem Test entscheidet, was „richtig“ ist, findet fast alles in Ordnung. Ein vorher
festgelegtes Ergebnis macht den Test objektiv und wiederholbar – jeder Kollege kommt zum selben
Urteil.

</details>

## Praxisbezug im Betrieb

- **Checkliste als Vorlage** im Ticketsystem: jeder Arbeitsplatz gleich geprüft.
- **Automatisierte Tests** prüfen Server nach jeder Änderung, etwa in der Pipeline.
- **Lessons Learned** nach einem Rollout: Was ändern wir beim nächsten Mal?

## Typische Prüfungsfalle

- **Testprotokoll ohne erwartetes Ergebnis:** Dann ist nichts überprüfbar.
- **Fehler nur notiert, nicht nachgetestet.**
- **Nur Technik getestet:** Auch Benutzerkonto, Rechte und Datenschutzeinstellungen gehören dazu.
- **Ursache nicht behoben:** Ohne Verbesserung wiederholt sich der Fehler.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Qualität | Grad, in dem Anforderungen erfüllt sind |
| Testfall | einzelne Prüfung mit erwartetem Ergebnis |
| Testprotokoll | dokumentiert alle Testfälle und Ergebnisse |
| Abnahme | Kunde billigt das Ergebnis |
| PDCA | Zyklus zur ständigen Verbesserung |

## Merksatz

**Vorher festlegen, was richtig ist, dann testen, protokollieren, nachbessern – und die Ursache so
beheben, dass der Fehler nicht wiederkommt.**
