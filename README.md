# LEIT – AP1-Lernbegleiter

Lokales Lernprogramm zur Vorbereitung auf die Abschlussprüfung Teil 1 (AP1) der IT-Berufe,
zugeschnitten auf Fachinformatik Systemintegration. Inhalte (Markdown/YAML) und Programm
(Python) sind getrennt; weitere Prüfungsteile kommen als zusätzliche Inhaltspakete dazu.

**Stand:** Phase 0 – Repo-Struktur, Inventur des Materials, Faktencheck, Lernstil-Analyse.
Das Programm selbst folgt ab Phase 1.

## Schnellstart

Voraussetzung: [uv](https://docs.astral.sh/uv/) und Python 3.12+.

```bash
uv sync --all-groups              # Abhängigkeiten installieren
uv run ap-trainer                 # Programm starten (Phase 0: Platzhalter)
uv run ap-tools inventur --check  # zeigen, was sich in quellen/ geändert hat
uv run pytest                     # Tests
```

## Neues Material einspielen

1. Datei in den passenden Unterordner von `quellen/` legen – sprechender Name, keine Zeichen
   `: | ? * " < >` (z. B. `quellen/eigene/lf05-dhcp.pdf`).
2. `git add quellen/ && git commit -m "Quellen: DHCP-Skript ergänzt" && git push`
3. Die GitHub Action legt ein Issue „Inventur: …“ an.
4. In einer Claude-Sitzung „Bearbeite Issue #N“ schreiben – Claude sichtet, prüft und öffnet
   einen Pull Request. Gemergt wird nur von dir.

## Wichtige Dokumente

| Datei | Inhalt |
| --- | --- |
| `docs/anforderungen.md` | Anforderungsdokument (maßgebliche Spezifikation) |
| `docs/inventur.md` | Was liegt in `quellen/`, wozu gehört es, was fehlt |
| `docs/pruefprotokoll.md` | Gefundene fachliche Fehler mit Korrektur und Beleg |
| `docs/lernstil-analyse.md` | Lernstil aus den eigenen Dokumenten, Profilvorschlag |
| `docs/entscheidungen.md` | Entscheidungen aus der Umsetzung |
| `CLAUDE.md` | Arbeitsregeln für Claude in diesem Repo |
| `content/ap1/katalog.yaml` | Themenbaum AP1 (Entwurf) |
