---
id: ipv6-adressen
titel: "IPv6-Adressen: Aufbau, Kürzen und Adressarten"
themen: [ipv6]
reihenfolge: 1
voraussetzungen: [zahlensysteme]
dauer_min: 35
quelle: "Neu erstellt (Claude). Adressarchitektur nach RFC 4291, Textdarstellung nach RFC 5952, Dokumentationspräfix nach RFC 3849, ULA nach RFC 4193; Kürzungen mit Pythons ipaddress gegengeprüft."
belege:
  - {titel: "Prüfungskatalog AP1 2025: IPv4 und IPv6 ausdrücklich genannt; IPv6 wurde bereits früher abgefragt (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "RFC 4291: IP Version 6 Addressing Architecture", url: "https://www.rfc-editor.org/rfc/rfc4291"}
  - {titel: "RFC 5952: A Recommendation for IPv6 Address Text Representation", url: "https://www.rfc-editor.org/rfc/rfc5952"}
  - {titel: "RFC 3849: IPv6 Address Prefix Reserved for Documentation (2001:db8::/32)", url: "https://www.rfc-editor.org/rfc/rfc3849"}
  - {titel: "RFC 4193: Unique Local IPv6 Unicast Addresses (fc00::/7)", url: "https://www.rfc-editor.org/rfc/rfc4193"}
status: ungeprüft
---

## Worum geht es?

IPv4 hat rund 4,3 Milliarden Adressen – längst zu wenig. **[IPv6](glossar:ipv6)** hat 128 Bit: etwa
3,4 × 10³⁸ Adressen. In den bisherigen Prüfungen brachte IPv6 rund **28 Punkte**.

- Aufbau und Schreibweise
- **Kürzungsregeln** – Prüfungsklassiker
- Adressarten und was es nicht mehr gibt

Beispieladressen stammen aus **2001:db8::/32**, dem Bereich, der für Dokumentation reserviert ist.

## Wie funktioniert es?

### Aufbau: acht Blöcke à 16 Bit

Eine IPv6-Adresse besteht aus **8 Blöcken** zu je **16 Bit**, jeder als **4 Hex-Ziffern**, getrennt
durch Doppelpunkte:

`2001:0db8:0000:0000:0008:0800:200c:417a`

| Teil | Blöcke | Bit | Bedeutung |
| --- | --- | ---: | --- |
| Präfix (Netz) | `2001:0db8:0000:0000` | 64 | Netz und Subnetz |
| Interface-ID | `0008:0800:200c:417a` | 64 | Schnittstelle im Subnetz |

Ein Subnetz hat in der Regel genau **/64** – also 2⁶⁴ Adressen für Geräte.

### Kürzen: zwei Regeln

**Regel 1:** Führende Nullen in jedem Block dürfen weg.
`0db8` → `db8`, `0008` → `8`, `0000` → `0`

**Regel 2:** **Eine** zusammenhängende Folge von Null-Blöcken darf durch `::` ersetzt werden –
**nur einmal** pro Adresse.

| Schritt | Adresse |
| --- | --- |
| voll | `2001:0db8:0000:0000:0008:0800:200c:417a` |
| Regel 1 | `2001:db8:0:0:8:800:200c:417a` |
| Regel 2 | **`2001:db8::8:800:200c:417a`** |

### Kürzen: die Feinheiten

Gibt es **zwei** Null-Folgen, kürzt du die **längere**. Sind beide gleich lang, die **erste**:

`2001:db8:0:0:1:0:0:1` → **`2001:db8::1:0:0:1`**

Weitere Regeln für die einheitliche Schreibweise (RFC 5952):

- Hex-Buchstaben **klein** schreiben.
- Einen **einzelnen** Null-Block nicht mit `::` kürzen, sondern als `0` stehen lassen.
- Nullen **am Ende** eines Blocks bleiben: `0800` → `800`, nicht `08`.

### Zurück zur vollen Form

Fehlende Blöcke ergeben sich aus der Zahl der vorhandenen: `2001:db8::8:800:200c:417a` hat 6 Blöcke,
also stehen für `::` genau **8 − 6 = 2** Null-Blöcke.

### Adressarten

| Präfix | Art | Zweck |
| --- | --- | --- |
| `2000::/3` | Global Unicast | weltweit routbar, wie öffentliche IPv4 |
| `fe80::/10` | Link-Local | nur im lokalen Segment, jede Schnittstelle hat eine |
| `fc00::/7` (praktisch `fd00::/8`) | Unique Local (ULA) | intern, ähnlich privaten IPv4-Bereichen |
| `::1` | Loopback | der Rechner selbst (wie 127.0.0.1) |
| `ff00::/8` | Multicast | an eine Gruppe von Empfängern |

**Broadcast gibt es in IPv6 nicht mehr.** Aufgaben, die IPv4 per Broadcast löst (z. B. ARP), erledigt
IPv6 mit **Multicast**.

> **Halten wir kurz fest:**
>
> 1. 128 Bit, 8 Blöcke à 16 Bit, Hex. Präfix meist /64, Rest Interface-ID.
> 2. Führende Nullen weg; `::` nur einmal, für die längste Null-Folge.
> 3. Link-Local `fe80::/10`, Global `2000::/3`, ULA `fd00::/8`, kein Broadcast.

## Warum ist es so?

128 Bit dezimal geschrieben wären unlesbar lang. Hex fasst 4 Bit in eine Ziffer, Kürzungen sparen die
vielen Nullen, die in echten Adressen häufig vorkommen.

<details>
<summary>Warum darf :: nur einmal vorkommen?</summary>

Bei `2001::1::1` wäre unklar, wie viele Null-Blöcke an welcher Stelle fehlen: 1 + 4, 2 + 3, 3 + 2
oder 4 + 1? Mit nur einem `::` lässt sich die fehlende Anzahl eindeutig aus 8 minus vorhandene
Blöcke berechnen.

</details>

<details>
<summary>Warum braucht IPv6 keine NAT mehr?</summary>

Es gibt genug Adressen, damit jedes Gerät eine eigene, weltweit eindeutige bekommt. NAT war bei IPv4
eine Notlösung gegen Adressmangel. Schutz bietet bei IPv6 die **Firewall**, nicht das Verstecken
hinter einer Adresse.

</details>

## Praxisbezug im Betrieb

- **`ip -6 addr`** zeigt auf einem RHEL-Server mindestens eine `fe80::`-Adresse, auch ohne
  IPv6-Konfiguration.
- **In URLs** steht eine IPv6-Adresse in eckigen Klammern: `https://[2001:db8::10]:8443/`.
- **Firewall-Regeln für beide Protokolle pflegen:** Eine Regel nur für IPv4 lässt IPv6 offen.

## Typische Prüfungsfalle

- **`::` zweimal:** Ungültig.
- **Nullen am Blockende gestrichen:** `0800` wird zu `800`, nicht zu `8`.
- **Kürzere Null-Folge gekürzt:** Immer die längste, bei Gleichstand die erste.
- **Broadcast-Adresse gesucht:** Gibt es in IPv6 nicht.
- **Blöcke mit 8 Bit:** Ein Block hat 16 Bit (4 Hex-Ziffern).

## Nicht verwechseln

| Begriff | IPv4 | IPv6 |
| --- | --- | --- |
| Länge | 32 Bit | 128 Bit |
| Schreibweise | 4 × dezimal, Punkte | 8 × hex, Doppelpunkte |
| Loopback | 127.0.0.1 | ::1 |
| intern | 10/8, 172.16/12, 192.168/16 | fd00::/8 (ULA) |
| automatisch lokal | 169.254.0.0/16 | fe80::/10 |
| Broadcast | ja | nein, Multicast |

## Merksatz

**Acht Blöcke, je vier Hex-Ziffern. Vorne Nullen weg, :: nur einmal für die längste Null-Folge – und
Broadcast gibt es nicht mehr.**
