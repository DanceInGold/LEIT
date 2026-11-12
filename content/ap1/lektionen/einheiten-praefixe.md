---
id: einheiten-praefixe
titel: "Bit, Byte und Präfixe: warum die 2-TB-Platte nur 1,82 TiB hat"
themen: [zahlensysteme]
reihenfolge: 2
voraussetzungen: []
dauer_min: 25
quelle: "Neu erstellt (Claude). Dezimale SI-Präfixe nach SI-Broschüre (BIPM), binäre Präfixe nach IEC 80000-13; alle Umrechnungen nachgerechnet."
belege:
  - {titel: "IEC 80000-13:2008 Quantities and units – Part 13: Information science and technology (Präfixe Ki, Mi, Gi, Ti)"}
  - {titel: "BIPM: The International System of Units (SI), 9. Auflage 2019 – SI-Präfixe k = 10³, M = 10⁶, G = 10⁹, T = 10¹²", url: "https://www.bipm.org/en/publications/si-brochure"}
status: ungeprüft
---

## Worum geht es?

Du kaufst eine Festplatte mit **2 TB**. Das Betriebssystem zeigt aber nur **1,82 TB** an. Betrug?
Nein – zwei verschiedene Präfix-Systeme.

- **Bit und Byte:** die Grundeinheiten.
- **Dezimale Präfixe** (k, M, G, T) und **binäre Präfixe** (Ki, Mi, Gi, Ti).
- Diese Einheiten brauchst du für jede Aufgabe zu Datenmengen und Übertragungszeiten.

## Wie funktioniert es?

### Bit und Byte

| Einheit | Zeichen | Größe |
| --- | --- | --- |
| Bit | bit | eine Stelle, 0 oder 1 |
| Byte | B | 8 Bit |

Faustregel: **kleines b = Bit, großes B = Byte.** Datenraten stehen meist in **Bit** pro Sekunde
(Mbit/s), Dateigrößen in **Byte** (MB).

### Zwei Präfix-Systeme

| dezimal (SI) | Faktor | binär (IEC) | Faktor |
| --- | --- | --- | --- |
| k (Kilo) | 10³ = 1.000 | Ki (Kibi) | 2¹⁰ = 1.024 |
| M (Mega) | 10⁶ = 1.000.000 | Mi (Mebi) | 2²⁰ = 1.048.576 |
| G (Giga) | 10⁹ | Gi (Gibi) | 2³⁰ = 1.073.741.824 |
| T (Tera) | 10¹² | Ti (Tebi) | 2⁴⁰ ≈ 1,0995 × 10¹² |

- **Hersteller** von Festplatten und Netzwerktechnik rechnen **dezimal**.
- **Betriebssysteme** rechnen oft **binär**, schreiben aber manchmal trotzdem „GB“ oder „TB“.

### Rechenbeispiel: die 2-TB-Platte

1. Hersteller: 2 TB = 2 × 10¹² Byte = 2.000.000.000.000 Byte
2. Betriebssystem teilt durch 2⁴⁰ = 1.099.511.627.776
3. 2.000.000.000.000 ÷ 1.099.511.627.776 = **1,819 TiB**

Es fehlt kein einziges Byte – nur die Einheit ist eine andere. Der Unterschied wächst mit jeder
Stufe: bei Kilo 2,4 %, bei Tera schon rund 10 %.

### Bit pro Sekunde in Byte pro Sekunde

Eine Leitung mit **100 Mbit/s** überträgt höchstens:

100.000.000 bit/s ÷ 8 = 12.500.000 B/s = **12,5 MB/s**

Teile Bit durch 8, um Byte zu erhalten. Multipliziere Byte mal 8, um Bit zu erhalten.

> **Halten wir kurz fest:**
>
> 1. b = Bit, B = Byte, 1 B = 8 bit.
> 2. k, M, G, T = Tausenderschritte; Ki, Mi, Gi, Ti = 1.024er-Schritte.
> 3. Datenraten in bit/s, Dateigrößen in Byte – also durch 8 teilen.

## Warum ist es so?

Speicher ist in Zweierpotenzen aufgebaut, darum lag „1 Kilobyte = 1.024 Byte“ für Programmierer
nahe. Das kollidiert mit dem SI-System, in dem Kilo immer 1.000 heißt.

<details>
<summary>Warum gibt es die Präfixe Ki, Mi, Gi überhaupt?</summary>

Weil „GB“ zwei Bedeutungen hatte, gab es Streit und sogar Klagen wegen „fehlender“ Kapazität.
Deshalb wurden 1998 eigene binäre Präfixe eingeführt, heute in IEC 80000-13 genormt. Seitdem ist
klar: GB = 10⁹, GiB = 2³⁰.

</details>

## Praxisbezug im Betrieb

- **Linux:** `df -h` zeigt binäre Werte (G meint GiB), `df -H` dezimale. Beim Vergleich mit dem
  Datenblatt immer prüfen, welches gemeint ist.
- **Archivkapazität planen:** Bei 500 TB Rohdaten ist der Unterschied zwischen TB und TiB rund
  45 TiB – das ist mehr als eine ganze Festplatte.
- **Download-Anzeige:** Browser zeigen MB/s, der Provider verkauft Mbit/s.

## Typische Prüfungsfalle

- **b und B verwechselt:** 100 Mbit/s sind 12,5 MB/s, nicht 100 MB/s.
- **Falsche Basis:** Gibt die Aufgabe „1 KiB = 1.024 Byte“ vor, rechne binär. Steht nur „kB“, meist
  dezimal. Lies die Vorgabe.
- **Präfixe gemischt:** Erst alles in dieselbe Einheit bringen (z. B. Bit), dann rechnen.

## Nicht verwechseln

| Angabe | Bedeutung |
| --- | --- |
| 1 kB | 1.000 Byte |
| 1 KiB | 1.024 Byte |
| 1 MB | 1.000.000 Byte |
| 1 MiB | 1.048.576 Byte |
| 1 Mbit | 1.000.000 Bit = 125.000 Byte |
| 1 MB/s | 8 Mbit/s |

## Merksatz

**Klein b ist Bit, groß B ist Byte, und dazwischen liegt der Faktor 8. Ohne i rechnet man in
Tausendern, mit i in 1.024ern.**
