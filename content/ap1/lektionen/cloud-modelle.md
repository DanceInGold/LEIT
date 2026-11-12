---
id: cloud-modelle
titel: "Cloud: IaaS, PaaS, SaaS, DaaS und virtuelle Desktops"
themen: [cloud-modelle]
reihenfolge: 1
voraussetzungen: []
dauer_min: 25
quelle: "Neu erstellt (Claude). Service- und Bereitstellungsmodelle nach NIST SP 800-145; DaaS und virtuelle Desktops nach gängiger Herstellerliteratur; Beispiele fiktiv."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 03.01: Cloudlösungen, z. B. Software as a Service, Desktop as a Service; virtuelle Desktops (Cloud oder lokal) (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "NIST SP 800-145: The NIST Definition of Cloud Computing", url: "https://csrc.nist.gov/pubs/sp/800/145/final"}
status: ungeprüft
---

## Worum geht es?

**[Cloud Computing](glossar:cloud-computing)** heißt: IT-Leistungen über das Netz beziehen, nach
Bedarf und nach Verbrauch bezahlt. Entscheidend ist, **wie viel** der Anbieter übernimmt.

Analogie **Pizza**:

| Modell | Pizza-Vergleich |
| --- | --- |
| eigener Betrieb (On-Premises) | alles selbst: Teig, Belag, Ofen, Tisch |
| IaaS | Ofen und Küche gemietet, Pizza selbst gemacht |
| PaaS | fertiger Teig und Ofen, du belegst nur |
| SaaS | Pizza wird fertig geliefert |

## Wie funktioniert es?

### Wer verwaltet was?

| Ebene | On-Premises | IaaS | PaaS | SaaS |
| --- | :---: | :---: | :---: | :---: |
| Anwendung und Daten | Kunde | Kunde | Kunde | **Anbieter** (Daten: Kunde) |
| Laufzeitumgebung, Middleware | Kunde | Kunde | **Anbieter** | **Anbieter** |
| Betriebssystem | Kunde | Kunde | **Anbieter** | **Anbieter** |
| Virtualisierung, Server, Speicher, Netz | Kunde | **Anbieter** | **Anbieter** | **Anbieter** |

### Die Modelle mit Beispiel

| Modell | Bedeutung | Beispiel |
| --- | --- | --- |
| **IaaS** – Infrastructure as a Service | virtuelle Server, Speicher, Netze | VM für einen Testserver mieten |
| **PaaS** – Platform as a Service | Plattform zum Betreiben eigener Software | Container-Plattform, verwaltete Datenbank |
| **SaaS** – Software as a Service | fertige Anwendung im Browser | Online-Office, Ticketsystem, E-Mail |
| **DaaS** – Desktop as a Service | kompletter Arbeitsplatz-Desktop aus der Cloud | Windows-Desktop im Browser für Aushilfen |

### Bereitstellungsmodelle

| Modell | Wer nutzt die Infrastruktur? |
| --- | --- |
| Public Cloud | viele Kunden beim selben Anbieter |
| Private Cloud | nur eine Organisation, im eigenen oder fremden Rechenzentrum |
| Hybrid Cloud | Kombination aus beiden |
| Community Cloud | mehrere Organisationen mit gleichen Anforderungen (z. B. Behörden) |

### Virtuelle Desktops: lokal oder aus der Cloud

| | VDI im eigenen Rechenzentrum | DaaS aus der Cloud |
| --- | --- | --- |
| Hardware | eigene Server | beim Anbieter |
| Kosten | hohe Anschaffung | monatlich pro Benutzer |
| Kontrolle | vollständig | beim Anbieter, Vertrag regelt |
| Endgerät | beides: Thin Client, Notebook, Tablet | |

> **Halten wir kurz fest:**
>
> 1. IaaS = Infrastruktur, PaaS = Plattform, SaaS = fertige Software, DaaS = Desktop.
> 2. Je weiter rechts, desto mehr übernimmt der Anbieter.
> 3. Public, Private, Hybrid, Community = wer die Infrastruktur teilt.

## Warum ist es so?

Unternehmen wollen sich auf ihr Geschäft konzentrieren. Was nicht zum Kern gehört – Hardware tauschen,
Betriebssysteme patchen – kann ein Anbieter oft günstiger und schneller.

<details>
<summary>Warum bleibt der Kunde trotzdem für die Daten verantwortlich?</summary>

Auch bei SaaS entscheidet der Kunde, **welche** Daten er hochlädt und wer Zugriff bekommt. Nach DSGVO
bleibt er Verantwortlicher, der Anbieter ist Auftragsverarbeiter. Deshalb braucht es einen
AV-Vertrag, eine Prüfung des Speicherorts und ein eigenes Konzept für Backup und Zugriffe.

</details>

## Praxisbezug im Betrieb

- **Testsystem für ein paar Wochen:** IaaS statt eigene Hardware kaufen.
- **OpenShift im eigenen Rechenzentrum** ist eine private PaaS: Entwickler liefern Container, die
  Plattform kümmert sich um den Rest.
- **Kostenfalle:** Verbrauchsabrechnung im Blick behalten – vergessene VMs kosten weiter.

## Typische Prüfungsfalle

- **IaaS und PaaS vertauscht:** Bei PaaS verwaltet der Kunde **kein** Betriebssystem.
- **SaaS = keine Verantwortung:** Die Daten bleiben in der Verantwortung des Kunden.
- **DaaS vergessen:** Der Katalog nennt Desktop as a Service ausdrücklich.
- **Nur Vorteile:** Abhängigkeit vom Anbieter, Datenschutz und Internetverbindung nennen.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| IaaS | virtuelle Hardware mieten |
| PaaS | Plattform für eigene Anwendungen |
| SaaS | fertige Anwendung nutzen |
| DaaS | Desktop aus der Cloud |
| VDI | virtuelle Desktops im eigenen Rechenzentrum |
| On-Premises | alles im eigenen Haus betrieben |

## Merksatz

**Infrastruktur, Plattform, Software, Desktop – je weiter oben im Stapel der Anbieter übernimmt, desto
weniger musst du selbst betreiben. Die Daten bleiben aber deine.**
