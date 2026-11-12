# Changelog

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen nach
[Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

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
