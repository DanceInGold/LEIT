# Entscheidungen

Getroffene Entscheidungen mit Begründung. Die Grundsatzentscheidungen vom 12.11.2026 stehen
in `docs/anforderungen.md`, Kap. 12; hier folgen die Entscheidungen aus der Umsetzung.

| Nr. | Datum | Entscheidung | Begründung | Rückgängig machen |
| --- | --- | --- | --- | --- |
| E-01 | 12.11.2026 | Quelldateien beim Verschieben nach `quellen/` umbenannt (Kleinbuchstaben, Bindestriche, keine `: \| ? * " < >`). | Die Moodle-Dateinamen enthielten `:` und `\|`; solche Dateien können unter Windows nicht ausgecheckt werden (NF-01). Inhalt und Prüfsumme bleiben gleich; Zuordnung alt → neu in `docs/inventur.md`. | Umbenennen per `git mv`; das Manifest erkennt Umbenennungen an der Prüfsumme. |
| E-02 | 12.11.2026 | Notion-Exporte behalten ihre innere Ordnerstruktur. | Die Markdown-Dateien verweisen relativ auf ihre Bilder (in LF05 sogar ordnerübergreifend). | – |
| E-03 | 12.11.2026 | Ordner `quellen/` gegliedert in `eigene/`, `portfolios/`, `lernfelder/`, `pruefung/`. | Trennt allein verfasstes Material (Stilvorlage) von Gruppenarbeiten, Schulvorgaben und Prüfungsquellen. | Ordner verschieben; Manifest erkennt Umbenennung. |
| E-04 | 12.11.2026 | `ap-tools` nutzt `argparse` statt Typer. | Typer war in der Umgebung nicht installierbar; `argparse` ist Standardbibliothek, liefert `--help` und Unterbefehle und spart eine Abhängigkeit. Die Konvention „jedes Werkzeug ein Unterbefehl mit `--help`“ bleibt erfüllt. | Austausch nur in `tools/cli.py`. |
| E-05 | 12.11.2026 | Inventurskript extrahiert zusätzlich Text aus `.xlsx`. | Fünf Excel-Anhänge im LF03-Portfolio; ohne Extraktion wären sie für die Sichtung nur als Binärdatei sichtbar. | – |
| E-06 | 12.11.2026 | Inventur schreibt das Manifest nur, wenn sich etwas geändert hat. | Vermeidet Commits, die nur den Zeitstempel ändern. | – |
| E-07 | 12.11.2026 | `katalog.yaml` als Entwurf aus dem Katalog-Delta angelegt, Gewichte und Aufwände noch leer. | Der vollständige Katalog fehlt (F-01); Gewichte ohne Katalog wären geraten. Entfallene Themen stehen schon mit Gewicht 0 drin. | Wird nach F-01 vervollständigt. |
| E-08 | 12.11.2026 | Kein `uv.lock` im ersten PR. | In der Arbeitsumgebung war kein Netzzugriff für `uv lock` möglich. Die CI erzeugt beim ersten Lauf ein Lock; es wird im nächsten PR eingecheckt. | – |
