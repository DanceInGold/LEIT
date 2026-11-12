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
| E-09 | 12.11.2026 | Eigenes Material ist nur Kontext und Stilvorlage; alle Lektionen schreibt Claude neu. | Entscheidung des Azubis nach Phase 0. Anforderungsdokument Kap. 6 (Schritt 5) und Kap. 12 entsprechend präzisiert. | – |
| E-10 | 12.11.2026 | BPMN wird als freiwilliges Zusatzthema mit kleinem Gewicht geführt, nicht als Katalogthema. | Nicht im Katalog-Delta belegt; EPK steht auf dem Beiblatt. Der Azubi wünscht lieber zu viel als zu wenig Stoff. Laut Quelle erstellt ein bundesweiter Ausschuss die AP1 (nur Baden-Württemberg weicht ab), der Katalog 2025 gilt damit für die Hamburger Prüfung mit hoher Wahrscheinlichkeit. | Gewicht in `katalog.yaml` ändern. |
| E-11 | 12.11.2026 | Folien „Vernetzte Systeme“ bleiben in `quellen/pruefung/`, gelten als fremd und nicht als Stilvorlage. | Nicht vom Azubi erstellt, Stil gefällt ihm nicht. | – |
| E-12 | 12.11.2026 | Gewichte bis zum Eintreffen des vollständigen Katalogs vorläufig aus Clusterpunkten berechnet. | Katalog ist bestellt (F-01). Berechnung in `core/weighting.py`, Eingangsdaten in `katalog.yaml`. | Neuberechnung nach Katalog-Integration. |
| E-13 | 12.11.2026 | Lernstand mit der Standardbibliothek `sqlite3` statt SQLModel. | Weniger Abhängigkeiten, Migrationen über `PRAGMA user_version` überschaubar, in jeder Umgebung testbar. Die Lernlogik bleibt davon unberührt (Pydantic-Modelle). | Austausch nur in `storage/db.py`. |
| E-14 | 12.11.2026 | NiceGUI auf Version 2.x festgelegt (`>=2.10,<3`), fsrs auf `>=5,<7`. | Die Oberfläche nutzt APIs der 2er-Reihe (Upload, Download); Version 3 hat sie geändert. Wechsel bewusst in einem eigenen PR. | Versionsgrenzen in `pyproject.toml`. |
| E-15 | 12.11.2026 | Glossarkarten entstehen erst, wenn eine Lektion des Themas gelesen wurde. | Wiederholt wird nur, was schon gelernt ist; sonst wäre der Kartenstapel am ersten Tag überfüllt. | `service.Trainer.mark_lesson_read`. |
| E-16 | 12.11.2026 | Server lauscht standardmäßig nur auf `127.0.0.1`; für das Smartphone `--lan`. | Ohne Anmeldung soll der Lernbegleiter nicht ungefragt im ganzen Netz erreichbar sein. | Startoption. |
