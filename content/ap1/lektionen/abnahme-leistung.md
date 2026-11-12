---
id: abnahme-leistung
titel: "Abnahme, Dokumentation und Leistungsbestätigung"
themen: [abnahme-doku, leistungsbestaetigung]
reihenfolge: 1
voraussetzungen: []
dauer_min: 25
quelle: "Neu erstellt (Claude). Abnahme beim Werkvertrag nach § 640 BGB; Mängelarten nach §§ 434, 437 BGB; Inhalte von Abnahmeprotokoll und Übergabedokumentation als Praxisbeispiel. Keine Rechtsberatung."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkte 07.07 (Abnahmeprotokoll, zu übergebende Dokumentation, Schlecht-/Falsch-/Minderlieferung) und 07.08 (Bestätigung erbrachter Leistungen, Nachkalkulation, Folgeaufträge) – Themenzuordnung siehe content/ap1/katalog.yaml"}
  - {titel: "BGB § 640 Abnahme; § 434 Sachmangel; § 437 Rechte des Käufers bei Mängeln", url: "https://www.gesetze-im-internet.de/bgb/"}
status: ungeprüft
---

## Worum geht es?

Das Projekt ist technisch fertig – aber erst mit der **[Abnahme](glossar:abnahme)** ist es auch
vertraglich abgeschlossen. Danach folgen Dokumentation, Leistungsbestätigung, Rechnung und im besten
Fall ein Folgeauftrag.

```mermaid
flowchart LR
  T["Test und<br/>Vorführung"] --> A["Abnahme mit<br/>Protokoll"]
  A --> D["Dokumentation<br/>übergeben"]
  D --> L["Leistung bestätigen,<br/>Rechnung"]
  L --> N["Nachkalkulation"]
  N --> F["Folgeauftrag?"]
```

## Wie funktioniert es?

### Was die Abnahme bewirkt

Beim Werkvertrag erklärt der Kunde mit der Abnahme: **Das Werk entspricht im Wesentlichen dem
Vertrag** (§ 640 BGB). Danach …

- wird die **Vergütung fällig**,
- beginnt die **Verjährungsfrist** für Mängelansprüche,
- muss im Streit der **Kunde** einen Mangel beweisen, vorher der Auftragnehmer die Mangelfreiheit.

### Das Abnahmeprotokoll

| Inhalt | Beispiel |
| --- | --- |
| Projekt, Vertragsparteien, Datum, Ort | Archivserver, ArchivTech und Kunde, 29.01.2027 |
| geprüfte Leistungen | Installation, Migration, Monitoring |
| Testergebnisse gegen das Pflichtenheft | Abrufzeit 1,6 s (Soll: unter 2 s) ✔ |
| festgestellte Mängel mit Frist | Alarm-Mail geht an falsche Adresse, Behebung bis 05.02. |
| Ergebnis | abgenommen / abgenommen mit Vorbehalt / verweigert |
| Unterschriften beider Seiten | |

Kleine Mängel verhindern die Abnahme nicht – sie werden **vorbehalten** und nachgebessert.

### Zu übergebende Dokumentation

- **Betriebsdokumentation:** Konfiguration, IP-Adressen, Zugänge (sicher übergeben)
- **Benutzerdokumentation:** Anleitung für die Anwender
- **Testprotokolle** und **Abnahmeprotokoll**
- **Lizenz- und Garantienachweise**, Seriennummern
- **Notfall- und Wiederherstellungsanleitung**

### Schlecht-, Falsch- und Minderlieferung

| Art | Bedeutung | Beispiel |
| --- | --- | --- |
| Schlechtlieferung | Sache hat einen Mangel | Netzteil defekt |
| Falschlieferung | andere Sache als bestellt | 16 GB statt 32 GB RAM |
| Minderlieferung | zu geringe Menge | 8 statt 10 Notebooks |

Der Kunde verlangt zuerst **Nacherfüllung**: reparieren, umtauschen oder nachliefern.

### Leistungsbestätigung, Nachkalkulation, Folgeaufträge

- **Leistungsbestätigung:** Der Kunde bestätigt Art und Umfang der erbrachten Leistung, oft mit
  Stundennachweis. Sie ist die Grundlage der Rechnung.
- **Nachkalkulation:** Plan und Ist vergleichen (siehe Kapitel Kalkulation).
- **Folgeaufträge:** Wartungsvertrag, Erweiterung, Schulungen – eine saubere Abnahme ist die beste
  Werbung.

> **Halten wir kurz fest:**
>
> 1. Abnahme = Kunde billigt das Werk; danach Zahlung fällig, Gewährleistungsfrist läuft.
> 2. Protokoll: Leistungen, Tests, Mängel mit Frist, Ergebnis, Unterschriften.
> 3. Schlecht- = Mangel, Falsch- = andere Sache, Minderlieferung = zu wenig.

## Warum ist es so?

Ohne Abnahme bleibt offen, ob der Vertrag erfüllt ist. Das Protokoll schafft Klarheit für beide Seiten
und verhindert späteren Streit darüber, was geliefert wurde.

<details>
<summary>Warum muss die Dokumentation mit übergeben werden?</summary>

Der Kunde muss das System betreiben, auch wenn der Dienstleister nicht da ist. Ohne Konfiguration,
Zugänge und Notfallanleitung wäre er abhängig. Oft ist die Dokumentation ausdrücklich Teil der
vereinbarten Leistung – fehlt sie, ist das Werk nicht vollständig.

</details>

## Praxisbezug im Betrieb

- **Abnahme vorbereiten:** Testfälle aus dem Pflichtenheft ableiten und gemeinsam durchgehen.
- **Zugangsdaten** nie im Protokoll, sondern über einen sicheren Weg (Passwortmanager, getrennte
  Übergabe).
- **Wartungsvertrag anbieten**, solange der Kunde zufrieden ist.

## Typische Prüfungsfalle

- **Abnahme = Lieferung:** Abnahme ist die **Billigung** des Werks, nicht nur die Übergabe.
- **Kleiner Mangel = Abnahme verweigert:** Unwesentliche Mängel werden vorbehalten.
- **Falsch- und Minderlieferung verwechselt:** andere Sache gegenüber zu geringer Menge.
- **Folgen der Abnahme vergessen:** Vergütung fällig, Frist beginnt, Beweislast wechselt.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Abnahme | Kunde billigt das Werk als vertragsgemäß |
| Abnahmeprotokoll | schriftliches Ergebnis der Abnahme |
| Leistungsbestätigung | Kunde bestätigt erbrachte Leistungen, Grundlage der Rechnung |
| Schlechtlieferung | Ware mit Mangel |
| Falschlieferung | andere Ware als bestellt |
| Minderlieferung | zu geringe Menge |

## Merksatz

**Testen, abnehmen, protokollieren, dokumentieren – mit der Unterschrift wird bezahlt, die
Gewährleistung beginnt, und der nächste Auftrag ist in Reichweite.**
