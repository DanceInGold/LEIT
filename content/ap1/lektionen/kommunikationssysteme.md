---
id: kommunikationssysteme
titel: "Kommunikationssysteme: Videokonferenz und Social Media im Unternehmen"
themen: [kommunikationssysteme]
reihenfolge: 1
voraussetzungen: []
dauer_min: 20
quelle: "Neu erstellt (Claude). Anforderungen an Videokonferenzsysteme nach BSI-Kompendium Videokonferenzsysteme und gängiger Praxis; Bandbreitenwerte als Annahmen gekennzeichnet und nachgerechnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 03.02: Kommunikationssysteme, z. B. Videokonferenz; Social Media neu aufgenommen (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "BSI: Kompendium Videokonferenzsysteme (KoViKo), 2020"}
status: geprüft
---

## Worum geht es?

Teams arbeiten an mehreren Standorten und im Homeoffice. **Videokonferenzen** ersetzen Reisen,
**Social Media** erreicht Kunden und Bewerber. Beides stellt Anforderungen an Technik, Sicherheit und
Datenschutz.

## Wie funktioniert es?

### Was eine Videokonferenz braucht

| Bereich | Anforderung |
| --- | --- |
| Endgerät | Kamera, Mikrofon (am besten Headset), Lautsprecher |
| Netzwerk | genug Bandbreite **im Upload**, geringe Latenz, stabile Verbindung |
| Software | Client oder Browser, Bildschirmfreigabe, Chat, Aufzeichnung |
| Sicherheit | Transportverschlüsselung, Wartebereich, Kennwort für Besprechungen |
| Datenschutz | Anbieter mit Sitz/Rechenzentrum in der EU oder AV-Vertrag, Aufzeichnung nur mit Einwilligung |

### Rechenbeispiel: reicht die Leitung des Standorts?

Annahme: Jeder Teilnehmer sendet ein HD-Videobild mit **2 Mbit/s** und empfängt die Bilder der anderen.
Am Standort sitzen **8 Personen** in **8 getrennten** Konferenzen.

1. Upload: 8 × 2 Mbit/s = **16 Mbit/s**
2. Der Anschluss bietet 100 Mbit/s Download, aber nur **10 Mbit/s Upload**.
3. 16 > 10 → **Der Upload reicht nicht.** Bilder ruckeln oder werden in der Qualität reduziert.

Lösung: Anschluss mit mehr Upload, Video nur bei Bedarf, oder ein gemeinsamer Konferenzraum.

### Social Media im Unternehmen

| Chancen | Risiken |
| --- | --- |
| Kunden direkt erreichen, Support | Shitstorm, Imageschaden |
| Fachkräfte und Azubis gewinnen | Datenschutz: Kundendaten in fremden Plattformen |
| Wissen teilen, Expertise zeigen | Social Engineering: Angreifer sammeln Infos über Mitarbeitende |
| kostengünstige Reichweite | versehentliche Veröffentlichung interner Details |

Eine **Social-Media-Richtlinie** regelt, wer für das Unternehmen sprechen darf und was nicht nach außen
gehört.

> **Halten wir kurz fest:**
>
> 1. Videokonferenz: Headset, Upload-Bandbreite, Verschlüsselung, Datenschutz.
> 2. Bandbreite pro Teilnehmer × Anzahl = Bedarf am Standort, meist ist der Upload der Engpass.
> 3. Social Media: Reichweite gegen Image-, Datenschutz- und Sicherheitsrisiken; Richtlinie hilft.

## Warum ist es so?

Bei normalen Internetanschlüssen ist der Upload oft viel kleiner als der Download. In einer
Videokonferenz **senden** alle aber gleichzeitig – deshalb fällt der Upload zuerst als Engpass auf.

<details>
<summary>Warum ist Social Media ein Sicherheitsthema?</summary>

Angreifer bereiten Phishing gezielt vor: Wer ist neu im Team, wer ist im Urlaub, welche Software nutzt
die Firma? Solche Details stehen oft öffentlich in Profilen. Eine bewusste Richtlinie und Schulungen
verringern dieses Risiko.

</details>

## Praxisbezug im Betrieb

- **Headsets statt Laptop-Mikrofon** reduzieren Echos deutlich.
- **Konferenzräume** mit eigener Hardware entlasten die Leitung gegenüber vielen Einzelverbindungen.
- **Bildschirm teilen:** vorher prüfen, ob vertrauliche Fenster offen sind.

## Typische Prüfungsfalle

- **Download statt Upload geprüft:** Bei Videokonferenzen zählt oft der Upload.
- **Datenschutz vergessen:** Aufzeichnungen und Anbieterwahl betreffen personenbezogene Daten.
- **Nur Vorteile von Social Media:** Risiken mit Gegenmaßnahme nennen.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Upload | Daten senden |
| Download | Daten empfangen |
| Latenz | Verzögerung bis zur Antwort, wichtig für Gespräche |
| Social-Media-Richtlinie | Regeln für Auftritte im Namen des Unternehmens |
| Social Engineering | Angriff über Täuschung von Menschen |

## Merksatz

**Video braucht Upload, Gespräche brauchen geringe Latenz – und Social Media braucht klare Regeln, wer
was sagen darf.**
