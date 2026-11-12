# Changelog

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen nach
[Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Hinzugefügt
- Elf Kapitel für die letzten 13 Themen: UML (Anwendungsfall/Klasse, Aktivität), EPK und BPMN
  (Zusatz), Softwarearten und Stamm-/Bewegungsdaten, Support und Rollout, Suchoperatoren,
  Urheberrecht und Lizenzen, Barrierefreiheit, Softwareergonomie, Qualität und Testprotokoll,
  Rechtsformen (Zusatz) (LI-01). Damit hat jedes relevante Katalogthema mindestens ein Kapitel.
- Fünf Glossarbegriffe (GL-01).

### Hinzugefügt
- Zwölf Kapitel zu Systemen und Netz: HDD/SSD, UEFI und Dateisysteme, Installation, Betriebssysteme,
  Client-Server und Domäne, Ethernet/LWL/WLAN, Netzwerkkomponenten, Cloud-Modelle, Geräteklassen und
  Auslastung, Konsolenbefehle, Skriptsprachen, nachhaltige IT (LI-01).
- Vier Glossarbegriffe (GL-01).

### Hinzugefügt
- Zehn Kapitel für zwölf Themen aus Projekt, Kunde und Verträgen: Projekt und SMART-Ziele,
  Teambildung, Wirtschaftlichkeit, Kauf/Miete/Leasing, Lasten- und Pflichtenheft, Verträge,
  Abnahme und Leistungsbestätigung, Kundenbedarf und Märkte, Kommunikationssysteme, Präsentation
  (LI-01). Ein Kapitel kann jetzt mehrere kleine Themen abdecken.
- Sechs Glossarbegriffe (GL-01).

### Hinzugefügt
- Elf Kapitel zu Sicherheit und Datenschutz: Schutzziele; Schutzbedarf feststellen und vererben;
  DSGVO-Grundsätze; Betroffenenrechte und Datenpannen; TOM; ISMS und Risikomatrix;
  Authentifizierung und Passwort-Policy; Härtung und Personal Firewall; Datensicherung;
  Verfügbarkeit, NAS und USV (LI-01).
- Neun Glossarbegriffe (GL-01).

### Hinzugefügt
- Elf Kapitel für die Planwochen 5–6: Verschlüsselungsverfahren; Hash, Signatur, Zertifikat;
  Datenmengen berechnen; Übertragungszeit; IPv6-Adressen; IPv6-Subnetze und SLAAC; Wasserfall und
  agil; Scrum; Klassen und Objekte; Kapselung; englische Fachtexte (LI-01).
- 13 Glossarbegriffe zu Kryptografie, IPv6, Vorgehensmodellen und OOP (GL-01).

### Hinzugefügt
- Neun Kapitel für die Planwochen 4–5: relationale Tabellen und Normalisierung (ERM Kapitel 2),
  OSI-Modell, Ethernet/ARP/IP/TCP, Anwendungsprotokolle, Zahlensysteme, Einheiten und Präfixe,
  IPv4-Adressen, Subnetze bilden, Subnetz prüfen und VLSM (LI-01).
- Zwölf Glossarbegriffe (Normalisierung, Redundanz, OSI-Modell, MAC-Adresse, ARP, TTL, Port, TCP,
  DNS, DHCP, Subnetzmaske, NAT) (GL-01).

### Hinzugefügt
- Neun Kapitel für die Planwochen 2–3: Pseudocode (Bausteine und Verzweigungen; Schleifen, Felder
  und Funktionen), Schreibtischtest (Code von Hand durchrechnen; Fehler in Code finden),
  Projektplanung (Projektstrukturplan und Vorgangsliste; Netzplan; Gantt-Diagramm), Kalkulation
  (Verkaufspreis; Stundensatz, Vor- und Nachkalkulation) (LI-01).
- 23 Glossarbegriffe zu diesen Themen (GL-01).

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
