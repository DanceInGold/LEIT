# Changelog

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen nach
[Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

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
