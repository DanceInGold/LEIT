# Prüfprotokoll (Faktencheck)

Stand: 12.11.2026 · Phase 0 · Ablauf siehe `CLAUDE.md`, Abschnitt „Ablauf Faktencheck“.

**Ergebnis:** 53 Befunde in 8 Quellen, davon 15 Fehler, 17 Ungenauigkeiten, 4 veraltete Aussagen
und 17 Hinweise. Die meisten Fehler betreffen Scrum-Begriffe, die Abgrenzung von ARP, NAT und
Routing sowie die ER-Modellierung – genau die Themen, bei denen die Lektionen Begriffe besonders
scharf trennen müssen. Kein Quelltext in `quellen/` wurde verändert.

**Schwere:** Fehler = sachlich falsch · ungenau = missverständlich oder unvollständig ·
veraltet = früher richtig, heute nicht mehr · Hinweis = Verbesserung oder Prüfgrenze.
**Status:** offen = Korrektur fließt bei der Aufbereitung in die Lektion ein · nicht prüfbar =
aus Repo-Quellen nicht belegbar · Entscheidung = braucht eine Antwort des Azubis.

## Anforderungsdokument (`docs/anforderungen.md`)

| ID | Stelle | Aussage | Befund und Korrektur | Beleg | Schwere | Status |
| --- | --- | --- | --- | --- | --- | --- |
| P-01 | Kap. 2, „Korrektur für den Katalog 2025“ | „KI-Grundlagen und BPMN neu hinzugekommen“ | BPMN steht weder in der Änderungstabelle noch wird es dort erwähnt; ein Leser weist in den Kommentaren darauf hin, dass BPMN „im AP1-Katalog mit keinem Wort erwähnt“ wird. Im gemeinsamen Beiblatt steht nur die **EPK**-Notation. Vorschlag: BPMN streichen, EPK als „Beiblatt-Notation, nicht im Katalog“ führen. Die Quelle ap1-trainer-pro.de war aus dieser Umgebung nicht abrufbar. | `quellen/pruefung/katalog-2025-aenderungen-it-berufe-podcast-190.pdf`, S. 4–12 (Tabelle), S. 22–23 (Kommentare zu EPK), S. 24 (Kommentar zu BPMN) | ungenau | erledigt: BPMN als Zusatzthema, Text korrigiert (E-10) |
| P-02 | Kap. 2, Tabelle Prüfungsrahmen | „Katalog aus dem Repo ist die maßgebliche Themenquelle“ | Im Repo liegt nur die Änderungsliste (Delta), nicht der Katalog. Der Autor schreibt selbst: „Das ist nur das Delta und nicht der komplette Katalog.“ | ebd., S. 22 | Hinweis | offen: Katalog bestellt (F-01) |
| P-03 | Kap. 2, Themengewichtung | Punkte je Thema (Nutzwertanalyse 45, ERM 42 …), „Datenschutz in 7 von 11 Prüfungen“ | Stammt von der Website des IT-Berufe-Podcasts, nicht aus einer Datei im Repo. Plausibel, aber hier nicht nachprüfbar. | – | Hinweis | nicht prüfbar |

## Netzwerkgrundlagen (`quellen/eigene/netzwerkgrundlagen.pdf`)

| ID | Seite | Aussage | Befund und Korrektur | Beleg | Schwere | Status |
| --- | --- | --- | --- | --- | --- | --- |
| P-10 | S. 4 | DNS-Cache: „sollte die IP-Adresse im Cache für eine bestimmte Zeit nicht genutzt werden, wird diese wieder aus dem Cache gelöscht“ (TTL) | Die TTL ist eine **feste Gültigkeitsdauer**, die der zuständige (autoritative) DNS-Server je Eintrag vorgibt. Der Eintrag läuft nach Ablauf ab – egal, wie oft er genutzt wurde. Nutzung verlängert die TTL nicht. | RFC 1035, Abschn. 3.2.1 und 4.1.3; RFC 2181, Abschn. 8 | Fehler | offen |
| P-11 | S. 2 | Interner DNS-Server als Forwarder „schickt nun eine spezifische Anfrage an den Router, welcher sich mit dem … externen DNS-Server verbindet und sich dann von dort die IP-Adresse holt“ | Der interne DNS-Server fragt den Forwarder (z. B. 8.8.8.8) **selbst**; der Router leitet das Paket nur weiter (Routing, ggf. NAT) und ist an der Namensauflösung nicht beteiligt. Nur im Heimnetz-Fall „Router-DNS“ ist der Router selbst DNS-Proxy. | RFC 1034, Abschn. 5 (Resolver) | ungenau | offen |
| P-12 | S. 6 | Router im Fall „Zielnetz direkt angeschlossen“: verpackt die Antwort „mit der Host-PC MAC-Adresse als Ziel (weiß er durch seine NAT)“ | Zwischen eigenen Subnetzen findet **keine NAT** statt. Die Antwort trägt die IP des Host-PCs als Ziel; die passende MAC-Adresse kennt der Router aus seinem **ARP-Cache**. NAT betrifft nur den Übergang privat ↔ öffentlich. | RFC 826 (ARP); RFC 3022 (NAT) | Fehler | offen |
| P-13 | S. 7 | „Die MAC-Adresse ist das Transportmittel (Absender und Empfänger ändern sich in jedem Schritt)“ | Die MAC-Adressen ändern sich an **jedem Router** (L3-Hop), nicht an Switches – ein Switch leitet den Frame unverändert weiter. „Jeder Schritt“ heißt also „jedes Teilnetz“. | IEEE 802.1D (Bridging); RFC 1812, Abschn. 5.2 | ungenau | offen |
| P-14 | S. 6 | ARP: Empfänger „hört das über den Broadcast Channel und antwortet“ | Ergänzen: Die ARP-Anfrage ist ein Broadcast, die **Antwort ein Unicast**; beide Seiten speichern das Paar IP–MAC im ARP-Cache (zeitlich begrenzt). | RFC 826 | Hinweis | offen |
| P-15 | S. 6 | MAC-Adresse „identifiziert das Gerät immer als Individuum, unabhängig welche IP das Gerät hat“ | Die MAC-Adresse gehört zur **Netzwerkschnittstelle**, nicht zum Gerät (ein Laptop hat mehrere), ist softwareseitig änderbar und wird bei WLAN oft zufällig erzeugt (MAC-Randomisierung). Sie ist nur im lokalen Netzsegment sichtbar. | IEEE 802 (EUI-48) | ungenau | offen |
| P-16 | S. 10 | „Die Standard-Subnetzmaske ist 255.255.255.0“ | Es gibt keine allgemeine Standardmaske. /24 ist in Heimnetzen üblich und war die Vorgabe der früheren Klasse C; seit CIDR wird die Maske frei nach Bedarf gewählt. | RFC 4632 (CIDR) | ungenau | offen |
| P-17 | S. 10 | „Das zeigt uns, dass es für jeden Block nur 255 theoretische Möglichkeiten gibt“ | Ein Oktett hat **256** Werte (0 bis 255 = 2⁸). | Rechnung: 2⁸ = 256 | Fehler | offen |
| P-18 | S. 11 | VLAN-Beispiel: „VLAN1 … Netzwerkadresse 192.168.178.0, Nutzbare Hosts: .0 bis .127“ | Bei 192.168.178.0/25 ist .0 die Netzadresse und .127 die Broadcastadresse – nutzbar sind **.1 bis .126** (126 Hosts). VLAN2 192.168.178.128/25: nutzbar .129–.254 (Router .129, Clients ab .130 stimmt). Die Maske /25 = 255.255.255.128 fehlt im Beispiel. | Rechnung: 2⁷ − 2 = 126 | Fehler | offen |
| P-19 | S. 11 | „Ohne Subnetting wäre es nicht möglich, von einem VLAN in das nächste VLAN zu kommunizieren“ | Ursache-Wirkung umdrehen: VLANs trennen Broadcast-Domänen auf Schicht 2. Zwischen VLANs braucht es deshalb **Routing** (Router-on-a-Stick oder Layer-3-Switch); dafür erhält jedes VLAN ein eigenes IP-Subnetz. | IEEE 802.1Q | ungenau | offen |
| P-20 | S. 7, 12 | „SAT Table…“, „SWAT Tabelle“ | Gemeint ist die **MAC-Adresstabelle** des Switches (auch SAT = Source Address Table oder CAM-Tabelle). „SWAT“ ist ein Tippfehler. | IEEE 802.1D | Hinweis | offen |
| P-21 | S. 6–7, 12 | Kapitel „IP-Adressen (öffentlich/privat/NAT)“, „Switching“, „Routing“, „Pakete“ | Nur Überschriften, kein Inhalt. Lücke wird bei der Aufbereitung neu geschrieben. | – | Hinweis | offen |

Bestätigt: Umrechnung 192.168.56.120 = 11000000.10101000.00111000.01111000; Stellenwerte 2⁷…2⁰;
UND-Verknüpfung zur Netzadresse; Routing-Tabelle mit 0.0.0.0/0 als Gateway of Last Resort;
private IP wird beim Übergang ins Internet per NAT/PAT durch öffentliche IP + Port ersetzt.

## Projektmanagement (`quellen/eigene/projektmanagement.pdf`)

| ID | Seite | Aussage | Befund und Korrektur | Beleg | Schwere | Status |
| --- | --- | --- | --- | --- | --- | --- |
| P-30 | S. 1, Diagramm | Wasserfall: Analyse → Design → Implementierung → **Betrieb** → **Test** | Test kommt **vor** der Inbetriebnahme: Anforderungsanalyse → Entwurf → Implementierung → Test → Einführung/Betrieb (Wartung). | Royce (1970); gängige Lehrbuchdarstellung | Fehler | offen |
| P-31 | S. 3 | Sprint Planning: „welche Storys seit dem letzten Sprint Planning erreicht wurden und was bis zum nächsten … erreicht werden soll (Retroperspektive)“ | Drei Events vermischt: Der Rückblick auf das Ergebnis ist das **Sprint Review**, der Rückblick auf Zusammenarbeit und Prozess die **Sprint Retrospective**. Das **Sprint Planning** plant nur den kommenden Sprint (Sprint-Ziel, Auswahl, Plan = Sprint Backlog). „Retroperspektive“ heißt korrekt Retrospektive. | Scrum Guide 2020, „Scrum Events“ | Fehler | offen |
| P-32 | S. 3 | Scrum mit „Daily- und Weekly Stand-Up“ | Ein **Weekly Stand-Up gibt es in Scrum nicht**. Die Events sind: Sprint, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective. Review und Retro fehlen im Text ganz (das Diagramm zeigt sie). | Scrum Guide 2020 | Fehler | offen |
| P-33 | S. 3 | Scrum Master sorgt dafür, dass „alle Meetings … durchgeführt werden“; Entwickler „halten mit dem Scrum Master die Stand-Ups ab“ | Das Daily Scrum gehört den **Developers**; der Scrum Master sorgt dafür, dass es stattfindet, muss aber nicht teilnehmen. Seine Rolle: Coach und Verantwortlicher für die Wirksamkeit des Teams. | Scrum Guide 2020, „Scrum Master“, „Daily Scrum“ | ungenau | offen |
| P-34 | S. 3 | Entwickler „halten alles in einem Kanban Board fest“ | Scrum-Artefakte sind **Product Backlog, Sprint Backlog und Increment** (mit Product Goal, Sprint Goal, Definition of Done). Ein Board ist ein optionales Hilfsmittel, kein Scrum-Bestandteil. | Scrum Guide 2020, „Scrum Artifacts“ | ungenau | offen |
| P-35 | S. 1, 3 | „Unter klassischem PM versteht man das Wasserfallmodell“, „Unter einer agilen PM-Methode versteht man Scrum“ | Beides sind Beispiele, keine Definitionen: Wasserfall ist ein klassisches Modell neben anderen, Scrum ein agiles Framework neben Kanban, XP u. a. Für die AP1 2025 werden nur Wasserfall und Scrum ausdrücklich genannt. | Katalog-Delta, 01.01 | ungenau | offen |
| P-36 | S. 3 | Product Owner „repräsentiert unseren Kunden. Er stellt die Anforderungen“ | Genauer: Der PO ist verantwortlich, den Produktwert zu maximieren, und verwaltet und **priorisiert das Product Backlog**. Anforderungen kommen von Stakeholdern/Kunden; der PO entscheidet über die Reihenfolge. | Scrum Guide 2020, „Product Owner“ | ungenau | offen |
| P-37 | S. 4, Pro/Contra | Lineares PM: „Test-Risiko: Da erst ganz am Ende getestet wird …“ neben „Qualitätssicherung (V-Modell)“ | Widerspruch im Dokument: Das V-Modell plant zu jeder Entwurfsstufe eine Teststufe von Anfang an. Das Test-Risiko gilt für den reinen Wasserfall. | – | Hinweis | offen |
| P-38 | S. 1–2 | V-Modell als zweites lineares Modell | Fachlich korrekt, aber seit Katalog 2025 nicht mehr AP1-relevant (nur Wasserfall und Scrum). | Katalog-Delta, 01.01 | Hinweis | offen |

Bestätigt: Sprintlänge „meist 2–4 Wochen“/„max. 30 Tage“ (Scrum Guide: höchstens ein Monat);
Inkrement am Sprintende; Vergleichstabelle Planung/Fokus/Produkt/Änderungen entspricht dem
Agilen Manifest.

## Lehrgangsfolien (`quellen/pruefung/vernetzte-systeme-it-infrastruktur-l3-2026.pdf`)

| ID | Folie | Aussage | Befund und Korrektur | Beleg | Schwere | Status |
| --- | --- | --- | --- | --- | --- | --- |
| P-40 | Dateititel, Folien 2, 3, 10, 11, 17 | Titel „PRÜFUNGSRELEVANT“, „AP1-Fokus“; Lernziel 8 mit RAID und SAN; WWAN mit LTE/5G; Übungsaufgabe RAID-Wahl | RAID, SAN und LTE/5G sind seit dem Katalog 2025 **nicht mehr AP1-Stoff** (Katalogvorwort: SQL und RAID „ausschließlich in Teil 2“). Für AP2 bleiben sie relevant. | Katalog-Delta S. 4, 7, 11; Kommentar S. 18 | veraltet | offen |
| P-41 | 10 | RAID 1 Nutzkapazität „1/2 · (n · N)“ | Stimmt nur für zwei Platten. Allgemein ist ein Spiegel so groß wie **eine** Platte (N). | – | Hinweis | offen |
| P-42 | 3 | Stern-Topologie: „Hoher Ausfallschutz bei Kabelbruch“ | Ergänzen: Ein Kabelbruch trifft nur einen Teilnehmer, aber der zentrale Switch ist ein **Single Point of Failure**. | – | ungenau | offen |
| P-43 | 12 | Typ-1-Beispiel „Microsoft Hyper-V Server“ | Das kostenlose Produkt „Hyper-V Server“ endete mit Version 2019; Hyper-V als Rolle in Windows Server ist weiterhin Typ 1. Virtuelle Server sind 2025 aus dem AP1-Katalog gestrichen (nur noch virtuelle Desktops). | Microsoft Lifecycle; Katalog-Delta 03.01 | veraltet | offen |
| P-44 | 8 | Übungsaufgabe 1 ohne Lösung | Nachgerechnet für die spätere Aufgabe: 172.16.48.0/20, 4 Subnetze à ≥ 100 Hosts → **/25** (126 Hosts), Maske **255.255.255.128**; 1. Subnetz 172.16.48.0, erster Host .1, letzter Host .126, Broadcast .127; Echtzeitvideo → **UDP** (kein Neusenden, geringe Latenz). | Rechnung: 2⁷ − 2 = 126 ≥ 100 | Hinweis | offen |

Bestätigt: Verfügbarkeit = MTBF / (MTBF + MTTR); 99,9 % ≈ 8,76 h und 99,999 % ≈ 5,26 min
Ausfall pro Jahr; USV-Klassen VFD (offline), VI (line-interactive), VFI (online); Hub Schicht 1,
Switch Schicht 2, Router Schicht 3; „Switches trennen Kollisionsdomänen, Router trennen
Broadcast-Domänen“; nutzbare Hosts = 2^(32 − Präfix) − 2; 3-2-1-Regel; Zuordnung OSI ↔ TCP/IP.

## LF01-Portfolio (`quellen/portfolios/lf01-portfolio-unternehmen.pdf`)

Unternehmensfakten wurden nur stichprobenartig geprüft, weil sie nicht prüfungsrelevant sind.

| ID | Seite | Aussage | Befund und Korrektur | Beleg | Schwere | Status |
| --- | --- | --- | --- | --- | --- | --- |
| P-50 | S. 8 | „Als Übersicht haben wir eine EPK erstellt“ | Das Diagramm ist ein Flussdiagramm aus Kästen und Pfeilen. Eine EPK braucht abwechselnd **Ereignisse und Funktionen** und Konnektoren (UND, ODER, XOR). | ARIS-/EPK-Notation (Scheer); Beiblatt AP1 | Fehler | offen |
| P-51 | S. 24 | „Artemis II, welche im Februar 2026 mit 5 Astronauten … fliegen wird“ | Artemis II startete am **1. April 2026** mit **vier** Astronaut:innen. | [Spektrum](https://www.spektrum.de/news/nasa-mission-artemis-ii-aufbruch-zum-mond/2317791), [ZDF](https://www.zdfheute.de/panorama/artemis-2-crew-mond-100.html) | veraltet | offen |
| P-52 | S. 11–12 | ZEROe: erstes Wasserstoff-Passagierflugzeug „bis 2035“ | Airbus hat das Programm im Februar 2025 zurückgestellt; Verzögerung um mehrere Jahre. | [airliners.de](https://www.airliners.de/airbus-verschiebt-entwicklung-wasserstoff-flugzeug/79099), [electrive](https://www.electrive.net/2025/02/10/airbus-pausiert-auch-entwicklung-von-wasserstoff-flugzeug/) | veraltet | offen |
| P-53 | S. 8 | „Die Kernzeit für den Arbeitsbeginn liegt flexibel zwischen 06:30 und 09:30 Uhr“ | Begriff: **Kernzeit** ist die Zeit mit Anwesenheitspflicht; das flexible Fenster heißt Gleitzeitrahmen. | – | ungenau | offen |
| P-54 | S. 13, 16, 18, 24 | „Soll ich Ihnen noch Details … heraussuchen?“, „Möchten Sie, dass ich …“, „die von dir genannten Schwerpunkte“, LaTeX „$-253^\circ C$“ | Reste von KI-Antworten im Text. Dokument wird nicht als Stilvorlage verwendet; Aussagen daraus nur nach eigener Prüfung übernehmen. | – | Hinweis | offen |

Bestätigt: Airbus SE ist eine Europäische Aktiengesellschaft (Sitz Leiden, NL; Zentrale Toulouse);
Markt für zivile Großraumflugzeuge als Oligopol (Duopol Airbus/Boeing).

## LF03-Portfolio (`quellen/portfolios/lf03-notion/`)

| ID | Stelle | Aussage | Befund und Korrektur | Beleg | Schwere | Status |
| --- | --- | --- | --- | --- | --- | --- |
| P-60 | Markdown, TH4 Schritt 1 | „Leasingrate ca. 3,33 % pro Monat … Daraus ergibt sich 300 € Leasingkosten pro Jahr pro Gerät“ | 3,33 % × 1.000 € × 12 = **400 €** pro Jahr. Die 300 € (= 1.200 € für 4 Geräte in der Excel-Tabelle) entsprechen **2,5 %** pro Monat. | Rechnung | Fehler | offen |
| P-61 | `LeaseOrBuyTH4.xlsx`, Zeile 18 | „Die Abweichung in Prozent beträgt 11,5 %“ (520 € / 4.500 €) | 520 / 4.500 = 11,56 % → gerundet **11,6 %**. Tilgungsplan (5 % Zinsen auf Restschuld, 4.500 € gesamt) und Leasing (4.800 € + 220 € Restwert = 5.020 €) sind korrekt. | Rechnung | Hinweis | offen |
| P-62 | Markdown, TH1 Ping-Test | Erstes Paket geht verloren, weil „die Kommunikation … über das Routing läuft und … eine direkte Verbindung via MAC nicht möglich ist“ | Ursache ist die **ARP-Auflösung**: Der PC muss erst die MAC des Gateways, der Router die MAC des Ziels erfragen; Packet Tracer verwirft das erste ICMP-Paket währenddessen. Die eigene Excel-Notiz („muss zuerst ARP ausführen“) war richtig. | RFC 826; Cisco Packet Tracer-Verhalten | ungenau | offen |
| P-63 | `IPAM_TH4-Zustand_(1).xlsx` | LTLounge04 bis LTLounge08 haben alle die MAC 00D0.FFA8.3D80 | MAC-Adressen müssen im Netz **eindeutig** sein – Kopierfehler in der Dokumentation. | IEEE 802 | Fehler | offen |
| P-64 | beide IPAM-Dateien | Subnetzmaske als „255255255128“ | Die Zelle ist als Zahl formatiert, die Punkte fehlen. Als Text formatieren. | – | Hinweis | offen |
| P-65 | Markdown, TH4 Schritt 2.2 | WPA2 mit PSK „lounge42“ stellt „ein angemessenes Sicherheitsniveau“ dar | Heute wird **WPA3** (SAE) empfohlen; WPA2-PSK mit kurzem Schlüssel ist per Wörterbuchangriff angreifbar. | BSI IT-Grundschutz NET.2.2 (WLAN-Nutzung) | ungenau | offen |
| P-66 | Markdown, TH1 | „Netzwerkadresse 172.16.10“ | Vollständig: 172.16.10.0/25 und 172.16.10.128/25 (zwei VLANs). | – | Hinweis | offen |

## LF04-Portfolio (`quellen/portfolios/lf04-portfolio-schutzbedarfsanalyse.pdf`)

| ID | Seite | Aussage | Befund und Korrektur | Beleg | Schwere | Status |
| --- | --- | --- | --- | --- | --- | --- |
| P-70 | S. 3, 9 | „pro Anforderungsniveau drei Bausteine gewählt“; „Basis-Anforderungen (3 Objekte), Standard-Anforderungen (3 Objekte), Anforderungen bei hohem Schutzbedarf (3 Objekte)“ | Konzeptfehler: Die Niveaus Basis/Standard/erhöht gelten für die **einzelnen Anforderungen innerhalb eines Bausteins**, nicht für Bausteine oder Objekte. Modellierung heißt: Bausteine auf Zielobjekte abbilden; welche Anforderungen umgesetzt werden, folgt aus Absicherungsvariante (Basis-, Standard-, Kern-Absicherung) und Schutzbedarf. | BSI-Standard 200-2, Kap. 8.3; IT-Grundschutz-Kompendium, Aufbau der Bausteine | Fehler | offen |
| P-71 | S. 9 | „Anforderungen bei hohem Schutzbedarf“ | Fachbegriff: Anforderungen bei **erhöhtem** Schutzbedarf. | IT-Grundschutz-Kompendium | ungenau | offen |
| P-72 | S. 6, EPK „Scooter ausleihen“ | XOR-Verzweigung direkt nach dem Ereignis „Verbindungsversuch gestartet“ | Nach einem Ereignis darf **kein XOR/ODER-Split** folgen – Ereignisse entscheiden nicht. Der XOR gehört hinter die Funktion „App versucht Verbindung herzustellen“. Außerdem fehlt die Rückführung für „weiterer Verbindungsversuch“. | EPK-Modellierungsregeln (Scheer) | Fehler | offen |
| P-73 | S. 11 | Baustein-Anforderungen INF.10.A5, INF.7.A5, APP.1.1.A17, SYS.1.1.A22, APP.4.3.A22, NET.3.1.A19, NET.1.2.A25, APP.3.3.A12 | Einzelne IDs nicht gegen das aktuelle Kompendium geprüft (Quelle hier nicht verfügbar). Für die AP1 zählt das Vorgehen, nicht die Nummer. SYS.2.1.A1 „Sichere Benutzerauthentisierung“ (Basis) ist korrekt. | – | Hinweis | nicht prüfbar |
| P-74 | S. 6–10 | Vorgehen Strukturanalyse → Schutzbedarfsfeststellung → Modellierung → IT-Grundschutz-Check; Kategorien normal/hoch/sehr hoch | Korrekt. Ergänzen: In der Strukturanalyse gehören auch **Netzplan und Kommunikationsverbindungen** dazu; die NET-Objekte fehlen in der Tabellenaufzählung. | BSI-Standard 200-2, Kap. 8.1 | Hinweis | offen |

## LF05-Portfolio (`quellen/portfolios/lf05-notion/`)

| ID | Stelle | Aussage | Befund und Korrektur | Beleg | Schwere | Status |
| --- | --- | --- | --- | --- | --- | --- |
| P-80 | `UpdatedERD.drawio.png` (V3) | Entität Bestellung mit Attribut **KundenNr** (unterstrichen) | Fremdschlüssel gehören ins **relationale Modell**, nicht ins ERM – dort drückt die Beziehung „tätigt“ (1:n) den Zusammenhang aus. Unterstrichen wäre KundenNr zudem Teil des Primärschlüssels, was falsch ist (BestellNr identifiziert allein). | Chen (1976); Kemper/Eickler, Datenbanksysteme, Kap. 2 | Fehler | offen |
| P-81 | ebd. | Beziehungen „enthält“ tragen BestellNr/ZutatenNr, ZutatenNr/RezeptNr, ABNR/ZutatenNR, NährwertNr/ZutatenNr, ErkaNR/RezeptNr als Attribute | Gleiche Ursache: Schlüssel der beteiligten Entitäten werden im ERM nicht an die Beziehung geschrieben. Echte Beziehungsattribute wie **Menge** bleiben. Beim Überführen ins Relationenmodell entsteht daraus die Zwischentabelle mit zusammengesetztem Schlüssel. | ebd. | Fehler | offen |
| P-82 | ebd. | Zutat hat das Attribut „Lieferant“ **und** die Beziehung „liefert“ zu Lieferant | Redundanz: Die Beziehung genügt, das Attribut entfällt. | ebd. | Fehler | offen |
| P-83 | ebd. | Zutat hat Kalorien, Protein, Kohlenhydrate **und** eine m:n-Beziehung zur Entität Nährwerte | Doppelte Modellierung derselben Information; eine Variante wählen (für flexible Nährwerte die Entität). | ebd. | ungenau | offen |
| P-84 | Markdown (auch LF03) | Daily: „Was haben wir am Tag zuvor gemacht (Retroperspektive)?“; „Weekly Stand-Up (Iteration Retro)“ | Siehe P-31/P-32: Rückblick im Daily ist kein Retrospektive-Event; korrekt „Retrospektive“. | Scrum Guide 2020 | ungenau | offen |
| P-85 | Markdown, Sprint 3 | „Zeitraum 30.07 – 02.07“ | Tippfehler, gemeint ist 30.06. – 02.07. | – | Hinweis | offen |
| P-86 | alle drei ERD-PNGs | – | Linien und Kardinalitäten sind weiß auf transparentem Hintergrund (Dark-Mode-Export) und auf weißem Grund unsichtbar. Für Lektionen hell neu zeichnen. | – | Hinweis | offen |

## LF07-Portfolio (`quellen/portfolios/lf07-notion/`)

Keine Befunde. Bestätigt: SPI am Arduino Uno auf Pins 11 (MOSI), 12 (MISO), 13 (SCK); analoge
Pins A0–A3 als digitale Ausgänge nutzbar; 28BYJ-48 im Vollschritt mit zwei Spulen hat mehr
Drehmoment als im Halbschritt; getrennte Versorgung der Aktoren mit gemeinsamer Masse gegen
Brownout.

## Lernfeld-Seiten (`quellen/lernfelder/`)

Keine fachlichen Aussagen, die zu prüfen wären (Aufgabenstellungen). Hinweis: LF05-Szenario B
fordert SQL-JOINs und Subselects – für AP1 2025 entfallen, für die Datenbank-Lektion nur das
ERM nutzen.

## Neue Lektionen und Glossar (Phase 1)

Alle Inhalte in `content/ap1/` sind neu geschrieben (E-09) und tragen bis zum Merge
`status: ungeprüft`. Geprüft wurden jede Zahl, jede Formel und jede Datenrate gegen die in der
Lektion genannten Belege; alle Rechenbeispiele wurden per Skript nachgerechnet.

| Lektion | Geprüfte Kernaussagen | Beim Gegenlesen korrigiert |
| --- | --- | --- |
| `hardware-pc-aufbau` | Formfaktor-Maße, PCIe-Raten je Lane (3.0/4.0/5.0), SATA III 6 Gbit/s ≈ 600 MB/s, Rechnung PCIe 4.0 x4 = 7,88 GB/s | – |
| `hardware-cpu-ram` | DDR-Prinzip (2 Übertragungen/Takt), DDR5-5600 = 2800 MHz Takt, Bandbreite 44,8 / 89,6 / 25,6 GB/s, SRAM vs. DRAM, SMT | Deep-Links ohne geprüfte Adresse durch Startseiten der Normungsgremien ersetzt |
| `hardware-netzteil-anschluesse` | η-Rechnung 300 W → 333,3 W, Stromkosten 175,98 €, 80-PLUS-Stufen (115 V), HDMI/DP/USB-Raten, ppi 92/109, USB-Kopierzeiten | 50-Hz-Wechselspannung wechselt 100-mal (nicht 50-mal) pro Sekunde die Richtung |
| `angebotsvergleich-quantitativ` | Bezugskalkulation A/B/C (7.978,18 / 8.065,50 / 7.758,60 €), Skonto als Jahreszins ≈ 36,7 % | Unsichere Buchquelle durch das Schema der Handelskalkulation ersetzt |
| `nutzwertanalyse` | Nutzwerte 7,50 / 6,95 / 6,50, Gewichte = 100 %, Preispunkte 10,0 / 9,7 / 9,6 | – |
| `erm-grundlagen` | Chen-Notation, (min,max), Übersetzung 1 : n / n : m / 1 : 1 | Unbelegte Aussage, das Prüfungs-Beiblatt enthalte die ERM-Notation, entfernt |

## Neue Lektionen und Glossar (Woche 2–3)

Neun Kapitel und 23 Glossarbegriffe, im PR mit `status: ungeprüft`. Alle Rechenbeispiele
(Schreibtischtests, Netzplan, Gantt-Termine, Kalkulation, Stundensatz) wurden mit einem
unabhängigen Skript nachgerechnet; der Python-Code der Lektion wurde ausgeführt. Alle Diagramme
wurden mit der Mermaid-Kommandozeile gerendert und angesehen.

| Lektion | Geprüfte Kernaussagen | Beim Gegenlesen korrigiert / nicht prüfbar |
| --- | --- | --- |
| `pseudocode-verzweigung` | Katalog 04.07 „Kontrollstrukturen … mittels Pseudocode“, Struktogramm/PAP entfallen; drei Grundstrukturen (Böhm/Jacopini 1966, DIN 66261); Auswertung der `else if`-Kette (12 → hot, 30 → warm, 400 → cold) | **Nicht prüfbar:** ob die Prüfung eine bestimmte Pseudocode-Schreibweise vorgibt – der vollständige Katalog mit Beiblatt fehlt (F-01). Die Lektion sagt deshalb nur, dass es keine Norm gibt und eine Vorgabe der Aufgabe gilt. |
| `pseudocode-schleifen` | kopf-/fußgesteuert/Zählschleife, `until` = Abbruch-, `do … while` = Weiterlaufbedingung, De Morgan, Summe 950 / Maximum 450, Python `range(1, 5)` = 1–4, Python ohne fußgesteuerte Schleife | – |
| `schreibtischtest-durchfuehren` | Katalog 04.07 „Schreibtischtest mit gegebenem Quellcode“; Trace: Ausgabe 5; `pruefziffer([4, 0, 1, 2, 3])` = 6 (ausgeführt); `/`, `//`, `%` nach Python-Doku | 41 Punkte stammen aus der Auswertung im Anforderungsdokument (Kap. 2), nicht aus dem Katalog. |
| `fehler-im-code-finden` | Katalog 04.07 „Fehler in gegebenem Quellcode finden“; `if x = 5:` ist in Python ein SyntaxError; Durchschnitt 237,5; drei Fehler und Korrektur | – |
| `projektstrukturplan` | Katalog 01.01 „Strukturplan, Netzplan, Gantt-Diagramm“ (Autor-Kommentar in der Quelle, S. 22); Begriffe nach DIN 69901-5; 100-%-Regel (PMI) | Normtext DIN 69901-5 liegt nicht im Repo; Begriffe sinngemäß, nicht wörtlich wiedergegeben. |
| `netzplan` | FAZ/FEZ/SAZ/SEZ, Maximum vorwärts / Minimum rückwärts, GP = SAZ − FAZ, FP = min FAZ Nachfolger − FEZ (Uni Bremen eGS 07-2), Projektdauer 15, kritischer Pfad A-B-E-F-G-I, FP ≤ GP | Hinweis auf zwei Zählweisen (Zeitpunkte ab 0 vs. Tage mit − 1) ergänzt, weil Lehrbücher hier abweichen. |
| `gantt-diagramm` | Termine ab Mo 11.01.2027 ohne Wochenenden, Ende Fr 29.01.2027; Meilenstein mit Dauer 0 | Buchangabe zu Gantt (Erscheinungsjahr unsicher) durch allgemeinen Beleg ersetzt; Meilensteine im Diagramm auf feste Daten gesetzt, weil Mermaid sie sonst auf den nächsten Werktag schiebt. |
| `kalkulation-verkaufspreis` | Schema Bezugspreis → Listenverkaufspreis; Skonto/Rabatt im Hundert (Lexware); 4.000,00 → 7.555,56 € brutto, Probe 5.600,00 €; Fehler bei × 1,02 = 2,24 €; USt 19 % nach § 12 Abs. 1 UStG | – |
| `kalkulation-vor-nach` | Stundensatz 90.000 € ÷ 1.500 h = 60,00 €, × 1,15 = 69,00 €; 1.680 / 1.500 h; Vorkalkulation 2.760,00 €, Nachkalkulation 3.120,00 €, Abweichung +30 %, nach Aufwand 3.588,00 € | Alle Kostenannahmen sind fiktiv und als Annahmen gekennzeichnet. |
