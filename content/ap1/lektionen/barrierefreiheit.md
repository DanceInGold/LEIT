---
id: barrierefreiheit
titel: "Barrierefreiheit: Arbeitsplatz, IT-Systeme und Websites"
themen: [barrierefreiheit]
reihenfolge: 1
voraussetzungen: []
dauer_min: 30
quelle: "Neu erstellt (Claude). Prinzipien nach W3C WCAG 2.2; Pflichten nach Barrierefreiheitsstärkungsgesetz (BFSG, anzuwenden seit 28.06.2025) und BITV 2.0; Hilfsmittel nach Katalogwortlaut. Keine Rechtsberatung."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkte 03.03, 04.02, 04.07: Barrierefreier Zugriff auf IT-Systeme, z. B. Einstellungsmöglichkeiten auf Webseiten; Unterstützung durch zusätzliche Hardware (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "W3C: Web Content Accessibility Guidelines (WCAG) 2.2", url: "https://www.w3.org/TR/WCAG22/"}
  - {titel: "Barrierefreiheitsstärkungsgesetz (BFSG)", url: "https://www.gesetze-im-internet.de/bfsg/"}
  - {titel: "Destatis, Pressemitteilung Juli 2026: 7,8 Millionen schwerbehinderte Menschen leben in Deutschland", url: "https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/07/PD26_246_227.html"}
status: ungeprüft
---

## Worum geht es?

**[Barrierefreiheit](glossar:barrierefreiheit)** heißt: Alle Menschen können IT nutzen – auch mit
Seh-, Hör-, motorischen oder kognitiven Einschränkungen. Der Katalog 2025 nennt drei Ebenen:

| Ebene | Beispiel |
| --- | --- |
| **Arbeitsplatz** | größerer Monitor, Spezialtastatur, Headset |
| **IT-System** | Bildschirmlupe, Sprachausgabe, hoher Kontrast |
| **Website** | Alternativtexte, Tastaturbedienung, gute Kontraste |

Seit dem **28.06.2025** gilt in Deutschland das **Barrierefreiheitsstärkungsgesetz** (BFSG): Viele
Produkte und Dienstleistungen, etwa Online-Shops und Banking, müssen barrierefrei sein.

## Wie funktioniert es?

### Arbeitsplatz: Hardware

| Einschränkung | Hilfsmittel |
| --- | --- |
| Sehen | großer Monitor, zweiter Monitor, Braillezeile |
| Hören | Headset mit Verstärkung, visuelle Signale statt Töne |
| Motorik | breitere oder ergonomische Tastatur, Trackball, Spracheingabe |
| Sprechen | Texteingabe statt Telefon, Chat |

### IT-System: Einstellungen

- Bildschirmlupe, Schrift vergrößern, Skalierung
- Kontrastmodus, Dunkelmodus, Farbfilter für Farbfehlsichtigkeit
- Screenreader (Sprachausgabe)
- Untertitel, Sprachsteuerung
- Einrastfunktion für Tastenkombinationen

### Websites: die vier Prinzipien der WCAG

| Prinzip | Bedeutung | Beispiel |
| --- | --- | --- |
| **wahrnehmbar** | Inhalte lassen sich mit verschiedenen Sinnen erfassen | Alternativtext für Bilder, Untertitel, Kontrast |
| **bedienbar** | alles ist ohne Maus nutzbar | Tastaturbedienung, sichtbarer Fokus, genug Zeit |
| **verständlich** | Inhalte und Bedienung sind klar | einfache Sprache, verständliche Fehlermeldungen |
| **robust** | funktioniert mit Hilfstechnik | sauberes HTML, beschriftete Formularfelder |

Eselsbrücke aus dem Englischen: **POUR** (perceivable, operable, understandable, robust).

### Beispiel: ein barrierefreies Formularfeld

```html
<label for="kundennr">Kundennummer</label>
<input id="kundennr" name="kundennr" type="text" required>
```

Der Screenreader liest „Kundennummer, Eingabefeld, erforderlich“. Ohne `<label>` hört man nur
„Eingabefeld“ – und weiß nicht, was hinein soll.

> **Halten wir kurz fest:**
>
> 1. Barrierefreiheit auf drei Ebenen: Arbeitsplatz-Hardware, Systemeinstellungen, Websites.
> 2. WCAG: wahrnehmbar, bedienbar, verständlich, robust.
> 3. Seit 28.06.2025 verpflichtet das BFSG viele Unternehmen zu barrierefreien Angeboten.

## Warum ist es so?

Laut Statistischem Bundesamt leben rund 7,8 Millionen Menschen mit schwerer Behinderung in Deutschland
– fast jeder Zehnte. Dazu kommen ältere Menschen und vorübergehende Einschränkungen. Barrierefreiheit hilft außerdem allen – Untertitel im
lauten Zug, Tastaturbedienung für Power-User.

<details>
<summary>Warum ist ein Alternativtext so wichtig?</summary>

Ein Screenreader kann ein Bild nicht sehen. Ohne Alternativtext liest er nur „Bild“ oder den
Dateinamen. Ein guter Alternativtext beschreibt den **Zweck**: nicht „Diagramm“, sondern „Abrufzeit
sinkt von 8 auf 1,6 Sekunden“.

</details>

## Praxisbezug im Betrieb

- **Arbeitsplatz einrichten:** Bei Bedarf Hilfsmittel beantragen, oft mit Förderung.
- **Interne Anwendungen** mit der Tastatur testen: Kommt man überall hin?
- **Kundenportal:** Kontraste, Formularbeschriftungen und Fehlermeldungen prüfen – Prüfwerkzeuge im
  Browser helfen.

## Typische Prüfungsfalle

- **Nur an Rollstühle gedacht:** Es geht um alle Einschränkungen, auch Sehen, Hören, Kognition.
- **Barrierefreiheit = Design-Frage:** Es geht um Nutzbarkeit und ist teilweise gesetzlich vorgeschrieben.
- **Farbe als einzige Information:** Rot/Grün allein erkennen nicht alle.
- **Maßnahme ohne Ebene:** Sag, ob Hardware, Systemeinstellung oder Website gemeint ist.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| WCAG | internationale Richtlinien für barrierefreie Webinhalte (W3C) |
| BFSG | deutsches Gesetz, verpflichtet viele Unternehmen seit 2025 |
| BITV 2.0 | Verordnung für öffentliche Stellen |
| Screenreader | liest Bildschirminhalte vor |
| Braillezeile | gibt Text in Blindenschrift aus |

## Merksatz

**Wahrnehmbar, bedienbar, verständlich, robust – und ein Bild ohne Alternativtext ist für viele
unsichtbar.**
