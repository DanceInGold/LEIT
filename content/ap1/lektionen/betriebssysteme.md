---
id: betriebssysteme
titel: "Betriebssysteme: Einsatzzweck, Dateirechte und Freigaben"
themen: [betriebssysteme]
reihenfolge: 1
voraussetzungen: []
dauer_min: 30
quelle: "Neu erstellt (Claude). Unix-Rechte nach POSIX/GNU coreutils (chmod), NTFS- und Freigaberechte nach Microsoft-Dokumentation; Beispiele fiktiv."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 04.03: Betriebssysteme (Einsatzzweck, Filemanagement, Freigaben) – Themenzuordnung siehe content/ap1/katalog.yaml"}
  - {titel: "GNU coreutils: chmod – change file mode bits", url: "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html"}
  - {titel: "Microsoft-Dokumentation zu Freigabe- und NTFS-Berechtigungen (wirksam ist die restriktivere Kombination)"}
status: geprüft
---

## Worum geht es?

Das **Betriebssystem** verwaltet Hardware, startet Programme und regelt, **wer** auf **welche** Dateien
zugreifen darf. Für die Prüfung zählen drei Fragen:

1. Welches Betriebssystem für welchen **Einsatzzweck**?
2. Wie funktionieren **Dateirechte**?
3. Wie gibt man Ordner im Netz **frei**?

## Wie funktioniert es?

### Betriebssysteme und Einsatzzweck

| Einsatz | typische Systeme | Merkmale |
| --- | --- | --- |
| Client-Arbeitsplatz | Windows, macOS, Linux | Bedienoberfläche, Office, Peripherie |
| Server | Linux (z. B. RHEL), Windows Server | stabil, Dienste, Fernwartung, oft ohne Oberfläche |
| mobil | Android, iOS/iPadOS | Touch, App-Stores, zentral verwaltbar (MDM) |
| eingebettet | Linux-Varianten, Echtzeitsysteme | Router, Drucker, Maschinen |

### Dateirechte unter Linux

Jede Datei hat Rechte für **Besitzer (u)**, **Gruppe (g)** und **andere (o)**:

| Recht | Datei | Ordner | Wert |
| --- | --- | --- | ---: |
| r | lesen | Inhalt auflisten | 4 |
| w | schreiben | Dateien anlegen/löschen | 2 |
| x | ausführen | betreten | 1 |

Beispiel: `-rwxr-x--- archiv.sh`

| Wer | Rechte | Wert |
| --- | --- | ---: |
| Besitzer | rwx | 4 + 2 + 1 = **7** |
| Gruppe | r-x | 4 + 0 + 1 = **5** |
| andere | --- | **0** |

Gesetzt mit `chmod 750 archiv.sh`, Besitzer ändern mit `chown`.

### Dateirechte unter Windows (NTFS)

NTFS nutzt **Zugriffssteuerungslisten** (ACL) mit Rechten wie Lesen, Schreiben, Ändern, Vollzugriff –
für Benutzer und Gruppen. Rechte werden an Unterordner **vererbt**, wenn man es nicht abschaltet.

### Freigaben im Netz

Unter Windows (SMB) gibt es **zwei** Ebenen:

1. **Freigabeberechtigung** – gilt beim Zugriff über das Netz
2. **NTFS-Berechtigung** – gilt immer, auch lokal

**Wirksam ist die restriktivere** der beiden.

| Freigabe | NTFS | Ergebnis übers Netz |
| --- | --- | --- |
| Vollzugriff | Lesen | **Lesen** |
| Lesen | Ändern | **Lesen** |
| Ändern | Ändern | **Ändern** |

Linux stellt Freigaben per **NFS** oder mit Samba per **SMB** bereit; auch dort gelten zusätzlich die
Dateirechte.

> **Halten wir kurz fest:**
>
> 1. Einsatzzweck bestimmt das System: Client, Server, mobil, eingebettet.
> 2. Linux: rwx für Besitzer/Gruppe/andere, r = 4, w = 2, x = 1.
> 3. Freigabe und NTFS: Die restriktivere Berechtigung gewinnt.

## Warum ist es so?

Mehrere Personen arbeiten am selben System. Ohne Rechte könnte jeder alles lesen und löschen. Das
Betriebssystem setzt das **Prinzip der minimalen Rechte** technisch durch.

<details>
<summary>Warum gibt es bei Windows zwei Rechte-Ebenen?</summary>

Freigaberechte stammen aus einer Zeit, in der Dateisysteme wie FAT32 gar keine Rechte kannten. Sie
schützen den Zugang übers Netz. NTFS-Rechte schützen die Dateien selbst. Viele Admins setzen die
Freigabe großzügig (z. B. „Authentifizierte Benutzer: Ändern“) und steuern alles Feinere über NTFS.

</details>

## Praxisbezug im Betrieb

- **Abteilungsordner:** Rechte über **Gruppen** vergeben, nicht über einzelne Personen.
- **Skripte auf RHEL** brauchen das x-Recht: `chmod +x archiv.sh`.
- **Rechte prüfen:** `ls -l` unter Linux, Reiter „Sicherheit“ oder `icacls` unter Windows.

## Typische Prüfungsfalle

- **Oktalwert falsch addiert:** r-x = 5, nicht 6.
- **Freigabe allein betrachtet:** NTFS-Rechte gelten zusätzlich – die strengere gewinnt.
- **x bei Ordnern vergessen:** Ohne x kann man einen Ordner nicht betreten.
- **Rechte an Personen statt Gruppen:** schwer zu pflegen.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Freigabeberechtigung | gilt nur beim Netzzugriff |
| NTFS-Berechtigung | gilt immer, lokal und übers Netz |
| chmod | Rechte unter Linux ändern |
| chown | Besitzer unter Linux ändern |
| SMB | Freigabeprotokoll (Windows, Samba) |
| NFS | Freigabeprotokoll (Unix/Linux) |

## Merksatz

**Lesen vier, Schreiben zwei, Ausführen eins – für Besitzer, Gruppe, andere. Und bei Windows-Freigaben
gewinnt immer das strengere Recht.**
