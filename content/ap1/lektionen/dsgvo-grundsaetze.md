---
id: dsgvo-grundsaetze
titel: "Datenschutz nach DSGVO: Grundsätze, Rechtsgrundlagen, Einwilligung"
themen: [datenschutz]
reihenfolge: 1
voraussetzungen: []
dauer_min: 35
quelle: "Neu erstellt (Claude). Alle Aussagen nach dem Wortlaut der DSGVO (Art. 4, 5, 6, 7, 9, 37) und § 38 BDSG; Beispiele fiktiv. Keine Rechtsberatung."
belege:
  - {titel: "Prüfungskatalog AP1 2025: Datenschutz nach DSGVO und BDSG (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "Verordnung (EU) 2016/679 (DSGVO), Art. 4, 5, 6, 7, 9, 37", url: "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679"}
  - {titel: "§ 38 BDSG: Datenschutzbeauftragte nichtöffentlicher Stellen (in der Regel mindestens 20 Personen)", url: "https://www.gesetze-im-internet.de/bdsg_2018/__38.html"}
status: geprüft
---

## Worum geht es?

Informationssicherheit schützt **Daten** des Unternehmens. Datenschutz schützt **Menschen** – ihr
Recht, selbst über ihre Daten zu bestimmen.

- Grundlage ist die **DSGVO** (EU, seit 25.05.2018), ergänzt durch das deutsche **BDSG**.
- Sie gilt für **[personenbezogene Daten](glossar:personenbezogene-daten)**.
- Dieses Kapitel: Begriffe, sieben Grundsätze, Rechtsgrundlagen, Einwilligung.
  Das nächste: Rechte der Betroffenen, Anonymisierung, Datenpannen.

## Wie funktioniert es?

### Was sind personenbezogene Daten?

Alle Informationen, die sich auf eine **identifizierte oder identifizierbare** Person beziehen
(Art. 4 Nr. 1).

| personenbezogen | nicht personenbezogen |
| --- | --- |
| Name, E-Mail `m.muster@kunde.example` | Durchschnittsalter aller Kunden |
| IP-Adresse, Kundennummer | Wetterdaten |
| Login-Protokoll mit Benutzername | Seriennummer eines Lagerservers |

**Besondere Kategorien** (Art. 9) sind besonders geschützt: Gesundheit, Religion, ethnische Herkunft,
politische Meinung, Gewerkschaftszugehörigkeit, genetische und biometrische Daten, Sexualleben.

### Die sieben Grundsätze (Art. 5)

| Grundsatz | heißt im Alltag |
| --- | --- |
| Rechtmäßigkeit, Treu und Glauben, Transparenz | nur mit Rechtsgrundlage, offen erklärt |
| Zweckbindung | nur für den Zweck, für den erhoben wurde |
| Datenminimierung | nur so viel wie nötig |
| Richtigkeit | falsche Daten berichtigen oder löschen |
| Speicherbegrenzung | löschen, wenn der Zweck erfüllt ist |
| Integrität und Vertraulichkeit | technisch und organisatorisch schützen |
| Rechenschaftspflicht | Einhaltung **nachweisen** können |

### Ohne Rechtsgrundlage keine Verarbeitung (Art. 6)

Jede Verarbeitung braucht **mindestens eine** dieser Grundlagen:

| Buchstabe | Rechtsgrundlage | Beispiel |
| --- | --- | --- |
| a | Einwilligung | Newsletter |
| b | Vertrag oder Vertragsanbahnung | Lieferadresse für die Bestellung |
| c | rechtliche Verpflichtung | Rechnungen aufbewahren (Steuerrecht) |
| d | lebenswichtige Interessen | Notfall |
| e | öffentliche Aufgabe | Behörden |
| f | berechtigtes Interesse (mit Abwägung) | Videoüberwachung des Serverraums |

### Die Einwilligung (Art. 7)

Eine gültige Einwilligung ist …

- **freiwillig** – ohne Druck, nicht an andere Leistungen gekoppelt, wenn unnötig,
- **informiert** – Zweck und Verantwortlicher sind klar,
- **eindeutig** – aktive Handlung, kein vorangekreuztes Häkchen,
- **jederzeit widerrufbar** – so einfach wie erteilt.

Der Verantwortliche muss sie **nachweisen** können.

### Wer ist wer?

| Rolle | Wer | Beispiel |
| --- | --- | --- |
| Betroffene Person | deren Daten verarbeitet werden | Kunde |
| Verantwortlicher | entscheidet über Zweck und Mittel | ArchivTech als Arbeitgeber |
| Auftragsverarbeiter | verarbeitet im Auftrag (Art. 28) | ArchivTech, die für Kunden archiviert |
| Datenschutzbeauftragter | berät und überwacht | Pflicht in Deutschland in der Regel ab 20 Personen, die ständig automatisiert verarbeiten (§ 38 BDSG) |

> **Halten wir kurz fest:**
>
> 1. Personenbezogen = Person identifizierbar, auch über IP oder Kundennummer.
> 2. Sieben Grundsätze, u. a. Zweckbindung, Datenminimierung, Speicherbegrenzung.
> 3. Keine Verarbeitung ohne Rechtsgrundlage; Einwilligung nur eine von sechs.

## Warum ist es so?

Wer viele Daten über Menschen hat, hat Macht über sie. Die DSGVO dreht die Logik um: Verarbeiten ist
**verboten, außer** es ist erlaubt (Verbot mit Erlaubnisvorbehalt).

<details>
<summary>Warum ist die Einwilligung oft die schlechteste Rechtsgrundlage?</summary>

Sie kann jederzeit widerrufen werden – dann muss die Verarbeitung enden. Für Dinge, die für den
Vertrag nötig sind (Lieferadresse) oder gesetzlich vorgeschrieben (Rechnungen), passt deshalb
Art. 6 Abs. 1 lit. b oder c besser. Die Einwilligung ist für Freiwilliges gedacht.

</details>

## Praxisbezug im Betrieb

- **Logs** enthalten Benutzernamen und IP-Adressen – also personenbezogene Daten. Aufbewahrungsdauer
  festlegen.
- **Testdaten:** Echte Kundendaten gehören nicht in Testsysteme; besser pseudonymisieren oder
  künstliche Daten erzeugen.
- **Archivierung im Kundenauftrag** braucht einen Auftragsverarbeitungsvertrag (AVV, Art. 28).

## Typische Prüfungsfalle

- **IP-Adresse nicht personenbezogen:** Sie kann eine Person identifizierbar machen und zählt deshalb
  dazu.
- **Einwilligung als einzige Grundlage:** Es gibt sechs.
- **Vorangekreuztes Häkchen:** Keine gültige Einwilligung.
- **Datenschutz = IT-Sicherheit:** Datenschutz schützt Personen, IT-Sicherheit alle Informationen.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Datenschutz | Schutz von Personen vor Missbrauch ihrer Daten |
| Informationssicherheit | Schutz aller Informationen (V, I, V) |
| Verantwortlicher | entscheidet über Zweck und Mittel |
| Auftragsverarbeiter | verarbeitet weisungsgebunden im Auftrag |
| Zweckbindung | nur für den ursprünglichen Zweck |
| Datenminimierung | nur so viel wie nötig |

## Merksatz

**Ohne Rechtsgrundlage nichts, nur so viel wie nötig, nur für den Zweck, nur so lange wie nötig – und
alles nachweisbar.**
