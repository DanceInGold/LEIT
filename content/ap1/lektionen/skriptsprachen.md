---
id: skriptsprachen
titel: "Skriptsprachen: Aufgaben automatisieren mit Shell-Skripten"
themen: [skriptsprachen]
reihenfolge: 1
voraussetzungen: [pseudocode]
dauer_min: 30
quelle: "Neu erstellt (Claude). Bash nach GNU-Bash-Referenzhandbuch, PowerShell nach Microsoft-Dokumentation; Beispielskript fiktiv und mit bash -n auf Syntax geprüft."
belege:
  - {titel: "Prüfungskatalog AP1 2025: Skriptsprachen, z. B. Shell-Skript – Themenzuordnung siehe content/ap1/katalog.yaml (04.06)"}
  - {titel: "GNU Bash Reference Manual", url: "https://www.gnu.org/software/bash/manual/bash.html"}
  - {titel: "Microsoft Learn: What is PowerShell?", url: "https://learn.microsoft.com/en-us/powershell/scripting/overview"}
status: geprüft
---

## Worum geht es?

Admins erledigen viele Aufgaben immer wieder: Logs aufräumen, Sicherungen prüfen, Benutzer anlegen.
**Skriptsprachen** automatisieren das. Ein **[Skript](glossar:skript)** ist eine Textdatei mit Befehlen,
die ein **Interpreter** Zeile für Zeile ausführt.

| Sprache | typisch für |
| --- | --- |
| Bash (Shell) | Linux-Server, Automatisierung auf RHEL |
| PowerShell | Windows, Active Directory, Microsoft 365 |
| Python | plattformübergreifend, größere Automatisierungen |

## Wie funktioniert es?

### Interpretiert oder kompiliert?

| | Skriptsprache (interpretiert) | kompilierte Sprache |
| --- | --- | --- |
| Ausführung | Interpreter liest den Quelltext beim Start | vorher in Maschinencode übersetzt |
| Änderung | Datei bearbeiten, sofort neu starten | neu übersetzen |
| Tempo | meist langsamer | meist schneller |
| Beispiele | Bash, PowerShell, Python | C, C++, Go |

### Ein Shell-Skript lesen

Das Skript prüft, ob die nächtlichen Archivdateien da sind:

```bash
#!/bin/bash
# Prüft, ob für jeden Kunden die heutige Archivdatei existiert
ZIEL="/data/archiv/$(date +%F)"
FEHLER=0

for KUNDE in nord sued west; do
    if [ -f "$ZIEL/$KUNDE.tar.gz" ]; then
        echo "OK: $KUNDE"
    else
        echo "FEHLT: $KUNDE"
        FEHLER=$((FEHLER + 1))
    fi
done

exit $FEHLER
```

| Zeile | Bedeutung |
| --- | --- |
| `#!/bin/bash` | **Shebang**: mit welchem Interpreter ausführen |
| `ZIEL=…` | Variable setzen (ohne Leerzeichen um `=`) |
| `$(date +%F)` | Befehl ausführen, Ergebnis einsetzen, z. B. `2027-01-29` |
| `for … in …; do … done` | Zählschleife über eine Liste |
| `if [ -f … ]` | Bedingung: Datei existiert? |
| `$((FEHLER + 1))` | rechnen |
| `exit $FEHLER` | Rückgabewert: 0 = alles in Ordnung |

### Ausführen und planen

```bash
chmod +x pruefe_archiv.sh      # ausführbar machen
./pruefe_archiv.sh             # starten
echo $?                        # Rückgabewert anzeigen
```

Regelmäßig starten mit **cron**: `30 6 * * * /opt/skripte/pruefe_archiv.sh` → täglich um 6:30 Uhr.

### Dasselbe in PowerShell

```text
foreach ($kunde in "nord","sued","west") {
    if (Test-Path "D:\Archiv\$kunde.zip") { "OK: $kunde" } else { "FEHLT: $kunde" }
}
```

Die Bausteine sind dieselben wie im Pseudocode: Variablen, Schleifen, Verzweigungen.

> **Halten wir kurz fest:**
>
> 1. Skript = Textdatei mit Befehlen, ein Interpreter führt sie aus.
> 2. Bash: Shebang, Variablen, `for`, `if`, Rückgabewert mit `exit`.
> 3. Ausführbar machen mit `chmod +x`, planen mit cron.

## Warum ist es so?

Was von Hand fünf Minuten dauert und jeden Tag anfällt, kostet im Jahr Tage – und wird irgendwann
vergessen. Ein Skript macht es jedes Mal gleich, protokolliert und meldet Fehler.

<details>
<summary>Warum ist der Rückgabewert so wichtig?</summary>

Andere Programme werten ihn aus: cron, Monitoring, Jenkins. Liefert das Skript bei einem Fehler eine
Zahl ungleich 0, schlägt der Job sichtbar fehl und jemand wird benachrichtigt. Ein Skript, das immer
0 liefert, verschweigt Probleme.

</details>

## Praxisbezug im Betrieb

- **Jenkins-Pipelines** rufen Shell-Skripte auf; ein Exit-Code ungleich 0 bricht den Build ab.
- **Shell oder Python?** Für ein paar Befehle reicht Bash; bei Logik, Daten und Fehlerbehandlung wird
  Python übersichtlicher.
- **Skripte versionieren:** in Git, mit Review – wie jeden anderen Code.

## Typische Prüfungsfalle

- **Leerzeichen bei der Zuweisung:** `ZIEL = …` ist in Bash falsch.
- **Shebang fehlt:** Das Skript läuft eventuell mit der falschen Shell.
- **Kein x-Recht:** `Permission denied` beim Start.
- **Exit-Code missverstanden:** 0 = Erfolg, alles andere = Fehler.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Skript | Textdatei mit Befehlen für einen Interpreter |
| Interpreter | führt Quelltext zur Laufzeit aus |
| Compiler | übersetzt vorher in Maschinencode |
| Shebang | erste Zeile `#!…`, wählt den Interpreter |
| Exit-Code | Rückgabewert, 0 = Erfolg |
| cron | Zeitplaner unter Linux |

## Merksatz

**Was du dreimal von Hand machst, wird ein Skript: Shebang oben, Variablen, Schleife, Bedingung – und
ein ehrlicher Exit-Code am Ende.**
