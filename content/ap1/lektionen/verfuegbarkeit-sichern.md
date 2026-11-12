---
id: verfuegbarkeit-sichern
titel: "Verfügbarkeit sichern: Prozentwerte, Redundanz, NAS und USV"
themen: [verfuegbarkeit-backup]
reihenfolge: 2
voraussetzungen: []
dauer_min: 30
quelle: "Neu erstellt (Claude). Verfügbarkeitsrechnung (Serien- und Parallelschaltung) nach Zuverlässigkeitstheorie; USV-Klassen VFD/VI/VFI nach IEC 62040-3; alle Werte nachgerechnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 06.04: Sicherung der Verfügbarkeit, z. B. NAS (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "IEC 62040-3: Uninterruptible power systems (UPS) – Method of specifying the performance and test requirements (VFD, VI, VFI)"}
status: ungeprüft
---

## Worum geht es?

„Das System soll zu **99,9 %** verfügbar sein.“ Klingt nach fast immer. Wie viele Stunden Ausfall
sind das im Jahr? Und wie erreicht man solche Werte?

- **Verfügbarkeit in Prozent** in Ausfallzeit umrechnen
- **Redundanz** rechnerisch verstehen
- **NAS** und **USV** als typische Maßnahmen

## Wie funktioniert es?

### Prozent in Ausfallzeit

Ein Jahr hat 365 × 24 = **8.760 Stunden**. Ausfallzeit = (1 − Verfügbarkeit) × 8.760 h.

| Verfügbarkeit | Ausfall pro Jahr | Rechnung |
| ---: | ---: | --- |
| 99 % | 87,6 h ≈ 3,65 Tage | 0,01 × 8.760 h |
| 99,9 % | 8,76 h | 0,001 × 8.760 h |
| 99,99 % | 52,6 min | 0,0001 × 8.760 h × 60 |
| 99,999 % | 5,3 min | 0,00001 × 8.760 h × 60 |

Jede weitere Neun teilt die erlaubte Ausfallzeit durch zehn – und kostet deutlich mehr.

### Hintereinander: Verfügbarkeit sinkt

Ein Dienst braucht **Server** (99 %) **und** **Switch** (99,5 %). Fällt einer aus, ist der Dienst weg.

Gesamt = 0,99 × 0,995 = **0,98505 ≈ 98,5 %**

Jede zusätzliche Komponente in der Kette **senkt** die Gesamtverfügbarkeit.

### Parallel: Redundanz hebt sie

Zwei Server mit je 99 % arbeiten **redundant** – einer reicht. Ausfall nur, wenn **beide** gleichzeitig
ausfallen:

1. Ausfallwahrscheinlichkeit je Server: 1 − 0,99 = 0,01
2. beide zugleich: 0,01 × 0,01 = 0,0001
3. Gesamt = 1 − 0,0001 = **0,9999 = 99,99 %**

Aus zweimal „87,6 Stunden im Jahr“ wird „52,6 Minuten im Jahr“.

### Maßnahmen für Verfügbarkeit

| Maßnahme | schützt gegen |
| --- | --- |
| redundante Netzteile, Lüfter, Netzwerkanschlüsse | Ausfall einer Komponente |
| Cluster, zweiter Standort | Ausfall eines ganzen Servers oder Raums |
| **USV** (unterbrechungsfreie Stromversorgung) | Stromausfall, Spannungsschwankungen |
| Datensicherung | Datenverlust |
| Monitoring | lange unbemerkte Ausfälle |

### NAS: Speicher im Netz

Ein **[NAS](glossar:nas)** (Network Attached Storage) ist ein Speichergerät mit eigenem
Betriebssystem, das Dateien **über das Netzwerk** bereitstellt (SMB, NFS).

| | NAS | DAS (Direct Attached Storage) |
| --- | --- | --- |
| Anbindung | über das Netzwerk | direkt am Server (USB, SAS) |
| Zugriff | viele Clients gleichzeitig | nur der angeschlossene Rechner |
| Einsatz | Freigaben, Sicherungsziel | lokale Erweiterung |

NAS-Geräte bieten oft mehrere Platten mit Ausfallschutz, Snapshots und Replikation auf ein zweites NAS.

### USV-Klassen

| Klasse (IEC 62040-3) | auch genannt | Prinzip |
| --- | --- | --- |
| VFD | Offline, Standby | schaltet bei Ausfall auf Akku um, kurze Umschaltzeit |
| VI | Line-Interactive | wie VFD, gleicht zusätzlich Spannungsschwankungen aus |
| VFI | Online, Doppelwandler | Verbraucher hängen **immer** am Wechselrichter, keine Umschaltzeit |

Für Server: meist **VFI**. Die USV soll den Betrieb überbrücken oder Systeme **geordnet
herunterfahren**.

> **Halten wir kurz fest:**
>
> 1. Ausfallzeit = (1 − Verfügbarkeit) × 8.760 h.
> 2. Reihe: multiplizieren (sinkt). Parallel: 1 − Produkt der Ausfallwahrscheinlichkeiten (steigt).
> 3. NAS = Speicher übers Netz; USV-Klasse VFI für Server.

## Warum ist es so?

Ausfälle lassen sich nie ganz verhindern. Redundanz sorgt dafür, dass ein einzelner Ausfall nicht
zum Gesamtausfall wird – kein **Single Point of Failure**.

<details>
<summary>Warum ist RAID kein Thema mehr?</summary>

Der Katalog 2025 hat RAID und SAN gestrichen und nennt stattdessen NAS. Die Idee dahinter – mehrere
Platten, damit der Ausfall einer einzelnen nicht schadet – steckt aber in vielen NAS-Geräten. Für die
Prüfung reicht: NAS kann Ausfallschutz für Platten bieten, ersetzt aber keine Datensicherung.

</details>

## Praxisbezug im Betrieb

- **SLA lesen:** 99,9 % heißt fast 9 Stunden Ausfall im Jahr – passt das zum Geschäftsprozess?
- **Single Points of Failure suchen:** ein Switch, ein Netzteil, eine Internetleitung.
- **USV testen:** Akkus altern; ein Test zeigt, ob die Überbrückungszeit noch reicht.

## Typische Prüfungsfalle

- **Prozent falsch umgerechnet:** 99,9 % → 0,1 % Ausfall = 0,001 × 8.760 h.
- **Reihe und parallel vertauscht:** Reihe multipliziert Verfügbarkeiten, parallel multipliziert
  Ausfallwahrscheinlichkeiten.
- **NAS und SAN verwechselt:** NAS stellt **Dateien** übers Netz bereit; SAN ist gestrichen.
- **USV = Notstromaggregat:** Die USV überbrückt Minuten, ein Aggregat erzeugt länger Strom.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Verfügbarkeit | Anteil der Zeit, in der ein System nutzbar ist |
| Redundanz | doppelte Auslegung, damit ein Ausfall nicht schadet |
| Single Point of Failure | Komponente, deren Ausfall alles lahmlegt |
| NAS | Speichergerät, das Dateien übers Netzwerk bereitstellt |
| USV | überbrückt Stromausfälle mit Akkus |

## Merksatz

**Jede Neun teilt die Ausfallzeit durch zehn. In Reihe wird es schlechter, parallel besser – und die
USV hält den Server so lange, bis er sauber herunterfährt.**
