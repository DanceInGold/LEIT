---
id: schutzziele
titel: "Schutzziele: Vertraulichkeit, Integrität, Verfügbarkeit"
themen: [schutzziele]
reihenfolge: 1
voraussetzungen: []
dauer_min: 25
quelle: "Neu erstellt (Claude). Schutzziele nach BSI IT-Grundschutz (Glossar) und BSI-Standard 200-2; erweiterte Schutzziele nach gängiger Fachliteratur."
belege:
  - {titel: "Prüfungskatalog AP1 2025: Schutzziele (Vertraulichkeit, Verfügbarkeit, Integrität) ausdrücklich genannt (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "BSI-Standard 200-2: IT-Grundschutz-Methodik (Grundwerte Vertraulichkeit, Integrität, Verfügbarkeit)", url: "https://dhge.de/DHGE/dam/jcr:d14c502f-f112-475b-aace-64f5f6041088/BSI_Standard_200-2.pdf"}
status: ungeprüft
---

## Worum geht es?

Informationssicherheit klingt nach Firewalls und Virenscannern. Dahinter stehen aber drei einfache
Fragen – die **[Schutzziele](glossar:schutzziele)**:

| Schutzziel | Frage | Analogie |
| --- | --- | --- |
| **Vertraulichkeit** | Sehen nur Befugte die Daten? | verschlossener Brief |
| **Integrität** | Sind die Daten richtig und unverändert? | Siegel auf dem Umschlag |
| **Verfügbarkeit** | Sind Daten und Systeme da, wenn man sie braucht? | Post kommt pünktlich an |

Eselsbrücke: **CIA** – Confidentiality, Integrity, Availability.

Jede Sicherheitsmaßnahme dient mindestens einem dieser Ziele. Darauf bauen Schutzbedarf, TOM und
ISMS in den nächsten Kapiteln auf.

## Wie funktioniert es?

### Bedrohung und Maßnahme je Schutzziel

Beispiel Archivsystem der ArchivTech GmbH:

| Schutzziel | Bedrohung | Maßnahme |
| --- | --- | --- |
| Vertraulichkeit | Unbefugter liest Personalakten im Archiv | Berechtigungskonzept, Verschlüsselung |
| Integrität | Rechnungsbetrag wird nachträglich geändert | Hashwerte, Signaturen, Protokollierung |
| Verfügbarkeit | Festplattenausfall, Ransomware | Datensicherung, Redundanz, USV |

### Die erweiterten Schutzziele

Neben den drei Grundwerten nennen viele Quellen weitere Ziele:

| Schutzziel | Bedeutung | Beispiel |
| --- | --- | --- |
| Authentizität | Echtheit: Daten stammen wirklich vom angegebenen Absender | Zertifikat, Signatur |
| Verbindlichkeit (Nichtabstreitbarkeit) | Wer etwas getan hat, kann es nicht leugnen | signierte Freigabe |
| Zurechenbarkeit | Aktionen lassen sich einer Person zuordnen | persönliche Konten, Logs |

Im Katalog stehen ausdrücklich die **drei Grundwerte**.

### Ein Vorfall, mehrere Ziele

Viele Angriffe treffen mehrere Ziele zugleich. **Ransomware** zum Beispiel:

1. verschlüsselt Daten → **Verfügbarkeit** weg
2. lädt Daten vorher heraus und droht mit Veröffentlichung → **Vertraulichkeit** verletzt
3. kann Dateien verändern → **Integrität** fraglich

> **Halten wir kurz fest:**
>
> 1. Vertraulichkeit = nur Befugte, Integrität = unverändert und korrekt, Verfügbarkeit = nutzbar,
>    wenn nötig.
> 2. Erweitert: Authentizität, Verbindlichkeit, Zurechenbarkeit.
> 3. Ein Vorfall kann mehrere Schutzziele verletzen.

## Warum ist es so?

Ohne gemeinsame Begriffe redet jeder über „Sicherheit“ – und meint etwas anderes. Die Schutzziele
machen klar, **was** geschützt werden soll. Erst dann lässt sich die passende Maßnahme wählen.

<details>
<summary>Warum gibt es manchmal Zielkonflikte?</summary>

Mehr Vertraulichkeit kann Verfügbarkeit kosten: Ist ein Archiv stark verschlüsselt und der Schlüssel
geht verloren, sind die Daten sicher – aber für immer weg. Eine zweite Kopie erhöht die
Verfügbarkeit, schafft aber eine weitere Stelle, die vertraulich bleiben muss. Gute Planung wägt ab.

</details>

## Praxisbezug im Betrieb

- **Ticket bewerten:** „Nur Lesezugriff für alle“ betrifft die Vertraulichkeit, „Server langsam“ die
  Verfügbarkeit.
- **Prüfsummen bei Archivdaten** sichern die Integrität über Jahre – Bitfehler fallen beim Prüfen auf.
- **Monitoring** überwacht die Verfügbarkeit, **Logs** sichern die Zurechenbarkeit.

## Typische Prüfungsfalle

- **Integrität mit Verfügbarkeit verwechselt:** Gelöschte Daten = Verfügbarkeit, veränderte Daten =
  Integrität.
- **Verschlüsselung für Verfügbarkeit:** Verschlüsselung schützt die **Vertraulichkeit**.
- **Nur ein Ziel genannt:** Fragt die Aufgabe nach betroffenen Schutzzielen, prüfe alle drei.
- **Authentizität als Grundwert:** Im BSI-Grundschutz sind die Grundwerte V, I, V.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Vertraulichkeit | Schutz vor unbefugtem **Lesen** |
| Integrität | Schutz vor unbemerktem **Verändern** |
| Verfügbarkeit | Schutz vor **Ausfall** |
| Authentizität | Echtheit des Absenders oder der Daten |
| Verbindlichkeit | Handlung kann nicht abgestritten werden |

## Merksatz

**C-I-A: Nur Befugte lesen, nichts wird heimlich verändert, und alles ist da, wenn man es braucht.**
