# Lernstil-Analyse (LS-02)

Stand: 12.11.2026 · Phase 0 · Grundlage: die beiden eigenen Lerndokumente und die drei
Notion-Portfolios (LF03, LF05, LF07), die nach eigener Angabe ohne KI geschrieben sind.
Nicht als Stilvorlage verwendet: das LF01-Portfolio (erkennbar KI-Passagen, P-54) und das
LF04-Portfolio (Gruppentext mit vielen Floskeln, Anteil des Azubis unklar). Die Lehrgangsfolien
„Vernetzte Systeme“ bleiben außen vor, bis ihre Herkunft geklärt ist (F-02).

**Ergebnis:** Der Azubi lernt **top-down über ein durchgehendes Praxisbeispiel**: erst ein
Gesamtdiagramm des Ablaufs, dann jeder Schritt mit „Warum?“, echten Zahlen und einem kurzen
Zwischenfazit, am Ende eine Merktabelle. Die drei Annahmen aus dem Anforderungsdokument werden
zu zwei Dritteln bestätigt; neu ist ein klares Muster bei Begriffsverwechslungen.

## Kennzahlen

| Dokument | Wörter | Seiten/Umfang | Grafiken | Tabellen | Auffälligkeiten |
| --- | ---: | --- | ---: | ---: | --- |
| Netzwerkgrundlagen | 2.484 | 12 S. | 11 (davon 2 als Tabellenbild) | 0 als Text, 3 als Bild | 20 × „Schritt“, 4 × „Halten wir kurz fest“, 7 Beispiele, 2 Alltagsanalogien, Du/Ihr-Ansprache |
| Projektmanagement | 957 | 5 S. | 3 | 3 | Pro/Contra-Tabellen, Vergleichstabelle, „Zusammenfassung zum Auswendig lernen“, „Wann verwende ich was?“ |
| LF03-Portfolio | 3.010 | 42 Überschriften | 16 | 2 | Top-down-Erklärung des Netzes in drei Ebenen (Was? Wie gewährleistet? Womit umgesetzt?), ausdrücklich nach Minto-Pyramide und didaktischer Reduktion |
| LF05-Portfolio | 1.531 | 28 Überschriften | 5 | 2 | Versionierte Artefakte (ERD V1 → V2 → V3) mit Begründung der Änderung |
| LF07-Portfolio | 1.694 | 14 Überschriften | 4 | 2 | Tabelle „Herausforderung – Ursache – Lösung“ |

## Beobachtete Muster

1. **Großes Bild zuerst.** Die Netzwerkgrundlagen beginnen mit einem Gesamtdiagramm „Host-PC
   ruft youtube.com auf“ und dem Satz, dass es „anfangs etwas überwältigend“ wirkt, dann folgt
   „Schritt für Schritt“. Im LF03-Portfolio wird das Netz bewusst von außen nach innen erklärt.
2. **Ein durchgehendes Beispiel mit echten Zahlen.** 192.168.178.99/24 → 208.65.153.238 zieht
   sich durch DNS, Subnetz-Check und Routing; die Dual-Umrechnung wird für jedes Oktett einzeln
   vorgerechnet.
3. **Ursache vor Detail.** Typische Formulierungen: „Wozu brauchen wir das denn?“, „Warum? Weil
   …“. Erklärt wird über Abläufe (erst A, deshalb B), nicht über Definitionen.
4. **Zwischenfazit nach jedem Abschnitt.** „Halten wir kurz fest:“ mit nummerierter Liste.
5. **Analogien aus dem Alltag.** IP = Postanschrift, MAC = Personalausweis; MAC = Transportmittel,
   IP = Navi; Subnetzmaske = Ausmaskieren aus der Bildbearbeitung.
6. **Merkstoff getrennt vom Verständnis.** Tabellen ausdrücklich „gut zum Auswendiglernen“,
   Pro/Contra-Tabellen, Vergleich „Wann verwende ich was?“.
7. **Selbst gezeichnete Diagramme** (draw.io, Mermaid) für jeden Prozess; Fotos kaum.
8. **Lockerer Ton**, direkte Ansprache, kleine Pointen („Boom!“, „Naja, so einfach ist es dann
   leider doch nicht“).
9. **Gliederung vor Inhalt.** Kapitelüberschriften werden vorab angelegt und später gefüllt –
   in den Netzwerkgrundlagen sind vier Kapitel noch leer.
10. **Begriffe benachbarter Konzepte verschwimmen.** Wiederkehrend in mehreren Dokumenten:
    Sprint Review/Retrospektive/Planning, Daily/„Weekly Stand-up“, ARP vs. NAT, TTL als
    Leerlaufzeit, Anforderungsniveau vs. Baustein, Fremdschlüssel im ERM (P-31, P-12, P-10, P-70,
    P-80). Das Verständnis der Abläufe ist meist richtig, der Fachbegriff am falschen Platz.

## Abgleich mit den Annahmen (Anforderungsdokument Kap. 3)

| Annahme | Befund | Bewertung |
| --- | --- | --- |
| Lernt über Ursache-Wirkung-Ketten: erst das Warum, dann das Detail | Muster 1–3 in allen eigenen Dokumenten | **bestätigt** |
| Löst Themen vollständig auf, statt Teilwissen stehen zu lassen | Wo geschrieben wird, sehr gründlich (jedes Oktett einzeln); aber vier angelegte Kapitel sind leer | **überwiegend bestätigt** – Tiefe ja, Vollständigkeit über alle Themen braucht Unterstützung durch den Plan |
| Lernt in Einheiten von 30–60 Minuten | Aus den Dokumenten nicht ableitbar | **offen** – per Fragebogen (LS-01) abfragen |

Ergänzung zur Selbsteinschätzung (Kap. 12): Projektorganisation und agiles Arbeiten werden als
„sicher“ eingeschätzt und in allen Portfolios praktiziert – die Scrum-Fachbegriffe sind aber
mehrfach falsch. Der Einstufungstest (LP-02) sollte Scrum gezielt auf Begriffsebene prüfen,
damit das Thema nicht vorschnell verkürzt wird.

## Vorschlag für das Lernstil-Profil

| Parameter | Vorschlag | Begründung |
| --- | --- | --- |
| Erklärtiefe | **vollständig aufgelöst** | Muster 2–3; der Azubi schreibt selbst bis auf Bit-Ebene |
| Einstieg | **Praxisbeispiel zuerst** | Muster 1–2: Gesamtablauf am konkreten Fall, dann Theorie |
| Darstellung | **Diagramm** (Tabellen für Merkstoff, Analogien ergänzend) | Muster 5–7 |
| Aufgabenmix | erklären 40 % · rechnen 35 % · zuordnen 25 % | Stärke im Erklären; Rechnen ausbauen (Subnetting, Kosten, Datenmengen); Zuordnen gegen Begriffsverwechslungen (Muster 10) |
| Session-Länge | **45 Min.** (vorläufig) | Mitte der angenommenen 30–60 Min.; im Fragebogen bestätigen |
| Hilfeverhalten | **erst selbst probieren** (vorläufig) | Indiz: eigenständige Fehlersuche im LF03-Fehlerprotokoll; schwach belegt, im Betrieb über LS-03 nachschärfen |

## Folgen für die Aufbereitung der Lektionen

- Jede Lektion beginnt mit einem Ablaufdiagramm des Gesamtvorgangs und einem durchgehenden
  Beispiel aus der fiktiven Firma (Linux-Server, Container, Archivierung großer Datenmengen).
- Nach jedem Teilschritt ein Kasten „Halten wir kurz fest“.
- Ein eigener Abschnitt **„Nicht verwechseln“** je Lektion grenzt benachbarte Begriffe ab
  (z. B. Review ↔ Retrospektive ↔ Planning; ARP ↔ NAT ↔ DNS). Die gefundenen Fehler werden zu
  Fehlerkarten (ZI-05) und Distraktoren in Zuordnungsaufgaben.
- Merktabellen am Ende, klar getrennt vom Erklärteil.
- Ton: locker, Du-Form, Fachbegriffe exakt nach Norm, Scrum Guide oder BSI.
