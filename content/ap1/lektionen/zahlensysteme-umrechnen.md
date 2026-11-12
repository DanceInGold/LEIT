---
id: zahlensysteme-umrechnen
titel: "Zahlensysteme: dual, dezimal und hexadezimal umrechnen"
themen: [zahlensysteme]
reihenfolge: 1
voraussetzungen: []
dauer_min: 35
quelle: "Neu erstellt (Claude). Stellenwertsysteme nach mathematischer Standardliteratur; alle Umrechnungen nachgerechnet."
belege:
  - {titel: "Prüfungskatalog AP1: Zahlensysteme (dual, hexadezimal), Einheiten und Präfixe – Themenzuordnung siehe content/ap1/katalog.yaml (zahlensysteme)"}
  - {titel: "Python-Dokumentation: Built-in Functions bin(), hex(), int(x, base)", url: "https://docs.python.org/3/library/functions.html#bin"}
status: ungeprüft
---

## Worum geht es?

Computer speichern alles als 0 und 1. Für Menschen ist das unlesbar, deshalb gibt es Kurzschriften:

| System | Basis | Ziffern | wo du es siehst |
| --- | ---: | --- | --- |
| Dualsystem (binär) | 2 | 0, 1 | Subnetzmasken, Bits |
| Dezimalsystem | 10 | 0–9 | Alltag, IPv4-Adressen |
| Hexadezimalsystem | 16 | 0–9, A–F | MAC-Adressen, IPv6, Farben, Hashwerte |

Ohne sichere Umrechnung klappt kein Subnetting und keine IPv6-Aufgabe. Darum üben wir hier jedes
Verfahren mit echten Zahlen.

## Wie funktioniert es?

### Das Prinzip: Stellenwerte

Jede Stelle ist eine **Potenz der Basis**. Dezimal: 172 = 1 × 100 + 7 × 10 + 2 × 1.

Im Dualsystem sind die Stellenwerte Zweierpotenzen. Für ein Byte (8 Bit) solltest du sie auswendig
können:

| 2⁷ | 2⁶ | 2⁵ | 2⁴ | 2³ | 2² | 2¹ | 2⁰ |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |

### Dual → dezimal

Addiere die Stellenwerte, unter denen eine **1** steht.

`10101100`:

| 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 |

128 + 32 + 8 + 4 = **172**

### Dezimal → dual: zwei Wege

**Weg 1 – abziehen** (schnell für ein Byte): Nimm von links jeden Stellenwert, der noch hineinpasst.

| Rest | passt 128? | 64? | 32? | 16? | 8? | 4? | 2? | 1? |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 172 | ja → 44 | nein | ja → 12 | nein | ja → 4 | ja → 0 | nein | nein |

Ergebnis: `1 0 1 0 1 1 0 0`

**Weg 2 – durch 2 teilen** (für jede Größe): Teile immer wieder durch 2 und notiere den Rest.
Die Reste **von unten nach oben** gelesen sind die Dualzahl.

| Rechnung | Ergebnis | Rest |
| --- | ---: | ---: |
| 172 ÷ 2 | 86 | 0 |
| 86 ÷ 2 | 43 | 0 |
| 43 ÷ 2 | 21 | 1 |
| 21 ÷ 2 | 10 | 1 |
| 10 ÷ 2 | 5 | 0 |
| 5 ÷ 2 | 2 | 1 |
| 2 ÷ 2 | 1 | 0 |
| 1 ÷ 2 | 0 | 1 |

Von unten gelesen: `10101100` ✔

### Dual ↔ hexadezimal

Eine Hex-Ziffer steht für genau **4 Bit** (ein Nibble). Teile die Dualzahl von rechts in Viererblöcke:

| Dual | 1010 | 1100 |
| --- | --- | --- |
| Wert | 8 + 2 = 10 | 8 + 4 = 12 |
| Hex | **A** | **C** |

172 = `10101100` = **0xAC**. Rückwärts genauso: jede Hex-Ziffer in 4 Bit aufschreiben.

| Hex | 0–9 | A | B | C | D | E | F |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dezimal | 0–9 | 10 | 11 | 12 | 13 | 14 | 15 |

### Hexadezimal → dezimal

Stellenwerte sind Potenzen von 16: 1, 16, 256, 4096 …

`0x1F4` = 1 × 256 + 15 × 16 + 4 × 1 = 256 + 240 + 4 = **500**

Einfacher bei kleinen Werten: erst nach dual, dann addieren. `0x3F` = `0011 1111` = 32 + 16 + 8 + 4 + 2 + 1 = **63**.

> **Halten wir kurz fest:**
>
> 1. Stellenwerte eines Bytes: 128, 64, 32, 16, 8, 4, 2, 1.
> 2. Eine Hex-Ziffer = 4 Bit, zwei Hex-Ziffern = 1 Byte.
> 3. Beim Teilen durch 2 die Reste von unten nach oben lesen.

## Warum ist es so?

Ein Bit kennt nur zwei Zustände – Strom an oder aus. Darum rechnen Computer zur Basis 2.

<details>
<summary>Warum gerade 16 als Kurzschrift und nicht 10?</summary>

16 ist 2⁴. Deshalb passt jede Hex-Ziffer **exakt** auf 4 Bit, und die Umrechnung geht ohne Rechnen,
nur durch Gruppieren. Bei Basis 10 gibt es diese saubere Zuordnung nicht. Eine MAC-Adresse mit
48 Bit wird so zu 12 lesbaren Zeichen.

</details>

<details>
<summary>Und was ist mit dem Oktalsystem?</summary>

Basis 8, eine Ziffer = 3 Bit. Du kennst es von Linux-Rechten: `chmod 750` heißt `111 101 000` –
Besitzer lesen/schreiben/ausführen, Gruppe lesen/ausführen, andere nichts. Für die AP1 reichen dual,
dezimal und hexadezimal.

</details>

## Praxisbezug im Betrieb

- **Subnetzmasken:** 255.255.255.192 ist `11111111.11111111.11111111.11000000` – das nächste Thema
  baut genau darauf auf.
- **Hashwerte und Container-IDs** sind Hex-Zeichenketten, etwa `sha256:9f86d081…`.
- **Python:** `bin(172)` → `'0b10101100'`, `hex(172)` → `'0xac'`, `int('AC', 16)` → `172`. Gut zum
  Prüfen beim Üben.

## Typische Prüfungsfalle

- **Reste falsch herum gelesen:** von **unten nach oben**.
- **Führende Nullen weggelassen:** Ein Oktett hat immer 8 Stellen: 5 = `00000101`.
- **Viererblöcke von links gebildet:** Immer von **rechts** gruppieren, links mit Nullen auffüllen.
- **Hex-Buchstaben verrechnet:** B = 11, D = 13 – die Tabelle A–F auswendig lernen.

## Nicht verwechseln

| Schreibweise | Bedeutung |
| --- | --- |
| `0b1010` oder 1010₂ | Dualzahl, Wert 10 |
| `0x1010` oder 1010₁₆ | Hexzahl, Wert 4112 |
| 1010₁₀ | Dezimalzahl tausendzehn |
| Bit | eine Stelle, 0 oder 1 |
| Nibble | 4 Bit = eine Hex-Ziffer |
| Byte | 8 Bit = zwei Hex-Ziffern |

## Merksatz

**128-64-32-16-8-4-2-1 sitzt im Schlaf. Vier Bit sind eine Hex-Ziffer, und beim Teilen durch zwei
liest man die Reste von unten.**
