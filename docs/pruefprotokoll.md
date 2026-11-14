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

## Neue Lektionen und Glossar (Woche 4–5)

Neun Kapitel und zwölf Glossarbegriffe, im PR mit `status: ungeprüft`. Alle Adressrechnungen wurden
mit Pythons `ipaddress`-Modul gegengeprüft, alle Umrechnungen mit `bin()`, `hex()` und `int()`.
Alle Diagramme wurden mit der Mermaid-Kommandozeile gerendert.

| Lektion | Geprüfte Kernaussagen | Beim Gegenlesen korrigiert / Hinweis |
| --- | --- | --- |
| `relationale-tabellen` | Relation/Tupel/Attribut; Änderungs-, Einfüge-, Löschanomalie; 1NF–3NF am Archivbeispiel; Ergebnis deckt sich mit den Tabellen aus `erm-grundlagen`; referentielle Integrität | **Hinweis:** Der Katalog nennt die Normalformen nicht ausdrücklich („Grundlagen relationaler Datenbanken“). Die Lektion stellt sie deshalb als Werkzeug dar, nicht als sicheren Prüfungsstoff. |
| `osi-modell` | sieben Schichten nach ISO/IEC 7498-1, Dateneinheiten, Geräte je Schicht, Zuordnung zum TCP/IP-Modell nach RFC 1122 | TLS ausdrücklich als nicht eindeutig zuordenbar gekennzeichnet (in Lehrbüchern uneinheitlich: Schicht 4–6). |
| `ethernet-arp-ip-tcp` | ARP-Anfrage Broadcast, Antwort Unicast, Cache (RFC 826); MAC-Wechsel je Router; TTL − 1 je Router (RFC 1812); Drei-Wege-Handschlag (RFC 9293); UDP (RFC 768) | Abgrenzung ARP/NAT/DNS und IP-TTL/DNS-TTL gezielt aufgenommen (Befunde P-10, P-12, P-14). |
| `anwendungsprotokolle` | DNS-Ablauf, TTL als feste Gültigkeitsdauer (RFC 1034/1035); DORA, UDP 67/68 (RFC 2131); Mail-Ports 25/587/465, 143/993, 110/995 (RFC 8314); Ports nach IANA | – |
| `zahlensysteme-umrechnen` | 172 = `10101100` = 0xAC (beide Verfahren), 0x1F4 = 500, 0x3F = 63, `chmod 750` = `111 101 000` | – |
| `einheiten-praefixe` | SI-Präfixe (BIPM), binäre Präfixe (IEC 80000-13); 2 TB = 1,819 TiB; 100 Mbit/s = 12,5 MB/s; Abweichung Kilo 2,4 %, Tera ≈ 10 % | – |
| `ipv4-adressen` | 172.16.45.130/26 → Netz .128, Hosts .129–.190, Broadcast .191, 62 Hosts; private Bereiche (RFC 1918), Link-Local (RFC 3927) | „Keine Standardmaske“ gemäß Befund P-16; NAT nur am Übergang ins Internet gemäß P-12. |
| `subnetze-bilden` | 192.168.10.0/24 → 4 × /26; 172.16.48.0/20 → 8 × /23 mit 510 Hosts; 172.16.48.255 ist bei /23 ein gültiger Host | – |
| `subnetz-pruefen-vlsm` | 10.20.0.140/26 vs. .100 → verschiedene Netze, .180 → gleiches Netz; VLSM /25, /26, /27, /30 lückenlos; Weiterleitungsentscheidung nach RFC 1122, 3.3.1 | /31 nach RFC 3021 nur als Vertiefung erwähnt. |

## Neue Lektionen und Glossar (Woche 5–6)

Elf Kapitel und 13 Glossarbegriffe, im PR mit `status: ungeprüft`. Rechnungen per Skript, IPv6-Kürzungen
und Subnetze mit `ipaddress`, Hashwerte mit `hashlib`; Python-Beispiele ausgeführt; alle Diagramme
gerendert.

| Lektion | Geprüfte Kernaussagen | Beim Gegenlesen korrigiert / Hinweis |
| --- | --- | --- |
| `verschluesselung-verfahren` | Katalog 06.04 (symmetrisch, asymmetrisch, hybrid); AES 128/192/256 (FIPS 197); n(n − 1)/2 = 45 bzw. 2n = 20 Schlüssel; TLS 1.3 mit Diffie-Hellman (RFC 8446) | **Nicht übernommen:** konkrete RSA-Mindestlängen. Die gefundene Sekundärquelle zur BSI TR-02102-1 widerspricht sich selbst (2000 vs. 3000 Bit); die Lektion verweist deshalb nur auf die TR. |
| `hash-signatur-zertifikat` | SHA-256 = 256 Bit = 64 Hex-Zeichen (FIPS 180-4); Hashpräfixe `ae581b52…`/`03c4a63a…` berechnet; Signatur privat/Prüfung öffentlich; X.509-Inhalte (RFC 5280); Passwort-Hashing mit Salt (OWASP) | Erste Fassung enthielt Platzhalter-Hashwerte; durch echte, berechnete Werte ersetzt. |
| `datenmengen-berechnen` | 36.000.000 B = 34,33 MiB; A4 @ 300 dpi = 2.480 × 3.508 px = 26.099.520 B; CD-Audio 10.584.000 B/min (IEC 60908); Full HD 10 s = 1.555.200.000 B | Zitat „gefühlt in jeder Prüfung“ als Kommentar des Autors gekennzeichnet, nicht als Katalogtext. |
| `uebertragungszeit` | 50 GB @ 1 Gbit/s = 400 s, mit 80 % = 500 s; 2 TB in 4 h → 1,11 Gbit/s; 20 Fotos in 1 min @ 100 Mbit/s; 500 TB @ 1 Gbit/s ≈ 46 Tage | – |
| `ipv6-adressen` | Kürzung `2001:db8::8:800:200c:417a` (Beispiel aus RFC 4291), `2001:db8::1:0:0:1` (RFC 5952: erste von gleich langen Folgen); Adressarten nach RFC 4291/4193; kein Broadcast | – |
| `ipv6-subnetze-slaac` | /48 → 65.536 /64-Subnetze, /56 → 256; EUI-64 aus `3c:52:82:1a:7f:09` = `3e52:82ff:fe1a:7f09`; SLAAC (RFC 4862), NDP (RFC 4861) | Präfixgrößen /48 für Unternehmen, höchstens /56 für Privatkunden nach RIPE-690 (Zusammenfassung der Internet Society). |
| `wasserfall-agil` | Katalog 01.01 „Projektphasen am Beispiel des Wasserfallmodells bzw. SCRUM“; weitere Vorgehensmodelle gestrichen; vier Werte des agilen Manifests | – |
| `scrum` | Verantwortlichkeiten, 5 Events mit Timeboxen (Sprint ≤ 1 Monat, Planning ≤ 8 h, Daily 15 min, Review ≤ 4 h, Retro ≤ 3 h), 3 Artefakte mit Commitments, Team ≤ 10 Personen (Scrum Guide 2020) | Unbelegte Aussage, Prüfungen akzeptierten „Rollen“ und „Verantwortlichkeiten“, durch neutrale Formulierung ersetzt. |
| `oop-klassen-objekte` | Katalog 04.06, Vererbung entfallen; UML-Klassennotation; Python-Code ausgeführt (`läuft`, `neu`, `400.0`) | – |
| `oop-kapselung` | UML-Sichtbarkeiten + − # ~; Python-Konvention `_` (PEP 8) und Name Mangling `__`; Setter-Prüfung ausgeführt | – |
| `englische-texte` | Wortbedeutungen (actual, eventually, billion = 10⁹, quotation, lead time) | „warranty“ als freiwillige Garantie präzisiert (nicht gesetzliche Gewährleistung). |

## Neue Lektionen und Glossar (Sicherheit und Datenschutz)

Elf Kapitel und neun Glossarbegriffe, im PR mit `status: ungeprüft`. Rechnungen (Sicherungsmengen,
Verfügbarkeit) per Skript nachgerechnet, alle Diagramme gerendert. Rechtliche Aussagen geben den
Wortlaut der Normen wieder und sind keine Rechtsberatung.

| Lektion | Geprüfte Kernaussagen | Hinweis |
| --- | --- | --- |
| `schutzziele` | Grundwerte V, I, V (BSI-Standard 200-2); erweiterte Ziele | – |
| `schutzbedarf-feststellen` | Kategorien wörtlich nach BSI-Standard 200-2, Kap. 8.2.1; sechs Schadensszenarien | Abgrenzungstabelle in Euro/Stunden ist ein fiktives Beispiel; das BSI überlässt die Werte der Institution. |
| `schutzbedarf-vererbung` | Maximumprinzip, Kumulations-, Verteilungseffekt (Kap. 8.2.2, sinngemäß); Basis-, Kern-, Standard-Absicherung (Kap. 3.3) | Verteilungseffekt ausdrücklich nur für Verfügbarkeit dargestellt. |
| `dsgvo-grundsaetze` | Art. 4 Nr. 1, Art. 5 (sieben Grundsätze), Art. 6 Abs. 1 lit. a–f, Art. 7, Art. 9; DSB-Pflicht in der Regel ab 20 Personen (§ 38 BDSG) | – |
| `dsgvo-betroffenenrechte` | Art. 12 Abs. 3 (1 Monat + 2 Monate), Art. 13–21, 77; Pseudonymisierung Art. 4 Nr. 5, Anonymisierung ErwG 26; Art. 33 (72 h), Art. 34; Art. 83 (20 Mio. € / 4 %) | – |
| `tom-massnahmen` | Art. 32 DSGVO; acht Kontrollen nach Anlage zu § 9 BDSG a. F.; ISB vs. DSB | Die acht Kontrollen stammen aus dem alten BDSG und sind als Gliederungshilfe gekennzeichnet, nicht als geltendes Recht. |
| `isms-risikomatrix` | PDCA (BSI 200-1), Risiko = Wahrscheinlichkeit × Schaden, Behandlungsoptionen (BSI 200-3); Matrixwerte konsistent (1–3 gering, 4–6 mittel, 8–9 hoch, 12–16 sehr hoch) | ISO 27001 bewusst nicht als Prüfungsstoff dargestellt (Katalog 2025 streicht ISO-Normen). |
| `authentifizierung-passwoerter` | Faktoren, 2FA; NIST SP 800-63B Rev. 4 (August 2025): 15 Zeichen ohne zweiten Faktor, keine Kompositionspflicht, Wechsel nur bei Verdacht, Sperrliste | Rev.-4-Werte über eine Sekundärquelle (Enzoic) bestätigt; NIST-Originalseite verlinkt. |
| `haertung-firewall` | Härtungsmaßnahmen (BSI SYS.1.1/SYS.2.1), Personal vs. Netzwerk-Firewall, firewalld-Befehle (RHEL 9) | – |
| `datensicherung` | Sicherungsarten; Woche: 620 GB inkrementell vs. 920 GB differenziell, Restore 6 vs. 2 Sätze; 3-2-1; Großvater-Vater-Sohn (BSI CON.3) | RAID als gestrichenes Thema gekennzeichnet. |
| `verfuegbarkeit-sichern` | 99 % = 87,6 h, 99,9 % = 8,76 h, 99,99 % = 52,6 min, 99,999 % = 5,3 min; Reihe 98,505 %, parallel 99,99 %; USV-Klassen VFD/VI/VFI (IEC 62040-3) | – |

## Neue Lektionen und Glossar (Projekt, Kunde, Verträge)

Zehn Kapitel für zwölf Katalogthemen (drei Kapitel decken je zwei kleine Themen ab) und sechs
Glossarbegriffe, im PR mit `status: ungeprüft`. Rechnungen per Skript, Diagramme gerendert.
Rechtliche Aussagen geben den Wortlaut der Normen wieder und sind keine Rechtsberatung.

| Lektion | Themen | Geprüfte Kernaussagen | Hinweis |
| --- | --- | --- | --- |
| `projekt-smart` | projekt-merkmale, smart-ziele | Projektbegriff DIN 69901-5 (Einmaligkeit der Bedingungen); SMART nach Doran 1981 | Unbelegte Aussage zur Prüfungspraxis beim „A“ entfernt. |
| `teambildung` | teambildung | Tuckman 1965 (vier Phasen), Tuckman/Jensen 1977 (Adjourning) | – |
| `wirtschaftlichkeit` | wirtschaftlichkeit | Amortisation 24.000 € ÷ 1.000 €/Monat = 24 Monate; Break-even NAS/Cloud bei 40 TB (2.400 € = 2.400 €) | Werte fiktiv. |
| `kauf-miete-leasing` | kauf-miete-leasing | 1.000 € / 1.044 € / 1.440 € je Gerät über 36 Monate | Bilanz- und Steuerfragen ausdrücklich an die Buchhaltung verwiesen. |
| `lasten-pflichtenheft` | lasten-pflichtenheft | Urheber und Inhalt nach DIN 69901-5 | – |
| `vertraege` | vertraege | §§ 433, 535, 611, 631 BGB; § 434 Abs. 5 (Falschlieferung) wörtlich geprüft; 2 Jahre ab Ablieferung, Vorrang der Nacherfüllung, § 377 HGB (IHK Pfalz) | Zuweniglieferung: Einordnung seit der Reform 2022 als umstritten gekennzeichnet (in § 434 Abs. 5 n. F. nicht mehr ausdrücklich genannt). |
| `abnahme-leistung` | abnahme-doku, leistungsbestaetigung | Wirkungen der Abnahme (§ 640 BGB): Fälligkeit, Verjährungsbeginn, Beweislast | – |
| `kundenbedarf` | kundenbedarf, maerkte-bedarfe | Bedürfnis/Bedarf/Nachfrage; Fragetechniken; Kommunikationsquadrat (Schulz von Thun 1981) | „Märkte und Bedarfe“ hat im Katalog-Auszug keinen Unterpunkt; Inhalt deshalb auf Grundbegriffe beschränkt. |
| `kommunikationssysteme` | kommunikationssysteme | Upload-Rechnung 8 × 2 Mbit/s = 16 Mbit/s > 10 Mbit/s | Bandbreite je Teilnehmer als Annahme gekennzeichnet; nicht geprüfte BSI-Deep-Link-Adresse entfernt. |
| `praesentation` | praesentation | Aufbau, Medienwahl, Folienregeln, Medienkompetenz | Anteile und Schriftgrößen als Faustregeln gekennzeichnet. |

## Neue Lektionen und Glossar (Systeme und Netz)

Zwölf Kapitel für 13 Katalogthemen und vier Glossarbegriffe, im PR mit `status: ungeprüft`.
Rechnungen per Skript, Beispielskript mit `bash -n` geprüft, Diagramme gerendert.

| Lektion | Themen | Geprüfte Kernaussagen | Hinweis |
| --- | --- | --- | --- |
| `hdd-ssd` | speicher-hdd-ssd | 7.200 U/min → 8,33 ms je Umdrehung, 4,17 ms mittlere Rotationswartezeit; 600 TBW ÷ 100 GB/Tag ≈ 16,4 Jahre; Löschen von SSDs | Typische Werte (Datenrate, IOPS) als Größenordnungen gekennzeichnet; BSI-Deep-Link ohne geprüfte Adresse entfernt. |
| `uefi-dateisysteme` | bios-uefi-dateisysteme | MBR: 2³² × 512 B = 2 TiB, 4 primäre Partitionen; FAT32 max. 4 GiB − 1 B; ext4 16 TiB je Datei bei 4-KiB-Blöcken | RHEL-Standarddateisystem XFS ergänzt. |
| `installation-einrichtung` | installation-einrichtung | Ablauf, Partitionsschema, statisch vs. DHCP, nmcli; Ports SSH 22, RDP 3389, VNC 5900 | KI-Software nur knapp (Katalog nennt sie ohne Detail). |
| `betriebssysteme` | betriebssysteme | rwx = 4/2/1, `chmod 750`; Freigabe- und NTFS-Rechte: restriktivere gilt | Nicht geprüfte Microsoft-Adresse entfernt, Beleg ohne Link. |
| `client-server-domaene` | client-server-domaene | AD-Begriffe, Beitrittsschritte (DNS auf DC, Konto mit Beitrittsrecht, Neustart), `realm join` (RHEL 9) | – |
| `netzwerk-standards` | netzwerk-standards | 100BASE-TX/Cat 5, 1000BASE-T/Cat 5e, 10GBASE-T/Cat 6A, 100 m; Wi-Fi 4–7 = 802.11n/ac/ax/be; 2 TB über 1 Gbit/s = 16.000 s | WLAN-Raten als theoretische Bruttowerte gekennzeichnet. |
| `netzwerkkomponenten` | netzwerkkomponenten | Schichtzuordnung; PoE 15,4/30/bis 90 W (802.3af/at/bt) | – |
| `cloud-modelle` | cloud-modelle | IaaS/PaaS/SaaS und vier Bereitstellungsmodelle nach NIST SP 800-145; DaaS, VDI | – |
| `geraeteklassen` | geraeteklassen, auslastung-erweiterbarkeit | Auslastung 14,2/16 GB = 89 %, 410/512 GB = 80 % | 70–80 % als Faustregel gekennzeichnet. |
| `konsolenbefehle` | konsolenbefehle | Befehlspaare Windows/Linux; 169.254.0.0/16 = Link-Local (RFC 3927) | – |
| `skriptsprachen` | skriptsprachen | Beispielskript syntaktisch geprüft (`bash -n`); Shebang, Exit-Code, cron-Syntax | – |
| `nachhaltigkeit-energie` | nachhaltigkeit-energie | 0,4 kW × 8.760 h = 3.504 kWh = 1.051,20 €; PC/Thin Client 42,24 €/7,92 €, 50 Plätze 1.716 €; PUE 1,5 | Strompreis als Annahme. |

## Neue Lektionen und Glossar (Software, Qualität, Recht)

Elf Kapitel für 13 Katalogthemen und fünf Glossarbegriffe, im PR mit `status: ungeprüft`. Damit hat
jedes relevante Katalogthema (63) mindestens ein Kapitel. Rechnungen per Skript, Diagramme gerendert.

| Lektion | Themen | Geprüfte Kernaussagen | Hinweis |
| --- | --- | --- | --- |
| `uml-anwendungsfall-klasse` | uml | Use-Case-Elemente, include/extend, Multiplizitäten, Aggregation/Komposition (UML 2.5.1) | Mermaid zeichnet Use Cases nur annähernd; im Text auf die Papiernotation hingewiesen. |
| `uml-aktivitaet` | uml | Start, Aktion, Verzweigung/Zusammenführung, Gabelung/Vereinigung, Swimlanes (UML 2.5.1, Kap. 15); Schleife deckt sich mit `pseudocode-schleifen` | Gabelung/Vereinigung im Diagramm als Kasten angedeutet, Balken im Text erklärt. |
| `epk-bpmn` | epk, bpmn | EPK-Regeln (Ereignis–Funktion im Wechsel, kein XOR/ODER nach Ereignis); BPMN-Elemente (BPMN 2.0.2) | Als Zusatzthema gekennzeichnet (E-10). |
| `software-daten` | software-arten, stamm-bewegungsdaten | Softwarearten laut Katalog 03.01; ERP/SCM/CRM-Langformen; Stamm- vs. Bewegungsdaten | – |
| `support-ticket-rollout` | support-ki, rollout-ticketsystem | Support-Level 1st/2nd/3rd; Incident/Service Request/Problem (ITIL); Budget 62.070 € | ITIL als Anlehnung gekennzeichnet. |
| `suchoperatoren` | suchoperatoren | Operatoren nach Google-Hilfe; boolesche Operatoren | Beispiel mit gestrichenen Themen (SAN/RAID) ersetzt. |
| `urheberrecht-lizenzen` | urheberrecht-lizenzen | § 2, 7, 64, 69a–69d UrhG; GPL vs. MIT; 3.200 € vs. 2.640 € | – |
| `barrierefreiheit` | barrierefreiheit | WCAG 2.2 (POUR); BFSG anzuwenden seit 28.06.2025; Hilfsmittel laut Katalog | Statistik aktualisiert: 7,8 Mio. schwerbehinderte Menschen (Destatis, Juli 2026) statt einer Schätzung. |
| `masken-ergonomie` | masken-ergonomie | sieben Interaktionsprinzipien nach DIN EN ISO 9241-110:2020 (Erlernbarkeit, Benutzerbindung neu ggü. 2006) | – |
| `qualitaet-testprotokoll` | qualitaet | Qualitätsbegriff ISO 9000 (Hintergrund); Testprotokoll; Erstlösungsquote 48/60 = 80 % | ISO 9000 nur als Hintergrund, da ISO-Normen im Katalog gestrichen. |
| `rechtsformen-organisation` | rechtsformen-aufbauorganisation | GmbH 25.000 € (§ 5 GmbHG), UG ab 1 € (§ 5a), AG 50.000 € (§ 7 AktG); vier Organisationsformen | Als Zusatzthema gekennzeichnet. |

## Aufgaben und Generatoren (Phase 2, Aufgaben-Engine)

Sieben feste Aufgaben und zwei Generatoren, im PR mit `status: ungeprüft`. Jede Musterlösung
prüft `ap-tools check` automatisch (wird sie als richtig bewertet, zählt keine Falschantwort als
richtig). Die Generatoren rechnen von Hand (Restwertmethode, Bitoperationen) und werden in
1.000 Zufallsfällen gegen Pythons `int()`/`format()` bzw. das Modul `ipaddress` getestet.

| Aufgabe / Generator | Thema | Geprüfte Kernaussagen | Hinweis |
| --- | --- | --- | --- |
| `zahlen-hexziffer-bits` | zahlensysteme | 16 Werte = 2⁴ → 4 Bit je Hex-Ziffer (Nibble) | – |
| `zahlen-praefixe-zuordnen` | zahlensysteme | k = 10³, M = 10⁶ (SI); Ki = 2¹⁰ = 1.024, Mi = 2²⁰ = 1.048.576 (IEC 80000-13) | – |
| `zahlen-nibble-byte-luecke` | zahlensysteme | 1 Byte = 2 Hex-Ziffern; FF = 255, 256 Werte | – |
| `zahlen-groessen-ordnen` | zahlensysteme | KiB 1.024 < MB 10⁶ < MiB 1.048.576 < GB 10⁹ < GiB 1.073.741.824 Byte | per Skript nachgerechnet |
| `zahlen-warum-hex` | zahlensysteme | Hex ↔ 4 Bit; IPv6 in Hex notiert (RFC 4291, Abschnitt 2.2) | Operator „erläutern“ |
| `subnetz-gueltiger-host` | ipv4-subnetting | 192.168.10.64/26: Maske .192, Broadcast .127, Hosts .65–.126; .130 außerhalb | mit `ipaddress` nachgerechnet |
| `subnetz-vorgehen-ordnen` | ipv4-subnetting | Fünf-Schritte-Schema wie Lektion `subnetze-bilden` | – |
| Generator `zahlensysteme` | zahlensysteme | Stellenwerte 2ⁿ und 16ⁿ; Viererblöcke von rechts; Fehlerbilder: Bitreihenfolge, Reste falsch herum gelesen, Blöcke von links, Stellenwerte 10ⁿ | – |
| Generator `ipv4-subnetting` | ipv4-subnetting | Maske, Schrittweite 256 − Maskenwert, Netz/Broadcast, Hosts 2ʰ − 2, Subnetze 2ⁿ (RFC 950, RFC 4632); Adressen aus RFC-1918-Bereichen | Fehlerbilder: Hostmaske statt Netzmaske, nächste Netzadresse als Broadcast, „.255 ist immer Broadcast“, „− 2“ vergessen |

## Rechengeneratoren (Phase 2)

Vier Generatoren, im PR mit `status = "ungeprüft"`. Jede Variante rechnet der Generator exakt mit
Brüchen; die Tests lesen die Werte aus dem Aufgabentext und rechnen unabhängig nach (Modul
`ipaddress`, `Decimal` mit 50 Stellen), je 1.000 Zufallsfälle, lokal zusätzlich 2.800 weitere Seeds.
Alle Lektionsbeispiele werden in den Tests nachgerechnet. Beim Prüfen keine Fehler in bestehenden
Inhalten gefunden.

| Generator | Thema | Geprüfte Kernaussagen | Hinweis |
| --- | --- | --- | --- |
| `ipv6` | ipv6 | Kürzen nach RFC 5952 Abschnitt 4 (führende Nullen, längste Null-Folge ab 2 Blöcken, bei Gleichstand die erste, Kleinbuchstaben); /64-Subnetze = 2^(64 − Präfix); EUI-64 nach RFC 4291 Anhang A (ff:fe einfügen, Universal/Local-Bit umdrehen); SLAAC nach RFC 4862 | Fehlerbilder: führende Nullen stehen gelassen, kürzere Null-Folge gekürzt, „::“ zweimal, Nullen am Blockende gestrichen, rechts aufgefüllt, „− 2“ wie bei IPv4, falsches Bit umgedreht |
| `datenmengen` | datenmengen-uebertragung | Bild = Pixel × Farbtiefe ÷ 8; Scan: mm ÷ 25,4 × dpi; Audio = Abtastrate × Bittiefe × Kanäle × s ÷ 8; Video = Bild × fps × s; t = Bit ÷ bit/s; dezimale Präfixe (SI) | Beispiele der Lektionen (36 MB, 2.480 × 3.508 Pixel, 400 s) nachgerechnet |
| `stromkosten` | nachhaltigkeit-energie | kWh = kW × h; 8.760 h pro Jahr; P_auf = P_ab ÷ η; PUE = Gesamtleistung ÷ IT-Leistung (ISO/IEC 30134-2) | Strompreise als Annahme in der Aufgabe genannt; Beispiele 1.051,20 € und 42,24 € nachgerechnet |
| `kostenvergleich` | wirtschaftlichkeit | Amortisation = Investition ÷ Rückfluss; Rückfluss = Einsparung − laufende Kosten; Break-even durch Gleichsetzen; Abschreibung = Anschaffung ÷ Nutzungsdauer | Beispiele 24 Monate und 40 TB nachgerechnet |

## Aufgaben Paket 1 (Planwochen bis Anfang Dezember)

63 feste Aufgaben für acht Themen, im PR mit `status: ungeprüft`. Alle Rechenwerte wurden mit
einem eigenen Skript (`Decimal` mit Rundung auf Cent, Netzplan vorwärts/rückwärts, Pseudocode als
Python ausgeführt) nachgerechnet; `ap-tools check` prüft, dass jede Musterlösung als richtig und
keine typische Falschantwort als richtig gilt.

| Datei | Aufgaben | Geprüfte Kernaussagen | Beim Nachrechnen korrigiert |
| --- | ---: | --- | --- |
| `hardware-komponenten.yaml` | 10 | DDR5-5600 = 2.800 MHz, 4800 MT/s × 8 Byte = 38,4 GB/s; PCIe 3.0 ≈ 0,985 GB/s je Lane; P_auf = 250 W ÷ 0,9 = 277,78 W; √(3840² + 2160²) = 4.405,81 → 163,18 ppi; USB-C ohne DP Alt Mode gibt kein Bild aus; AM5 nur DDR5 | Pixeldiagonale zunächst mit 4.405,68 angesetzt, richtig ist 4.405,81 |
| `angebotsvergleich.yaml` | 8 | Bezugskalkulation 1.992,00 → 1.752,96 → 1.717,90 → 1.747,80 €; Docks A 3.463,27 € / B 3.401,00 €; Nutzwerte 7,3 / 7,4 | Fehlerbild „Skonto vom Listenpreis“ bei den Docks zunächst falsch beziffert (richtig 3.454,20 €) |
| `erm-relational.yaml` | 9 | Chen-Notation; 1 : n / n : m; Anomalien; 1NF–3NF (Codd 1970/1972); Importreihenfolge nach Fremdschlüsseln | – |
| `pseudocode.yaml` | 6 | Grenzwerte `< 30`/`< 365`; Feldsumme 890, Anzahl > 200 = 2; `range(1, 5)` endet bei 4 | – |
| `schreibtischtest.yaml` | 6 | Quadratsumme 30, x = 5; NAS-Schleife 4 Monate / 470 / 50; Prüfziffer [9, 2, 6, 5] → 36 → 4; `//`, `%`, `/` in Python | Fehlerbild „Zeilen vertauscht“ zunächst mit 440 statt 490 beziffert |
| `projektplanung.yaml` | 8 | Netzplan A–F: Dauer 14, GP C = 4, FP C = 0; Verzögerungen im Lektionsnetzplan: B + 2 → 17, H + 2 → 15, C + 4 → 16 | – |
| `kalkulation.yaml` | 7 | Switch: 1.440,00 → 1.584,00 → 1.616,33 → 1.701,40 → 2.024,67 €; Stundensatz 84.000 ÷ 1.400 = 60 €/h; Nachkalkulation −120 €, +26,67 % | Toleranz der gerundeten Preisstufen verkleinert, damit „Skonto aufgeschlagen“ (1.615,68 €) als Fehler erkannt wird |
| `osi-protokolle.yaml` | 9 | OSI-Schichten (ISO/IEC 7498-1); ARP Broadcast/Unicast (RFC 826); DORA (RFC 2131); TTL je Router − 1 (RFC 791/1812); Ports laut IANA; DNS-TTL ab Abruf | – |

Alle Korrekturen betrafen neue, noch nicht gemergte Aufgaben; in bestehenden Lektionen wurden
keine Fehler gefunden.

## Aufgaben Paket 2 (Sicherheit, Datenschutz, Vorgehensmodelle, OOP, Englisch, Kundenbedarf)

57 feste Aufgaben für neun Themen, im PR mit `status: ungeprüft`. Rechenwerte per Skript
nachgerechnet, OOP-Code in Python ausgeführt; `ap-tools check` prüft Musterlösungen und Fehlerbilder.

| Datei | Aufgaben | Geprüfte Kernaussagen | Beim Prüfen korrigiert |
| --- | ---: | --- | --- |
| `verschluesselung.yaml` | 9 | Schlüsselanzahl n(n − 1)/2 bzw. 2n (25 Standorte: 300 / 50 / 25 geheim); SHA-256 = 256 Bit = 64 Hex-Zeichen (FIPS 180-4); Signatur privat/öffentlich (RFC 8017); Passwörter mit Salt und langsamem Verfahren (OWASP); Zertifikatsprüfung Name und Gültigkeit (RFC 5280, RFC 9525) | Verweis auf eine BSI-Anforderungsnummer entfernt, die sich nicht sicher belegen ließ; jetzt nur Baustein ORP.4 |
| `schutzziele.yaml` | 5 | Grundwerte V, I, V (BSI 200-2); Zuordnung von Vorfällen und Maßnahmen; Ransomware mit Datenabfluss | – |
| `bsi-schutzbedarf.yaml` | 7 | Kategorien normal/hoch/sehr hoch; sechs Schadensszenarien; Maximumprinzip, Kumulations-, Verteilungseffekt (BSI 200-2, Kap. 8.2) | – |
| `datenschutz.yaml` | 7 | Personenbezug inkl. IP-Adresse (Art. 4 Nr. 1, EuGH C-582/14); Art. 5, 6, 15–21, 33, 83 Abs. 5; 72 h ab Bekanntwerden (Fr 16:00 → Mo 16:00); Bußgeld 4 % vs. 20 Mio. € (höherer Betrag) | **Aufbewahrungsfrist für Rechnungen:** im Entwurf „zehn Jahre“, seit 01.01.2025 gelten für Buchungsbelege **acht Jahre** (§ 147 Abs. 3 AO, Viertes Bürokratieentlastungsgesetz) – korrigiert. Bestehende Lektionen nennen „zehn Jahre“ nur als Kundenanforderung, nicht als Gesetzesfrist; kein Handlungsbedarf |
| `vorgehensmodelle.yaml` | 8 | Scrum Guide 2020: drei Verantwortlichkeiten, fünf Events, Artefakte mit Commitments; Timeboxen 8 h / 15 min / 4 h / 3 h; Wasserfall nach Royce 1970 | – |
| `oop-grundlagen.yaml` | 6 | UML-Sichtbarkeit + − # (UML 2.5.1); Objektzustand (a.status = neu, a.groesse_gb = 40, Dauer 60 s / 160 s, in Python ausgeführt); Kapselung mit Setter-Prüfung | – |
| `englische-texte.yaml` | 6 | Fachwörter und falsche Freunde (Cambridge Dictionary); englisches Angebot 5.000,00 → 4.750,00 → 4.655,00 → 4.700,00 € | – |
| `kundenbedarf.yaml` | 5 | Fragearten, aktives Zuhören, Vier-Seiten-Modell (Schulz von Thun 1981) | – |
| `maerkte-bedarfe.yaml` | 4 | Bedürfnis → Bedarf → Nachfrage; Wettbewerb und Preis | – |

## Aufgaben Paket 3 (Verfügbarkeit, Speicher, Installation, UML, Cloud, Netz, Kommunikation, Präsentation)

62 feste Aufgaben für neun Themen und der Generator `verfuegbarkeit`, im PR mit `status: ungeprüft`.
Rechenwerte per Skript mit `Decimal` nachgerechnet, die Schleife im UML-Aktivitätsdiagramm per
Schreibtischtest verfolgt, alle Mermaid-Diagramme mit der Mermaid-CLI gerendert und angesehen;
`ap-tools check` prüft Musterlösungen und Fehlerbilder.

| Datei | Aufgaben | Geprüfte Kernaussagen | Beim Prüfen korrigiert |
| --- | ---: | --- | --- |
| Generator `verfuegbarkeit` | – | Ausfallzeit = (1 − V) × 8.760 h; Reihe = Produkt; parallel = 1 − Produkt der Ausfallwahrscheinlichkeiten; Lektionswerte 87,6 h / 8,76 h / 52,56 min / 98,505 % / 99,99 % als Test | Prozentwerte zunächst auf zwei Nachkommastellen gerundet – 99,9975 % wurde als „100“ erwartet. Jetzt vier Nachkommastellen; drei redundante Server mit 99,5 % (99,99999 %) ausgeschlossen; Fehlerbild „100“ unterdrückt |
| `verfuegbarkeit-backup.yaml` | 10 | Inkrementell/differenziell (BSI CON.3): 800 GB + 4 × 30 GB = 920 GB bzw. 1.100 GB, Restore 5 bzw. 2 Sicherungen; 3-2-1-Regel; Generationenprinzip; Spiegelung ≠ Backup; USV-Klassen VFD/VI/VFI (IEC 62040-3); Router 99,5 % × Firewall-Paar 99,99 % = 99,49005 % | Gesamtverfügbarkeit im Entwurf mit 99,495 % angegeben, richtig 99,4901 %; Fehlerbild „alle in Reihe“ mit 98,5049 % statt 97,52 % beziffert |
| `speicher-hdd-ssd.yaml` | 6 | 5.400 U/min → 90/s → 11,11 ms → 5,56 ms mittlere Rotationswartezeit; 1.200 TBW ÷ 400 GB/Tag = 3.000 Tage = 8,22 Jahre (TBW dezimal); Secure Erase/Kryptolöschung/Zerstörung (BSI) | Link auf die NVMe-Spezifikationsseite nicht prüfbar – nur noch als Titel belegt |
| `bios-uefi-dateisysteme.yaml` | 6 | 2³² × 512 Byte = 2.199.023.255.552 Byte = 2 TiB, auf 4 TB bleiben 1,80 TB ungenutzt (Microsoft GPT-FAQ); FAT32 max. 4 GiB − 1 Byte; exFAT für Wechseldatenträger; NTFS unter macOS ab Werk nur lesbar; VT-x/AMD-V für KVM (RHEL 9 Doku) | Wörtliche KVM-Fehlermeldung im Entwurf nicht sicher belegbar – durch neutrale Beschreibung (`virt-host-validate`) ersetzt |
| `installation-einrichtung.yaml` | 7 | Ports SSH 22, RDP 3389, VNC 5900 (IANA); statische Konfiguration: Adresse mit Präfix, Gateway, DNS; DHCP für Clients (RFC 2131); RDP nicht ins Internet (BSI OPS.1.2.5) | – |
| `uml.yaml` | 9 | include = immer, extend = optional; Multiplizitäten 1, 0..*, 1..*; Aggregation ◇ / Komposition ◆; Gabelung/Vereinigung vs. Verzweigung/Zusammenführung (UML 2.5.1, Kap. 11, 15, 18); Schleife: immer Fehlschlag → 3 Versuche, Erfolg im 2. → 2 | – |
| `cloud-modelle.yaml` | 6 | IaaS/PaaS/SaaS/DaaS und Public/Private/Hybrid/Community (NIST SP 800-145); Kunde bleibt Verantwortlicher, Anbieter Auftragsverarbeiter (Art. 28 DSGVO); DaaS für befristeten Bedarf | – |
| `netzwerkkomponenten.yaml` | 6 | Schichten Repeater 1, Switch 2, Accesspoint 2, Router 3; VLANs (IEEE 802.1Q); PoE: 8 × 30 W + 16 × 15,4 W = 486,4 W > 370 W, es fehlen 116,4 W (IEEE 802.3af/at) | – |
| `kommunikationssysteme.yaml` | 6 | Upload als Engpass: 12 × 3 Mbit/s = 36 > 20 Mbit/s, höchstens ⌊20 ÷ 3⌋ = 6 Personen; Aufzeichnung nur mit Einwilligung (Art. 6 DSGVO); Social-Media-Risiken | – |
| `praesentation.yaml` | 6 | Anteile 10 % / 75 % / 15 % von 20 min = 2 / 15 / 3 min; Folienregeln; Medienwahl; Bildrechte (UrhG) | – |

Hinweis zur PoE-Aufgabe: Geplant wird mit der Höchstleistung je Port (15,4 W bzw. 30 W). Echte
Geräte ziehen oft weniger; für die Budgetplanung ist der Höchstwert die sichere Annahme.

Alle Korrekturen betrafen neue, noch nicht gemergte Aufgaben; in bestehenden Lektionen wurden
keine Fehler gefunden.

## Aufgaben Paket 4 (Anforderungen, Skripte, Domäne, Netz, Sicherheit, Recht, Ergonomie, Suche)

78 feste Aufgaben für 13 Themen (Planpositionen 30–44), im PR mit `status: ungeprüft`. Rechenwerte
per Skript nachgerechnet, das Bash-Skript und die fehlerhafte Zuweisung in Bash ausgeführt;
`ap-tools check` prüft Musterlösungen und Fehlerbilder.

| Datei | Aufgaben | Geprüfte Kernaussagen | Beim Prüfen korrigiert |
| --- | ---: | --- | --- |
| `lasten-pflichtenheft.yaml` | 6 | Lastenheft = Auftraggeber (was, wofür), Pflichtenheft = Auftragnehmer (wie, womit), Abnahme gegen das freigegebene Pflichtenheft (DIN 69901-5); funktional/nicht-funktional (ISO/IEC 25010) | Kernbegriffe der Freitextaufgabe zunächst „1“, „2“, „3“ – hätten jede Antwort getroffen; ersetzt |
| `skriptsprachen.yaml` | 6 | Shebang, Zuweisung ohne Leerzeichen, `$( )`, `[ -f ]`, Exit-Code 0 = Erfolg (Bash-Handbuch); Skript mit 2 fehlenden Dateien → exit 2 (in Bash ausgeführt); `0 3 * * 1-5` = werktags 3:00 (crontab(5)) | – |
| `client-server-domaene.yaml` | 6 | DNS muss auf den Domänencontroller zeigen (SRV-Einträge, Microsoft); Beitritt mit berechtigtem Konto und Neustart; Kerberos-Zeittoleranz standardmäßig 5 Minuten | – |
| `netzwerk-standards.yaml` | 7 | Wi-Fi 4/5/6/7 = 802.11n/ac/ax/be; 10GBASE-T über 80 m braucht Cat 6A (Cat 6 bis ca. 55 m); 3 TB × 8 ÷ 1 Gbit/s = 24.000 s = 6,67 h, bei 10 Gbit/s 40 min; Singlemode für 1,5 km (10GBASE-LR bis 10 km) | – |
| `authentifizierung.yaml` | 6 | Faktoren Wissen/Besitz/Inhärenz; FIDO2 > TOTP > SMS (NIST SP 800-63B Rev. 4); 94⁸ = 6.095.689.385.410.816 (≈ 7,06 Tage bei 10¹⁰/s), 26¹⁵ ≈ 1,68 · 10²¹ (≈ 5.319 Jahre) | Toleranz für die Zehnerpotenz-Angaben von 1 % auf 2 % erhöht – die im Hinweis vorgeschlagene Rundung 1,7 · 10²¹ wäre sonst als falsch gewertet worden |
| `haertung-firewall.yaml` | 6 | Härtung = Angriffsfläche verkleinern (BSI SYS.1.1, SYS.1.3); Personal Firewall kennt Programme; erste passende Regel gilt; SSH statt Telnet | – |
| `isms-risiko.yaml` | 6 | PDCA (BSI 200-1); Risiko = Wahrscheinlichkeit × Schaden, Werte 6 / 9 / 4; vermeiden, vermindern, übertragen, akzeptieren (BSI 200-3) | – |
| `tom.yaml` | 6 | Zutritt/Zugang/Zugriff und weitere Kontrollen (BDSG a. F., Anlage zu § 9); Art. 32 DSGVO; DSB-Interessenkonflikt (Art. 38 Abs. 6), Fachkunde (Art. 37 Abs. 5) | – |
| `barrierefreiheit.yaml` | 6 | WCAG 2.2: vier Prinzipien, 1.3.1, 1.4.1, 1.4.3, 3.3.2; `<label for>`; BFSG seit 28.06.2025, BITV 2.0 für öffentliche Stellen | – |
| `kauf-miete-leasing.yaml` | 5 | 6.000 × 0,026 × 48 = 7.488 €; 180 × 48 = 8.640 €; Miete ab dem 34. Monat teurer als Kauf (33 × 180 = 5.940 €, 34 × 180 = 6.120 €) | – |
| `masken-ergonomie.yaml` | 6 | Sieben Prinzipien der ISO 9241-110:2020 (Erlernbarkeit statt Lernförderlichkeit, neu Benutzerbindung, Individualisierbarkeit entfallen) | – |
| `vertraege.yaml` | 6 | Kauf/Werk/Dienst/Miete (§§ 433, 631, 611, 535); Falschlieferung = Mangel (§ 434 Abs. 5); Vorrang der Nacherfüllung (§ 439); Vertragsstrafe 5 % von 24.000 € = 1.200 €, 7 × 250 € gedeckelt; § 377 HGB | – |
| `suchoperatoren.yaml` | 6 | Operatoren laut Google-Hilfe; boolesche Abfragen über fünf Tickets: 2 / 3 / 2 Treffer | Lückentext zunächst mit Code-Formatierung um die Lücken – hätte die Eingabefelder zerschnitten; als normaler Text gesetzt |

Alle Korrekturen betrafen neue, noch nicht gemergte Aufgaben; in bestehenden Lektionen wurden
keine Fehler gefunden.
