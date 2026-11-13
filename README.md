# LEIT – AP1-Lernbegleiter

Lokales Lernprogramm zur Vorbereitung auf die Abschlussprüfung Teil 1 (AP1) der IT-Berufe,
zugeschnitten auf Fachinformatik Systemintegration. Inhalte (Markdown/YAML) und Programm
(Python) sind getrennt; weitere Prüfungsteile kommen als zusätzliche Inhaltspakete dazu.

**Stand:** Phase 2 läuft – Lernplan, Startseite „Heute“ mit Kennzahlen und Diagrammen,
Themen mit nummerierten Kapiteln, Lektionen Schritt für Schritt, Glossar, Lernkarten mit
Wiederholung nach FSRS und neu die Seite **Üben**: Aufgaben in sechs Formen, gestufte Hilfen und
Rechentrainer mit Prüfung jedes Zwischenschritts für Zahlensysteme, IPv4-Subnetting, IPv6,
Datenmengen und Übertragungszeit, Stromkosten sowie Amortisation und Kostenvergleich.

## Schnellstart

Voraussetzung: [uv](https://docs.astral.sh/uv/). Das Projekt nutzt Python 3.13 (`.python-version`);
uv lädt diese Version beim ersten `uv sync` selbst herunter, auch wenn auf dem Rechner eine neuere
installiert ist. Python 3.14 und neuer gehen noch nicht, weil NiceGUI 2.x dort nicht startet.

```bash
uv sync --all-groups              # Abhängigkeiten installieren
uv run ap-trainer                 # Lernbegleiter starten, öffnet http://127.0.0.1:8080
uv run ap-trainer --lan           # zusätzlich im WLAN erreichbar (Smartphone), Adresse steht im Terminal
uv run ap-tools check             # Inhalte gegen Schema und Verweise prüfen
uv run ap-tools check --streng    # zusätzlich Stilprüfung (Absatz- und Schrittlänge)
uv run ap-tools inventur --check  # zeigen, was sich in quellen/ geändert hat
uv run pytest                     # Tests
```

Beim ersten Start unter **Einstellungen** Prüfungstermin, Lernbeginn und Lernbudget festlegen. Ein
späterer Wechsel (z. B. von 15 auf 30 Stunden pro Woche) wird als weitere Budgetzeile mit
Startdatum eingetragen – der Plan rechnet sich sofort neu.

**Lernstand:** liegt in `~/.ap-trainer/lernstand.sqlite` (außerhalb des Repos). Sichern durch
Kopieren der Datei oder über *Einstellungen → Als JSON exportieren*. Andere Orte über die
Umgebungsvariablen `AP_TRAINER_DATA` (Lernstand) und `AP_TRAINER_CONTENT` (Inhaltspaket).

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
| `content/ap1/aufgaben/` | Aufgaben je Thema und die zugehörigen Rechengeneratoren |
