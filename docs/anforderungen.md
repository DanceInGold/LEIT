<!--
Quelle: Claude-Docs-Dokument „Anforderungsdokument: AP1-Lernbegleiter (FiSi)“
(https://claude.ai/artifact/VS2sfZBYyzcw3F5hADq8Qk), Stand Version 0.2 vom 12.11.2026,
exportiert am 12.11.2026. Die drei eingebetteten Grafiken sind als Text/Tabelle wiedergegeben.
Inhaltliche Korrekturen werden nicht hier still eingearbeitet, sondern in docs/pruefprotokoll.md
festgehalten (P-01 zu BPMN ist seit 12.11.2026 hier und im Original korrigiert).
-->

# Anforderungsdokument: AP1-Lernbegleiter (FiSi)

Nov 12, 2026 · @Thies · Version 0.2 (Entwurf)

## 1. Ausgangslage, Vision und Ziele

Der AP1-Lernbegleiter führt einen FiSi-Azubi über 8 bis 12 Wochen strukturiert bis zum Bestehen der AP1 – mit Erklärungen, die das Wie und Warum vorwegnehmen, aufsteigenden Übungen, Wiederholung nach Plan und sichtbarem Lernstand.

**Ausgangslage:** Aus zwei Lehrjahren liegen eigene Lerndokumente, die Lernfelder der Berufsschule und der seit 2025 gültige Prüfungskatalog in einem Git-Repository vor. Diese Inhalte sind verstreut, nicht geprüft und nicht nach Prüfungsrelevanz geordnet.

**Vision:** Ein persönlicher Lerncoach, der weiß, was in der Prüfung drankommt, was der Azubi schon kann, was er vergisst – und der jeden Tag sagt, was heute sinnvoll ist.

**Ziele (messbar):**

1. Jedes Thema des Prüfungskatalogs ist im Tool abgedeckt und einem Lernabschnitt zugeordnet.
2. Der Azubi erreicht vor der Prüfung in mindestens zwei vollständigen Prüfungssimulationen mindestens 92 von 100 Punkten (Zielwert, entspricht "sehr gut"; anpassbar).
3. Jeder Lernbaustein beantwortet ausdrücklich: Was ist das? Wie funktioniert es? Warum ist es so? Wofür brauche ich es im Betrieb?
4. Die Architektur erlaubt, AP2 (FiSi-Fachrichtung, später ggf. WiSo) als weiteres Inhaltspaket zu ergänzen, ohne den Kern umzubauen.

**Nicht-Ziele (Version 1):** Mehrbenutzerbetrieb mit Accounts, Bewertung durch Ausbilder, Ersatz für offizielle Prüfungsunterlagen, KI-Tutor. Spätere Jahrgänge nutzen das Tool mit einer eigenen Installation und eigenem Prüfungstermin.

## 2. Prüfungsrahmen AP1

Die AP1 "Einrichten eines IT-gestützten Arbeitsplatzes" ist eine schriftliche Prüfung von 90 Minuten, zählt 20 % zur Gesamtnote und ist für alle IT-Berufe identisch. Das Tool richtet Umfang, Zeitdruck und Aufgabenstil daran aus.

| Merkmal | Wert | Konsequenz für das Tool |
| --- | --- | --- |
| Prüfungsbereich | Einrichten eines IT-gestützten Arbeitsplatzes ([§ 9 FIAusbV](https://www.gesetze-im-internet.de/fiausbv/__9.html)) | Inhalte nach Berufsbildpositionen 1–7 und Prüfungskatalog ordnen |
| Dauer | 90 Minuten | Simulationen mit echtem Timer |
| Gewichtung | 20 % der Gesamtnote | Ziel- und Fortschrittsanzeige in Punkten |
| Aufgabenart | schriftlich, ungebundene (offene) Aufgaben | Freitext-, Rechen- und Zuordnungsaufgaben statt nur Multiple Choice |
| Gültigkeit | identisch für alle IT-Berufe | AP1-Paket ist berufsunabhängig, AP2-Pakete berufsspezifisch |
| Prüfungskatalog | seit 2025 geänderte Fassung (U-Form) | Katalog aus dem Repo ist die maßgebliche Themenquelle |

Quellen: [IHK Schwaben](https://www.ihk.de/schwaben/produktmarken/meine-pruefung/ausbildungspruefungen/pruefungen-a-z/fachinformatiker-ab-2020-5113338), [IHK Hagen](https://www.ihk.de/hagen/bildung/abschlusspruefungen/it-berufe-index-812540), [DIHK-Umsetzungshilfe (IHK München)](https://www.ihk-muenchen.de/Bildung/DiPa/Dokumente/4_IT-Berufe_DIHK-Umsetzungshilfe.pdf), [U-Form Prüfungstrainer](https://shopstage.u-form.de/media/dd/9f/63/1687157302/750.pdf). Der Prüfungstermin ist im Tool frei einstellbar, damit auch spätere Jahrgänge es nutzen können. Für den ersten Nutzer ist es der 24.02.2027; ab heute bleiben damit knapp 15 Wochen.

### Themengewichtung aus bisherigen Prüfungen

Die IHK veröffentlicht keine offizielle Gewichtung; das Tool stützt sich deshalb auf die [Auswertung aller 11 AP1-Prüfungen von Herbst 2021 bis Herbst 2026 durch den IT-Berufe-Podcast](https://it-berufe-podcast.de/vorbereitung-auf-die-ihk-abschlusspruefung-der-it-berufe/themen-der-schriftlichen-ihk-pruefungen-der-it-berufe/).

**Grafik: Drei Themencluster bringen gut ein Drittel der AP1-Punkte** (IT-Berufe-Podcast, Auswertung von 11 AP1-Prüfungen, Herbst 2021 bis Herbst 2026; Punkte je Cluster)

| Cluster | Punkte |
| --- | ---: |
| Hardware | 142 |
| Netzwerktechnik | 140 |
| IT-Sicherheit | 132 |
| Softwareentwicklung | 120 |
| Projektmanagement | 104 |
| Datenbanken | 81 |
| Wirtschaftlichkeit | 78 |
| Angebotsvergleich | 77 |
| Kundenberatung/Präsentieren | 72 |
| Multimedia | 51 |
| Datenschutz | 22 |
| Märkte und Bedarfe | 21 |
| Verträge | 15 |
| Leistungserbringung | 14 |
| Kundenbeziehungen | 9 |
| UML | 9 |
| Betriebssysteme | 4 |
| Software | 4 |
| Algorithmen | 2 |
| **Summe** | **1.097** |

Hardware kam in allen 11 Prüfungen vor, Netzwerktechnik, Softwareentwicklung und Wirtschaftlichkeit in je 10. Datenschutz bringt wenig Punkte, kommt aber in 7 von 11 Prüfungen vor und ist damit schnell verdiente Punkte. Die punktstärksten Einzelthemen sind Nutzwertanalyse (45), ERM (42), Schreibtischtest (41), Netzplan (35), Kosten berechnen (33), Dateigrößen berechnen (29) und IPv6 (28).

**Korrektur für den Katalog 2025:** Nur 4 der 11 Prüfungen (ab Frühjahr 2025) folgen dem neuen Katalog. SQL, Struktogramm, Programmablaufplan und RAID sind entfallen, KI-Grundlagen neu hinzugekommen; BPMN steht nicht im Katalog und wird als freiwilliges Zusatzthema mit kleinem Gewicht geführt (Entscheidung 12.11.2026, Prüfprotokoll P-01) ([Übersicht der Änderungen](https://ap1-trainer-pro.de/wissen/ap1-pruefung-2025-aenderungen/), [IT-Berufe-Podcast #190](https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/)). Das Tool rechnet deshalb so: Gewicht = Punkteanteil des Themas, Prüfungen ab 2025 zählen doppelt, entfallene Themen zählen null, neue Themen bekommen ein Mindestgewicht. Die Gewichte stehen in `katalog.yaml` und werden nach jeder neuen Prüfung aktualisiert; der Abgleich mit dem Prüfungskatalog im Repo erfolgt bei der Inventur.

## 3. Zielgruppe und Lernstil-Anpassung

Primärnutzer ist ein FiSi-Azubi im 3. Halbjahr, der Themen bis zum Grund auflösen will und lieber versteht als auswendig lernt. Das Tool passt sich an ein Lernstil-Profil an, das aus den eigenen Lerndokumenten abgeleitet und im Betrieb laufend nachgeschärft wird.

**Annahmen zum Nutzer (aus der Anfrage, zu bestätigen anhand des Repos):**

- Lernt über Ursache-Wirkung-Ketten: erst das Warum, dann das Detail.
- Löst Themen vollständig auf, statt Teilwissen stehen zu lassen.
- Lernt neben Betrieb und Berufsschule, also in Einheiten von etwa 30–60 Minuten.

**Betrieblicher Kontext:** Ausbildung bei Airbus im Team Inact von AIRINA (Airbus Enterprise Information Archiving, Archivierung u. a. von Konstruktionsplänen).

- Alltag: Automatisierung über Pipelines mit Python, Jenkins, GitHub, Docker-Images, Artifactory und OpenShift auf Red Hat Enterprise Linux.
- Selten: Verwaltung eigener Server und Anschluss von KVM-Switches und KVM-LCD-Konsolen im Rechenzentrum; hier gibt es bisher kaum Praxis.

**Folgen für das Tool:**

- Praxisbeispiele knüpfen, wo es passt, an diesen Alltag an: Linux-Server, Container, Pipelines, Rechenzentrum, Archivierung großer Datenmengen (z. B. Speicherbedarf und Übertragungszeiten von Konstruktionsplänen).
- Der klassische Büro-Arbeitsplatz, um den es in der AP1 geht (Windows-Client, Domänenbeitritt, Peripherie, Monitoranschlüsse, Ergonomie), kommt im Betrieb kaum vor und bekommt deshalb mehr Erklärung und Übung. Hardware ist zugleich der punktstärkste Cluster (Kap. 2).
- Hardware-Themen ohne Praxisgelegenheit werden über Bilder, Schemata und Zuordnungsaufgaben anschaulich gemacht, z. B. Rack-Aufbau, Anschlüsse, KVM-Verkabelung.
- Beispiele nutzen eine fiktive Firma nach diesem Muster und keine internen Airbus-Details, damit das Repo später ohne Nacharbeit öffentlich werden kann.

**Lernstil-Profil (konfigurierbare Parameter):**

| Parameter | Ausprägungen | Wirkung im Tool |
| --- | --- | --- |
| Erklärtiefe | kompakt · standard · vollständig aufgelöst | Wie viele Warum-Ebenen eine Erklärung standardmäßig zeigt |
| Einstieg | Praxisbeispiel zuerst · Theorie zuerst | Reihenfolge der Bausteine einer Lektion |
| Darstellung | Text · Diagramm · Tabelle · Analogie | Bevorzugte Form; andere bleiben aufklappbar |
| Aufgabenmix | rechnen · erklären · zuordnen | Gewichtung der Aufgabentypen in Sessions |
| Session-Länge | 15 · 30 · 45 · 60 Min. | Größe der Tagesration |
| Hilfeverhalten | früh Tipps · erst selbst probieren | Ab wann Hinweise angeboten werden |

**Anforderungen:**

- LS-01: Beim ersten Start wird das Profil per kurzem Fragebogen (unter 3 Minuten) vorbelegt.
- LS-02: Ein Analyse-Schritt wertet die Lerndokumente im Repo aus (Gliederungstiefe, Anteil Diagramme/Tabellen, Beispiele, Eselsbrücken) und schlägt Profilwerte vor.
- LS-03: Das Profil passt sich an: Werden Vertiefungen oft aufgeklappt, steigt die Standard-Erklärtiefe; werden Tipps oft vor dem ersten Versuch geöffnet, wird das Hilfeverhalten angepasst.
- LS-04: Jede Änderung des Profils ist sichtbar und manuell überschreibbar.

## 4. Funktionale Anforderungen

Neun Module bilden den Funktionsumfang; "Muss" ist Version 1.0, "Soll" folgt bis zur Prüfung, "Kann" danach. Jede Anforderung hat eine ID, auf die Issues und Commits im Repo verweisen.

### 4.1 Lernplan und Lernablauf (LP)

| ID | Anforderung | Prio |
| --- | --- | --- |
| LP-01 | Nutzer gibt Prüfungsdatum und Lernbudget an: Preset 15, 20 oder 30 Stunden pro Woche oder ein freier Wert, verteilt auf selbst gewählte Lerntage; lernfreie Zeiten (Urlaub, Feiertage) sind eintragbar. Das Tool erzeugt rückwärts einen Wochenplan bis zur Prüfung. Prüfungsdatum und Budget sind jederzeit änderbar; das Datum ist aus einer Terminliste im Inhaltspaket vorbelegt, damit jeder Jahrgang das Tool nutzen kann. | Muss |
| LP-02 | Ein Einstufungstest (ca. 20 Min.) misst den Startstand je Themengebiet; bekannte Themen werden im Plan verkürzt. | Muss |
| LP-03 | Themen werden nach Abhängigkeiten geordnet (z. B. Zahlensysteme vor Subnetting, OSI-Modell vor Protokollen). | Muss |
| LP-04 | Der Plan hat drei Phasen: Aufbau (ca. 60 %), Vertiefung und Mischtraining (ca. 25 %), Prüfungsmodus (ca. 15 %). | Muss |
| LP-05 | Eine Startseite "Heute" zeigt die Tagesration: fällige Wiederholungen, neue Lektion, Übungsblock. | Muss |
| LP-06 | Verpasste Tage verschieben den Plan automatisch; das Tool warnt, wenn das Ziel nicht mehr realistisch ist, und schlägt Kürzungen nach Prüfungsrelevanz vor. | Muss |
| LP-07 | Themen werden nach ihrem Punkteanteil in bisherigen Prüfungen gewichtet (Regel siehe Kap. 2, Themengewichtung); wichtigere Themen bekommen mehr Übungszeit und frühere Wiederholungen. | Muss |
| LP-08 | **Aufwandsschätzung:** Jedes Thema hat in `katalog.yaml` einen geschätzten Lernaufwand in Stunden (Erarbeiten + Üben), abgeleitet aus Umfang, Schwierigkeit und Gewichtung; Wiederholungen werden als Zuschlag eingerechnet. | Muss |
| LP-09 | **Machbarkeitsprüfung:** Beim Start und bei jeder Änderung vergleicht das Tool die benötigten Stunden (offene Themen nach Einstufung) mit den verfügbaren Stunden bis zur Prüfung und zeigt Puffer oder Fehlbetrag, mit konkretem Vorschlag (Budget erhöhen oder Themen nach Gewichtung kürzen). | Muss |
| LP-10 | **Zeitplan-Ampel:** Wöchentlicher Soll-Ist-Vergleich von Themen und Stunden mit Status "im Plan", "knapp" oder "im Verzug" und einer Prognose, ob das aktuelle Tempo bis zur Prüfung reicht. | Muss |
| LP-11 | **Kalibrierung:** Die tatsächliche Lernzeit je Thema wird gemessen; weicht sie dauerhaft von der Schätzung ab, passt das Tool die Schätzungen der restlichen Themen an (z. B. Faktor 1,3). | Soll |

### 4.2 Lerninhalte und Erklärungen (LI)

| ID | Anforderung | Prio |
| --- | --- | --- |
| LI-01 | Jede Lektion folgt dem Raster: Worum geht es? → Wie funktioniert es? → Warum ist es so? → Praxisbezug im Betrieb → typische Prüfungsfalle → Merksatz. | Muss |
| LI-02 | Erklärungen sind in Schichten aufklappbar ("Warum?" öffnet die nächste Ebene), bis zum Grundprinzip. | Muss |
| LI-03 | Jede Lektion nennt Voraussetzungen und verlinkt sie. | Muss |
| LI-04 | Fachbegriffe im Text sind mit dem Glossar verknüpft (Tooltip + Link). | Muss |
| LI-05 | Diagramme, Tabellen und Analogien je nach Lernstil-Profil. | Soll |
| LI-06 | Jede Lektion trägt Quelle und Prüfstatus (geprüft · ungeprüft · korrigiert). | Muss |

### 4.3 Fachwort-Kompendium (GL)

| ID | Anforderung | Prio |
| --- | --- | --- |
| GL-01 | Glossar mit Begriff, Abkürzung ausgeschrieben, Kurzdefinition (1 Satz), Erklärung, Beispiel, verwandten Begriffen, Themengebiet. | Muss |
| GL-02 | Lernkarten-Modus (Begriff ↔ Definition, Abkürzung ↔ Langform) mit Wiederholung nach Plan. | Muss |
| GL-03 | Merklisten zum Auswendiglernen: Ports, OSI-Schichten, RAID-Level, Einheiten und Präfixe, Schutzziele. | Muss |
| GL-04 | Volltextsuche und Filter nach Themengebiet und Lernstand. | Muss |
| GL-05 | Export als druckbarer Spickzettel (PDF) je Themengebiet. | Kann |

### 4.4 Aufgaben und Übungen (AU)

| ID | Anforderung | Prio |
| --- | --- | --- |
| AU-01 | Aufgabentypen: Multiple Choice, Zuordnung, Lückentext, Reihenfolge, Rechenaufgabe mit Lösungsweg, Freitext. | Muss |
| AU-02 | Fünf Schwierigkeitsstufen: 1 Erinnern, 2 Verstehen, 3 Anwenden, 4 Analysieren (mehrstufig), 5 Prüfungsniveau (Handlungssituation). | Muss |
| AU-03 | Aufgabengeneratoren erzeugen unbegrenzt Varianten für Rechenthemen: Subnetting (IPv4/IPv6), Zahlensysteme, Speicher- und Übertragungszeiten, Stromkosten und Verbrauch, Bildgrößen, RAID-Kapazität, Kostenvergleiche. | Muss |
| AU-04 | Rechenaufgaben prüfen Zwischenschritte, nicht nur das Endergebnis, und zeigen, in welchem Schritt der Fehler liegt. | Muss |
| AU-05 | Freitextantworten werden gegen eine Musterlösung mit Bewertungspunkten abgeglichen (Selbstbewertung anhand der Bewertungspunkte, mit Hinweis auf fehlende Kernbegriffe). | Muss |
| AU-06 | Die Stufe steigt nach 3 richtigen Antworten in Folge und sinkt nach 2 Fehlern. | Muss |
| AU-07 | Interaktive Simulationen: Subnetz-Rechner zum Selbstbauen, Paketweg durch das OSI-Modell, RAID-Ausfall durchspielen. | Soll |

### 4.5 Hilfestellungen (HI)

| ID | Anforderung | Prio |
| --- | --- | --- |
| HI-01 | Gestufte Hilfen: Hinweis 1 (Richtung), Hinweis 2 (Ansatz/Formel), Hinweis 3 (erster Schritt), vollständiger Lösungsweg. | Muss |
| HI-02 | Genutzte Hilfen fließen in die Bewertung des Lernstands ein (gelöst mit Hilfe ≠ sicher). | Muss |
| HI-03 | Fehlerspezifisches Feedback: typische Falschantworten haben eine eigene Erklärung, warum sie falsch sind. | Muss |
| HI-04 | Button "Erklär es mir anders" liefert eine alternative Erklärung (Analogie, Diagramm, einfachere Sprache). | Soll |

### 4.6 Wiederholung (WH)

| ID | Anforderung | Prio |
| --- | --- | --- |
| WH-01 | Wiederholung nach Spaced-Repetition-Algorithmus (FSRS oder SM-2) für Lernkarten und Aufgaben. | Muss |
| WH-02 | Fällige Wiederholungen haben Vorrang vor neuem Stoff; Obergrenze pro Tag einstellbar. | Muss |
| WH-03 | Wöchentlicher Mischtest über alle bisher gelernten Themen (Interleaving). | Muss |
| WH-04 | Kurz vor der Prüfung verdichtet sich der Plan zu einer Wiederholungsphase mit Schwerpunkt auf Schwachstellen. | Muss |

### 4.7 Fortschritt und Tracking (FT)

| ID | Anforderung | Prio |
| --- | --- | --- |
| FT-01 | Beherrschungsgrad pro Thema (0–100 %), berechnet aus Trefferquote, Schwierigkeitsstufe, Hilfenutzung und Abstand seit dem letzten Erfolg. | Muss |
| FT-02 | Übersicht als Themenkarte des Prüfungskatalogs mit Ampelfarben. | Muss |
| FT-03 | Prognose: voraussichtliche Punktzahl in der AP1 auf Basis der Simulationen und des Beherrschungsgrads. | Soll |
| FT-04 | Fehlerprotokoll: alle falsch gelösten Aufgaben, gruppiert nach Fehlerursache (Rechenfehler, Begriff verwechselt, Konzept nicht verstanden). | Muss |
| FT-05 | Lernzeit, Lernserie und Planerfüllung pro Woche. | Soll |

### 4.8 Prüfungssimulation (PS)

| ID | Anforderung | Prio |
| --- | --- | --- |
| PS-01 | Vollständige Simulation: 90 Minuten, Handlungssituation mit mehreren Aufgaben, Punkteverteilung wie in der echten Prüfung. | Muss |
| PS-02 | Während der Simulation keine Hilfen; Auswertung danach mit Musterlösung und Punktevergabe. | Muss |
| PS-03 | Teilsimulationen von 20–30 Minuten für einzelne Themenblöcke. | Soll |
| PS-04 | Nach jeder Simulation werden Schwachstellen automatisch in den Lernplan zurückgespielt. | Muss |

### 4.9 Material einspielen (MA)

| ID | Anforderung | Prio |
| --- | --- | --- |
| MA-01 | Eine Seite "Material einspielen" führt als Assistent Schritt für Schritt durch die Anleitung aus Kap. 6: jeder Schritt mit kurzer Erklärung, warum er nötig ist, und einem Haken, sobald er erledigt ist. | Muss |
| MA-02 | Das Tool führt die Inventur-Prüfung selbst aus und zeigt neue, geänderte, umbenannte und gelöschte Dateien in `quellen/` an, bevor gepusht wird. | Muss |
| MA-03 | Vorab-Check jeder Datei: unklarer Name (z. B. `scan_0034.pdf`), falscher Ordner, leere oder passwortgeschützte PDF, Scan ohne Textebene; jeweils mit Hinweis, was zu tun ist. | Muss |
| MA-04 | Die nötigen Git-Befehle werden mit vorbereiteter Commit-Nachricht zum Kopieren angezeigt; optional ein Button "Committen und pushen", der erst nach Bestätigung ausgeführt wird. | Soll |
| MA-05 | Nach dem nächsten Pull zeigt das Tool "Neu seit dem letzten Start": welche Lektionen, Begriffe und Aufgaben hinzugekommen sind und wie sich der Lernplan dadurch ändert. | Soll |
| MA-06 | Statusanzeige der Verarbeitung (Issue offen, Pull Request offen, übernommen) über die GitHub-Schnittstelle; braucht Internet und einen Zugriffsschlüssel und ist deshalb abschaltbar. | Kann |

Der Assistent ist besonders für spätere Jahrgänge wichtig, die eigenes Material mitbringen und die Pipeline nicht kennen.

## 5. Zusätzliche Ideen

Die drei wirksamsten Ergänzungen sind ein Operatoren-Training für offene Prüfungsfragen, Fehlerkarten aus eigenen Fehlern und eine durchgehende Handlungssituation, die alle Themen verbindet. Ein KI-Tutor ist bewusst nicht vorgesehen.

| ID | Idee | Nutzen | Prio |
| --- | --- | --- | --- |
| ZI-02 | **Operatoren-Training:** Unterschied zwischen nennen, beschreiben, erläutern, begründen, berechnen, vergleichen üben; Musterantworten je Operator. | Offene Aufgaben holen Punkte über die richtige Antworttiefe | Muss |
| ZI-03 | **Durchgehende Handlungssituation:** Eine fiktive Firma, deren neuer Arbeitsplatz über die Wochen Schritt für Schritt eingerichtet wird (Bedarf, Hardware, Netzwerk, Sicherheit, Übergabe). | Themen bleiben verbunden wie in der Prüfung | Soll |
| ZI-04 | **Feynman-Modus:** Azubi erklärt ein Thema in eigenen Worten und hakt danach ab, welche Kernpunkte der Checkliste er genannt hat. | Prüft echtes Verständnis statt Wiedererkennen | Soll |
| ZI-05 | **Fehlerkarten:** Jeder Fehler erzeugt automatisch eine Lernkarte mit der richtigen Erklärung. | Fehler werden gezielt wiederholt | Muss |
| ZI-06 | **Formelsammlung:** Alle Formeln mit Einheiten, Herleitung und Rechenbeispiel. | Rechenaufgaben sicher lösen | Muss |
| ZI-07 | **Prüfungstaktik:** Zeitplanung für 90 Minuten, Reihenfolge der Aufgaben, Umgang mit Blockaden. | Punkte nicht durch Zeitnot verlieren | Soll |
| ZI-08 | **Lernfeld-Abgleich:** Zuordnung Berufsschul-Lernfelder ↔ Prüfungskatalog ↔ eigene Dokumente; zeigt Lücken im Material. | Weiß, wo eigenes Material fehlt | Muss |
| ZI-09 | **Eigene Notizen und Eselsbrücken** an jeder Lektion und jedem Begriff. | Persönliches Material bleibt im Tool | Soll |
| ZI-10 | **Wochenbericht** (Lernzeit, Fortschritt, Schwachstellen) als Export, z. B. für den Ausbilder. | Motivation und Nachweis | Kann |
| ZI-11 | **Kurzsessions** von 5–10 Min. nur mit Lernkarten, auch auf dem Handy im selben WLAN. | Wartezeiten nutzen | Kann |
| ZI-12 | **Dezente Motivation:** Lernserie, Themen-Abzeichen bei 80 % Beherrschung, Countdown zur Prüfung. | Durchhalten über 15 Wochen | Kann |

## 6. Inhaltsmodell und Content-Pipeline

Inhalte und Programm werden getrennt: Alle Lerninhalte liegen als Markdown- und YAML-Dateien im Repo, das Tool liest sie nur ein. So bleiben Inhalte versionierbar, prüfbar und um AP2 erweiterbar.

**Pipeline vom Rohmaterial zum Lerninhalt:**

1. **Inventur (Skript, rein mechanisch):** `tools/inventory.py` listet alle Dateien in `quellen/` mit Format, Größe, Seitenzahl und Prüfsumme und legt den extrahierten Rohtext in `build/extrakte/` ab (per `.gitignore` nicht im Repo). Das Skript bewertet nichts, ordnet nichts zu und pusht nichts; die Prüfsummen speichert es in `docs/inventur-manifest.json` (im Repo), damit es beim nächsten Lauf neue, geänderte und gelöschte Dateien erkennt.
2. **Sichtung und Zuordnung (Claude):** Claude liest jedes Dokument vollständig, PDFs und PNGs zusätzlich als Bild, damit Tabellen, Diagramme und Skizzen nicht verloren gehen. Jedes Dokument wird den Themen des Prüfungskatalogs 2025 und den Lernfeldern zugeordnet; Lücken, Dopplungen und entfallene Themen werden markiert → `docs/inventur.md`.
3. **Faktencheck (Claude):** Aussagen gegen Normen, Herstellerdokumentation und Fachliteratur prüfen; Fehler in `docs/pruefprotokoll.md` festhalten, nicht stillschweigend ändern.
4. **Lernstil-Analyse (Claude):** Die eigenen Dokumente dienen als Stilvorlage (siehe LS-02).
5. **Aufbereitung (Claude):** Claude erstellt alle Themen neu, im Stil der eigenen Dokumente; das eigene Material dient nur als Kontext (welche Themen, wie der Azubi arbeitet) und als Stilvorlage (Entscheidung 12.11.2026). Alles im Raster aus LI-01, mit Quelle und Prüfstatus.
6. **Review (du):** Claude arbeitet auf einem eigenen Branch und öffnet einen Pull Request; erst nach deiner Freigabe landet etwas auf `main` und bekommt den Status "geprüft". Kein Skript committet oder pusht selbstständig.

### Anleitung: Neues Material einspielen

Neues Material kommt in drei Handgriffen ins Repo; den Rest erledigen GitHub Action und Claude, und nichts landet ohne deine Freigabe auf `main`. Skript, Manifest und Action richtet Claude einmalig in Phase 0 ein. Im Tool führt die Seite "Material einspielen" (Kap. 4.9) durch dieselben Schritte.

1. **Dateien ablegen:** Neue oder überarbeitete Dateien in den passenden Unterordner von `quellen/` legen, z. B. `quellen/eigene/` oder `quellen/lernfelder/`. Sprechende Namen verwenden (`lf05-dhcp.pdf` statt `scan_0034.pdf`); eine überarbeitete Datei behält ihren Namen, damit sie als Änderung erkannt wird.
2. **Committen und pushen:** `git add quellen/`, dann `git commit -m "Quellen: DHCP-Skript ergänzt"`, dann `git push`.
3. **Automatische Prüfung:** Die GitHub Action startet bei jeder Änderung in `quellen/`, führt `ap-tools inventur --check` aus und legt ein Issue an, z. B. "Inventur: 2 neu, 1 geändert", mit Dateiliste. Ohne Änderungen entsteht kein Issue.
4. **Claude beauftragen:** In einer Sitzung "Bearbeite Issue #12" schreiben (oder einfach "Hab neue Sachen hochgeladen").
5. **Claude verarbeitet:** Branch `inventur/<datum>` anlegen, `ap-tools inventur` ausführen (aktualisiert Manifest und Rohtext), jede gemeldete Datei vollständig sichten, zuordnen und prüfen, Lektionen und Glossar ergänzen, `docs/inventur.md` und `docs/pruefprotokoll.md` fortschreiben.
6. **Pull Request prüfen:** Claude öffnet einen PR mit Verweis auf das Issue und einer Zusammenfassung: welche Dateien, welche Themen, welche Fehler gefunden, welche Inhalte neu. Du liest, kommentierst oder gibst frei; der Merge schließt das Issue und setzt die Inhalte auf "geprüft".
7. **Weiterlernen:** Beim nächsten Start lädt das Tool die neuen Inhalte; neue Themen erscheinen im Lernplan und in der Machbarkeitsprüfung.

**Sonderfälle:**

- **Datei löschen:** aus `quellen/` entfernen und pushen. Claude prüft im PR, welche Inhalte darauf verweisen, und markiert sie als "Quelle fehlt", statt sie still zu löschen.
- **Datei umbenennen:** wird über die gleiche Prüfsumme als Umbenennung erkannt, nicht als neue Datei.
- **Nur nachsehen:** `uv run ap-tools inventur --check` zeigt lokal an, was sich geändert hat, und schreibt nichts.
- **Später optional:** eine geplante Aufgabe, die z. B. sonntags selbst nach Änderungen sucht und den PR vorbereitet; dann entfällt Schritt 4.

**Vorgeschlagene Repo-Struktur:**

```
/
├─ quellen/            # Rohmaterial (PDF, HTML, Markdown, PNG), unverändert
├─ docs/               # Anforderungen, Inventur, Manifest, Prüfprotokoll, Entscheidungen
├─ .github/workflows/  # CI und Inventur-Prüfung
├─ content/
│  └─ ap1/
│     ├─ paket.yaml    # Name, Katalogversion, Prüfungstermine, Prüfungsbereich
│     ├─ katalog.yaml  # Themenbaum, Abhängigkeiten, Gewichte
│     ├─ lektionen/    # eine Markdown-Datei je Lektion
│     ├─ glossar/      # ein YAML-Eintrag je Begriff
│     ├─ aufgaben/     # statische Aufgaben (YAML)
│     └─ simulationen/ # komplette Prüfungssätze
├─ src/ap_trainer/     # das Programm (Aufbau in Kap. 8)
├─ tools/              # Skripte der Content-Pipeline
├─ tests/              # pytest, gleiche Struktur wie src/
├─ pyproject.toml      # Abhängigkeiten, Startbefehle, Tool-Konfiguration
└─ CHANGELOG.md
```

**Beispiel Glossar-Eintrag:**

```yaml
id: dhcp
begriff: DHCP
langform: Dynamic Host Configuration Protocol
kurz: Protokoll, das Netzwerkgeräten automatisch IP-Konfiguration zuweist.
warum: Ohne DHCP müsste jede IP-Adresse von Hand vergeben werden – fehleranfällig und bei vielen Geräten nicht machbar.
beispiel: Laptop meldet sich im Firmen-WLAN an und erhält IP, Gateway und DNS-Server.
verwandt: [ip-adresse, dns, gateway]
thema: netzwerk
quelle: quellen/lf03-netzwerke.md
status: geprüft
```

Rechenaufgaben werden nicht als Datei gespeichert, sondern als Generator im Code, der Aufgabe, Lösungsweg und typische Fehler erzeugt (AU-03).

## 7. Nicht-funktionale Anforderungen

Das Tool läuft lokal als Python-Programm und wird im Browser bedient; es braucht weder Internet noch Konto, und der Lernstand geht nicht verloren.

| ID | Kategorie | Anforderung |
| --- | --- | --- |
| NF-01 | Plattform | Läuft mit Python 3.12+ auf Windows, Linux und macOS; Start mit einem Befehl (`uv run ap-trainer`), Bedienung im Browser. Smartphone-Zugriff im selben WLAN gehört zu Version 1.0; die Oberfläche funktioniert dafür auch auf schmalen Bildschirmen. |
| NF-02 | Offline | Alle Funktionen arbeiten ohne Internetverbindung. |
| NF-03 | Datenhaltung | Lernstand in einer lokalen SQLite-Datei je Nutzer; Export/Import als JSON; Backup durch Kopieren der Datei. |
| NF-04 | Datenschutz | Keine Weitergabe von Lerndaten an Dritte; die Lernstand-Datei ist per `.gitignore` vom Repo ausgeschlossen. |
| NF-05 | Bedienbarkeit | Tagesration mit höchstens 2 Klicks erreichbar; Tastaturbedienung für Übungen; Dark Mode. |
| NF-06 | Leistung | Seitenwechsel unter 300 ms; Aufgabengeneratoren liefern unter 100 ms. |
| NF-07 | Korrektheit | Jeder Generator hat Property-Tests (Hypothesis), die Lösung und Lösungsweg gegen eine unabhängige Referenzrechnung prüfen. |
| NF-08 | Wartbarkeit | Inhalte ohne Programmierkenntnisse in Markdown/YAML änderbar; Schema-Prüfung (Pydantic) bei jedem Start und in der CI. |
| NF-09 | Versionierung | Semantische Versionen (z. B. 1.2.0), CHANGELOG, Releases im Repo; Lernstand bleibt über Updates gültig (Datenbank-Migrationen). |
| NF-10 | Barrierearmut | Ausreichende Kontraste, skalierbare Schrift, Diagramme mit Textalternative. |
| NF-11 | Codequalität | Klare Schichten (Inhalte → Kern → Oberfläche), Typ-Hinweise überall, ruff und mypy ohne Fehler, Testabdeckung des Kerns mindestens 80 %. |
| NF-12 | Mehrere Jahrgänge | Prüfungstermin und Katalogversion sind Daten, kein Code: ein neuer Jahrgang oder ein neuer Prüfungskatalog braucht nur ein aktualisiertes Inhaltspaket. |

## 8. Technischer Umsetzungsvorschlag

Empfehlung: ein Python-Programm, das lokal startet und seine Oberfläche mit NiceGUI im Browser anzeigt. Inhalte, Lernlogik und Oberfläche sind strikt getrennt; die Lernlogik ist reines Python und damit ohne Oberfläche vollständig testbar.

**Grafik: Inhaltspakete speisen einen Python-Kern, der lokal läuft**

```
Inhaltspakete ──────────▶ Prüfung (CI) ───────────────▶ Auslieferung
content/ap1 (MD, YAML)    Schema-Prüfung mit Pydantic    Python-Paket, Start mit uv
später content/ap2-fisi   pytest, ruff, mypy             Releases mit Versionsnummer
                                                                  │
                                                                  ▼
┌─ App-Kern (reines Python, ohne Oberfläche testbar) ───────────────────────────┐
│  Lernplan        Wiederholung    Aufgaben      Fortschritt     Lernstil       │
│  Wochen, Heute   FSRS-Planer     Generatoren   Beherrschung    Profil, Anp.   │
└───────────────────────────────────────────────────────────────────────────────┘
        ▲▼                       ▲▼                         │
Oberfläche (NiceGUI)       Lokaler Speicher                 ▼
Heute · Lektionen ·        SQLite-Datei je Nutzer      Exporte
Glossar · Üben ·           Backup durch Kopieren       Lernstand als JSON,
Simulation · Statistik                                 Spickzettel, Wochenbericht
```

Die Engines im App-Kern kennen keine Prüfungsinhalte; alles Fachliche kommt aus den Paketen. Deshalb reicht für AP2 ein neues Paket.

**Technologie-Vorschlag:**

| Baustein | Vorschlag | Begründung |
| --- | --- | --- |
| Oberfläche | NiceGUI | Komplett in Python, läuft im Browser, interaktive Elemente, Markdown und Mermaid-Diagramme eingebaut |
| Projekt, Abhängigkeiten | uv + `pyproject.toml` | Ein Befehl richtet alles ein, Versionen sind festgeschrieben |
| Datenhaltung | SQLite über SQLModel | Eine Datei, keine Installation; Modelle sind zugleich Pydantic-Modelle |
| Inhalte | Markdown + YAML, Prüfung mit Pydantic | Lesbar, versionierbar, Fehler fallen beim Start und in der CI auf |
| Wiederholung | `fsrs` (Python-Paket) | Aktueller Stand der Spaced-Repetition-Forschung |
| Content-Werkzeuge | pdfplumber, BeautifulSoup, Typer | Text aus PDF und HTML ziehen, übersichtliche Kommandozeilen-Befehle |
| Tests | pytest, Hypothesis | Generatoren mit tausenden Zufallsfällen prüfen |
| Codequalität | ruff, mypy, pre-commit | Einheitlicher Stil und Typprüfung vor jedem Commit |
| CI | GitHub Actions | Tests, Typ- und Inhaltsprüfung bei jedem Push; Releases mit Versionsnummer |

NiceGUI statt Streamlit, weil Streamlit bei jeder Eingabe das ganze Skript neu ausführt, was Übungsabläufe mit Zustand umständlich macht; statt Flask, weil keine eigenen HTML-Templates nötig sind.

### Code-Struktur

```
src/ap_trainer/
├─ __main__.py        # Einstieg: lädt Einstellungen und startet die Oberfläche
├─ config.py          # Einstellungen: Prüfungstermin, Pfade, Lernstil
├─ content/           # Inhaltspakete laden und prüfen
│  ├─ models.py       # Pydantic-Modelle: Paket, Thema, Lektion, Begriff, Aufgabe
│  └─ loader.py       # liest content/, meldet Schemafehler verständlich
├─ core/              # Lernlogik, kennt weder Oberfläche noch Datenbank
│  ├─ planner.py      # Wochenplan und Tagesration
│  ├─ scheduler.py    # Wiederholung nach FSRS
│  ├─ mastery.py      # Beherrschungsgrad je Thema
│  ├─ weighting.py    # Themengewichtung aus katalog.yaml
│  └─ profile.py      # Lernstil-Profil und Anpassung
├─ tasks/
│  ├─ base.py         # gemeinsame Schnittstelle aller Aufgabentypen
│  ├─ types/          # Multiple Choice, Zuordnung, Lückentext, Rechnung, Freitext
│  └─ generators/     # subnetting.py, number_systems.py, transfer_time.py, power_cost.py …
├─ storage/           # SQLite-Zugriff, Migrationen, JSON-Export
└─ ui/                # eine Datei je Seite: today.py, lesson.py, glossary.py, practice.py, exam.py, stats.py

tools/
├─ cli.py             # gemeinsamer Einstieg: uv run ap-tools <befehl>
├─ inventory.py       # Dateiliste, Prüfsummen, Rohtext (keine Bewertung)
├─ extract.py         # Text aus PDF, HTML, Markdown
├─ check_content.py   # Schema- und Verweisprüfung aller Inhalte
└─ style_analysis.py  # Kennzahlen als Vorarbeit für Claudes Stilanalyse
```

**Konventionen:**

- Bezeichner auf Englisch, Kommentare, Docstrings und Inhalte auf Deutsch.
- `core/` importiert nie aus `ui/` oder `storage/`; Daten gehen als Modelle hinein und heraus. So ist die Lernlogik ohne Oberfläche testbar.
- Jede Datei hat genau eine Aufgabe und einen Kopf-Docstring, der sie in 1–2 Sätzen erklärt; Funktionen bleiben in der Regel unter 40 Zeilen.
- Ein neuer Aufgabengenerator ist eine neue Datei in `generators/` plus eine Testdatei; er registriert sich selbst, sonst wird nichts geändert.
- Jedes Werkzeug in `tools/` ist ein Unterbefehl von `ap-tools` mit `--help`.
- pre-commit führt ruff, mypy und die schnellen Tests vor jedem Commit aus.

**Arbeitsweise mit Claude im Repo:** Jede Anforderungs-ID wird ein Issue; Inhalte und Code kommen als Pull Request mit Verweis auf die ID. Faktencheck und Inventur entstehen als Dokumente in `docs/`, damit jede Korrektur nachvollziehbar bleibt.

## 9. Erweiterbarkeit für AP2

AP2 wird als zusätzliches Inhaltspaket (`content/ap2-fisi/`) ergänzt; Lernplan, Wiederholung, Aufgaben und Tracking funktionieren unverändert. Lernstand und Glossar aus AP1 bleiben erhalten und werden weiterverwendet.

- ER-01: Ein Paket beschreibt sich selbst in einer `paket.yaml` (Name, Prüfungsteil, Katalogversion, Prüfungstermine, Prüfungsbereiche mit Dauer und Gewichtung).
- ER-02: Mehrere Pakete können gleichzeitig aktiv sein; der Nutzer wählt das aktuelle Prüfungsziel.
- ER-03: Themen können paketübergreifend verknüpft werden (z. B. AP2-Netzwerkplanung setzt AP1-Subnetting voraus).
- ER-04: Neue Aufgabentypen werden als eigene Klasse in `tasks/types/` ergänzt, ohne bestehende zu ändern. Für AP2 absehbar: Fallstudie mit mehreren Teilaufgaben, Projektdokumentation prüfen, Fachgespräch-Training (Fragenkatalog zum eigenen Projekt).
- ER-05: Der Prüfungssimulator liest Dauer, Aufgabenart und Gewichtung aus der Paketbeschreibung, damit auch Prüfungsbereiche mit anderem Format (z. B. gebundene Aufgaben in WiSo) abbildbar sind.
- ER-06: Die Pakete sind berufsneutral benannt, damit später auch andere IT-Berufe eigene AP2-Pakete ergänzen können (AP1 ist für alle IT-Berufe identisch).
- ER-07: Ändert die IHK den Prüfungskatalog, entsteht eine neue Paketversion; Lernstände verweisen auf Themen-IDs, die über Versionen hinweg stabil bleiben, damit vorhandener Fortschritt übernommen wird.

## 10. Roadmap und Meilensteine

Das Tool darf das Lernen nicht verzögern: Nach zwei Wochen steht eine nutzbare Version 0.5, mit der täglich gelernt wird, während Übungen und Simulation dazukommen.

**Grafik: Ab Woche 2 wird mit dem Tool gelernt, die Funktionen wachsen parallel**

| Phase | Wochen | Inhalte | Ergebnis |
| --- | --- | --- | --- |
| 0 · Grundlagen | Woche 1 | Repo-Inventur, Katalog-Mapping, Faktencheck starten, Lernstil-Analyse | v0.1 Gerüst |
| 1 · Lernstart | Woche 1–2 | Heute-Seite, Lernplan, Lektionen-Ansicht, Glossar, Lernkarten, FSRS-Wiederholung | v0.5 · Lernen beginnt |
| 2 · Üben | Woche 3–5 | Aufgaben-Engine, Rechen-Generatoren, gestufte Hilfen, Fortschritt, Tracking | v1.0 |
| 3 · Prüfungsreife | Woche 6–8 | Prüfungssimulation, Fehlerkarten, Operatoren-Training, Punkteprognose | v1.5 |
| Lernbetrieb | Woche 9–15 | Lernen und Simulationen bis 24.02.2027, danach AP2-Paket | v2.0 |

Woche 1 beginnt am 12.11.2026, Phase 3 endet am 06.01.2027. Danach bleiben gut 7 Wochen reiner Lern- und Simulationsbetrieb bis zur Prüfung am 24.02.2027. Lektionen entstehen parallel, jeweils eine Woche vor ihrem Platz im Lernplan, damit Inhalte immer vor dem Lernen geprüft sind.

## 11. Abnahmekriterien

Version 1.0 gilt als abgenommen, wenn alle Muss-Anforderungen aus Kapitel 4 umgesetzt sind und die folgenden Prüfungen bestanden sind.

- [ ] Jedes Thema aus `katalog.yaml` hat mindestens eine Lektion, 5 Glossarbegriffe (wo sinnvoll) und Aufgaben auf den Stufen 1–4.
- [ ] Alle Lektionen haben den Status "geprüft"; das Prüfprotokoll listet jede inhaltliche Korrektur mit Quelle.
- [ ] Jeder Aufgabengenerator besteht 1.000 zufällige Testläufe ohne falsche Lösung.
- [ ] Ein vollständiger Lerntag (Wiederholung, Lektion, Übung) ist ohne Internetverbindung durchführbar.
- [ ] Export und Re-Import des Lernstands auf einem anderen Gerät liefern identische Fortschrittswerte.
- [ ] Der Lernplan passt sich nach 3 verpassten Tagen korrekt an und zeigt eine Warnung, falls das Ziel gefährdet ist.
- [ ] Ein Testnutzer (z. B. Mit-Azubi) findet sich ohne Anleitung in unter 5 Minuten zurecht.

## 12. Offene Fragen

Alle Fragen sind geklärt; die Umsetzung startet mit Phase 0 in einem neuen Chat.

| Frage | Entscheidung (12.11.2026) |
| --- | --- |
| Prüfungstermin | 24.02.2027; im Tool frei einstellbar für spätere Jahrgänge |
| Formate im Repo | PDF, HTML, Markdown, PNG |
| Material | Eigene Lerndokumente dienen nur als Kontext und Stilvorlage; alle Lektionen erstellt Claude neu im gleichen Stil (präzisiert am 12.11.2026) |
| Themengewichtung | Aus öffentlicher Auswertung der AP1-Prüfungen, korrigiert um den Katalog 2025 (Kap. 2) |
| Lernbudget | Presets 15, 20 und 30 Std./Woche oder frei; Aufwandsschätzung je Thema und Zeitplan-Check (LP-01, LP-08 bis LP-11) |
| Eigenes Budget | Start mit 15 Std./Woche, in einigen Wochen Wechsel auf ca. 30 Std./Woche; der Plan muss den Wechsel ohne Neustart übernehmen |
| Selbsteinschätzung | Sicher: Projektorganisation, agiles Projektmanagement. Unsicher: Netzwerktechnik (Grundverständnis vorhanden). Der Einstufungstest präzisiert das. |
| Inventur | Skript erledigt nur Mechanisches; Sichtung, Zuordnung und Faktencheck macht Claude; Übernahme nur per Pull Request (Kap. 6) |
| Plattformen | Windows und macOS; Smartphone-Zugriff im WLAN ist Teil von Version 1.0 |
| Code | Python, ausführlich kommentiert; der Azubi entwickelt nicht mit und reviewt keinen Code, Qualität sichern Tests, ruff und mypy |
| Repo-Rechte | Claude darf das Repo komplett umbauen, arbeitet auf Branches mit Pull Requests; gemergt wird nur vom Azubi |
| KI-Tutor | Gestrichen |
| Repo | Privat (`danceingold/leit`), alles darf hinein; Aufräumen und Veröffentlichung später |

**Phase 0 im neuen Chat:**

- [ ] `CLAUDE.md` anlegen: Ziel, Termin, Lernstil, Konventionen, Branch- und PR-Regeln, Ablauf Faktencheck
- [ ] Dieses Dokument als `docs/anforderungen.md` ablegen
- [ ] Repo-Grundstruktur nach Kap. 6 aufbauen, Originaldateien nach `quellen/` verschieben
- [ ] Inventur aller vorhandenen Dateien, Zuordnung zum Katalog, erste Einträge im Prüfprotokoll
- [ ] Lernstil-Analyse der eigenen Dokumente
- [ ] Pull Request mit Zusammenfassung von Phase 0

## Quellen

- [§ 9 FIAusbV – Gesetze im Internet](https://www.gesetze-im-internet.de/fiausbv/__9.html)
- [IHK Schwaben – Fachinformatiker ab 2020](https://www.ihk.de/schwaben/produktmarken/meine-pruefung/ausbildungspruefungen/pruefungen-a-z/fachinformatiker-ab-2020-5113338)
- [IHK Hagen – Prüfungsvorgaben IT-Berufe](https://www.ihk.de/hagen/bildung/abschlusspruefungen/it-berufe-index-812540)
- [DIHK-Umsetzungshilfe IT-Berufe (IHK München)](https://www.ihk-muenchen.de/Bildung/DiPa/Dokumente/4_IT-Berufe_DIHK-Umsetzungshilfe.pdf)
- [U-Form Prüfungstrainer AP1 (Leseprobe)](https://shopstage.u-form.de/media/dd/9f/63/1687157302/750.pdf)
- [IT-Berufe-Podcast – Themen der schriftlichen IHK-Prüfungen](https://it-berufe-podcast.de/vorbereitung-auf-die-ihk-abschlusspruefung-der-it-berufe/themen-der-schriftlichen-ihk-pruefungen-der-it-berufe/)
- [IT-Berufe-Podcast #190 – Neuer Prüfungskatalog AP1 ab 2025](https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/)
- [AP1-Prüfung 2025: Änderungen im Überblick](https://ap1-trainer-pro.de/wissen/ap1-pruefung-2025-aenderungen/)
