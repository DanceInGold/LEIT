---
id: fehler-im-code-finden
titel: "Fehler in gegebenem Code finden"
themen: [schreibtischtest]
reihenfolge: 2
voraussetzungen: [pseudocode]
dauer_min: 30
quelle: "Neu erstellt (Claude). Fehlerarten (Syntax-, Laufzeit-, Logikfehler) nach gängiger Lehrbuchgliederung; Beispielcode eigens mit eingebauten Fehlern geschrieben, korrigierte Fassung nachgerechnet."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 04.07: Fehler in einem gegebenen Quellcode finden (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "Python-Dokumentation: Errors and Exceptions (Syntax Errors, Exceptions)", url: "https://docs.python.org/3/tutorial/errors.html"}
status: ungeprüft
---

## Worum geht es?

In der Prüfung bekommst du Code, der **fast** stimmt. Du sollst die Fehler finden, die Zeile nennen
und eine Korrektur angeben.

- Der Katalog 2025 nennt das ausdrücklich: „Fehler in einem gegebenen Quellcode finden“.
- Das Werkzeug dafür kennst du schon: den Schreibtischtest.
- Dieses Kapitel zeigt die **drei Fehlerarten** und eine Checkliste, mit der du sie systematisch findest.

## Wie funktioniert es?

### Die drei Fehlerarten

| Fehlerart | Wann fällt er auf? | Beispiel |
| --- | --- | --- |
| [Syntaxfehler](glossar:syntaxfehler) | vor dem Start, Interpreter meldet ihn | `if x = 5` statt `if x == 5` in Python |
| Laufzeitfehler | während des Laufs, Programm bricht ab | Division durch 0, Index gibt es nicht |
| [Logischer Fehler](glossar:logischer-fehler) | gar nicht von selbst, Ergebnis ist falsch | `<` statt `>`, Grenze um eins daneben |

In der Prüfung geht es meist um **logische Fehler** – die meldet kein Werkzeug.

### Die Checkliste

Geh den Code mit diesen Fragen durch:

1. **Startwerte:** Ist jede Variable vor der ersten Nutzung belegt? Steht sie **vor** der Schleife?
2. **Schleifengrenzen:** Beginnt der Index richtig (0 oder 1)? Endet er bei `laenge - 1`?
3. **Vergleiche:** `<` oder `≤`? `>` oder `<`? Passt das zur Aufgabe?
4. **Fortschritt:** Ändert sich die Schleifenbedingung im Rumpf, damit die Schleife endet?
5. **Reihenfolge:** Wird ein Wert benutzt, bevor er berechnet ist?
6. **Sonderfälle:** Was passiert bei einem leeren Feld oder bei 0?
7. **Rückgabe:** Wird das Richtige zurückgegeben, an der richtigen Stelle?

### Rechenbeispiel: Durchschnitt mit drei Fehlern

Die Funktion soll die durchschnittliche Größe der Verzeichnisse liefern:

```text
1  function durchschnitt(groessen)
2      for i ← 1 to laenge(groessen) do
3          summe ← 0
4          summe ← summe + groessen[i]
5      end for
6      return summe / laenge(groessen)
7  end function
```

Test mit `[120, 450, 80, 300]` (Index ab 0). Erwartet: 950 ÷ 4 = **237,5**.

| i | groessen[i] | summe |
| ---: | ---: | ---: |
| 1 | 450 | 0 + 450 = 450 |
| 2 | 80 | 0 + 80 = 80 |
| 3 | 300 | 0 + 300 = 300 |
| 4 | gibt es nicht | Abbruch |

Die Tabelle zeigt sofort: `summe` beginnt jedes Mal bei 0, der erste Wert fehlt, und Index 4
gibt es nicht.

### Fehler benennen und korrigieren

So schreibst du die Antwort in der Prüfung:

| Zeile | Fehler | Korrektur |
| --- | --- | --- |
| 2 | Index startet bei 1 und endet bei 4 – erster Wert fehlt, Index 4 gibt es nicht | `for i ← 0 to laenge(groessen) - 1 do` |
| 3 | `summe` wird in jedem Durchlauf auf 0 gesetzt | `summe ← 0` vor die Schleife (vor Zeile 2) |
| 6 | Leeres Feld führt zur Division durch 0 | vorher `if laenge(groessen) = 0 then return 0` |

Die korrigierte Fassung:

```text
1  function durchschnitt(groessen)
2      if laenge(groessen) = 0 then
3          return 0
4      end if
5      summe ← 0
6      for i ← 0 to laenge(groessen) - 1 do
7          summe ← summe + groessen[i]
8      end for
9      return summe / laenge(groessen)
10 end function
```

Gegenprobe: 120 + 450 + 80 + 300 = 950, 950 ÷ 4 = **237,5** ✔

### Testwerte geschickt wählen

Ein einziger Testwert findet selten alle Fehler. Nimm drei Sorten:

| Testfall | Beispiel | findet z. B. |
| --- | --- | --- |
| Normalfall | `[120, 450, 80, 300]` | falsche Startwerte, falsche Rechnung |
| Grenzfall | `[500]` (ein Element) | Fehler am Anfang oder Ende der Schleife |
| Sonderfall | `[]` (leer) | Division durch 0, fehlende Prüfung |

> **Halten wir kurz fest:**
>
> 1. Syntaxfehler meldet der Interpreter, logische Fehler niemand.
> 2. Checkliste: Startwerte, Grenzen, Vergleiche, Fortschritt, Reihenfolge, Sonderfälle, Rückgabe.
> 3. Antwort immer mit Zeile, Fehler und Korrektur.

## Warum ist es so?

Logische Fehler sind gefährlich, **weil** das Programm normal läuft. Ein falscher Durchschnitt
landet unbemerkt in einem Bericht.

<details>
<summary>Warum sind Fehler an den Grenzen so häufig?</summary>

Menschen denken in „von 1 bis 4“, Computer zählen meist „von 0 bis 3“. Dazu kommt die Frage, ob
eine Grenze eingeschlossen ist (`≤`) oder nicht (`<`). An dieser Stelle passiert der bekannte
[Off-by-one-Fehler](glossar:off-by-one). Deshalb testet man gezielt das erste und letzte Element.

</details>

<details>
<summary>Warum ein falsches Vorzeichen richtig teuer werden kann</summary>

Ein Aufräumskript soll Dateien löschen, die **älter** als 365 Tage sind. Steht dort
`if alterTage < 365` statt `> 365`, löscht es genau die **neuen** Dateien. Syntaktisch ist alles in
Ordnung – nur ein Schreibtischtest oder ein Test mit Beispieldaten deckt das vor dem Einsatz auf.

</details>

## Praxisbezug im Betrieb

- **Code-Review im Pull Request:** Genau diese Checkliste hilft auch beim Review von Kollegen.
- **Linter und Typprüfung** (z. B. ruff, mypy) finden Syntax- und viele Tippfehler automatisch.
  Logische Fehler finden nur Tests.
- **Erst im Testsystem:** Skripte, die löschen oder verschieben, laufen zuerst mit einer
  Probelauf-Option (`--dry-run`) oder auf Testdaten.

## Typische Prüfungsfalle

- **Nur „Fehler in Zeile 3“ schreiben:** Es gibt Punkte für die Begründung **und** die Korrektur.
- **Richtigen Code „verbessern“:** Ändere nur, was wirklich falsch ist. Stil ist kein Fehler.
- **Folgefehler doppelt zählen:** Ein falscher Startwert macht viele Zeilen falsch. Gefragt ist die
  Ursache.
- **Index-Zählung übersehen:** Steht in der Aufgabe, dass Felder bei 1 beginnen, ist
  `for i ← 1 to laenge` richtig.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Syntaxfehler | Regel der Sprache verletzt, Programm startet nicht |
| Laufzeitfehler | Programm startet, bricht dann ab (Exception) |
| Logischer Fehler | Programm läuft durch, liefert aber ein falsches Ergebnis |
| Off-by-one | Schleife läuft einmal zu oft oder zu selten |
| Endlosschleife | Bedingung wird nie falsch, Programm hängt |

## Merksatz

**Startwert vor die Schleife, Grenzen prüfen, Sonderfall leer testen – und zu jedem Fehler gehören
Zeile, Begründung und Korrektur.**
