# Inventur des Materials

Stand: 12.11.2026 · Phase 0 · Manifest: `docs/inventur-manifest.json` (51 Dateien)

**Ergebnis in einem Satz:** Netzwerktechnik (IPv4, Subnetting, DNS/ARP/NAT, VLAN, DHCP) und
Projektmanagement (Wasserfall, Scrum) sind mit eigenem Material gut abgedeckt; die punktstärksten
übrigen Cluster – Hardware, Wirtschaftlichkeit/Angebotsvergleich und Softwareentwicklung – haben
fast kein eigenes Material und müssen neu erstellt werden. Der vollständige Prüfungskatalog 2025
liegt nicht im Repo, nur die Änderungsliste des IT-Berufe-Podcasts (offene Frage F-01).

Gesichtet wurden alle 51 Dateien vollständig: PDFs als Text und – wo Grafiken enthalten sind –
als Seitenbild, alle PNG/JPG als Bild, alle Excel-Anhänge zellweise, die HTML-Seite als Text.
Fachliche Fehler stehen in `docs/pruefprotokoll.md`, der Lernstil in `docs/lernstil-analyse.md`.

## 1. Neue Ablage in `quellen/`

Die Dateien wurden aus `Document Dump/` verschoben und umbenannt. Grund: Die Originalnamen
enthielten `:` und `|` – solche Dateien lassen sich unter Windows (Zielplattform, NF-01) nicht
auschecken. Inhalt und Prüfsumme sind unverändert. Die Notion-Exporte behalten ihre innere
Ordnerstruktur, damit die relativen Bildverweise in den Markdown-Dateien gültig bleiben.
`.DS_Store`-Dateien wurden entfernt und per `.gitignore` ausgeschlossen.

| Neuer Pfad (`quellen/…`) | Ursprünglicher Name (`Document Dump/…`) |
| --- | --- |
| `eigene/netzwerkgrundlagen.pdf` | `Netzwerkgrundlagen Lerndokument.pdf` |
| `eigene/projektmanagement.pdf` | `Projektmanagement Lerndokument.pdf` |
| `pruefung/katalog-2025-aenderungen-it-berufe-podcast-190.pdf` | `Neuer Prüfungskatalog für die AP1 … #190 - IT-Berufe-Podcast.pdf` |
| `pruefung/vernetzte-systeme-it-infrastruktur-l3-2026.pdf` | `PRÜFUNGSRELEVANT L3 IT-Systeme Betreiben 2026.pdf` |
| `portfolios/lf01-portfolio-unternehmen.pdf` | `LF01 Portfolio.pdf` |
| `portfolios/lf04-portfolio-schutzbedarfsanalyse.pdf` | `Gruppe11-LF04-Portfolio.pdf` |
| `portfolios/lf03-notion/` (Markdown + 19 Anhänge) | `Privat und Geteilt/` |
| `portfolios/lf05-notion/` (Markdown + 5 Bilder) | `LF 05/` |
| `portfolios/lf07-notion/` (Markdown + 4 Bilder) | `Portfolio LF07/` |
| `lernfelder/lf01-kursseite.pdf` | `Kurs: Lernfeld 01 IT - Das Unternehmen und Ihre Rolle … .pdf` |
| `lernfelder/lf02-szenario-a.pdf` | `LF02IT: Szenario A: Freies Szenario \| moodle@ITECH.pdf` |
| `lernfelder/lf03-kursseite.pdf` | `Kurs: Lernfeld 03 IT - Clients in Netzwerke einbinden … .pdf` |
| `lernfelder/lf03-szenario-1.html` | `LF3-D: Szenario 1 \| moodle@ITECH.html` |
| `lernfelder/lf04-kursseite.pdf` | `Kurs: Lernfeld 04 IT - Schutzbedarfsanalyse … .pdf` |
| `lernfelder/lf04-szenario-c.pdf` | `LF04IT: Szenario C \| moodle@ITECH.pdf` |
| `lernfelder/lf05-kursseite.pdf` | `Kurs: Lernfeld 05 IT - Software zur Verwaltung von Daten anpassen … .pdf` |
| `lernfelder/lf05-szenario-b.pdf` | `LF05IT: Szenario B \| moodle@ITECH.pdf` |
| `lernfelder/lf06-kursseite.pdf` | `Kurs: Lernfeld 06 IT - Serviceanfragen bearbeiten … .pdf` |
| `lernfelder/lf07-kursseite.pdf` | `Kurs: Lernfeld 07 IT - Cyber-Physische Systeme ergänzen … .pdf` |
| `lernfelder/lf07-szenario-a.pdf` | `LF07IT: Szenario A \| moodle@ITECH.pdf` |
| `lernfelder/lf07-szenario-b.pdf` | `LF07IT: Szenario B \| moodle@ITECH.pdf` |

## 2. Dateien im Einzelnen

Art: **eigen** = vom Azubi allein verfasst · **Gruppe** = Gruppenportfolio mit Beteiligung ·
**Schule** = Moodle-Seite der Berufsschule · **extern** = fremde Veröffentlichung.
Themen-IDs beziehen sich auf `content/ap1/katalog.yaml`.

### Eigene Lerndokumente

| Datei | Art | Umfang | Lernfeld | Katalog-Themen | Bewertung und Nutzung |
| --- | --- | --- | --- | --- | --- |
| `eigene/netzwerkgrundlagen.pdf` | eigen | 12 S., 21 Grafiken | LF3 | osi-protokolle, ipv4-subnetting, zahlensysteme, netzwerkkomponenten, konsolenbefehle | Stärkstes eigenes Dokument und **Hauptstilvorlage**. Durchgehendes Beispiel (Aufruf von youtube.com) mit Gesamtdiagramm, dann DNS → Subnetzmasken-Check → Routing/NAT → ARP/Switching → Dual-Umrechnung → Subnetting → VLAN. 12 fachliche Befunde (P-10 bis P-21). Kapitel Switching, Routing, Pakete, öffentliche/private IP und NAT sind nur Überschriften. |
| `eigene/projektmanagement.pdf` | eigen | 5 S., 3 Grafiken | LF1/LF3 (übergreifend) | vorgehensmodelle, weitere-vorgehensmodelle (V-Modell) | Zweite Stilvorlage: Diagramm je Modell, Pro/Contra-Tabellen, Vergleichstabelle, „Wann verwende ich was?“. **Scrum-Begriffe mehrfach falsch** (P-30 bis P-38) – wichtig, weil Scrum 2025 ausdrücklich im Katalog steht und der Azubi das Thema selbst als „sicher“ einschätzt. |

### Portfolios (Gruppenarbeiten)

| Datei | Art | Umfang | Lernfeld | Katalog-Themen | Bewertung und Nutzung |
| --- | --- | --- | --- | --- | --- |
| `portfolios/lf01-portfolio-unternehmen.pdf` | Gruppe | 24 S., 2 Grafiken | LF1 | rechtsformen-aufbauorganisation (außerhalb), maerkte-bedarfe, vorgehensmodelle, nachhaltigkeit-energie, epk (außerhalb) | Unternehmensporträt des Ausbildungsbetriebs. Enthält erkennbar KI-generierte Passagen (z. B. „Soll ich Ihnen noch Details … heraussuchen?“, P-54) – **nicht als Stilvorlage** verwenden. Prüfungsnutzen gering: Marktform Oligopol, Rechtsform SE, divisionale/Matrix-Organisation, V-Modell vs. agil. Enthält interne Betriebsdetails – nicht in `content/` übernehmen. |
| `portfolios/lf03-notion/` | Gruppe (Azubi federführend beim Netzwerkteil) | Markdown 24 KB, 13 Bilder, 5 Excel | LF3 | ipv4-subnetting, netzwerkkomponenten, osi-protokolle, kauf-miete-leasing, kalkulation, netzwerk-standards, vorgehensmodelle | Praxisfall Zentralbibliothek: IPAM, VLAN 110/120/210/220, Router-on-a-Stick, DHCP mit IP-Helper, Fehlerprotokoll (9 Fehler, Bottom-up nach OSI), WLAN mit WPA2, Kauf vs. Leasing mit Tilgungsplan. Sehr gute Quelle für Praxisaufgaben. Befunde P-60 bis P-66. Erklärt ausdrücklich „NO AI Prinzip“ → authentischer Stil. |
| `portfolios/lf04-portfolio-schutzbedarfsanalyse.pdf` | Gruppe | 15 S., 4 Grafiken | LF4 | bsi-schutzbedarf, schutzziele, tom, haertung-firewall, epk (außerhalb) | Vollständige Schutzbedarfsanalyse (Strukturanalyse → Schutzbedarfsfeststellung → Modellierung → IT-Grundschutz-Check) mit Maßnahmenkatalog und Awareness-Flyer. Gute Grundlage für IT-Sicherheit. Befunde P-70 bis P-74, darunter ein Konzeptfehler zu den Anforderungsniveaus und eine fehlerhafte EPK. |
| `portfolios/lf05-notion/` | Gruppe | Markdown 11 KB, 5 Bilder | LF5 | erm-relational, sql (entfallen), vorgehensmodelle | Drei ERD-Versionen (Chen-Notation) für „Kraut und Rüben“. ERM ist mit 42 Punkten das zweitstärkste Einzelthema der Auswertung → wertvoll als Übungsmaterial, inklusive der Fehler (P-80 bis P-83). Die SQL-Skripte liegen extern (GitHub `DanceInGold/LF05`) und sind für AP1 entfallen. |
| `portfolios/lf07-notion/` | Gruppe | Markdown 14 KB, 4 Bilder | LF7 | hardware-komponenten (Sensoren), vorgehensmodelle | IoT-Medikamentenspender (Raspberry Pi + Arduino, Sensoren, Aktoren). Technische Aussagen geprüft und korrekt. Für AP1 nur am Rand relevant (Sensoren als Hardwareprodukt, 03.01). Code extern (GitHub `DanceInGold/LF07`). |

### Lernfeld-Seiten der Berufsschule (Moodle)

Alle 12 Seiten wurden als Text und als Seitenbild gesichtet. Sie beschreiben Lernsituationen und
Szenarien, enthalten aber kaum Fachinhalt (die verlinkten Infotheken und Fachmodule fehlen).
Nutzen: Lernfeld-Abgleich (ZI-08), Szenarien als Vorlage für Handlungssituationen (ZI-03).
Die Seiten enthalten Namen und E-Mail-Adressen von Lehrkräften (siehe Abschnitt 8).

| Datei | Lernfeld | Inhalt | Katalog-Bezug |
| --- | --- | --- | --- |
| `lernfelder/lf01-kursseite.pdf` | LF1 Das Unternehmen und die eigene Rolle | Kompetenzbeschreibung, Infotheke-Themen (Nachhaltigkeit, Aufbau/Weisungsbefugnisse, Marktposition, Rechtsformen, SMART-Ziele) | smart-ziele, maerkte-bedarfe, nachhaltigkeit-energie |
| `lernfelder/lf02-szenario-a.pdf` | LF2 Arbeitsplätze nach Kundenwunsch ausstatten | Freies Szenario: eigenes Kundenunternehmen, Arbeitsplatz dimensionieren, anbieten, übergeben | hardware-komponenten, angebotsvergleich, kundenbedarf – **kein eigenes Material zu LF2 vorhanden** |
| `lernfelder/lf03-kursseite.pdf` | LF3 Clients in Netzwerke einbinden | Szenario Zentralbibliothek Hamburg, Playday, Szenario 1/X, Cisco-NetAcad-Hinweis | osi-protokolle, ipv4-subnetting, kauf-miete-leasing |
| `lernfelder/lf03-szenario-1.html` | LF3 | Vollständige Aufgabenstellung Teilhandlung 1–4 + Option Subnetzrechner/IPAM-Datenbank. Bilder sind nur verlinkt (Moodle), nicht enthalten. | ipv4-subnetting, netzwerkkomponenten, kauf-miete-leasing |
| `lernfelder/lf04-kursseite.pdf` | LF4 Schutzbedarfsanalyse | Szenarien A–C, Infotheke (Datenschutz, IT-Grundschutz) | bsi-schutzbedarf, datenschutz |
| `lernfelder/lf04-szenario-c.pdf` | LF4 | Auftrag MooveTeq: EPK „Scooter ausleihen“, Schutzbedarfsanalyse auf BSI-Standardniveau in 4 Schritten, Awareness-Material | bsi-schutzbedarf, schutzziele |
| `lernfelder/lf05-kursseite.pdf` | LF5 Software zur Verwaltung von Daten anpassen | Kunde „Kraut und Rüben“, Szenarien A/B, Leistungsnachweis (ERD, SQL, Präsentation) | erm-relational, datenschutz |
| `lernfelder/lf05-szenario-b.pdf` | LF5 | Aufgabenstellung mit JOINs/Subselect (SQL, entfallen) und DSGVO-Auskunft/Löschung; Ist-ERD als Bild | erm-relational, datenschutz, sql (entfallen) |
| `lernfelder/lf06-kursseite.pdf` | LF6 Serviceanfragen bearbeiten | Lernlandkarte (Ticketsystem optimieren, Kundenservice-Prozess), nur als Bild | support-ki, rollout-ticketsystem – **kein eigenes Material zu LF6 vorhanden** |
| `lernfelder/lf07-kursseite.pdf` | LF7 Cyber-physische Systeme ergänzen | CPS-Definition, Infotheke (Arduino, Break-Even, Pitch) | hardware-komponenten |
| `lernfelder/lf07-szenario-a.pdf` | LF7 | Hackathon-Ablauf, Mindestanforderungen (Sensoren, DB, Break-Even, Pitch auf Englisch) | kalkulation, englische-texte |
| `lernfelder/lf07-szenario-b.pdf` | LF7 | Designwettbewerb Lernräume mit CPS, Design Thinking | – |

### Prüfungsbezogene Quellen

| Datei | Art | Umfang | Bewertung und Nutzung |
| --- | --- | --- | --- |
| `pruefung/katalog-2025-aenderungen-it-berufe-podcast-190.pdf` | extern | 29 S. (Webseite mit 76 Kommentaren) | Gegenüberstellung alter/neuer AP1-Katalog von Stefan Macke. **Nur das Delta, nicht der vollständige Katalog** (der Autor betont das selbst mehrfach). Wichtige Zusatzinfos aus den Kommentaren: Katalogvorwort nennt SQL und RAID „ausschließlich in Teil 2“; Netzplan/Strukturplan/Gantt stehen in 01.01; EPK-Notation steht auf dem gemeinsamen Beiblatt, aber nicht im Katalog; BPMN ist im AP1-Katalog nicht genannt. Grundlage für `katalog.yaml` (Entwurf). |
| `pruefung/vernetzte-systeme-it-infrastruktur-l3-2026.pdf` | fremd (Lehrgangsmaterial, F-02) | 17 Folien | Kompakter Lehrgangsfoliensatz „Vernetzte Systeme & IT-Infrastruktur, 2. Lehrjahr“ mit 8 Lernzielen: Topologien, Netzwerkgeräte, IPv4/IPv6, OSI/TCP-IP, Verfügbarkeit (MTBF/MTTR), USV-Klassen, RAID/NAS/SAN, Hypervisor/Container, 3-2-1-Backup, Patch-Management, ITIL-Incident, Dokumentationsarten, Barrierefreiheit, RBAC/2FA/Härtung, zwei Übungsaufgaben. Fachlich weitgehend korrekt, aber der Titel „PRÜFUNGSRELEVANT … AP1“ stimmt für RAID, SAN und LTE/5G nicht mehr (P-40). |

## 3. Abdeckung des Prüfungskatalogs

Sortiert nach den Clusterpunkten der Prüfungsauswertung (Anforderungsdokument Kap. 2,
11 Prüfungen, 1.097 Punkte). Abdeckung: **gut** = eigenes Material erklärt das Thema ·
**teilweise** = Thema kommt vor, aber lückenhaft oder fehlerhaft · **fehlt** = kein Material.

| Cluster (Punkte) | Themen | Material im Repo | Abdeckung |
| --- | --- | --- | --- |
| Hardware (142) | hardware-komponenten, speicher-hdd-ssd, bios-uefi-dateisysteme, geraeteklassen, installation-einrichtung, cloud-modelle, barrierefreiheit, auslastung-erweiterbarkeit | Nur Randnotizen: Sensoren (LF07), Barrierefreiheit BITV (L3-Folie), Hypervisor/Container (L3) | **fehlt** – größte Lücke |
| Netzwerktechnik (140) | zahlensysteme, ipv4-subnetting, osi-protokolle, netzwerkkomponenten, netzwerk-standards, client-server-domaene, ipv6 | Netzwerkgrundlagen, LF03-Portfolio, L3-Folien, LF3-Szenario | **gut** für IPv4/Subnetting/DNS/ARP/VLAN/DHCP · **teilweise** IPv6 (nur Folie) · **teilweise** Ethernet/WLAN (nur WPA2 und 100-m-Grenze im LF03-Fall) · **fehlt** Domänenbeitritt, LWL |
| IT-Sicherheit (132) | schutzziele, bsi-schutzbedarf, tom, haertung-firewall, authentifizierung, verschluesselung, verfuegbarkeit-backup, isms-risiko | LF04-Portfolio, L3-Folien (RBAC, 2FA, Härtung, 3-2-1, USV) | **gut** Schutzbedarfsanalyse/Schutzziele · **teilweise** 2FA, Härtung, Backup · **fehlt** Verschlüsselung (symm./asymm./hybrid), Hash, Zertifikat, Signatur, ISMS, Risikomatrix |
| Softwareentwicklung (120) | pseudocode, schreibtischtest, oop-grundlagen, skriptsprachen, masken-ergonomie | – (LF03-Option „Subnetzrechner“ nur als Aufgabenstellung) | **fehlt** – Schreibtischtest allein 41 Punkte |
| Projektmanagement (104) | vorgehensmodelle, projekt-merkmale, smart-ziele, projektplanung, teambildung, lasten-pflichtenheft | Projektmanagement-Dokument, alle Portfolios (Scrum-Praxis) | **teilweise**: Wasserfall/Scrum vorhanden, aber Scrum-Events falsch (P-31 ff.) · **fehlt** Netzplan (35 P.), Gantt, PSP, SMART, Projektmerkmale, Lasten-/Pflichtenheft |
| Datenbanken (81) | erm-relational | LF05-Portfolio (3 ERD-Versionen), LF05-Szenario B | **teilweise**: ERDs vorhanden, aber mit Modellierungsfehlern (P-80 ff.); Kardinalitäten, Normalisierung, Schlüssel nicht erklärt |
| Wirtschaftlichkeit (78) | kalkulation, wirtschaftlichkeit, kauf-miete-leasing, stamm-bewegungsdaten, nachhaltigkeit-energie | LF03 Kauf vs. Leasing mit Tilgungsplan | **teilweise** Leasing · **fehlt** Kosten berechnen (33 P.), Amortisation, Stromkosten |
| Angebotsvergleich (77) | angebotsvergleich | – | **fehlt** – Nutzwertanalyse ist mit 45 Punkten das punktstärkste Einzelthema |
| Kundenberatung/Präsentieren (72) | kundenbedarf, praesentation, englische-texte, suchoperatoren | LF02-Szenario (nur Aufgabe) | **fehlt** |
| Multimedia (51) | datenmengen-uebertragung, kommunikationssysteme | – (Dual-Umrechnung als Grundlage in Netzwerkgrundlagen) | **fehlt** – Dateigrößen berechnen 29 Punkte |
| Datenschutz (22) | datenschutz | LF04-Flyer (DSGVO kurz), LF05-Szenario B (Auskunft/Löschung als Aufgabe) | **teilweise** |
| Märkte und Bedarfe (21) | maerkte-bedarfe | LF01-Portfolio (Marktformen am Beispiel) | **teilweise** |
| Verträge (15) | vertraege, urheberrecht-lizenzen | – | **fehlt** |
| Leistungserbringung (14) | qualitaet, rollout-ticketsystem, abnahme-doku, leistungsbestaetigung | L3-Folien (ITIL-Incident, Dokumentationsarten), LF03-Fehlerprotokoll | **teilweise** |
| Kundenbeziehungen (9) | support-ki | LF01 (ServiceNow als Beispiel), LF06-Lernlandkarte | **fehlt** inhaltlich |
| UML (9) | uml | – | **fehlt** – Aktivitätsdiagramm 2025 neu |
| Betriebssysteme (4) | betriebssysteme, konsolenbefehle | Netzwerkgrundlagen (`ipconfig /all`), LF03 (`show running-config`) | **teilweise** |
| Software (4) | software-arten | LF01 (Beispiele ERP/SCM/Cloud im Betrieb) | **teilweise** |

**Bilanz:** Von 60 aktiven bzw. neuen Themen in `katalog.yaml` sind 6 gut, 18 teilweise und 36
gar nicht durch eigenes Material abgedeckt (Liste je Thema in Anhang A). Die fehlenden Themen erstellt Claude laut Entscheidung
(Kap. 12) neu im Stil der eigenen Dokumente.

## 4. Lücken nach Priorität

Reihenfolge nach Punkten der Einzelthemen bzw. Cluster und nach Abhängigkeiten:

1. **Nutzwertanalyse / Angebotsvergleich** (45 P. Einzelthema) – fehlt komplett.
2. **Schreibtischtest, Pseudocode, Fehler im Code finden** (41 P.) – fehlt; Voraussetzung: Kontrollstrukturen.
3. **Hardware-Grundlagen** (Cluster 142 P.): CPU, RAM, Mainboard, Schnittstellen, HDD/SSD, Netzteil, Monitore/Anschlüsse, Geräteklassen, BIOS/UEFI, Dateisysteme. Im Betrieb kaum Praxis (Anforderungsdokument Kap. 3) → Schemata und Zuordnungsaufgaben.
4. **Netzplan, Gantt, Projektstrukturplan** (35 P.) – fehlt.
5. **Kosten berechnen, Amortisation, Stromkosten** (33 P.) – fehlt; Kauf/Leasing vorhanden.
6. **Dateigrößen und Übertragungszeiten** (29 P.) – fehlt; passt zum Betriebsalltag (Archivierung großer Datenmengen).
7. **IPv6** (28 P.) – nur eine Folie.
8. **Verschlüsselung, Hash, Zertifikate, Signaturen** – 2025 neu präzisiert, fehlt.
9. **UML-Aktivitätsdiagramm, Use-Case, Klassendiagramm** – fehlt.
10. **Domänenbeitritt, Client-Server, Konsolenbefehle** – fehlt bzw. nur angerissen.
11. **DSGVO-Betroffenenrechte, Anonymisierung/Pseudonymisierung** – 2025 neu, nur angerissen.
12. **Verträge und Vertragsstörungen, Abnahme, Mängelarten** – fehlt.
13. **Support-Level, Ticketsystem, KI-Unterstützung** – fehlt (LF6 ohne eigenes Material).
14. **SMART, Projektmerkmale, Lasten-/Pflichtenheft, Stamm-/Bewegungsdaten** – fehlt.
15. **Englische Fachtexte, Suchoperatoren, Präsentation** – fehlt.

## 5. Dopplungen

| Thema | Vorkommen | Umgang |
| --- | --- | --- |
| IPv4, Subnetting, Dual-Umrechnung | Netzwerkgrundlagen, L3-Folien (Formel + Übungsaufgabe), LF03-Portfolio (Praxis /25-Netze) | Netzwerkgrundlagen als Erklärbasis, L3-Aufgabe und LF03-IPAM als Übungen |
| Scrum / agiles Arbeiten | Projektmanagement-Dokument, Portfolios LF01, LF03, LF04, LF05, LF07 | Eine Lektion nach Scrum Guide; Portfolios liefern Praxisbeispiele, ihre Begriffsfehler werden zu Fehlerkarten (ZI-05) |
| Schutzziele, Härtung, 2FA | LF04-Portfolio, L3-Folien | LF04 als Praxisfall, L3 als Kurzübersicht |
| EPK | LF04-Portfolio, LF01-Portfolio, LF04-Szenario | Beide Diagramme fehlerhaft (P-50, P-72) – EPK nur als Beiblatt-Notation, geringe Gewichtung |
| ERD | drei Versionen in LF05 | Nur V3 verwenden, V1/V2 als Vergleich „was hat sich geändert“ |

## 6. Entfallene Themen im Material

Diese Inhalte sind seit dem Katalog 2025 nicht mehr AP1-relevant und bekommen Gewicht 0:

| Thema | Wo im Material |
| --- | --- |
| RAID, SAN | L3-Folien (Lernziel 8, RAID-Tabelle, Visualisierung, Übungsaufgabe 2 Teilaufgabe 1) |
| LTE/5G (WWAN) | L3-Folien (Netzwerk-Reichweiten) |
| SQL | LF05-Szenario B (JOINs, Subselect), LF05-Portfolio (Sprints 2–3), LF03-Szenario Option B |
| V-Modell (weitere Vorgehensmodelle) | Projektmanagement-Dokument, LF01-Portfolio |
| Virtuelle Server (2025 auf „virtuelle Desktops“ eingegrenzt) | L3-Folien (Hypervisor Typ 1/2) – Container/VM-Vergleich bleibt als Hintergrund nützlich |
| Rechtsformen, Aufbauorganisation (laut Podcast nur AP2) | LF01-Portfolio, LF01-Kursseite |

## 7. Technische Hinweise für die Pipeline

- **Transparente PNGs:** Die drei ERD-Bilder in LF05 sind im Dark-Mode von draw.io exportiert –
  Linien und Kardinalitäten sind weiß auf transparentem Grund und auf weißem Hintergrund
  unsichtbar. Beim Sichten auf dunklem Hintergrund rendern (in CLAUDE.md aufgenommen; Kandidat
  für den Vorab-Check MA-03).
- **Defekte PDF-Querverweise:** Alle Moodle-Drucke erzeugen „xref“-Warnungen; Text ist trotzdem
  vollständig lesbar. Das Skript unterdrückt die Meldungen.
- **HTML ohne Bilder:** `lf03-szenario-1.html` verweist auf Bilder auf dem Moodle-Server; sie
  fehlen im Repo.
- **Inhalte nur als Bild:** LF06-Lernlandkarte, Netzwerkdiagramme, Scrum-Grafiken, Ist-ERD in
  LF05-Szenario B – die Textextraktion allein reicht nicht.
- **Excel-Anhänge:** 5 Dateien in LF03; das Inventurskript extrahiert sie jetzt als Text
  (openpyxl). Ein Format `.xlsx` ist in Kap. 12 nicht als Repo-Format genannt, kommt aber vor.
- **Externe Verweise ohne Inhalt im Repo:** GitHub `DanceInGold/LF05` (SQL) und `DanceInGold/LF07`
  (Code), Google-Drive-Ordner, Trello-Board, Notion-Unterseiten (Stand-ups, Retros, Tabellenschema).

## 8. Personenbezogene Daten (vor einer Veröffentlichung bereinigen)

Das Repo ist privat und darf laut Kap. 12 alles enthalten. Für die spätere Veröffentlichung ist
vorgemerkt:

- Moodle-Seiten: Namen und E-Mail-Adressen von Lehrkräften.
- Portfolios: Vornamen von Mitschüler:innen, Reflexionstexte, Selbsteinschätzungen.
- LF01-Portfolio: interne Systemnamen und Abläufe des Ausbildungsbetriebs.
- LF03-Portfolio: WLAN-Schlüssel des Übungsszenarios (fiktiv, unkritisch).

In `content/` wird nichts davon übernommen (CLAUDE.md, Abschnitt „Betrieblicher Kontext“).

## 9. Offene Fragen

| ID | Frage | Warum wichtig |
| --- | --- | --- |
| F-01 | ✔ Bestellt, wird nachgereicht und dann integriert. – Gibt es den **vollständigen Prüfungskatalog 2025** (U-Form, ca. 7 €) als PDF oder Scan? | Im Repo liegt nur das Delta. Ohne den Katalog bleiben unveränderte Unterpunkte in `katalog.yaml` unvollständig, Ziel 1 („jedes Katalogthema abgedeckt“) ist nicht prüfbar. Alternative: öffentliche Themenliste des IT-Berufe-Podcasts als Ersatzquelle. |
| F-02 | ✔ Nicht selbst erstellt, keine Stilvorlage (E-11). – Ist `vernetzte-systeme-it-infrastruktur-l3-2026.pdf` **selbst erstellt** oder Material einer Lehrkraft/eines Lehrgangs? | Entscheidet, ob die Folien als Stilvorlage zählen und unter `eigene/` gehören. |
| F-03 | ✔ BPMN als freiwilliges Zusatzthema, Anforderungsdokument korrigiert (E-10). – Soll die Aussage „BPMN neu im Katalog 2025“ im Anforderungsdokument korrigiert werden (P-01)? | Sonst bekäme BPMN ein Mindestgewicht ohne Beleg. |
| F-04 | ✔ Eigenes Material ist nur Kontext; alle Lektionen werden neu geschrieben (E-09). – Gibt es eigene Notizen zu **LF2 und LF6** oder Unterlagen zu Hardware, Kalkulation, Nutzwertanalyse, Programmierung? | Genau dort liegen die größten Lücken; eigenes Material hätte Vorrang vor neu erstellten Lektionen. |

## Anhang A: Abdeckung je Thema

| Thema (ID) | Bereich | Stand 2025 | Abdeckung durch eigenes Material |
| --- | --- | --- | --- |
| Merkmale eines Projekts (`projekt-merkmale`) | b01 | neu | fehlt |
| SMART-Prinzip (`smart-ziele`) | b01 | neu | fehlt |
| Projektphasen: Wasserfallmodell und Scrum (`vorgehensmodelle`) | b01 | neu | teilweise |
| Phasen der Teambildung und -entwicklung (`teambildung`) | b01 | aktiv | fehlt |
| Projektplanung: Strukturplan, Netzplan, Gantt-Diagramm (`projektplanung`) | b01 | aktiv | fehlt |
| Machbarkeit und Wirtschaftlichkeit (z. B. Amortisation) (`wirtschaftlichkeit`) | b01 | neu | fehlt |
| Kosten berechnen, Vor- und Nachkalkulation (`kalkulation`) | b01 | aktiv | teilweise |
| Stammdaten und Bewegungsdaten (`stamm-bewegungsdaten`) | b01 | neu | fehlt |
| Support-Level (First/Second/Third) und KI-Unterstützung (`support-ki`) | b01 | neu | fehlt |
| Quantitative und qualitative Angebotsbewertung (Nutzwertanalyse) (`angebotsvergleich`) | b02 | neu | fehlt |
| Kundenbedarf ermitteln, situationsgerechte Kommunikation (`kundenbedarf`) | b02 | aktiv | fehlt |
| Technische und kaufmännische Texte auf Englisch (`englische-texte`) | b02 | aktiv | fehlt |
| Digitale Suchabfragen mit Suchoperatoren (`suchoperatoren`) | b02 | aktiv | fehlt |
| Präsentation und Medienkompetenz (`praesentation`) | b02 | aktiv | fehlt |
| Märkte und Bedarfe (`maerkte-bedarfe`) | b02 | aktiv | teilweise |
| Zahlensysteme (dual, hexadezimal), Einheiten und Präfixe (`zahlensysteme`) | b03 | aktiv | gut |
| Hardwareprodukte: CPU, Mainboard, RAM, Netzteil, Grafikkarte, Peripherie, Sensoren (`hardware-komponenten`) | b03 | aktiv | fehlt |
| Datenspeicher HDD und SSD (`speicher-hdd-ssd`) | b03 | neu | fehlt |
| BIOS/UEFI-Einstellungen, Dateisysteme (FAT32, NTFS, APFS, ext4) (`bios-uefi-dateisysteme`) | b03 | aktiv | fehlt |
| Standard-, Branchen- (ERP, SCM, CRM), System-, Entwicklungs- und KI-Software (`software-arten`) | b03 | neu | teilweise |
| Cloudlösungen: SaaS, IaaS, PaaS, DaaS; virtuelle Desktops (`cloud-modelle`) | b03 | aktiv | fehlt |
| Kommunikationssysteme: Videokonferenz, Social Media (`kommunikationssysteme`) | b03 | neu | fehlt |
| Netzwerkkomponenten: Router, Switch, Accesspoint, Gateway (`netzwerkkomponenten`) | b03 | aktiv | gut |
| OSI-Modell und Netzwerkprotokolle (Ethernet, IP, DNS, …) (`osi-protokolle`) | b03 | aktiv | gut |
| IPv4-Adressierung und Subnetting (`ipv4-subnetting`) | b03 | neu | gut |
| IPv6-Adressierung (`ipv6`) | b03 | neu | teilweise |
| Client-Server-Systeme, Einbindung eines Clients in eine Domäne (`client-server-domaene`) | b03 | neu | fehlt |
| Ethernet- und WLAN-Standards, LWL (`netzwerk-standards`) | b03 | aktiv | teilweise |
| Barrierefreiheit: Arbeitsplatz, IT-Systeme, Websites (`barrierefreiheit`) | b03 | neu | teilweise |
| Übertragungsraten, -zeiten und Datenmengen berechnen (Bild, Video, Dokument) (`datenmengen-uebertragung`) | b03 | neu | fehlt |
| Auslastung, Erweiterbarkeit, Zukunftssicherheit (`auslastung-erweiterbarkeit`) | b03 | aktiv | fehlt |
| Ökologische Aspekte: Energieverbrauch, Stromkosten, Recycling (`nachhaltigkeit-energie`) | b03 | aktiv | teilweise |
| Lasten- und Pflichtenheft (Zweck, Urheber, Inhalt) (`lasten-pflichtenheft`) | b04 | aktiv | fehlt |
| Installation: Betriebssystem, Partitionierung, IP-Konfiguration, Remote-Desktop (`installation-einrichtung`) | b04 | aktiv | fehlt |
| Geräteklassen: Desktop, Notebook, All-in-One, Thin Client, Tablet, Smartphone (`geraeteklassen`) | b04 | aktiv | fehlt |
| Betriebssysteme: Einsatzzweck, Dateimanagement, Freigaben (`betriebssysteme`) | b04 | aktiv | fehlt |
| Schutz der Urheber, Lizenzen (`urheberrecht-lizenzen`) | b04 | aktiv | fehlt |
| Konsolenbefehle: Dateien und Netzwerk-Troubleshooting (ipconfig, ip, ping, nslookup, …) (`konsolenbefehle`) | b04 | neu | teilweise |
| Klassen, Attribute, Objekte, Methoden, Sichtbarkeit (`oop-grundlagen`) | b04 | neu | fehlt |
| Skriptsprachen, z. B. Shell-Skript (`skriptsprachen`) | b04 | aktiv | fehlt |
| Kontrollstrukturen in Pseudocode (`pseudocode`) | b04 | neu | fehlt |
| UML: Anwendungsfall-, Klassen-, Aktivitätsdiagramm (`uml`) | b04 | neu | fehlt |
| Bildschirmmasken: Softwareergonomie, Corporate Identity, Barrierefreiheit (`masken-ergonomie`) | b04 | aktiv | fehlt |
| Fehler in Quellcode finden, Schreibtischtest (`schreibtischtest`) | b04 | neu | fehlt |
| Grundlagen relationaler Datenbanken, einfache ER-Modelle (`erm-relational`) | b04 | neu | teilweise |
| Qualitätsmaßnahmen, Testprotokoll für das Einrichten eines Arbeitsplatzes (`qualitaet`) | b05 | aktiv | teilweise |
| Schutzziele Vertraulichkeit, Integrität, Verfügbarkeit (`schutzziele`) | b06 | neu | gut |
| Technisch-organisatorische Maßnahmen; IT-Sicherheits- vs. Datenschutzbeauftragter (`tom`) | b06 | neu | teilweise |
| Symmetrische, asymmetrische, hybride Verschlüsselung; Hash, Zertifikat, Signatur (`verschluesselung`) | b06 | neu | fehlt |
| Authentifizierung (2FA), Passwort-Policy bewerten (`authentifizierung`) | b06 | neu | teilweise |
| Härtung von Betriebssystemen, Personal Firewall (`haertung-firewall`) | b06 | neu | teilweise |
| Sicherung der Verfügbarkeit (z. B. NAS, Datensicherung) (`verfuegbarkeit-backup`) | b06 | aktiv | teilweise |
| Schutzbedarfsanalyse nach BSI IT-Grundschutz, Schutzbedarfskategorien (`bsi-schutzbedarf`) | b06 | neu | gut |
| ISMS kennen und unterstützen, Risiko-Matrix (`isms-risiko`) | b06 | neu | fehlt |
| DSGVO/BDSG-Grundzüge, Betroffenenrechte, Einwilligung, Anonymisierung/Pseudonymisierung (`datenschutz`) | b06 | neu | teilweise |
| Vertragsbestandteile, Vertragsstörungen (`vertraege`) | b07 | aktiv | fehlt |
| Kauf, Miete, Leasing (`kauf-miete-leasing`) | b07 | aktiv | teilweise |
| Rolloutprozesse, Ticketsystem, Budget (`rollout-ticketsystem`) | b07 | aktiv | fehlt |
| Abnahmeprotokoll, zu übergebende Dokumentation, Schlecht-/Falsch-/Minderlieferung (`abnahme-doku`) | b07 | aktiv | teilweise |
| Bestätigung erbrachter Leistungen, Nachkalkulation, Folgeaufträge (`leistungsbestaetigung`) | b07 | aktiv | fehlt |
