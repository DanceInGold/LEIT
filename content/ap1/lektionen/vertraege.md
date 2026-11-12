---
id: vertraege
titel: "Verträge: Vertragsarten, Bestandteile und Vertragsstörungen"
themen: [vertraege]
reihenfolge: 1
voraussetzungen: []
dauer_min: 35
quelle: "Neu erstellt (Claude). Nach BGB (§§ 286, 293, 339, 433, 434, 437–439, 535, 611, 631, 640) und § 377 HGB; Zusammenfassung der Mängelrechte nach IHK Pfalz; Beispiele fiktiv. Keine Rechtsberatung."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 07.01: Vertragsbestandteile, z. B. Leistungsbeschreibung, Termine, Entgelte, Lasten- und Pflichtenheft, Konventionalstrafen; Vertragsstörungen (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "§ 434 Abs. 5 BGB: Einem Sachmangel steht es gleich, wenn der Verkäufer eine andere Sache als die vertraglich geschuldete Sache liefert", url: "https://lxgesetze.de/bgb/434"}
  - {titel: "IHK Pfalz: Mängelanspruch, Garantie, Gewährleistung (2 Jahre ab Ablieferung, Nacherfüllung, Rücktritt, Minderung, Schadensersatz, § 377 HGB)", url: "https://www.ihk.de/pfalz/recht/recht/maengelanspruch-garantie-gewaehrleistung-1274082"}
status: ungeprüft
---

## Worum geht es?

IT-Dienstleister verkaufen Hardware, erstellen Software, betreuen Systeme. Jedes Mal steckt ein
**anderer Vertragstyp** dahinter – mit anderen Pflichten. Und manchmal läuft etwas schief:
**Vertragsstörungen**.

- vier Vertragsarten, die in der IT ständig vorkommen
- was in einen Vertrag gehört
- was bei Verzug und Mängeln passiert

## Wie funktioniert es?

### Vier Vertragsarten

| Vertrag | geschuldet ist … | IT-Beispiel | BGB |
| --- | --- | --- | --- |
| **Kaufvertrag** | Übergabe einer mangelfreien Sache und Eigentum | 10 Notebooks | § 433 |
| **[Werkvertrag](glossar:werkvertrag)** | ein **Erfolg**, ein fertiges Werk | Archivserver betriebsbereit einrichten | § 631 |
| **Dienstvertrag** | eine **Tätigkeit**, kein Erfolg | Admin-Stunden nach Aufwand, Schulung | § 611 |
| **Mietvertrag** | Gebrauch auf Zeit | Server für eine Messe | § 535 |

Die wichtigste Unterscheidung: **Werkvertrag = Erfolg**, **Dienstvertrag = Bemühen**.

### Was in einen Vertrag gehört

| Bestandteil | Beispiel |
| --- | --- |
| Vertragspartner | ArchivTech GmbH und Kunde |
| Leistungsbeschreibung | Pflichtenheft als Anlage |
| Termine | Fertigstellung bis 29.01.2027 |
| Entgelt und Zahlungsbedingungen | 2.760 € netto, 30 Tage netto |
| Abnahme | Abnahmeprotokoll nach erfolgreichem Test |
| Konventionalstrafe (Vertragsstrafe, § 339) | 200 € je Tag Verzug, höchstens 5 % |
| Gewährleistung, Haftung, Gerichtsstand | |

### Vertragsstörungen

| Störung | Wer? | Beispiel |
| --- | --- | --- |
| **Lieferverzug** | Verkäufer | Server kommt nach dem vereinbarten Termin (§ 286) |
| **mangelhafte Lieferung** | Verkäufer | Netzteil defekt, falsches Modell geliefert |
| **Annahmeverzug** | Käufer | Kunde nimmt die Lieferung nicht an (§ 293) |
| **Zahlungsverzug** | Käufer | Rechnung nach Fristablauf nicht bezahlt |

### Mangelhafte Lieferung: die Rechte des Käufers

Eine Sache ist mangelhaft, wenn sie nicht der Vereinbarung oder dem Üblichen entspricht. Auch eine
**Falschlieferung** (andere Sache) steht einem Mangel gleich (§ 434 Abs. 5).

```mermaid
flowchart LR
  M["Mangel"] --> N["1. Nacherfüllung<br/>Reparatur oder neue Sache<br/>(Käufer wählt)"]
  N -->|"scheitert oder<br/>Frist verstrichen"| R["2. Rücktritt<br/>oder Minderung"]
  N -->|"bei Verschulden"| S["Schadensersatz"]
```

- **Vorrang der Nacherfüllung:** Der Verkäufer bekommt zuerst eine Chance (§ 439).
- **Frist:** Mängelansprüche verjähren bei beweglichen Sachen in der Regel nach **2 Jahren ab
  Ablieferung** (§ 438).
- **Zwischen Kaufleuten:** Ware **unverzüglich prüfen** und Mängel rügen (§ 377 HGB), sonst gehen die
  Rechte verloren.

> **Halten wir kurz fest:**
>
> 1. Kauf = Sache, Werk = Erfolg, Dienst = Tätigkeit, Miete = Gebrauch auf Zeit.
> 2. Vertrag: Leistung, Termine, Entgelt, Abnahme, Vertragsstrafe.
> 3. Mangel: erst Nacherfüllung, dann Rücktritt oder Minderung, bei Verschulden Schadensersatz.

## Warum ist es so?

Der Vertragstyp bestimmt, wofür ein Dienstleister haftet. Beim Werkvertrag schuldet er das
funktionierende Ergebnis – beim Dienstvertrag „nur“ sorgfältige Arbeit.

<details>
<summary>Warum ist Gewährleistung etwas anderes als Garantie?</summary>

Die **Gewährleistung** ist gesetzlich: Der Verkäufer haftet dafür, dass die Sache bei Übergabe
mangelfrei ist. Eine **Garantie** ist ein freiwilliges Zusatzversprechen (§ 443), oft vom Hersteller,
mit eigenen Bedingungen. Sie gilt zusätzlich, ersetzt die Gewährleistung aber nicht.

</details>

<details>
<summary>Und wenn zu wenig geliefert wird?</summary>

Kommen nur 8 statt 10 Notebooks, verlangt der Käufer die fehlenden 2 nach. Ob eine Zuweniglieferung
rechtlich als Sachmangel oder als nur teilweise erbrachte Leistung gilt, wird seit der BGB-Reform 2022
unterschiedlich beurteilt. Für die Praxis zählt: sofort prüfen, rügen und dokumentieren.

</details>

## Praxisbezug im Betrieb

- **Wareneingang prüfen:** Anzahl, Modell, Schäden – sofort, nicht erst bei der Installation (§ 377 HGB).
- **Werk oder Dienst?** Ein Festpreis für „Server betriebsbereit“ ist meist ein Werkvertrag; „40
  Stunden Unterstützung“ ein Dienstvertrag.
- **Vertragsstrafen** stehen oft in Kundenverträgen – Termine im Projektplan entsprechend absichern.

## Typische Prüfungsfalle

- **Werk- und Dienstvertrag vertauscht:** Erfolg oder Tätigkeit?
- **Sofort Rücktritt verlangt:** Zuerst kommt die Nacherfüllung.
- **Annahmeverzug beim Verkäufer:** Annahmeverzug betrifft den **Käufer**.
- **Garantie = Gewährleistung:** Garantie ist freiwillig, Gewährleistung gesetzlich.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Werkvertrag | Erfolg geschuldet, Abnahme nötig |
| Dienstvertrag | Tätigkeit geschuldet, kein Erfolg |
| Lieferverzug | Verkäufer liefert zu spät |
| Annahmeverzug | Käufer nimmt nicht an |
| Gewährleistung | gesetzliche Mängelhaftung des Verkäufers |
| Garantie | freiwilliges Zusatzversprechen |
| Konventionalstrafe | vereinbarte Strafe, z. B. bei Verzug |

## Merksatz

**Kauf liefert eine Sache, Werk einen Erfolg, Dienst eine Tätigkeit. Bei Mängeln darf der Verkäufer
zuerst nachbessern – erst danach kommen Rücktritt oder Minderung.**
