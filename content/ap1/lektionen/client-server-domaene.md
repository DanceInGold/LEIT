---
id: client-server-domaene
titel: "Client-Server und Domäne: einen Rechner ins Active Directory aufnehmen"
themen: [client-server-domaene]
reihenfolge: 1
voraussetzungen: []
dauer_min: 30
quelle: "Neu erstellt (Claude). Active Directory nach Microsoft-Dokumentation; Linux-Domänenbeitritt mit realmd/SSSD nach Red-Hat-Dokumentation; Beispielnamen fiktiv (.example nach RFC 2606)."
belege:
  - {titel: "Prüfungskatalog AP1 2025, Unterpunkt 03.02: Einbindung eines Clients in eine Domäne (laut Änderungsliste IT-Berufe-Podcast #190)", url: "https://it-berufe-podcast.de/neuer-pruefungskatalog-fuer-die-ap1-der-it-berufe-ab-2025-it-berufe-podcast-190/"}
  - {titel: "Microsoft Learn: Active Directory Domain Services Overview", url: "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview"}
  - {titel: "Red Hat Enterprise Linux 9: Integrating RHEL systems directly with Windows Active Directory (realm join)", url: "https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/integrating_rhel_systems_directly_with_windows_active_directory/index"}
status: geprüft
---

## Worum geht es?

In kleinen Netzen hat jeder Rechner eigene Benutzerkonten. Ab einer gewissen Größe ist das nicht mehr
zu verwalten. Eine **[Domäne](glossar:domaene)** verwaltet Benutzer, Rechner und Regeln **zentral** –
in Windows-Umgebungen mit **Active Directory (AD)**.

- Client-Server gegenüber Peer-to-Peer
- Was eine Domäne bietet
- Schritte, um einen Client in die Domäne aufzunehmen

## Wie funktioniert es?

### Client-Server oder Peer-to-Peer?

| | Client-Server | Peer-to-Peer (Arbeitsgruppe) |
| --- | --- | --- |
| Rollen | Server stellt Dienste bereit, Clients nutzen sie | alle gleichberechtigt |
| Verwaltung | zentral | an jedem Rechner einzeln |
| Größe | beliebig | wenige Rechner |
| Beispiel | Domäne, Dateiserver, Mailserver | Heimnetz, kleines Büro |

### Was eine Domäne bietet

```mermaid
flowchart LR
  DC["Domänencontroller<br/>Active Directory"] --> B["Benutzer<br/>und Gruppen"]
  DC --> R["Computer-<br/>konten"]
  DC --> G["Gruppenrichtlinien<br/>(GPO)"]
  C1["Client 1"] --> DC
  C2["Client 2"] --> DC
  S["Dateiserver"] --> DC
```

- **Single Sign-on:** einmal anmelden, überall in der Domäne arbeiten
- **zentrale Konten:** Ein gesperrtes Konto ist sofort überall gesperrt
- **Gruppenrichtlinien:** Einstellungen wie Passwortregeln oder Laufwerke zentral verteilen
- **Rechte über Gruppen:** Abteilung „Buchhaltung“ bekommt Zugriff auf ihren Ordner

### Einen Windows-Client aufnehmen

| Schritt | Was | Warum |
| --- | --- | --- |
| 1 | IP-Konfiguration prüfen, **DNS-Server = Domänencontroller** | Der Client findet die Domäne über DNS |
| 2 | eindeutigen **Computernamen** vergeben | wird zum Computerkonto im AD |
| 3 | Systemeinstellungen → Domäne `archivtech.example` eintragen | Beitritt starten |
| 4 | Anmeldedaten eines Kontos **mit Beitrittsrecht** eingeben | nicht jeder darf Rechner aufnehmen |
| 5 | **Neustart** | Richtlinien werden angewendet |
| 6 | mit Domänenkonto anmelden und testen | Laufwerke, Richtlinien, Zugriff |

Auch Linux-Server können beitreten, auf RHEL etwa mit `realm join archivtech.example`.

> **Halten wir kurz fest:**
>
> 1. Domäne = zentrale Verwaltung von Benutzern, Rechnern und Richtlinien (Active Directory).
> 2. Vor dem Beitritt: DNS muss auf den Domänencontroller zeigen.
> 3. Beitritt braucht ein berechtigtes Konto und einen Neustart.

## Warum ist es so?

Zentrale Verwaltung heißt: eine Änderung, sofort überall wirksam. Wer das Unternehmen verlässt, wird an
einer Stelle gesperrt statt an 50 Rechnern.

<details>
<summary>Warum ist DNS beim Beitritt so wichtig?</summary>

Der Client sucht den Domänencontroller über spezielle DNS-Einträge (SRV-Records). Zeigt sein DNS auf
den Router oder einen öffentlichen DNS-Server, kennt dieser die interne Domäne nicht – der Beitritt
scheitert mit „Domäne nicht gefunden“. Das ist der häufigste Fehler.

</details>

## Praxisbezug im Betrieb

- **Neue Mitarbeitende:** Konto im AD anlegen, in Gruppen aufnehmen – Rechte und Laufwerke kommen
  automatisch.
- **Linux und AD:** Server melden Benutzer über SSSD am AD an, Gruppen steuern sudo-Rechte.
- **Uhrzeit:** Weicht die Uhr des Clients zu stark ab, schlägt die Anmeldung (Kerberos) fehl.

## Typische Prüfungsfalle

- **DNS auf den Router gestellt:** Domäne wird nicht gefunden.
- **Kein Neustart:** Richtlinien greifen erst danach.
- **Arbeitsgruppe und Domäne verwechselt:** Arbeitsgruppe = dezentral, Domäne = zentral.
- **Lokales Admin-Konto genügt:** Für den Beitritt braucht es ein Domänenkonto mit Beitrittsrecht.

## Nicht verwechseln

| Begriff | Bedeutung |
| --- | --- |
| Domäne | zentral verwalteter Verbund von Benutzern und Rechnern |
| Domänencontroller | Server, der das Active Directory bereitstellt |
| Arbeitsgruppe | Peer-to-Peer, jeder Rechner verwaltet sich selbst |
| Gruppenrichtlinie (GPO) | zentral verteilte Einstellungen |
| Single Sign-on | einmal anmelden, viele Dienste nutzen |

## Merksatz

**Einmal zentral statt fünfzigmal einzeln: DNS auf den Domänencontroller, berechtigtes Konto,
Neustart – und schon gelten Konten und Richtlinien der Domäne.**
