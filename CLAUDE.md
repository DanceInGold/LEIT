# CLAUDE.md – AP1-Lernbegleiter (LEIT)

Maßgeblich ist `docs/anforderungen.md` (Anforderungsdokument v0.2, Entscheidungen in Kap. 12).
Diese Datei fasst zusammen, wie in diesem Repo gearbeitet wird.

## Ziel und Termin

- Lokales Python-Programm (NiceGUI im Browser), das einen FiSi-Azubi strukturiert zur AP1 führt:
  Lernplan, Lektionen mit Wie/Warum, Glossar, Aufgaben, Wiederholung (FSRS), Simulation.
- Erster Nutzer: Prüfung am **24.02.2027**. Termin, Budget und Katalogversion sind Daten im
  Inhaltspaket (`content/ap1/paket.yaml`), nie Code – spätere Jahrgänge tauschen nur das Paket.
- Lernbudget: Start 15 Std./Woche, später ca. 30 Std./Woche; der Plan muss den Wechsel ohne
  Neustart übernehmen.
- Ziel: zwei vollständige Simulationen mit mind. 92/100 Punkten vor der Prüfung.

## Lernstil (Kurzfassung, Details in `docs/lernstil-analyse.md`)

- Erst das große Bild (Gesamtablauf als Diagramm), dann Schritt für Schritt in die Tiefe.
- Jede Erklärung beantwortet: Was ist das? Wie funktioniert es? **Warum** ist es so?
  Wofür im Betrieb? Typische Prüfungsfalle? Merksatz? (Raster LI-01)
- Ein durchgehendes Rechenbeispiel mit echten Zahlen, jeder Zwischenschritt ausgeschrieben.
- Kurze Zwischenfazits („Halten wir kurz fest:“), Merktabellen zum Auswendiglernen,
  Vor-/Nachteil-Tabellen, „Wann verwende ich was?“.
- Alltagsanalogien (IP = Postanschrift, MAC = Personalausweis) – aber Fachbegriffe exakt.
- Locker, direkt, Du-Form; selbst gezeichnete Diagramme statt Fotos.
- Bekannte Schwachstelle: Begriffe benachbarter Konzepte verschwimmen (Scrum-Events, ARP/NAT,
  TTL). Lektionen grenzen ähnliche Begriffe ausdrücklich voneinander ab.

## Schreibregeln für Lektionen (gegen Textüberladung)

- Die Oberfläche zeigt eine Lektion Schritt für Schritt: je Raster-Abschnitt ein Schritt,
  Unterüberschriften (`###`) teilen einen Abschnitt in weitere Schritte.
- Absätze höchstens **40 Wörter**, ein Schritt höchstens **220 sichtbare Wörter**. Was darüber
  hinausgeht, wandert in eine Vertiefung (`<details><summary>Warum …?</summary>`), eine Tabelle
  oder einen eigenen `###`-Schritt. `uv run ap-tools check --streng` prüft das, auch in der CI.
- Lieber Liste, Tabelle oder Diagramm als Fließtext; Zwischenfazit als Hinweiskasten
  `> **Halten wir kurz fest:** …`.
- Ein Thema hat mehrere kurze Kapitel (Lektionen, `reihenfolge: 1, 2, …`) statt einer langen;
  ein Kapitel dauert ca. 20–40 Minuten.

## Umgang mit dem eigenen Material

Das Material in `quellen/` ist **nur Kontext**: welche Themen behandelt wurden, wie der Azubi
arbeitet und schreibt, wo er Fehler macht. Lektionen werden **nicht** daraus aufbereitet,
sondern vollständig neu geschrieben und gegen belastbare Quellen geprüft. Die Lehrgangsfolien
`quellen/pruefung/vernetzte-systeme-it-infrastruktur-l3-2026.pdf` sind fremd und keine Stilvorlage.

## Betrieblicher Kontext für Beispiele

Alltag des Azubis: Linux-Server (RHEL), Python, Jenkins, GitHub, Docker, Artifactory, OpenShift,
Archivierung großer Datenmengen. Selten: Rechenzentrum, KVM-Switches. Beispiele nutzen eine
**fiktive Firma** nach diesem Muster – keine internen Details des Ausbildungsbetriebs, keine
echten Namen von Mitschüler:innen oder Lehrkräften in `content/`.

## Repo-Aufbau (Kap. 6)

```
quellen/     Rohmaterial, unverändert (eigene/, portfolios/, lernfelder/, pruefung/)
docs/        Anforderungen, Inventur, Manifest, Prüfprotokoll, Lernstil, Entscheidungen
content/ap1/ paket.yaml, katalog.yaml, lektionen/, glossar/, aufgaben/, simulationen/
src/ap_trainer/  Programm: content/ → core/ → tasks/ → storage/ → ui/
tools/       Pipeline-Werkzeuge (uv run ap-tools <befehl>)
tests/       pytest, Spiegel von src/ und tools/
```

## Konventionen

- Bezeichner Englisch; Kommentare, Docstrings, Inhalte, Commit-Nachrichten Deutsch.
- `core/` importiert nie aus `ui/` oder `storage/`; Daten als Pydantic-Modelle hinein und heraus.
- Jede Datei eine Aufgabe, Kopf-Docstring in 1–2 Sätzen, Funktionen i. d. R. unter 40 Zeilen.
- Neuer Aufgabengenerator = neue Datei in `tasks/generators/` + Testdatei mit Hypothesis-Tests
  gegen eine unabhängige Referenzrechnung (NF-07); er registriert sich selbst.
- Jedes Werkzeug in `tools/` ist ein Unterbefehl von `ap-tools` mit `--help`.
- Vor jedem Commit: `uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest`.
- Python ausführlich kommentieren; der Azubi reviewt keinen Code – Qualität sichern Tests,
  ruff und mypy (Kerntestabdeckung ≥ 80 %).
- Commits und Issues verweisen auf Anforderungs-IDs (z. B. `LP-03`, `AU-04`).

## Branches, Pull Requests, Merge

- Nie direkt auf `main` arbeiten. Branch je Vorhaben: `phase-<n>/<thema>`, `inventur/<JJJJ-MM-TT>`,
  `inhalt/<thema>`, `fix/<thema>`.
- Jede Änderung kommt als Pull Request mit Zusammenfassung (welche Dateien, welche Themen,
  welche Fehler gefunden, welche Inhalte neu) und Verweis auf Issue/Anforderungs-ID.
- **Gemergt wird ausschließlich vom Azubi.** Claude merged nicht, pusht nicht auf `main`,
  kein Skript committet oder pusht selbstständig.
- Inhalte gelten erst nach dem Merge als „geprüft“. Neue Inhalte tragen im PR `status: ungeprüft`;
  der erste Commit des nächsten Branches setzt die gemergten Inhalte auf `geprüft`.

## Material einspielen (Kurzablauf, Details Kap. 6 der Anforderungen)

1. Azubi legt Dateien in `quellen/<unterordner>/` ab (sprechende Namen, Windows-taugliche Zeichen:
   keine `: | ? * " < >`), committet und pusht.
2. GitHub Action `inventur.yml` legt ein Issue „Inventur: …“ an.
3. Auf „Bearbeite Issue #N“: Branch `inventur/<datum>`, `uv run ap-tools inventur`, jede gemeldete
   Datei **vollständig** sichten (PDF/PNG zusätzlich als Bild, transparente PNGs auf dunklem
   Hintergrund prüfen), zuordnen, prüfen; `docs/inventur.md` und `docs/pruefprotokoll.md`
   fortschreiben; Lektionen/Glossar ergänzen; PR mit Verweis auf das Issue.
4. Gelöschte Quelle: verweisende Inhalte auf „Quelle fehlt“ setzen, nicht still löschen.

## Ablauf Faktencheck

1. Jede fachliche Aussage, die in Lektionen, Glossar oder Aufgaben übernommen wird, gegen eine
   belastbare Quelle prüfen: Normen/RFCs, Herstellerdoku, BSI, Gesetzestexte, Scrum Guide,
   Fachliteratur; für Prüfungsrelevanz den Prüfungskatalog (Fassung ab 2025).
2. Fehler werden **nicht still korrigiert**: Eintrag in `docs/pruefprotokoll.md` mit ID (`P-nn`),
   Quelle (Datei + Seite/Abschnitt), Originalaussage, Korrektur, Beleg, Schwere
   (Fehler · ungenau · veraltet · Hinweis), Status.
3. In `content/` trägt jede Lektion/jeder Begriff `quelle` und `status`
   (`ungeprüft` → `korrigiert` → `geprüft` erst nach Merge).
4. Was aus Quellen im Repo nicht prüfbar ist, wird als „nicht prüfbar“ markiert, nicht geraten.
5. Entfallene Katalogthemen (2025: SQL, RAID, SAN, Struktogramm, PAP, Vererbung, LTE/5G,
   SWOT, weitere Vorgehensmodelle, NoSQL, ISO 2700x) bekommen Gewicht 0 und werden nicht als
   prüfungsrelevant dargestellt.
