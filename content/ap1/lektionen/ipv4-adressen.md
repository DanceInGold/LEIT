---
id: ipv4-adressen
titel: "IPv4-Adressen: Netzanteil, Maske, Netz- und Broadcastadresse"
themen: [ipv4-subnetting]
reihenfolge: 1
voraussetzungen: [zahlensysteme]
dauer_min: 40
quelle: "Neu erstellt (Claude). IPv4 nach RFC 791, CIDR nach RFC 4632, private Adressen nach RFC 1918, Link-Local nach RFC 3927; Hinweis „keine Standardmaske“ wegen Befund P-16; alle Rechnungen nachgerechnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025: IPv4 und IPv6 ausdrücklich genannt (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "RFC 4632: Classless Inter-domain Routing (CIDR)", url: "https://www.rfc-editor.org/rfc/rfc4632"}
  - {titel: "RFC 1918: Address Allocation for Private Internets", url: "https://www.rfc-editor.org/rfc/rfc1918"}
  - {titel: "RFC 3927: Dynamic Configuration of IPv4 Link-Local Addresses (169.254.0.0/16)", url: "https://www.rfc-editor.org/rfc/rfc3927"}
status: ungeprüft
---

## Worum geht es?

Eine IPv4-Adresse wie `172.16.45.130` sagt zwei Dinge: **in welchem Netz** ein Rechner steht und
**welcher Rechner** es ist. Die **[Subnetzmaske](glossar:subnetzmaske)** legt fest, wo die Grenze
liegt.

- In diesem Kapitel: Aufbau, Maske, Netz- und Broadcastadresse, besondere Bereiche.
- Danach: Subnetze bilden und prüfen.
- Grundlage ist die Dualumrechnung aus „Zahlensysteme“.

## Wie funktioniert es?

### Aufbau: 32 Bit in vier Oktetten

Eine IPv4-Adresse hat **32 Bit**, geschrieben als vier Dezimalzahlen von 0 bis 255:

| | 1. Oktett | 2. Oktett | 3. Oktett | 4. Oktett |
| --- | --- | --- | --- | --- |
| dezimal | 172 | 16 | 45 | 130 |
| dual | 10101100 | 00010000 | 00101101 | 10000010 |

Analogie: Der **Netzanteil** ist die Straße, der **Hostanteil** die Hausnummer.

### Die Subnetzmaske und CIDR

Die Maske hat an jeder Stelle des **Netzanteils** eine 1 und im **Hostanteil** eine 0. Die Einsen
stehen immer links, ohne Lücke.

| Schreibweise | Wert |
| --- | --- |
| Punktschreibweise | 255.255.255.192 |
| dual | 11111111.11111111.11111111.11000000 |
| CIDR (Präfix) | **/26** – so viele Einsen |

Bei /26 sind 26 Bit Netzanteil und 32 − 26 = **6 Bit Hostanteil**.

Es gibt **keine** allgemeine Standardmaske. /24 ist in kleinen Netzen nur üblich; seit CIDR wählt man
die Maske nach Bedarf.

### Rechenbeispiel: 172.16.45.130/26

Die ersten drei Oktette gehören bei /26 ganz zum Netz. Spannend ist nur das 4. Oktett:

| | dual | dezimal |
| --- | --- | ---: |
| Adresse | 10 000010 | 130 |
| Maske | 11 000000 | 192 |
| **Netzadresse** (UND) | 10 000000 | **128** |
| **Broadcast** (Hostbits = 1) | 10 111111 | **191** |

Ergebnis:

| Kennzahl | Wert |
| --- | --- |
| Netzadresse | 172.16.45.128 |
| erster Host | 172.16.45.129 |
| letzter Host | 172.16.45.190 |
| Broadcastadresse | 172.16.45.191 |
| nutzbare Hosts | 2⁶ − 2 = **62** |

### Netzadresse per UND, Broadcast per Einsen

- **Netzadresse:** Adresse **UND** Maske – Bit für Bit, nur 1 und 1 ergibt 1. Alle Hostbits werden 0.
- **Broadcastadresse:** alle Hostbits auf **1**. Ein Paket an diese Adresse erreicht alle im Netz.
- **Nutzbare Hosts:** 2^(Hostbits) − 2, weil Netz- und Broadcastadresse keinem Rechner gehören.

| Präfix | Maske | Hostbits | nutzbare Hosts |
| ---: | --- | ---: | ---: |
| /24 | 255.255.255.0 | 8 | 254 |
| /25 | 255.255.255.128 | 7 | 126 |
| /26 | 255.255.255.192 | 6 | 62 |
| /27 | 255.255.255.224 | 5 | 30 |
| /28 | 255.255.255.240 | 4 | 14 |
| /30 | 255.255.255.252 | 2 | 2 |

### Besondere Adressbereiche

| Bereich | Zweck |
| --- | --- |
| 10.0.0.0/8 | privat (RFC 1918) |
| 172.16.0.0/12 (172.16.0.0 – 172.31.255.255) | privat |
| 192.168.0.0/16 | privat |
| 127.0.0.0/8 | Loopback, der Rechner selbst (127.0.0.1) |
| 169.254.0.0/16 | Link-Local: selbst vergeben, wenn kein DHCP antwortet |

**Private** Adressen werden im Internet nicht geroutet. Am Übergang ersetzt der Router sie per
**[NAT](glossar:nat)** durch seine öffentliche Adresse – aber nur dort, nicht zwischen internen Netzen.

> **Halten wir kurz fest:**
>
> 1. Präfix = Anzahl Einsen in der Maske, Hostbits = 32 − Präfix.
> 2. Netzadresse = Adresse UND Maske; Broadcast = alle Hostbits 1.
> 3. Nutzbare Hosts = 2^Hostbits − 2.

## Warum ist es so?

Router müssen nicht jeden Rechner der Welt kennen, nur **Netze**. Die Maske sagt ihnen, welcher Teil
der Adresse das Netz ist.

<details>
<summary>Warum gerade UND für die Netzadresse?</summary>

UND mit 1 lässt ein Bit, wie es ist; UND mit 0 macht es zu 0. Die Maske wirkt also wie eine
Schablone: Den Netzanteil lässt sie durch, den Hostanteil löscht sie. Das kann jede CPU in einem
einzigen Schritt – darum ist Routing so schnell.

</details>

<details>
<summary>Warum gibt es private Adressen?</summary>

32 Bit reichen für rund 4,3 Milliarden Adressen – zu wenig für alle Geräte der Welt. Private Bereiche
dürfen in jedem Firmennetz wiederverwendet werden. Mit NAT teilen sich viele interne Geräte eine
öffentliche Adresse. IPv6 löst das Problem grundsätzlich.

</details>

## Praxisbezug im Betrieb

- **`ip -4 addr`** auf einem RHEL-Server zeigt Adresse und Präfix, z. B. `inet 10.0.1.10/24`.
- **169.254.x.x am Client** heißt fast immer: DHCP-Server nicht erreicht – Kabel, VLAN oder DHCP prüfen.
- **Container-Netze** nutzen ebenfalls private Bereiche; Überschneidungen mit dem Firmennetz führen
  zu schwer zu findenden Routing-Fehlern.

## Typische Prüfungsfalle

- **Hosts mit 2^n statt 2^n − 2:** Netz- und Broadcastadresse abziehen.
- **Netzadresse als Host vergeben:** 172.16.45.128/26 ist das Netz, kein Rechner.
- **172.32.x.x als privat:** Der private Bereich endet bei 172.31.255.255.
- **„Standardmaske 255.255.255.0“:** Gibt es nicht; die Maske richtet sich nach dem Bedarf.
- **NAT zwischen internen Netzen:** Intern wird geroutet, NAT passiert am Übergang ins Internet.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Netzadresse | erste Adresse, alle Hostbits 0, bezeichnet das Netz |
| Broadcastadresse | letzte Adresse, alle Hostbits 1, erreicht alle im Netz |
| Gateway | Router-Adresse im eigenen Netz, oft der erste Host |
| Subnetzmaske | trennt Netz- und Hostanteil |
| Präfix /26 | Kurzform der Maske: 26 Einsen |
| private Adresse | nur intern, im Internet nicht geroutet |

## Merksatz

**Maske UND Adresse gibt das Netz, alle Hostbits auf eins gibt den Broadcast – und dazwischen passen
2 hoch Hostbits minus 2 Rechner.**
