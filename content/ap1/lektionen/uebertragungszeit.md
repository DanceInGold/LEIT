---
id: uebertragungszeit
titel: "Übertragungszeit und Datenrate berechnen"
themen: [datenmengen-uebertragung]
reihenfolge: 2
voraussetzungen: [zahlensysteme]
dauer_min: 30
quelle: "Neu erstellt (Claude). Grundformel Zeit = Datenmenge ÷ Datenrate; Nutzdatenrate mit Overhead als Annahme der Aufgabe; alle Beispiele per Skript nachgerechnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 03.03: Übertragungsraten und Übertragungszeiten berechnen, z. B. Dauer eines Downloads bei vorgegebener Datenrate (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
status: geprüft
---

## Worum geht es?

Wie lange dauert es, ein Archivpaket zu übertragen? Und welche Leitung brauche ich, damit die
nächtliche Sicherung rechtzeitig fertig wird?

Eine einzige Formel, in drei Richtungen umgestellt:

| gesucht | Formel |
| --- | --- |
| Zeit | **t = Datenmenge ÷ Datenrate** |
| Datenrate | Datenrate = Datenmenge ÷ t |
| Datenmenge | Datenmenge = Datenrate × t |

Der Trick: Datenmenge und Datenrate müssen in **derselben Einheit** stehen – am sichersten in **Bit**.

## Wie funktioniert es?

### Vorgehen in vier Schritten

1. **Datenmenge in Bit:** Byte × 8.
2. **Datenrate in bit/s:** Präfixe ausschreiben (1 Gbit/s = 1.000.000.000 bit/s).
3. **Teilen:** Ergebnis in Sekunden.
4. **Umrechnen:** in Minuten oder Stunden, wie gefragt.

### Beispiel 1: Archivpaket über 1 Gbit/s

Ein Archivpaket hat **50 GB**, die Leitung **1 Gbit/s**.

1. 50 GB = 50 × 10⁹ Byte × 8 = **400.000.000.000 Bit** (4 × 10¹¹)
2. 1 Gbit/s = **1.000.000.000 bit/s** (10⁹)
3. t = 4 × 10¹¹ ÷ 10⁹ = **400 s**
4. 400 s = **6 min 40 s**

### Mit Overhead rechnen

Nicht die ganze Datenrate steht für Nutzdaten bereit: Protokoll-Header (Ethernet, IP, TCP) und
Wartezeiten kosten Kapazität. Gibt die Aufgabe z. B. **80 % Nutzdatenrate** an:

- nutzbare Rate: 10⁹ × 0,8 = 8 × 10⁸ bit/s
- t = 4 × 10¹¹ ÷ 8 × 10⁸ = **500 s** = **8 min 20 s**

Steht keine Angabe in der Aufgabe, rechnest du mit der vollen Datenrate.

### Beispiel 2: Welche Leitung brauche ich?

Jede Nacht sollen **2 TB** ins externe Rechenzentrum, Zeitfenster **4 Stunden**.

1. 2 TB = 2 × 10¹² Byte × 8 = **1,6 × 10¹³ Bit**
2. 4 h = 4 × 3.600 = **14.400 s**
3. Datenrate = 1,6 × 10¹³ ÷ 14.400 ≈ **1,11 × 10⁹ bit/s = 1,11 Gbit/s**

Eine 1-Gbit/s-Leitung reicht also **nicht** – selbst ohne Overhead. Die nächste übliche Stufe ist
**10 Gbit/s**.

### Beispiel 3: Was schafft die Leitung?

Wie viele Fotos à **36 MB** lassen sich in **1 Minute** über **100 Mbit/s** übertragen?

1. Datenmenge = 10⁸ bit/s × 60 s = 6 × 10⁹ Bit ÷ 8 = **750.000.000 Byte**
2. 750.000.000 ÷ 36.000.000 = 20,8 → **20 vollständige Fotos**

> **Halten wir kurz fest:**
>
> 1. t = Datenmenge ÷ Datenrate – beides in Bit.
> 2. Byte × 8 = Bit; Präfixe ausschreiben, dann teilen.
> 3. Overhead nur einrechnen, wenn die Aufgabe ihn vorgibt.

## Warum ist es so?

Netzwerktechnik misst seit jeher in **Bit pro Sekunde**, weil Leitungen Bits einzeln übertragen.
Dateien bestehen aus Bytes. Wer die Formel anwendet, muss deshalb zuerst übersetzen.

<details>
<summary>Warum ist der echte Download oft langsamer als die Rechnung?</summary>

Die Rechnung nimmt eine ideale Leitung an. Real kommen Protokoll-Header, Bestätigungen (TCP),
Latenz, andere Nutzer auf derselben Leitung und die Geschwindigkeit des Servers oder der Festplatte
dazu. Das schwächste Glied bestimmt das Tempo.

</details>

<details>
<summary>Warum nicht einfach einen Datenträger verschicken?</summary>

Bei sehr großen Mengen ist das manchmal wirklich schneller. 500 TB brauchen über 1 Gbit/s rund
46 Tage. Große Cloud-Anbieter bieten deshalb Transfer-Geräte an, die per Spedition reisen.

</details>

## Praxisbezug im Betrieb

- **Sicherungsfenster planen:** Datenmenge der Nacht ÷ verfügbare Rate muss kleiner sein als das
  Zeitfenster – mit Reserve.
- **Erwartung klären:** Bei 1 Gbit/s sind höchstens 125 MB/s drin; meldet ein Kollege 300 MB/s,
  stimmt etwas mit der Messung nicht.
- **Artefakt-Downloads im CI:** Große Images bremsen jede Pipeline; die Rechnung zeigt, ob ein Cache
  in der Nähe lohnt.

## Typische Prüfungsfalle

- **Byte nicht in Bit umgerechnet:** Das Ergebnis ist dann achtmal zu klein.
- **Präfixe gemischt:** GB durch Mbit/s, ohne vorher auszuschreiben.
- **Stunden falsch:** 1 h = 3.600 s, nicht 600.
- **Rundung bei Anzahlen:** 20,8 Fotos heißt 20 **vollständige** Fotos.
- **Binär gemeint, dezimal gerechnet:** Steht in der Aufgabe GiB, rechne mit 1.024³.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Datenrate (Bandbreite) | Bit pro Sekunde, z. B. 1 Gbit/s |
| Datenmenge | Größe der Daten in Byte, z. B. 50 GB |
| Übertragungszeit | Datenmenge ÷ Datenrate |
| Nutzdatenrate | Anteil der Datenrate, der für Nutzdaten übrig bleibt |
| Latenz | Verzögerung bis zum ersten Bit, nicht die Rate |

## Merksatz

**Zeit ist Menge durch Rate – aber erst, wenn beides Bit ist. Bytes mal acht, Präfixe ausschreiben,
dann teilen.**
