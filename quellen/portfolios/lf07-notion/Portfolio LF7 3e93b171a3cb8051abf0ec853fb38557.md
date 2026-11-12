# Portfolio LF7

**Cyber-Physische Systeme** – Technische Dokumentation und Arbeitsprozess

---

### **Einleitung**

Herzlich Willkommen zu unserem Portfolio zum Projekt „Smart Dispenser“. In diesem Dokument möchten wir unseren Arbeitsprozess von der ersten Systemidee bis zur technischen Umsetzung vorstellen. Dabei geht es nicht nur um das fertige Produkt, sondern vor allem darum, wie wir als Team gearbeitet, Aufgaben verteilt, technische Teilprobleme bearbeitet und die einzelnen Komponenten anschließend zu einem Gesamtsystem zusammengeführt haben.

Unser Projekt beschäftigt sich mit einem intelligenten, vernetzten Medikamentenspender. Das System soll die zeitgerechte und kontrollierte Ausgabe von Medikamenten unterstützen. Dafür werden zentrale Software, Sensorik, Aktorik, lokale Speicherung und eine Benutzeroberfläche miteinander verbunden.

Nach Einleitung und Zielsetzung folgen Projekt- und Teamorganisation, die einzelnen Sprints, verwendete Tools und Artefakte sowie eine abschließende Reflexion.

---

### Inhalt

In den folgenden Kapiteln befassen wir uns mit der Dokumentation folgender Themen und Schritte:

- Projekt und Teamorganisation
- Sprint 1: Systemanforderungen und Architektur
- Sprint 2: Systementwicklung
- Sprint 3: Integration, Optimierung und Abgabevorbereitung
- Sprint 4: Integration, UI und Statusverwaltung
- Technische Herausforderungen und Lösungen
- Technische Umsetzung
- Artefakte
- Reflexion
- Individuelle Kompetenzen und Lernentwicklung

### **Zielsetzung des Projektes**

Ziel des Projektes war die Entwicklung eines **Cyber-Physische Systems**, das digitale Steuerlogik mit physischer Sensorik und Aktorik verbindet. Der Smart Dispenser soll einen Medikamentenplan verwalten, zu festgelegten Zeitpunkten eine Ausgabe auslösen und die Interaktion des Benutzers über Sensoren erfassen.

---

### Das Szenario

Für unser Projekt haben wir uns für eine **Kombination aus Szenario A und Szenario B** entschieden. Dadurch konnten wir Anforderungen aus beiden Szenarien miteinander verbinden und auf unsere eigene Projektidee übertragen.

Als **Problemfeld** haben wir die **sichere und zuverlässige Einnahme von Medikamenten** gewählt. Dabei beschäftigten wir uns insbesondere mit der Frage, wie vergessene oder fehlerhafte Medikamenteneinnahmen vermieden und die Einnahme besser nachvollziehbar gemacht werden kann.

Als Lösung für dieses Problemfeld entwickelten wir einen **smarten Medikamentenspender**. Unser Ziel war es, verschiedene technische Komponenten miteinander zu verbinden und daraus eine funktionierende **IoT-basierte Lösung** zu entwickeln.

---

### **Teammanagement**

Wir haben uns für eine agile ****Arbeitsweise **nach dem Scrum-Prinzip** entschieden. Die festgelegten Verantwortungsbereiche dienen dabei der Übersicht und Strukturierung unserer Zusammenarbeit. **Technische Entscheidungen sowie wichtige Integrationsfragen werden gemeinsam im Team besprochen und getroffen.**

![TeamOrgaAgileLF07.drawio (1).drawio.png](Portfolio%20LF7/TeamOrgaAgileLF07.drawio_(1).drawio.png)

Die Rollen dienen hauptsächlich der Übersicht. Jedes Teammitglied arbeitet grundsätzlich an Teilaufgaben mit; Entscheidungen werden im Team getroffen.

**Überfachliche Ziele innerhalb der Gruppe:** 

- Arbeitsteilung innerhalb des Teams verbessern.
- Technische Aufgaben in Arbeitspakete aufteilen.
- Schnittstellen zwischen Teilkomponenten gemeinsam definieren.
- Regelmäßige Abstimmung über Fortschritt und Probleme.
- Eigenständiges Arbeiten mit anschließender Integration.
- Technische Entscheidungen nachvollziehbar dokumentieren.

---

### Tools

Wir haben uns dazu entschieden, die folgenden Tools zu verwenden, um unser Team zu organisieren, das Lernfeld zu planen, unser Projekt umzusetzen und unsere Ergebnisse zu dokumentieren.

**Trello**

- Zentrale Plattform zur Organisation unserer Aufgaben
- Erstellung und Verwaltung von Aufgaben
- Übersicht über offene, laufende und abgeschlossene Aufgaben
- Aufgabenverteilung innerhalb des Teams
- Nachverfolgung unseres Projektfortschritts

**Google Drive**

- Gemeinsame Ablage unserer Dateien und Dokumente
- Speicherung von Dokumentationen und Projektunterlagen
- Gemeinsames Bearbeiten und Austauschen von Dateien
- Zentraler Zugriff auf wichtige Projektdateien

**GitHub**

- Verwaltung und Versionierung unseres Quellcodes
- Gemeinsames Arbeiten am Code
- Dokumentation von Änderungen am Projekt
- Nachvollziehbarkeit der Entwicklung

**WhatsApp**

- Schnelle und unkomplizierte Kommunikation innerhalb des Teams
- Abstimmung bei Fragen und Problemen
- Kurzfristige Absprachen
- Kommunikation außerhalb der gemeinsamen Arbeitsphasen

**Discord**

- Kommunikation innerhalb des Teams
- Abstimmung bei Fragen und Problemen
- Austausch während der gemeinsamen Arbeitsphasen
- Schnelle Absprachen und Informationsaustausch

---

### Arbeitsweise

Wir haben unsere Zusammenarbeit in regelmäßigen Abstimmungen und gemeinsamen Arbeitsphasen organisiert.

#### Daily

Die Dailys dienten dazu, den aktuellen Arbeitsstand im Team abzugleichen und die nächsten Schritte zu planen. Dabei wurden folgende Punkte besprochen:

- **Was wurde zuletzt erledigt?**
- **Was wird als Nächstes bearbeitet?**
- **Welche technischen oder organisatorischen Probleme gibt es?**
- **Aktualisierung des Kanban-Boards**

#### Team Exchange & Integration

Neben den Dailys gab es einen regelmäßigen Austausch innerhalb des Teams. Nach Abschluss größerer Arbeitsabschnitte haben wir gemeinsam auf den bisherigen Fortschritt zurückgeblickt und die nächsten Schritte geplant.

Außerdem wurden die fertiggestellten **Teilkomponenten gemeinsam integriert** und auf ihr Zusammenspiel überprüft.

Das Ziel dieser Arbeitsweise war, Transparenz zu schaffen und zu verhindern, dass einzelne technische Teilbereiche unabhängig voneinander in eine Richtung entwickelt werden, die später nicht mehr mit dem Gesamtsystem kompatibel ist.

---

# Durchführung des Projekts

Nach der gemeinsamen Planung und Organisation begann die eigentliche Durchführung unseres Projektes. Die Umsetzung wurde in vier Sprints unterteilt. Jeder Sprint hatte einen eigenen Schwerpunkt und baute auf den Ergebnissen des vorherigen Sprints auf.

---

**Sprint 1: Systemanforderungen und Architektur**

Zu Beginn haben wir das Szenario und die Anforderungen des Smart Dispensers analysiert. Anschließend wurde die technische Architektur in einzelne Ebenen aufgeteilt.

**Aufgaben**

- Anforderungen des Medikamentenspenders sammeln.
- Hauptkomponenten identifizieren.
- Verantwortungsbereiche der Komponenten festlegen.
- Daten- und Steuerflüsse definieren.
- Raspberry Pi als zentrale Logikeinheit und Arduino als hardwarenahe Einheit einordnen.
- Grundlegende Systemarchitektur und Zusammenspiel der Komponenten festlegen.

**Ergebnis**

Als Ergebnis entstand die technische Gesamtübersicht. Sie zeigt Verwaltung und Speicherung, zentrale Logik, Sensorik und Aktorik sowie den physischen Ausgabeprozess. ([LF07 – Google Drive)](https://drive.google.com/file/d/1NiGBejKTnzeJEqN1hDaU7AIY8aJ9Y5X3/view?usp=sharing) 

![mermaid-diagram-2026-09-24-071820.png](Portfolio%20LF7/mermaid-diagram-2026-09-24-071820.png)

![mermaid-diagram-2026-09-28-095213 (1).png](Portfolio%20LF7/mermaid-diagram-2026-09-28-095213_(1).png)

---

**Sprint 2: Aufteilung der Teilhandlungen und technischen Verantwortungsbereiche**

Nachdem wir im ersten Sprint die grundlegende Systemarchitektur und die Anforderungen an unseren Smart Dispenser festgelegt hatten, lag der Schwerpunkt im zweiten Sprint auf der **konkreten Aufgabenverteilung und Umsetzung der einzelnen Teilsysteme**.

Dafür haben wir das Gesamtsystem in mehrere technische Teilbereiche aufgeteilt und die entsprechenden Aufgaben innerhalb des Teams verteilt. Ziel war es, dass die einzelnen Teammitglieder ihre jeweiligen Bereiche **eigenständig fertigstellen, testen und dokumentieren**, sodass im darauffolgenden Sprint die einzelnen Teilsysteme zu einem Gesamtsystem zusammengeführt werden konnten.

**Aufgabenverteilung und Umsetzung**

Zu Beginn des Sprints haben wir die zuvor definierten Funktionen auf die einzelnen technischen Bereiche verteilt. Dabei wurden unter anderem folgende Bereiche betrachtet:

![image.png](Portfolio%20LF7/image.png)

- System Architektur & Konzept: Gruppe
- Hardware Features & Mechanik: Thies
- Sensoren und Erkennung: Valentina
- UI & Integration: Jessica
- Software, Management & Vernetzung: Lenon

Die jeweiligen Teammitglieder waren anschließend dafür verantwortlich, **ihren zugewiesenen Teilbereich technisch umzusetzen**. Dabei ging es nicht nur darum, einzelne Funktionen zu programmieren, sondern die jeweiligen Teilsysteme möglichst vollständig vorzubereiten.

Dazu gehörten insbesondere:

1. **Umsetzung der jeweiligen Funktion**
2. **Testen des Teilsystems**
3. **Beheben auftretender Fehler**
4. **Dokumentieren der technischen Umsetzung**
5. **Hochladen und Sichern des aktuellen Entwicklungsstands auf GitHub**

Durch diese Vorgehensweise konnten die einzelnen Teilbereiche unabhängig voneinander entwickelt werden. Beispielsweise konnte die Sensorik getestet und dokumentiert werden, während parallel an der Steuerung der Aktoren oder an der Benutzeroberfläche gearbeitet wurde.

---

**Sprint 3: Sensorik, Aktorik und Ausgabeprozess**

Im nächsten Schritt wurde die Hardwareebene betrachtet. Die Sensoren liefern Zustandsinformationen an die Logik, während die Aktoren die daraus resultierenden Aktionen physisch ausführen.

**Sensorik**

| **Komponente** | **Funktion** |
| --- | --- |
| IR-Sensor | Erkennung der Raum-/Personenpräsenz. |
| Ultraschall/IR | Erkennung einer Hand im Ausgabebereich. |
| RFID-Leser | Authentifizierung beim Befüllen/Nachfüllen. |

**Technischer Ablauf**

- Person wird erkannt.
- Anzeige wird aktiviert bzw. aktualisiert.
- Hand wird im Ausgabebereich erkannt.
- Zentrale Logik gibt die Ausgabe frei.
- Dosiermechanismus wird angesteuert.
- Entnahme bzw. relevanter Zustand wird überwacht.
- Bei Timeout wird ein Warnsignal ausgelöst.
- Status wird weitergegeben bzw. protokolliert.

---

**Sprint 4: Integration, UI und Statusverwaltung**

Nach der Entwicklung der einzelnen Teilbereiche wurden die Komponenten zusammengeführt. Fokus war das Zusammenspiel zwischen Konfiguration, Zeitsteuerung, Sensoren, Aktoren und Benutzerinformation.

- Konfiguration und Medikamentenplan an die zentrale Logik anbinden.
- Zeitsteuerung mit dem Ausgabeprozess verbinden.
- Sensorzustände auswerten.
- Aktoren abhängig vom Systemzustand ansteuern.
- OLED-Anzeige mit dem Prozess synchronisieren.
- Status- und Ereignisinformationen speichern bzw. weitergeben.

---

## Technische Herausforderungen und Lösungen

Während der Entwicklung unseres Medikamentenspenders sind verschiedene technische Herausforderungen und Fehler aufgetreten. Diese haben wir gemeinsam analysiert und schrittweise gelöst. Die Dokumentation der Probleme und Lösungen zeigt unseren Entwicklungsprozess und macht nachvollziehbar, wie wir als Team mit technischen Schwierigkeiten umgegangen sind.

| **Technische Herausforderung** | **Ursache / Problem** | **Lösung** |
| --- | --- | --- |
| **Arduino RAM-Overflow** | Das OLED-Display und die verwendete Bibliothek benötigten zu viel des begrenzten Arduino-SRAMs. Dadurch kam es zu Abstürzen. | Das Display wurde vom Arduino auf den Raspberry Pi ausgelagert. Das Rendering erfolgt nun über Python und der Arduino übernimmt hauptsächlich die Sensor- und Hardwaresteuerung. |
| **Stepper-Motor verliert Schritte** | Der 28BYJ-48 Stepper hatte im Half-Step-Modus nicht genügend Drehmoment und konnte bei mechanischen Widerständen Schritte verlieren. | Der Stepper wurde auf einen Dual-Coil Full-Step-Modus umgestellt. Zusätzlich wurde die Geschwindigkeit reduziert und eine kurze Pause vor Richtungswechseln eingebaut. |
| **SPI-Pin-Konflikt** | Der RFID-Reader benötigt die SPI-Pins 11, 12 und 13. Diese wurden ursprünglich auch für den Stepper verwendet. | Der Stepper wurde auf die Analog-Pins A0–A3 umverkabelt, die auch als digitale Ausgänge verwendet werden können. Dadurch konnten die SPI-Pins für den RFID-Reader freigehalten werden. |
| **Brownout durch Servos** | Beim Anlaufen der Servos entstanden hohe Stromspitzen. Dadurch brach die Versorgungsspannung ein und das System konnte einfrieren. | Die stromhungrigen Aktoren wurden von der Logikversorgung entkoppelt und sollen über eine separate Stromversorgung mit gemeinsamem GND versorgt werden. |
| **Befehls-Staus und Serial Timeout** | Bei längeren Stepper-Bewegungen reagierte die serielle Kommunikation nicht zuverlässig bzw. Python lief in einen Timeout. | Das Timeout wurde auf 60 Sekunden erhöht. Zusätzlich wartet die Python-Bridge synchron auf die Bestätigung `ACK:STP`, bevor der nächste Schritt ausgeführt wird. |

---

**Artefakte**

Während des Projektes haben wir verschiedene Artefakte gesammelt, um unseren Arbeits- und Entwicklungsprozess nachvollziehbar zu dokumentieren. Dabei haben wir insbesondere **GitHub, Google Drive und Trello** genutzt.

https://github.com/DanceInGold/LF07

https://drive.google.com/drive/folders/1hYJykWVRJvGD8WTam5FiKeJbFOsW51r1?usp=share_link

[LF07 - Project Tracker | Trello](https://trello.com/b/fb2PK4tQ)

---

### **Ergebnis**

Durch die Aufteilung des Projektes in technische Teilbereiche konnten wir die verschiedenen Komponenten zunächst unabhängig bearbeiten und anschließend über definierte Schnittstellen integrieren. Besonders wichtig war dabei die Kommunikation zwischen Raspberry Pi und Arduino, da sie die Verbindung zwischen zentraler Softwarelogik und physischer Hardware bildet.

Das Ergebnis ist eine technische Gesamtarchitektur, in der Verwaltung, zentrale Logik, Sensorik, Aktorik und physischer Ausgabeprozess miteinander verbunden sind. Die endgültige Bewertung einzelner Funktionen sollte anhand der dokumentierten Testergebnisse erfolgen.

---

### **Reflexion**

Wie bei unserem bisherigen Portfolio soll jedes Teammitglied kurz auf die eigene Arbeit und die Zusammenarbeit eingehen. Dabei können beispielsweise folgende Punkte betrachtet werden:

**Kompetenzbogen:** [LF07 – Google Drive](https://drive.google.com/drive/folders/1hYJykWVRJvGD8WTam5FiKeJbFOsW51r1)