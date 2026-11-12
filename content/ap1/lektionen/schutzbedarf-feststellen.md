---
id: schutzbedarf-feststellen
titel: "Schutzbedarf feststellen: normal, hoch, sehr hoch"
themen: [bsi-schutzbedarf]
reihenfolge: 1
voraussetzungen: [schutzziele]
dauer_min: 35
quelle: "Neu erstellt (Claude). Schutzbedarfskategorien und Schadensszenarien wörtlich nach BSI-Standard 200-2, Kapitel 8.2.1; Beispielbewertung fiktiv."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 06.03: Schutzbedarfskategorien (normal, hoch, sehr hoch) ableiten und begründen (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "BSI-Standard 200-2: IT-Grundschutz-Methodik, Kapitel 8.2.1 Definition der Schutzbedarfskategorien, Schadensszenarien", url: "https://dhge.de/DHGE/dam/jcr:d14c502f-f112-475b-aace-64f5f6041088/BSI_Standard_200-2.pdf"}
status: ungeprüft
---

## Worum geht es?

Nicht alles braucht Hochsicherheit. Der Speiseplan der Kantine ist weniger schützenswert als die
Personalakten. Die **[Schutzbedarfsfeststellung](glossar:schutzbedarf)** nach BSI-Grundschutz klärt:
**Wie schlimm wäre ein Schaden?**

- Bewertet wird je **Schutzziel**: Vertraulichkeit, Integrität, Verfügbarkeit.
- Ergebnis ist eine von **drei Kategorien**: normal, hoch, sehr hoch.
- Die Prüfung verlangt: Kategorie **ableiten und begründen**.

## Wie funktioniert es?

### Die drei Kategorien (BSI-Standard 200-2)

| Kategorie | Definition |
| --- | --- |
| **normal** | „Die Schadensauswirkungen sind begrenzt und überschaubar.“ |
| **hoch** | „Die Schadensauswirkungen können beträchtlich sein.“ |
| **sehr hoch** | „Die Schadensauswirkungen können ein existentiell bedrohliches, katastrophales Ausmaß erreichen.“ |

Was „beträchtlich“ heißt, legt jede Firma selbst fest – etwa in Euro, in Ausfallstunden oder in
der Zahl betroffener Personen.

### Die sechs Schadensszenarien

Damit die Bewertung nicht aus dem Bauch kommt, fragt man nach sechs Szenarien:

1. Verstoß gegen **Gesetze, Vorschriften, Verträge**
2. Beeinträchtigung des **informationellen Selbstbestimmungsrechts** (Datenschutz)
3. Beeinträchtigung der **persönlichen Unversehrtheit**
4. Beeinträchtigung der **Aufgabenerfüllung**
5. **negative Innen- oder Außenwirkung** (Image)
6. **finanzielle Auswirkungen**

Für jedes Schutzziel gilt das **schlimmste** Szenario.

### Beispiel einer Abgrenzungstabelle

Die ArchivTech legt fest, was die Kategorien für sie bedeuten:

| Szenario | normal | hoch | sehr hoch |
| --- | --- | --- | --- |
| finanzielle Auswirkungen | unter 10.000 € | bis 500.000 € | über 500.000 € |
| Aufgabenerfüllung (Ausfall) | bis 24 h tolerierbar | bis 4 h tolerierbar | keine Stunde tolerierbar |
| Datenschutz | geringe Folgen für Betroffene | erhebliche Folgen | Gefahr für Leib, Leben, Existenz |

### Rechenbeispiel: das Kundenarchiv bewerten

Im Archiv liegen Verträge und Personalunterlagen von Kunden.

| Schutzziel | Kategorie | Begründung |
| --- | --- | --- |
| Vertraulichkeit | **hoch** | Personaldaten Dritter; ein Leck verstößt gegen DSGVO und Kundenverträge und schadet dem Ruf erheblich |
| Integrität | **hoch** | verfälschte Verträge können rechtliche Folgen und Schadensersatz nach sich ziehen |
| Verfügbarkeit | **normal** | ein Ausfall von einem Tag ist für Archivabrufe tolerierbar |

So sieht eine Prüfungsantwort aus: **Kategorie + Szenario + konkreter Grund**.

> **Halten wir kurz fest:**
>
> 1. Je Schutzziel eine Kategorie: normal, hoch, sehr hoch.
> 2. Begründung über die sechs Schadensszenarien.
> 3. Das schwerste Szenario bestimmt die Kategorie.

## Warum ist es so?

Sicherheit kostet Geld und Bequemlichkeit. Mit dem Schutzbedarf setzt man **Prioritäten**: Wo er hoch
ist, lohnen sich starke Maßnahmen. Wo er normal ist, reichen die Standardmaßnahmen des Grundschutzes.

<details>
<summary>Warum je Schutzziel getrennt bewerten?</summary>

Ein öffentlicher Webauftritt hat **keine** vertraulichen Inhalte (Vertraulichkeit normal), darf aber
nicht ausfallen oder verfälscht werden (Verfügbarkeit und Integrität hoch). Eine Gesamtnote „hoch“
würde unnötig teure Verschlüsselung verlangen und die eigentliche Schwäche verdecken.

</details>

## Praxisbezug im Betrieb

- **Neue Anwendung einführen:** Vor dem Betrieb wird der Schutzbedarf festgestellt; daraus folgen
  Backup-Takt, Zugriffsrechte und Überwachung.
- **Mit dem Fachbereich bewerten:** Wie schlimm ein Ausfall ist, weiß der Fachbereich oft besser als
  die IT.
- **Dokumentieren:** Die Tabelle wird Teil des Sicherheitskonzepts und regelmäßig überprüft.

## Typische Prüfungsfalle

- **Nur die Kategorie genannt:** Ohne Begründung gibt es kaum Punkte.
- **Eine Kategorie für alles:** Bewerte Vertraulichkeit, Integrität und Verfügbarkeit einzeln.
- **„mittel“ oder „niedrig“:** Die BSI-Kategorien heißen normal, hoch, sehr hoch.
- **Szenario passt nicht zum Schutzziel:** Ein Ausfall betrifft die Verfügbarkeit, nicht die
  Vertraulichkeit.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Schutzziel | **was** geschützt wird: V, I, V |
| Schutzbedarf | **wie sehr** es geschützt werden muss |
| Schadensszenario | Blickwinkel, aus dem man den Schaden bewertet |
| Schutzbedarfskategorie | normal, hoch oder sehr hoch |

## Merksatz

**Normal ist überschaubar, hoch beträchtlich, sehr hoch existenzbedrohend – je Schutzziel einzeln,
und immer mit Szenario begründet.**
