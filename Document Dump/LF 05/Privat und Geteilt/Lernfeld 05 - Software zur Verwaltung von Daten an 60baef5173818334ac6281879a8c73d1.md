# Lernfeld 05 - Software zur Verwaltung von Daten anpassen

---

---

---

*Iterartion Docs*

| [Retroperspektive Iteration 1](https://app.notion.com/p/Retroperspektive-Iteration-1-38daef517381800b8194dcf2a5c7c8a3?pvs=21)  |
| --- |
| [Retroperspektive Iteration 2](https://app.notion.com/p/Retroperspektive-Iteration-2-38faef517381806ba8fae5147b798202?pvs=21)  |

---

---

---

---

---

# Einleitung

Herzlich Willkommen zu unserem Portfolio zum Lernfeld 05 - Software zur Verwaltung von Daten anpassen. Wir freuen uns euch im Laufe dieses Dokuments unseren Arbeitsprozess zum erreichen der Anforderungen vorzustellen und hoffen, dass Ihr etwas hieraus Lernen könnt und einen Eindruck von uns als Team bekommt.

*Note: Dieses Lernfeld ist mit 80 Stunden eingetragen und wurde in 8-10 Tagen durchgeführt. Das beträgt ca. 9 Stunden pro Tag. Da dies ziemlich sportlich ist wurde dieses mal weniger wert auf das Design des Portfolios gelegt um den inhaltlichen Wert auf dem gleichen Niveau zu halten wie bisher.*

*Note 2: In diesem Portfolio gehen wir nach dem NO AI Prinzip. Kein Text in diesem Portfolio wurde von AI geschrieben.*

# Inhalt

In den Folgenden Kapiteln befassen wir uns mit der Dokumentation folgender Themen und Schritte:

- Projekt und Teamorganisation
- Sprint 1: ERD anpassen
- Sprint 2: ERD in SQL Umsetzen
- Sprint 3: SQL SELECT Abfragen
- Sprint 4: Individuelle Kompetenzen und Lernphase
- Artefakte
- Reflexion

# Zielsetzung des Lernfeldes

Dieses Lernfeld legt fachlich seine Schwerpunkte auf das allgemeine Verständnis, simple Modellierung und Entwicklung von Datenbanken. Überfachlich wird das Projekt in einem SCRUM Team bearbeitet und daher liegt hier die Methodenkompetenz.

### Fachkompetenz: Datenbankmodellierung und SQL

Am Ende dieses Lernfeldes wird von jedem Teammitglied erwartet das dieser sich mit den Grundbegriffen von Datenbanken, Entity Relationship Modell/Diagramm, Tabellenschemas, Normalformen, SQL Syntax und simplen SQL Abfragen zur Anpassung von Daten in einem DBMS (Datenbank Management System) auskennt.

### Methodenkompetenz: Agiles Arbeiten im Team

Wie bereits im Lernfeld zuvor wollen wir unsere Teamarbeit stärken und unser wissen und Methoden dessen festigen. Wie genau wir das erreichen wollen, wird später in der Team Orga nochmal erläutert.

---

# Projekt und Teamorganisation

Im folgenden möchten wir einen kurzen Überblick geben wie wir uns als Team Strukturiert und vorbereitet haben.

---

## Teammanagement

Zur Umsetzung haben wir uns an einer agilen Arbeitsweise nach dem **Scrum-Modell** orientiert, um strukturiert und effizient im Team arbeiten zu können. Dazu haben wir uns in Rollen eingeteilt (mit Rücksichtnahme auf die Überfachlichen Kompetenzen) und einen gemeinsamen Workspace errichtet.

![TeamOrgaAgileLF05.drawio.png](Lernfeld%2005%20-%20Software%20zur%20Verwaltung%20von%20Daten%20an/TeamOrgaAgileLF05.drawio.png)

Selbstverständlich dient das nur der einfachen Darstellung. Jedes Teammitglied hat aktiv am Prozess der Teilhandlungen mitgearbeitet (als Developer). Entscheidungen wurden im Team gefällt.

---

## Tools

Wir haben uns dazu entschieden die folgenden Tools zu verwenden um das Team zu Managen und das Lernfeld zu Planen, durchzuführen und zu Dokumentieren:

### Notion

- Zentrale Plattform für die gesamte Projektorganisation
- Nutzung eines Kanban-Boards zur Aufgabenverteilung
- Dokumentation von Fortschnitten, Ergebnissen und Lerninhalten

### WhatsApp

- Schnelle und unkomplizierte Kommunikation im Team
- Abstimmung bei Fragen oder kurzfristigen Änderungen

### Sonstige

- Excel für das Tabellenschema,
- [Draw.io](http://Draw.io) für ERD und Diagramme
- XAMPP für einen Lokalen Server
- HeidiSQL zur entwicklung der SQL Abfragen und als Schnittstelle zur Datenbank
- GitHub zum Teilen und dokuemntieren der SQL Codes

---

## Arbeitsweise

Bei der Arbeitsweise haben wir uns ebenfalls an die Scrum Methode gehalten. Konkret waren unsere Sprints so Strukturiert:

- Daily Stand-Up’s
    - Was haben wir am Tag zuvor gemacht (Retroperspektive)?
    - Was haben wir Heute vor?
    - Welche Probleme gibt es?
    - Aktualisierung des KanBan Boards
- Weekly Stand-Up’s (Iteration Retro)
    - Retroperspektive was wir die letzte Woche gemacht haben
    - Planung der nächsten Schritte
    - Einschätzung des aktuellen Projektstands
    - Anpassung der Arbeitsweise bei bedarf
    - Aktualisierung des KanBan Boards
- KanBan Board

Das Ziel dieser Arbeitsweise war es, Transparenz und schnelle Kommunikation zu ermöglichen um das Verständnisnevau aller Teammitglieder auf einen Stand zu bringen.

---

## Aufgabenverteilung

Nachdem wir uns alle erst einzeln, dann gemeinsam, das Lernfeld angeschaut haben, haben wir die Teilhandlungen in einzelne Schritte bzw. Arbeitspakete unterteilt, und anschließend als Sprits definiert.

#### Sprint 1: ERD anpassen

Der Sprint 1 soll nach Absprache ca. ein bis zwei Tage andauern. In diesem möchten wir die grundlagen für die datenbankmodellierung via ERD erlernen und für kraut und Rüben anpassen um die kundenanforderungen zu erfüllen.

Sprint 1 wurde für den 24.06 angelegt.

#### Sprint 2: ERD in SQL Umsetzen

Der 2. Sprint beinhaltet das erstellen der SQL Abfragen zur erstellung der Datenbank nach Kundenanforderung.

Sprint 2 wurde für den Zeitraum 26.06 - 30.06 angelegt.

#### Sprint 3: SQL SELECT Abfragen

Im 3. Sprint sollen SQL SELECT Abfragen erstellt werden, um die Kundenanforderungen umzusetzen.

Sprint 3 wurde für den Zeitraum 30.07 - 02.07 angelegt.

#### Sprint 4: Individuelle Kompetenzen und Lernphase

Im 4. Sprint wollen wir die restliche Zeit nutzen um unsere Individuellen Kompetenzziele zu erreichen und fehlende Kompetenzen nachzuholen oder zu verstärken.

Sprint 4 wurde für den Zeitraum 03.07 - 08.07 angelegt.

Sprint 1 und 2 haben wir gemeinsam im Team erarbeitet, das erlangen der Fachkompetenzen unterlag jedoch der Eigenverantwortung.

---

---

## Sprint 1: ERD und Tabellenschema

Das ERD haben wir gemeinsam als Gruppe mit [draw.io](http://draw.io) angepasst. Im Sprints 2 und 3 sind uns jedoch auch weitere Dinge aufgefallen die nochmal am ERD geändert werden müssen.

#### ERD V.1

Das ist unsere erste Version die wir zum LN 1 Teil A vorbereitet hatten. Allergene und Beschränkungen wurden nach Absprache mit dem Lehrerteam an die Zutat gehängt.

![ERD.drawio.png](Lernfeld%2005%20-%20Software%20zur%20Verwaltung%20von%20Daten%20an/ERD.drawio.png)

#### ERD V.2

In dieser Version haben wir die vom Lehrerteam geforderte Änderung bzgl. der Allergene und Beschraenkungen

![UpdatedERDfixed.png](Lernfeld%2005%20-%20Software%20zur%20Verwaltung%20von%20Daten%20an/UpdatedERDfixed.png)

#### ERD V.3

Das ist unsere Finale Version des ERDs

![UpdatedERD.drawio.png](../Lernfeld%205%20-%20HQ/387aef51738181eb9aa70042f7a3375b/Document%20Archive/Angepasstes%20ERD/UpdatedERD.drawio.png)

Tabellenschema: [TabellenschemaERD.xlsx](https://app.notion.com/p/TabellenschemaERD-xlsx-391aef517381801f8dfcc8edc1b0fa38?pvs=21) 

---

---

## Sprint 2: SQL CREATE DATABASE & INSERT Dump

Für das SQL CREATE DATABASE Script haben wir die beiden von Moodle bereitgestellten Scripts an unser Tabellenschema angepasst.

Wir haben mithilfe von Kommentaren die Übersicht und Verständlichkeit optimiert unsere neuen Tabellen hinzugefügt und im INSERT Dump Beispiel Daten für die neuen leeren Tabellen integrert. 

---

---

## Sprint 3: SQL Abfragen (Kundenanforderung)

Wir haben die Anforderungen die von Krautundrueben gestellt wurden analysiert und dann in ToDos festgehalten. Nach absprache haben wir die einzelnen ToDos dann zugeteilt und dann im Backlog definiert.

Die Zuteilung sah wie folgt aus:

- Einzelne SQL CRUD Abfragen um folgende Daten zu erstellen, lesen, ändern und zu Löschen:
    - Rezepte - Lenon
    - Kunden - Lenon
    - Lieferanten - Jessica
    - Zutaten - Jessica
    - Allergene und Beschränkungen - Jonas x
    - Nährwerte - Jonas x
    - Bestellungen - Thies
    - Ernährungskategorien - Valentina
- Dokumentation warum wir die Abfragen wie geschrieben haben - alle
- SQL SELECT Abfragen um:
    - Zutaten Anhand eines Rezepts anzuzeigen - Jessica
    - Rezepte anhand vorgegebener Ernährungskategorien anzeigen - Lenon
    - Auswahl bzw. ausschluss von Rezepten anhand Allergenen und Beschränkungen - Lenon
    - Auswahl aller Rezepte anhand einer bestimmten Zutat - Jonas
    - Berechnung der durschnittlichen Nährwerte anhand aller Bestellungen eines Kunden - Thies
    - Auswahl aller Zutaten die keinem Rezept zugewiesen sind - Valentina
- *optional: Zugriff auf Personenbezogene Daten beschränken*
- DELETE/UPDATE/INSERT etc. für das Konzept der Löschung von Kundendaten - wer fertig is
- Drei weitere Abfragen (to be defined) mit Inner Join, Left/Right Join und Subselects. - wer fertig is

[https://github.com/DanceInGold/LF05](https://github.com/DanceInGold/LF05)

---

---

## Sprint 4: Individuelle Kompetenzen und Lernphase

Im Sprint 4 haben wir uns auf das abschließende Fachgespräch vorbereitet, offene Fragen geklärt und unsere individuellen Kompetenzen erweitert.

---

### **Ergebnisbewertung**

Nach Abschluss des Lernfeldes können wir alle Anforderungen als Umgesetzt vorzeigen. Unser Verständnis für Datenbanken und SQL hat sich auf ein professionelles Niveau erweitert und wir konnten uns gut in die Arbeitsweise eines Agile Teams einarbeiten.

---

## Reflexion

| Reflexion Valentina | Reflexion Jessica | Reflexion Jonas | Reflexion Lenon | Reflexion Thies |
| --- | --- | --- | --- | --- |
|  | Ich finde die Gruppenarbeit sehr gut. Wir haben gut zusammengearbeitet und uns gegenseitig unterstützt, wenn jemand etwas nicht verstanden hat. 

Das Lernfeld fand ich interessant, besonders weil ich vorher noch keine Erfahrung mit Datenbanken hatte. Ich konnte viele neue Inhalte lernen und mein Verständnis durch die praktischen Aufgaben verbessern. | Insgesamt habe ich in den 2 Wochen viel gelernt. Allerdings bräuchte ich wahrscheinlich noch 1 Woche zusätzlich um das Thema vollends zu verstehen. Auch hatte ich in der 1 Woche Schwierigkeiten mich in der Gruppe einzufinden und deren Arbeitsweise zu verstehen. | Die Zusammenarbeit im Team hat sehr gut funktioniert. Durch den regelmäßigen Austausch konnten wir uns gegenseitig unterstützen und unsere Aufgaben erfolgreich umsetzen. Insgesamt sind wir mit unserem Ergebnis zufrieden und haben unser Ziele erreicht. | Dieses Lernfeld hat grundlegend Spaß gemacht. Die Teamarbeit lief sehr gut und wir konnten uns jeden Tag gut abholen und so austauschen das jeder auf einem ähnlichen Niveau ist. 

Leider war der Berufsschulblock etwas zu kurz für ein 80 Stunden Lernfeld aber dadurch konnten wir erkennen das wir im Team auch unter Zeitdruck gut arbeiten können und Ergebnisse abliefern.

Ich hatte zum Thema SQL keine Vorkenntnisse aber eine Woche Vorbereitungszeit und Grundlegendes Verständnis von Programmiersprachen hat es ir ermöglicht schnell alle Aspekte zu verstehen.  |

Das wir die zum Anfang des Lernfeldes definierten Ziele erreicht haben und an teilen sogar übertroffen haben, würden wir uns die **Note 1** geben.

---

---

---

---

![image.png](Lernfeld%2005%20-%20Software%20zur%20Verwaltung%20von%20Daten%20an/image.png)

[*KanBan Board in Notion*](https://app.notion.com/p/387aef517381806c94d4f6daaf624d86?pvs=21)

---

---

---

Artefakte

---

---

###