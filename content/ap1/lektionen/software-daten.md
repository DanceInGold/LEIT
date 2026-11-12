---
id: software-daten
titel: "Softwarearten, ERP/CRM/SCM sowie Stamm- und Bewegungsdaten"
themen: [software-arten, stamm-bewegungsdaten]
reihenfolge: 1
voraussetzungen: []
dauer_min: 30
quelle: "Neu erstellt (Claude). Einteilung von Software und Unternehmensanwendungen nach gängiger Wirtschaftsinformatik-Literatur; Stamm- und Bewegungsdaten nach betriebswirtschaftlicher Standardliteratur; Beispiele fiktiv."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkte 03.01 (Standard-, Branchensoftware, z. B. ERP, SCM, CRM; Systemsoftware; Entwicklungssysteme; KI-Software) und 01.02 (Stamm- und Bewegungsdaten) (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
status: ungeprüft
---

## Worum geht es?

Software ist nicht gleich Software. Der Katalog unterscheidet mehrere **Arten** und nennt die
Unternehmensanwendungen **ERP, SCM, CRM** ausdrücklich. Dazu kommt eine Frage, die in jedem dieser
Systeme steckt: Welche Daten ändern sich selten, welche ständig?

## Wie funktioniert es?

### Softwarearten

| Art | Zweck | Beispiele |
| --- | --- | --- |
| **Systemsoftware** | betreibt die Hardware, Grundlage für alles andere | Betriebssystem, Treiber, Firmware |
| **Standardsoftware** | für viele Nutzer gleich, gekauft oder abonniert | Office-Paket, Browser, Datenbanksystem |
| **Branchensoftware** | für eine bestimmte Branche | Praxissoftware für Ärzte, Warenwirtschaft im Handel |
| **Individualsoftware** | eigens für ein Unternehmen entwickelt | Archivportal der ArchivTech |
| **Entwicklungssysteme** | Software entwickeln | Compiler, Interpreter, Editor, Debugger, IDE |
| **KI-Software** | Texte, Code, Bilder erzeugen oder auswerten | Chat-Assistent, Code-Assistent |

### Unternehmensanwendungen

| Abkürzung | Langform | Aufgabe |
| --- | --- | --- |
| **ERP** | Enterprise Resource Planning | steuert die Ressourcen des ganzen Unternehmens: Einkauf, Lager, Produktion, Vertrieb, Finanzen, Personal |
| **SCM** | Supply Chain Management | plant die Lieferkette vom Lieferanten bis zum Kunden |
| **CRM** | Customer Relationship Management | verwaltet Kundenbeziehungen: Kontakte, Angebote, Verkaufschancen, Support |

### Stamm- und Bewegungsdaten

| | **Stammdaten** | **Bewegungsdaten** |
| --- | --- | --- |
| ändern sich | selten | ständig, entstehen bei jedem Vorgang |
| Lebensdauer | lange | beziehen sich auf einen Vorgang oder Zeitpunkt |
| Beispiele | Kunde (Name, Adresse), Artikel, Lieferant, Mitarbeiter | Bestellung, Rechnung, Lagerbewegung, Ticket, Arbeitszeit |

Bewegungsdaten **verweisen** auf Stammdaten: Eine Rechnung enthält die Kundennummer, nicht die ganze
Adresse.

### Beispiel im Archiv

| Datensatz | Art | Begründung |
| --- | --- | --- |
| Kunde „Kunde Nord GmbH“, Adresse, Vertrag | Stammdaten | ändert sich selten |
| Speicherklasse „cold“ mit Preis pro TB | Stammdaten | festgelegter Tarif |
| Upload von 2.000 Dokumenten am 12.11. | Bewegungsdaten | einzelner Vorgang |
| Monatsrechnung November | Bewegungsdaten | bezieht sich auf einen Zeitraum |

> **Halten wir kurz fest:**
>
> 1. System-, Standard-, Branchen-, Individualsoftware, Entwicklungssysteme, KI-Software.
> 2. ERP = ganzes Unternehmen, SCM = Lieferkette, CRM = Kundenbeziehungen.
> 3. Stammdaten selten geändert, Bewegungsdaten bei jedem Vorgang neu.

## Warum ist es so?

Getrennte Stammdaten verhindern Redundanz: Die Adresse eines Kunden steht einmal im System, jede
Rechnung verweist nur darauf. Das ist dieselbe Idee wie bei der Normalisierung von Datenbanken.

<details>
<summary>Warum Standardsoftware, wenn Individualsoftware genau passt?</summary>

Standardsoftware ist sofort verfügbar, günstiger, erprobt und wird vom Hersteller weiterentwickelt.
Individualsoftware passt genau, kostet aber Entwicklung, Wartung und eigenes Wissen. Oft wird
Standardsoftware angepasst (Customizing) – ein Mittelweg.

</details>

## Praxisbezug im Betrieb

- **Datenqualität:** Doppelte Kunden in den Stammdaten führen zu falschen Rechnungen und Auswertungen.
- **Schnittstellen:** CRM und ERP tauschen Kunden- und Auftragsdaten aus.
- **KI-Software einführen:** Datenschutz, Lizenz und Richtlinie klären, bevor Firmendaten hineingehen.

## Typische Prüfungsfalle

- **ERP, SCM, CRM vertauscht:** Kunde = CRM, Lieferkette = SCM, alles zusammen = ERP.
- **Rechnung als Stammdatum:** Rechnungen sind Bewegungsdaten.
- **Betriebssystem als Standardsoftware:** Es ist Systemsoftware.
- **Langformen falsch:** Die Langformen gehören dazu.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Systemsoftware | betreibt Hardware (Betriebssystem, Treiber) |
| Standardsoftware | für viele Kunden gleich |
| Individualsoftware | für einen Kunden entwickelt |
| Stammdaten | langlebig, selten geändert |
| Bewegungsdaten | entstehen bei Vorgängen |

## Merksatz

**ERP steuert alles, SCM die Lieferkette, CRM die Kunden. Stammdaten bleiben, Bewegungsdaten
passieren – und verweisen auf die Stammdaten.**
