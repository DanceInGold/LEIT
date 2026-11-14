# Changelog

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen nach
[Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Hinzugefügt (Phase 3 · Prüfungssimulation)
- **Prüfungssimulation** (PS-01, PS-02, PS-04): neuer Menüpunkt „Simulation“ mit vollständigen
  AP1-Sätzen – Ausgangssituation, vier Aufgaben zu 20–30 Punkten, 100 Punkte, 90-Minuten-Timer mit
  automatischer Abgabe. Während der Prüfung keine Hilfen und kein Feedback.
- **Auswertung** mit Punkten je Teilaufgabe (Teilpunkte auf halbe Punkte gerundet), IHK-Note,
  deiner Antwort, Erklärung erkannter Fehler, Lösungsweg und Musterlösung; Freitexte werden danach
  selbst bewertet. Fortschritt zum Ziel „2 Simulationen mit mindestens 92 Punkten“ (E-40).
- **Schwachstellen zurück in den Lernplan** (PS-04): Jede Teilaufgabe zählt als Versuch auf Stufe 5
  „Prüfungsniveau“ (AU-02) – Fehler landen im Fehlerprotokoll, als Fehlerkarten und im
  Beherrschungsgrad. Themen unter 70 % der Punkte erscheinen auf „Heute“, bis sie sicher sitzen.
- **Simulation 1** „Neue Arbeitsplätze für eine Steuerkanzlei“: 18 Teilaufgaben aus Bedarf,
  Angebotsvergleich, Nutzwertanalyse, Hardware, Subnetting, Netzkonfiguration, Übertragungszeit, VLAN,
  Schutzziele, Schutzbedarf, Verfügbarkeit, Datensicherung, Schreibtischtest, Amortisation, Scrum, Rollout.
- **Simulation 2** „Neuer Standort für eine Fahrradmanufaktur“: 17 Teilaufgaben aus Netzplan,
  SMART-Ziele, Teamphasen, Lasten-/Pflichtenheft, Stromkostenvergleich, PC-Komponenten, Energiesparen,
  Angebotskalkulation, IPv6, OSI-Schichten, Ports, TCP/UDP, asymmetrische Verschlüsselung, digitale
  Signatur, DSGVO-Betroffenenrechte, ER-Modell und 2FA – kaum Überschneidung mit Simulation 1.
- **Simulationen 3–6** (E-41): „Server und Netz für eine Spedition“, „Patientenportal für eine
  Physiotherapie“, „Kundenservice für eine Kaffeerösterei“ und „Neue Filiale für ein Reisebüro“
  (Generalprobe). Zusammen mit 1 und 2 kommt jedes Thema des Prüfungskatalogs 2025 in mindestens einer
  Simulation vor; punktstarke Themen wie Angebotsvergleich, ERM und Schreibtischtest mehrfach.
- **Operatoren-Training** (ZI-02, E-42): neue Seite, erreichbar über „Üben“. Merktabelle der sieben
  Operatoren (nennen, beschreiben, erläutern, begründen, vergleichen, berechnen, beurteilen) mit
  Anforderungsbereich, Antwortform, typischem Fehler und Prüfpunkten. Vier Beispiele zeigen dieselbe Sache
  mit jedem Operator gefragt und beantwortet. Trainingsrunde mit 7 Aufgaben: Erwartung zuordnen, Operator an
  der Musterantwort erkennen, selbst schreiben und selbst bewerten – ohne Einfluss auf Stufen und Fehlerkarten.
- Inhaltsformat `content/ap1/simulationen/<id>.yaml` mit Prüfung in `ap-tools check`
  (100 Punkte, 20–30 Punkte je Aufgabe, Themen, Musterlösungen, Fehlerbilder); Lernstand-Tabelle
  `simulation_runs` (Migration 4), im JSON-Export enthalten.


### Behoben
- Dunkelmodus: Die Leiste mit Timer und „Abgeben“-Knopf in der Simulation war weiß und der Timer
  darin unsichtbar; ebenso der Willkommenshinweis auf „Heute“. Beide nutzen jetzt eigene Farbklassen
  für Hell und Dunkel; ein Test verhindert Tailwind-`dark:`-Klassen in der Oberfläche.
- Reihenfolge-Aufgaben: Eine unberührte (zufällige) Startreihenfolge zählt nicht mehr als Antwort. In
  der Simulation gibt sie 0 statt zufälliger Teilpunkte, beim Üben erscheint der Hinweis, erst zu sortieren.


## [1.0.0] – 2026-11-14 – Phase 2 (Üben)

Version 1.0 bringt das Üben: 341 feste Aufgaben und 7 Rechentrainer für alle 63 prüfungsrelevanten
Themen, gestufte Hilfen mit fehlerspezifischem Feedback, Stufensteuerung, Beherrschungsgrad,
Themenkarte, Fehlerprotokoll, Fehlerkarten und den wöchentlichen Mischtest. Sie ist das Ergebnis
von Phase 2 laut Zeitplan (Kap. 10); die formale Abnahme nach Kap. 11 folgt nach Phase 3 (E-39).

### Hinzugefügt

**Aufgaben-Engine**

- Aufgaben-Engine mit sechs Aufgabentypen: Multiple Choice, Zuordnung, Lückentext, Reihenfolge,
  Rechenaufgabe mit Zwischenschritten, Freitext mit Selbstbewertung (AU-01, AU-05) und fünf Stufen (AU-02).
- Rechenaufgaben prüfen jeden Zwischenschritt und nennen den ersten falschen (AU-04); typische
  Falschantworten haben eine eigene Erklärung, jeder Fehler eine Ursache für das Fehlerprotokoll
  (HI-03, Vorbereitung FT-04). Zahlen dürfen deutsch oder englisch geschrieben werden, mit Einheit.
- Gestufte Hilfen: Richtung, Ansatz, erster Schritt, Lösungsweg; die genutzte Hilfe wird gespeichert (HI-01, HI-02).
- Aufgabengeneratoren „zahlensysteme“ und „ipv4-subnetting“ mit je vier Stufen, jeweils mit
  1.000 Zufallsfällen gegen eine unabhängige Referenz getestet (AU-03, NF-07).
- Stufensteuerung: drei sicher gelöste Aufgaben in Folge → Stufe höher, zwei Fehler → tiefer (AU-06).
- Seite „Üben“ mit Themenübersicht und Übungsansicht; „Heute“ zeigt den Übungsblock zum aktuellen Thema (LP-05).
- Lösungsversuche im Lernstand (Migration 3), im JSON-Export enthalten (NF-03).
- Aufgabendateien `content/ap1/aufgaben/<thema>.yaml` mit Prüfung in `ap-tools check`; erste sieben Aufgaben.

**Rechengeneratoren**

- Vier neue Generatoren mit je vier Stufen (AU-03), jeweils mit 1.000 Zufallsfällen gegen eine
  unabhängige Nachrechnung getestet (NF-07):
  - **IPv6:** kürzen nach RFC 5952, ausschreiben, /64-Subnetze aus /48 bis /60, SLAAC mit EUI-64.
  - **Datenmengen:** Bildgröße, Übertragungszeit, Scan/Audio/Video, Nachtsicherung, Overhead, Fotos pro Minute.
  - **Stromkosten:** kWh, Jahreskosten, PC vs. Thin Client, Netzteil-Wirkungsgrad, PUE.
  - **Kostenvergleich:** Amortisation, Rückfluss, Break-even, NAS oder Cloud mit Abschreibung.
- Antwortformat `ipv6`: jede gültige Schreibweise zählt, auf Wunsch mit Präfixlänge.
- Zahlen dürfen mit Zehnerpotenz eingegeben werden („4 × 10^11“, „4·10¹¹“, „4e11“).
- Rauchtest öffnet je Thema eine Aufgabe der Stufe 4.

**Aufgaben, Paket 1**

- 63 feste Aufgaben für acht Themen der ersten Planwochen, je Thema alle Stufen 1–4 und mehrere
  Aufgabentypen, mit Hinweisen und typischen Falschantworten (AU-01, AU-02, HI-01, HI-03):
  Hardware (10), Angebotsvergleich und Nutzwertanalyse (8), ERM und relationale Tabellen (9),
  Pseudocode (6), Schreibtischtest und Fehler im Code (6), Projektplanung (8), Kalkulation (7),
  OSI-Modell und Protokolle (9).
- Rauchtest öffnet drei weitere Aufgaben (Netzplan, Freitext Hardware, Port-Zuordnung).

**Aufgaben, Paket 2**

- 57 feste Aufgaben für neun weitere Themen, je Thema Stufen 1–4 (AU-01, AU-02, HI-01, HI-03):
  Verschlüsselung (9), Schutzziele (5), BSI-Schutzbedarf (7), Datenschutz (7), Vorgehensmodelle (8),
  OOP (6), Englische Texte (6), Kundenbedarf (5), Märkte und Bedarfe (4).
- Rauchtest öffnet drei weitere Aufgaben (Schlüsselanzahl, englische Herstellermail, OOP-Codeverfolgung).

**Aufgaben, Paket 3**

- 62 feste Aufgaben für neun weitere Themen, je Thema Stufen 1–4 (AU-01, AU-02, HI-01, HI-03):
  Verfügbarkeit und Datensicherung (10), HDD/SSD (6), BIOS/UEFI und Dateisysteme (6),
  Installation (7), UML (9), Cloud-Modelle (6), Netzwerkkomponenten (6), Kommunikationssysteme (6),
  Präsentation (6).
- Neuer Generator **Verfügbarkeit** (AU-03) mit vier Stufen: Ausfallzeit pro Jahr, Reihenschaltung,
  redundante Server, SLA-Prüfung mit Serverpaar und Switch; 1.000 Zufallsfälle gegen eine
  unabhängige Nachrechnung (NF-07).
- Die Übungsseite zeigt Mermaid-Diagramme und aufklappbare Vertiefungen in Situation, Frage,
  Lösungsweg und Musterlösung – wie die Lektionsansicht (UML-Aufgaben).
- Rauchtest öffnet vier weitere Aufgaben (Verfügbarkeit Stufe 4, PoE-Budget, UML-Schleife, UML-Freitext).

**Aufgaben, Paket 4**

- 78 feste Aufgaben für 13 weitere Themen, je Thema Stufen 1–4 (AU-01, AU-02, HI-01, HI-03):
  Lasten-/Pflichtenheft (6), Skriptsprachen (6), Client-Server und Domäne (6), Netzwerkstandards (7),
  Authentifizierung (6), Härtung und Firewall (6), ISMS und Risikomatrix (6), TOM (6),
  Barrierefreiheit (6), Kauf/Miete/Leasing (5), Bildschirmmasken (6), Verträge (6), Suchoperatoren (6).
- Rauchtest öffnet drei weitere Aufgaben (Skript verfolgen, Passwortlänge, Vertragsstrafe).

**Aufgaben, Paket 5**

- 74 feste Aufgaben für die letzten 18 Themen; damit hat jedes prüfungsrelevante Thema Übungsaufgaben
  (AU-01, AU-02, HI-01, HI-03): Projektmerkmale (4), SMART (4), Teambildung (4), Geräteklassen (4),
  Auslastung/Erweiterbarkeit (4), Support-Level und KI (5), Rollout und Ticketsystem (4), EPK (4),
  BPMN (3), Konsolenbefehle (5), Software-Arten (4), Stamm-/Bewegungsdaten (4), Urheberrecht und
  Lizenzen (5), Abnahme und Dokumentation (4), Leistungsbestätigung (3), Qualität und Testprotokoll (4),
  Rechtsformen und Aufbauorganisation (4), Betriebssysteme (5).
- Rauchtest öffnet drei weitere Aufgaben (EPK-Fehler mit Diagramm, chmod, Lizenzmodelle).

**Fortschritt**

- **Beherrschungsgrad je Thema** (FT-01, 0–100 %) aus Trefferquote der letzten zehn Versuche (nach
  Stufe gewichtet, Hilfen mindern), höchster sicher gelöster Stufe und Abstand zum letzten Erfolg (E-34).
- **Fortschrittsseite mit Themenkarte** (FT-02): je Prüfungsbereich eine Kachel pro Thema in
  Ampelfarben (sicher ab 80 %, unsicher ab 50 %, Lücke, noch nicht geübt) mit Symbol, schwächste
  Themen zuerst; Klick führt zum Üben. Dazu der nach Prüfungsgewicht gemittelte Gesamtgrad.
- **Fehlerprotokoll** (FT-04): alle falsch gelösten Aufgaben nach Ursache (Rechenfehler, Begriff
  verwechselt, Konzept nicht verstanden, nicht erkannt), je Aufgabe ein Eintrag mit „Nochmal“-Knopf;
  später richtig gelöste Aufgaben gelten als behoben (E-35).
- Beherrschungsgrad auch auf der Übungsübersicht und der Themenseite; Themenseite verlinkt zum Üben.

**Wiederholung**

- **Fehlerkarten** (ZI-05, WH-01): Jede falsch gelöste Aufgabe wird zur Lernkarte – vorne die
  Aufgabe mit Situation und Diagrammen, hinten der Lösungsweg, dazu ein Link, um sie noch einmal
  selbst zu lösen. Die Karten laufen über FSRS mit den Glossarkarten; ein erneuter Fehler stellt
  die Karte sofort wieder fällig. Varianten eines Rechentrainers teilen sich je Stufe eine Karte (E-37).
- **Wöchentlicher Mischtest** (WH-03): zehn Aufgaben quer durch alle begonnenen Themen, schwache
  Themen mit hohem Prüfungsgewicht häufiger, nie dasselbe Thema zweimal hintereinander. Ab zwei
  begonnenen Themen erscheint er alle sieben Tage auf „Heute“; das Ergebnis steht auf „Fortschritt“ (E-38).
- Nach einer falschen Antwort zeigt die Übung „Als Fehlerkarte gespeichert“.

### Geändert

- Neue Aufgaben und Generatoren tragen im Pull Request `status: ungeprüft` und werden mit dem ersten
  Commit nach dem Merge auf `geprüft` gesetzt (E-23); alle Inhalte dieser Version sind geprüft.
- Aufgabenablauf der Übungsseite in eine wiederverwendbare Funktion ausgelagert (Übung und Mischtest);
  Markdown mit Diagrammen für Aufgaben und Karten in `ui/rich.py`.

### Behoben

- „Nächste Aufgabe“ brachte dieselbe Aufgabe erneut, wenn die aktuelle Stufe eines Themas nur eine
  feste Aufgabe hat (z. B. BIOS/UEFI Stufe 1). Jetzt kommt eine noch nicht gesehene Aufgabe der
  nächstgelegenen Stufe; direkt wiederholt wird nur, wenn das Thema nur eine Aufgabe hat (AU-06).
- „Nächste Aufgabe“ pendelte in kleinen Themen zwischen zwei Aufgaben (z. B. SMART: A, B, A, C, A, D),
  sobald alle Aufgaben einmal dran waren. Jetzt rotieren sie reihum; die letzten drei verschiedenen
  Aufgaben sind gesperrt (AU-06, E-36).

## [0.6.1] – 2026-11-12 – Kapitel für alle Themen

Nachgetragen: Der Tag `v0.6.1` stand ohne eigenen Abschnitt im Changelog.

### Hinzugefügt

- Neun Kapitel für die Planwochen 2–3: Pseudocode (Bausteine und Verzweigungen; Schleifen, Felder
  und Funktionen), Schreibtischtest (Code von Hand durchrechnen; Fehler in Code finden),
  Projektplanung (Projektstrukturplan und Vorgangsliste; Netzplan; Gantt-Diagramm), Kalkulation
  (Verkaufspreis; Stundensatz, Vor- und Nachkalkulation) (LI-01).
- 23 Glossarbegriffe zu diesen Themen (GL-01).
- Neun Kapitel für die Planwochen 4–5: relationale Tabellen und Normalisierung (ERM Kapitel 2),
  OSI-Modell, Ethernet/ARP/IP/TCP, Anwendungsprotokolle, Zahlensysteme, Einheiten und Präfixe,
  IPv4-Adressen, Subnetze bilden, Subnetz prüfen und VLSM (LI-01).
- Zwölf Glossarbegriffe (Normalisierung, Redundanz, OSI-Modell, MAC-Adresse, ARP, TTL, Port, TCP,
  DNS, DHCP, Subnetzmaske, NAT) (GL-01).
- Elf Kapitel für die Planwochen 5–6: Verschlüsselungsverfahren; Hash, Signatur, Zertifikat;
  Datenmengen berechnen; Übertragungszeit; IPv6-Adressen; IPv6-Subnetze und SLAAC; Wasserfall und
  agil; Scrum; Klassen und Objekte; Kapselung; englische Fachtexte (LI-01).
- 13 Glossarbegriffe zu Kryptografie, IPv6, Vorgehensmodellen und OOP (GL-01).
- Elf Kapitel zu Sicherheit und Datenschutz: Schutzziele; Schutzbedarf feststellen und vererben;
  DSGVO-Grundsätze; Betroffenenrechte und Datenpannen; TOM; ISMS und Risikomatrix;
  Authentifizierung und Passwort-Policy; Härtung und Personal Firewall; Datensicherung;
  Verfügbarkeit, NAS und USV (LI-01).
- Neun Glossarbegriffe (GL-01).
- Zehn Kapitel für zwölf Themen aus Projekt, Kunde und Verträgen: Projekt und SMART-Ziele,
  Teambildung, Wirtschaftlichkeit, Kauf/Miete/Leasing, Lasten- und Pflichtenheft, Verträge,
  Abnahme und Leistungsbestätigung, Kundenbedarf und Märkte, Kommunikationssysteme, Präsentation
  (LI-01). Ein Kapitel kann jetzt mehrere kleine Themen abdecken.
- Sechs Glossarbegriffe (GL-01).
- Zwölf Kapitel zu Systemen und Netz: HDD/SSD, UEFI und Dateisysteme, Installation, Betriebssysteme,
  Client-Server und Domäne, Ethernet/LWL/WLAN, Netzwerkkomponenten, Cloud-Modelle, Geräteklassen und
  Auslastung, Konsolenbefehle, Skriptsprachen, nachhaltige IT (LI-01).
- Vier Glossarbegriffe (GL-01).
- Elf Kapitel für die letzten 13 Themen: UML (Anwendungsfall/Klasse, Aktivität), EPK und BPMN
  (Zusatz), Softwarearten und Stamm-/Bewegungsdaten, Support und Rollout, Suchoperatoren,
  Urheberrecht und Lizenzen, Barrierefreiheit, Softwareergonomie, Qualität und Testprotokoll,
  Rechtsformen (Zusatz) (LI-01). Damit hat jedes relevante Katalogthema mindestens ein Kapitel.
- Fünf Glossarbegriffe (GL-01).

## [0.6.0] – Überblick und Kapitel

### Hinzugefügt
- Startseite mit Kennzahlen (Tage bis zur Prüfung, erledigter Stoff, Lernzeit der Woche,
  fällige Karten) und vier Diagrammen: Lernzeit geplant/gelernt, Fortschritt je
  Prüfungsbereich, Lernminuten der letzten 14 Tage, fällige Karten der nächsten 7 Tage (LP-10, E-19).
- Themenseite mit nummerierten Kapiteln und Lesestand; Lektionen zeigen „Kapitel n von m“
  und führen am Ende direkt zum nächsten Kapitel.
- Stilprüfung gegen Textüberladung (`ap-tools check --streng`, in der CI aktiv, E-18).
- Lernzeit der Lernkarten wird gemessen und fließt in die Statistik ein (Migration 2).
- Ende-zu-Ende-Rauchtest, der jede Seite einmal abruft (CI).

### Geändert
- Lektionsansicht Schritt für Schritt statt als lange Seite; Umschalter „Alles auf einer Seite“.
- Alle sechs Lektionen gekürzt und in kleinere Schritte gegliedert; Zwischenfazits als Hinweiskasten.

## [0.5.0] – Phase 1 (Lernstart)

### Hinzugefügt
- Inhaltsmodell (Pydantic) für Paket, Katalog, Lektion und Glossarbegriff mit verständlichen
  Fehlermeldungen; `ap-tools check` prüft Schema und Verweise, auch in der CI (NF-08).
- Themengewichtung aus den Prüfungspunkten (LP-07, vorläufig bis zum vollständigen Katalog).
- Lernplan rückwärts von der Prüfung mit Phasen, Abhängigkeiten, Lernbudget-Perioden,
  lernfreien Zeiten, Machbarkeitsprüfung und Zeitplan-Ampel (LP-01, LP-03, LP-04, LP-06 bis LP-10).
- Wiederholung nach FSRS mit Lernkarten aus dem Glossar (WH-01, WH-02, GL-02).
- Lokaler Lernstand in SQLite mit Migrationen, Export und Import als JSON (NF-03, NF-09).
- Oberfläche (NiceGUI): Heute, Plan, Themen, Lektion mit aufklappbaren „Warum?“-Ebenen und
  Glossar-Tooltips, Glossar mit Suche und Filter, Lernkarten mit Tastaturbedienung, Einstellungen;
  Dunkelmodus, schmale Bildschirme, `--lan` für das Smartphone (LP-05, LI-01 bis LI-04, LI-06,
  GL-01, GL-04, NF-01, NF-05).
- Sechs Lektionen (Hardware ×3, quantitativer Angebotsvergleich, Nutzwertanalyse, ERM) und
  29 Glossarbegriffe für die ersten Planwochen.

### Geändert
- Eigenes Material dient nur noch als Kontext und Stilvorlage (E-09); BPMN als Zusatzthema (E-10).

## [0.1.0] – Phase 0 (Gerüst)

### Hinzugefügt
- `CLAUDE.md` mit Ziel, Termin, Lernstil, Konventionen, Branch-/PR-Regeln und Faktencheck-Ablauf.
- `docs/anforderungen.md` (Anforderungsdokument v0.2), `docs/inventur.md`,
  `docs/pruefprotokoll.md`, `docs/lernstil-analyse.md`, `docs/entscheidungen.md`.
- Repo-Grundstruktur nach Kap. 6: `quellen/`, `content/ap1/`, `src/ap_trainer/`, `tools/`, `tests/`.
- `content/ap1/paket.yaml` und `content/ap1/katalog.yaml` (Entwurf, 73 Themen inkl. entfallener).
- Inventur-Werkzeug `ap-tools inventur` mit Prüfsummen-Manifest, Erkennung von neuen,
  geänderten, umbenannten und gelöschten Dateien, Rohtext aus PDF, HTML, Markdown und Excel.
- GitHub Actions: CI (ruff, mypy, pytest) und Inventur-Prüfung mit automatischem Issue.

### Geändert
- Rohmaterial aus `Document Dump/` nach `quellen/` verschoben und Windows-tauglich umbenannt.
