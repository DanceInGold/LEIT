---
id: tom-massnahmen
titel: "Technisch-organisatorische Maßnahmen und wer wofür zuständig ist"
themen: [tom]
reihenfolge: 1
voraussetzungen: [schutzziele]
dauer_min: 30
quelle: "Neu erstellt (Claude). TOM nach Art. 32 DSGVO; die acht Kontrollbereiche nach der Anlage zu § 9 BDSG a. F. (bis 2018) als verbreitete Gliederungshilfe; Rollen nach Art. 37–39 DSGVO und BSI-Standard 200-2. Keine Rechtsberatung."
belege:
  - {titel: "Prüfungskatalog AP1 2025: Technisch-organisatorische Maßnahmen (TOM); Unterscheidung IT-Sicherheitsbeauftragter und Datenschutzbeauftragter; personelle Maßnahmen (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "Verordnung (EU) 2016/679 (DSGVO), Art. 32 Sicherheit der Verarbeitung, Art. 37–39 Datenschutzbeauftragter", url: "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679"}
  - {titel: "BDSG a. F. (bis 24.05.2018), Anlage zu § 9 Satz 1: Zutritts-, Zugangs-, Zugriffs-, Weitergabe-, Eingabe-, Auftrags-, Verfügbarkeitskontrolle, Trennungsgebot"}
status: ungeprüft
---

## Worum geht es?

**[TOM](glossar:tom)** sind die konkreten Schutzmaßnahmen, mit denen ein Unternehmen Daten sichert.
Art. 32 DSGVO verlangt sie für personenbezogene Daten – angemessen zum Risiko.

- **technisch:** Software, Hardware, Gebäudetechnik (Verschlüsselung, Firewall, Schließanlage)
- **organisatorisch:** Regeln und Abläufe (Berechtigungskonzept, Passwort-Policy, Schulungen)

Außerdem klärt dieses Kapitel, wer im Betrieb wofür verantwortlich ist.

## Wie funktioniert es?

### Was Art. 32 DSGVO verlangt

Die Maßnahmen sollen unter anderem sicherstellen:

1. **Pseudonymisierung und Verschlüsselung**, wo sinnvoll
2. **Vertraulichkeit, Integrität, Verfügbarkeit und Belastbarkeit** der Systeme
3. **Wiederherstellung** nach einem Zwischenfall, rasch und zuverlässig
4. regelmäßige **Überprüfung**, ob die Maßnahmen wirken

### Die acht Kontrollen als Gliederung

Das alte BDSG (bis 2018) gliederte TOM in acht Kontrollen. Viele Betriebe und Prüfungsaufgaben nutzen
sie weiter:

| Kontrolle | Frage | Beispiel |
| --- | --- | --- |
| **Zutritt** | Wer kommt in den **Raum**? | Chipkarte am Serverraum |
| **Zugang** | Wer kann das **System benutzen**? | Login mit Passwort und 2FA |
| **Zugriff** | Wer darf welche **Daten** sehen oder ändern? | Rollen und Rechte im Archiv |
| Weitergabe | Sind Daten beim Transport geschützt? | TLS, verschlüsselte USB-Sticks |
| Eingabe | Wer hat was wann eingegeben oder geändert? | Protokollierung |
| Auftrag | Hält sich der Dienstleister an Weisungen? | AV-Vertrag, Kontrollen |
| Verfügbarkeit | Sind Daten gegen Verlust geschützt? | Backup, USV, Brandschutz |
| Trennung | Werden Daten für verschiedene Zwecke getrennt? | getrennte Mandanten |

### Zutritt, Zugang, Zugriff

Die drei werden ständig verwechselt. Merk dir den Weg zu den Daten:

```mermaid
flowchart LR
  P["Person"] -->|"Zutritt:<br/>Tür zum Raum"| R["Serverraum / Büro"]
  R -->|"Zugang:<br/>Anmeldung am System"| S["IT-System"]
  S -->|"Zugriff:<br/>Rechte auf Daten"| D["Daten"]
```

**Zu-tritt** mit den Füßen, **Zu-gang** zum Gerät, **Zu-griff** auf die Daten.

### Technisch, organisatorisch, personell

| Art | Beispiele |
| --- | --- |
| technisch | Verschlüsselung, Firewall, Virenschutz, Backup, Videoüberwachung |
| organisatorisch | Berechtigungskonzept, Passwort-Policy, Vier-Augen-Prinzip, Notfallplan |
| personell | Schulungen, Phishing-Übungen, Verpflichtung auf Vertraulichkeit |

**Personelle Maßnahmen** schaffen **Sicherheitsbewusstsein** – der Mensch ist oft das schwächste
Glied.

### Wer ist zuständig?

| | IT-Sicherheitsbeauftragter (ISB) | Datenschutzbeauftragter (DSB) |
| --- | --- | --- |
| schützt | alle **Informationen** des Unternehmens | **Personen** und ihre Daten |
| Grundlage | Unternehmensentscheidung, BSI-Grundschutz, ISMS | DSGVO Art. 37–39, § 38 BDSG |
| Aufgabe | Sicherheitskonzept, Vorfälle, Maßnahmen steuern | beraten, überwachen, Anlaufstelle für Betroffene und Behörde |
| Pflicht? | gesetzlich meist nicht (Ausnahme z. B. Kritische Infrastrukturen) | ja, unter den Voraussetzungen der DSGVO/des BDSG |

Beide arbeiten eng zusammen, sollten aber **nicht dieselbe Person** sein, weil sich Interessen
widersprechen können.

> **Halten wir kurz fest:**
>
> 1. TOM = technische und organisatorische Schutzmaßnahmen, angemessen zum Risiko (Art. 32).
> 2. Zutritt = Raum, Zugang = System, Zugriff = Daten.
> 3. ISB schützt Informationen, DSB schützt Personen.

## Warum ist es so?

Technik allein reicht nicht: Die beste Verschlüsselung hilft nichts, wenn das Passwort am Monitor klebt.
Darum gehören Regeln und Schulungen genauso dazu wie Software.

<details>
<summary>Warum sollten ISB und DSB nicht dieselbe Person sein?</summary>

Der ISB will oft **mehr** protokollieren und überwachen, um Angriffe zu erkennen. Der DSB achtet
darauf, dass **nicht zu viel** über Mitarbeitende gespeichert wird. Vereint eine Person beide Rollen,
kontrolliert sie sich selbst. Getrennte Rollen sorgen für eine echte Abwägung.

</details>

## Praxisbezug im Betrieb

- **TOM-Dokument:** Gehört zum Auftragsverarbeitungsvertrag – Kunden fragen danach, bevor sie ihr
  Archiv übergeben.
- **Berechtigungen prüfen:** Regelmäßig kontrollieren, wer auf welche Archivbereiche zugreifen darf;
  Austritte sofort sperren.
- **Phishing-Übungen** sind eine personelle Maßnahme, die messbar wirkt.

## Typische Prüfungsfalle

- **Zutritt, Zugang, Zugriff vertauscht:** Raum – System – Daten.
- **Nur technische Maßnahmen genannt:** Organisatorische und personelle gehören dazu.
- **ISB und DSB gleichgesetzt:** Unterschiedliche Schutzobjekte und Rechtsgrundlagen.
- **Maßnahme ohne Bezug:** Nenne, welches Schutzziel oder welche Kontrolle sie erfüllt.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Zutrittskontrolle | physischer Zugang zu Räumen |
| Zugangskontrolle | Nutzung von IT-Systemen (Anmeldung) |
| Zugriffskontrolle | Rechte auf Daten im System |
| technische Maßnahme | wirkt durch Technik |
| organisatorische Maßnahme | wirkt durch Regeln und Abläufe |
| personelle Maßnahme | wirkt durch Schulung und Bewusstsein |

## Merksatz

**Zutritt mit den Füßen, Zugang zum Gerät, Zugriff auf die Daten. Technik, Regeln und Menschen gehören
zusammen – der ISB schützt Informationen, der DSB Personen.**
