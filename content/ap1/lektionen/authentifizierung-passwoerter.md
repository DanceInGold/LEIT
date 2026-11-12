---
id: authentifizierung-passwoerter
titel: "Authentifizierung, 2FA und Passwort-Policy bewerten"
themen: [authentifizierung]
reihenfolge: 1
voraussetzungen: []
dauer_min: 30
quelle: "Neu erstellt (Claude). Faktoren und Passwortregeln nach NIST SP 800-63B Revision 4 (August 2025) und BSI IT-Grundschutz (Baustein ORP.4); Beispiel-Policy fiktiv."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 06.04: Authentifizierung (z. B. Zweifaktor) kennen, Passwort-Policy bewerten (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "NIST SP 800-63B Revision 4: Digital Identity Guidelines – Authentication and Authenticator Management", url: "https://pages.nist.gov/800-63-4/sp800-63b.html"}
  - {titel: "Enzoic: Zusammenfassung NIST SP 800-63B Rev. 4 (15 Zeichen ohne zweiten Faktor, keine Kompositionsregeln, kein regelmäßiger Wechsel, Sperrliste)", url: "https://www.enzoic.com/blog/nist-sp-800-63b-rev4/"}
  - {titel: "BSI IT-Grundschutz-Kompendium, Baustein ORP.4 Identitäts- und Berechtigungsmanagement"}
status: ungeprüft
---

## Worum geht es?

Bevor jemand an Daten kommt, muss das System wissen: **Wer bist du – und stimmt das?** Das ist die
**[Authentifizierung](glossar:authentifizierung)**.

- Drei Begriffe, die oft verwechselt werden: Identifikation, Authentifizierung, Autorisierung
- Drei Faktoren und die **Zwei-Faktor-Authentifizierung (2FA)**
- Eine **Passwort-Policy bewerten** – genau so fragt der Katalog

## Wie funktioniert es?

### Drei Schritte beim Anmelden

| Schritt | Frage | Beispiel |
| --- | --- | --- |
| Identifikation | **Wer** behauptest du zu sein? | Benutzername `t.azubi` |
| Authentifizierung | **Beweise** es! | Passwort + Code aus der App |
| Autorisierung | Was **darfst** du? | Leserecht auf das Archiv, kein Schreibrecht |

### Drei Faktoren

| Faktor | Beispiel |
| --- | --- |
| **Wissen** | Passwort, PIN |
| **Besitz** | Smartphone mit Authenticator-App, Hardware-Schlüssel (FIDO2), Chipkarte |
| **Inhärenz** (Sein) | Fingerabdruck, Gesichtserkennung |

**2FA** heißt: **zwei verschiedene** Faktoren. Passwort + PIN sind zweimal Wissen – das ist keine 2FA.

### Wie stark ist welche 2FA?

| Verfahren | Bewertung |
| --- | --- |
| Hardware-Schlüssel / Passkey (FIDO2) | sehr stark, phishing-resistent |
| Authenticator-App (TOTP, 6-stelliger Code) | gut |
| SMS-Code | besser als nichts, aber abfangbar (SIM-Tausch) |

### Was eine gute Passwort-Policy ausmacht

Aktuelle Empfehlungen (NIST SP 800-63B Rev. 4, ähnlich BSI) sind anders als die alten Regeln:

| Regel | aktuell empfohlen |
| --- | --- |
| Länge | **lang**: mindestens 15 Zeichen, wenn das Passwort allein schützt; lange Passphrasen erlauben |
| Komplexität | **keine** Pflicht zu Sonderzeichen-Mix |
| Wechsel | **nur bei Verdacht** auf Kompromittierung, nicht alle 90 Tage |
| Sperrliste | neue Passwörter gegen Listen bekannter oder geleakter Passwörter prüfen |
| Hilfsmittel | Passwortmanager und Einfügen erlauben |
| zusätzlich | 2FA für wichtige Konten |

### Rechenbeispiel: eine Policy bewerten

Die Policy der ArchivTech lautet: „mindestens 8 Zeichen, Groß- und Kleinbuchstaben, Ziffer,
Sonderzeichen; Wechsel alle 30 Tage; keine 2FA.“

| Punkt | Bewertung | Verbesserung |
| --- | --- | --- |
| 8 Zeichen | zu kurz | mindestens 15 Zeichen oder 2FA |
| Zeichenmix-Pflicht | führt zu Mustern wie `Sommer2026!` | stattdessen Länge und Sperrliste |
| Wechsel alle 30 Tage | führt zu `Sommer2026!` → `Herbst2026!` | Wechsel nur bei Verdacht |
| keine 2FA | ein gestohlenes Passwort reicht | 2FA für alle Fernzugänge |

> **Halten wir kurz fest:**
>
> 1. Identifikation = wer, Authentifizierung = Beweis, Autorisierung = Rechte.
> 2. 2FA = zwei **verschiedene** Faktoren aus Wissen, Besitz, Inhärenz.
> 3. Gute Policy: lang statt kompliziert, Wechsel nur bei Verdacht, Sperrliste, 2FA.

## Warum ist es so?

Länge schlägt Komplexität: Jedes zusätzliche Zeichen vervielfacht die Zahl der Möglichkeiten.
Erzwungene Komplexität und häufige Wechsel führen dagegen zu vorhersehbaren Mustern.

<details>
<summary>Warum ist häufiges Wechseln schädlich?</summary>

Wer alle 30 Tage ein neues Passwort braucht, zählt hoch oder hängt das Datum an. Angreifer kennen
diese Muster. Außerdem schreiben Menschen Passwörter dann eher auf. Studien und die neuen
Richtlinien empfehlen deshalb: wechseln, wenn es einen Grund gibt – dann aber sofort.

</details>

<details>
<summary>Warum ist ein Hardware-Schlüssel phishing-resistent?</summary>

Der Schlüssel prüft selbst, auf welcher Domain du dich anmeldest. Auf einer gefälschten Seite
verweigert er die Anmeldung. Einen Code aus einer App oder SMS kann man dagegen auf jeder
gefälschten Seite eintippen.

</details>

## Praxisbezug im Betrieb

- **SSH-Schlüssel statt Passwort** auf RHEL-Servern, Passwort-Login abschalten.
- **Konten mit Admin-Rechten** immer mit 2FA, ebenso VPN und Cloud-Zugänge.
- **Passwortmanager** für Teamzugänge statt Excel-Liste.

## Typische Prüfungsfalle

- **Passwort + Sicherheitsfrage als 2FA:** zweimal Wissen.
- **Authentifizierung und Autorisierung vertauscht:** erst beweisen, dann Rechte.
- **Alte Regeln als „sicher“ bewertet:** 90-Tage-Wechsel und Zeichenmix-Pflicht gelten heute als
  überholt.
- **Nur kritisieren:** Zu jeder Schwäche gehört eine Verbesserung.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Identifikation | Identität behaupten (Benutzername) |
| Authentifizierung | Identität nachweisen (Passwort, Token) |
| Autorisierung | Rechte zuteilen |
| 2FA | zwei Faktoren aus verschiedenen Kategorien |
| MFA | mindestens zwei Faktoren |
| Passkey | Anmeldung per Schlüsselpaar auf dem Gerät, ohne Passwort |

## Merksatz

**Wer bist du, beweis es, was darfst du. Zwei Faktoren müssen verschieden sein – und ein gutes Passwort
ist lang, nicht kompliziert.**
