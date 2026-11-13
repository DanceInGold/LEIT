"""Generator „IPv4-Subnetting“: Maske, Netzadresse, Broadcast, Hosts und Subnetze bilden (AU-03).

Stufen: 1 Präfix → Subnetzmaske, 2 Netz und Broadcast einer Adresse (Grenze im 4. Oktett),
3 dazu Host-Bereich und Hostanzahl (Grenze auch im 3. Oktett), 4 ein Netz nach Subnetz- oder
Hostanzahl aufteilen (Handlungssituation). Gerechnet wird mit Bitoperationen auf 32-Bit-Zahlen
wie in der Lektion „Subnetze bilden“; die Tests prüfen gegen Pythons Modul ``ipaddress``.
"""

from __future__ import annotations

import random

from ap_trainer.content.aufgaben import Aufgabe, Fehlerbild, Rechenschritt, Rechnung, Stufe
from ap_trainer.content.models import Beleg
from ap_trainer.tasks.generators import Generator, register

ALL_ONES = 0xFFFFFFFF

# Jede Stufe liefert: Schritte, Titel, Frage, Situation, Hinweise
type _Parts = tuple[list[Rechenschritt], str, str, str | None, list[str]]


def ip_str(value: int) -> str:
    """32-Bit-Zahl als Adresse in Punktschreibweise."""
    return ".".join(str((value >> shift) & 255) for shift in (24, 16, 8, 0))


def mask(prefix: int) -> int:
    """Subnetzmaske zu einem Präfix: ``prefix`` Einsen von links."""
    return (ALL_ONES << (32 - prefix)) & ALL_ONES


def boundary_octet(prefix: int) -> int:
    """Index (0–3) des Oktetts, in dem das letzte Netzbit liegt (Grenz-Oktett)."""
    return (prefix - 1) // 8


def octet(value: int, index: int) -> int:
    """Oktett ``index`` (0 = ganz links) einer Adresse."""
    return (value >> (24 - 8 * index)) & 255


def step_width(prefix: int) -> int:
    """Schrittweite: 256 minus Maskenwert im Grenz-Oktett."""
    return 256 - octet(mask(prefix), boundary_octet(prefix))


def usable_hosts(prefix: int) -> int:
    """Nutzbare Hosts: 2 hoch Hostbits minus Netz- und Broadcastadresse."""
    return (1 << (32 - prefix)) - 2


def _ip_step(
    frage: str, value: int, erklaerung: str, falsch: list[Fehlerbild] | None = None
) -> Rechenschritt:
    wrong = [f for f in (falsch or []) if f.antwort != ip_str(value)]
    return Rechenschritt(
        frage=frage, antwort=ip_str(value), format="ipv4", erklaerung=erklaerung, falsch=wrong
    )


def _num_step(
    frage: str, value: int, erklaerung: str, falsch: list[Fehlerbild] | None = None
) -> Rechenschritt:
    wrong = [f for f in (falsch or []) if f.antwort != str(value)]
    unique = list({f.antwort: f for f in wrong}.values())
    return Rechenschritt(frage=frage, antwort=str(value), format="zahl", erklaerung=erklaerung, falsch=unique)


def _mask_step(prefix: int) -> Rechenschritt:
    value = mask(prefix)
    swapped = Fehlerbild(
        antwort=ip_str(mask(32 - prefix)),
        warum="Das ist die Maske für die Hostbits. Das Präfix zählt die Einsen, also die Netzbits.",
        ursache="begriff",
    )
    falsch = [swapped] if 0 < 32 - prefix < 32 else []
    ones = f"{prefix} Einsen von links, dann {32 - prefix} Nullen"
    return _ip_step("Subnetzmaske", value, f"/{prefix} = {ones} → {ip_str(value)}.", falsch)


def _step_width_step(prefix: int) -> Rechenschritt:
    index = boundary_octet(prefix)
    mask_value = octet(mask(prefix), index)
    text = (
        f"Grenz-Oktett ist das {index + 1}. Oktett, Maskenwert {mask_value}: "
        f"256 − {mask_value} = {step_width(prefix)}."
    )
    return _num_step("Schrittweite im Grenz-Oktett", step_width(prefix), text)


def _network_step(address: int, prefix: int) -> Rechenschritt:
    network = address & mask(prefix)
    index = boundary_octet(prefix)
    width = step_width(prefix)
    value = octet(address, index)
    text = (
        f"Im {index + 1}. Oktett liegt {value} im Block ab {octet(network, index)} "
        f"(Vielfaches von {width}); dahinter nur Nullen → {ip_str(network)}."
    )
    return _ip_step("Netzadresse", network, text)


def _broadcast_step(address: int, prefix: int) -> Rechenschritt:
    network = address & mask(prefix)
    broadcast = network | (~mask(prefix) & ALL_ONES)
    falsch = [
        Fehlerbild(
            antwort=ip_str((broadcast + 1) & ALL_ONES),
            warum="Das ist schon die Netzadresse des nächsten Subnetzes. Der Broadcast liegt eins davor.",
            ursache="rechenfehler",
        )
    ]
    if boundary_octet(prefix) < 3:
        # Falle aus der Lektion: „.255 ist immer der Broadcast“
        falsch.append(
            Fehlerbild(
                antwort=ip_str(network | 255),
                warum="Bei dieser Maske liegt die Grenze nicht im 4. Oktett; eine Adresse auf .255 kann ein "
                "normaler Host sein. Der Broadcast ist die letzte Adresse des ganzen Subnetzes.",
                ursache="konzept",
            )
        )
    text = f"Alle Hostbits auf 1, also nächste Netzadresse minus 1 → {ip_str(broadcast)}."
    return _ip_step("Broadcastadresse", broadcast, text, falsch)


def _host_range_steps(address: int, prefix: int) -> list[Rechenschritt]:
    network = address & mask(prefix)
    broadcast = network | (~mask(prefix) & ALL_ONES)
    hostbits = 32 - prefix
    hosts_wrong = [
        Fehlerbild(
            antwort=str(2**hostbits),
            warum="Netz- und Broadcastadresse sind nicht als Host nutzbar – es fehlt das „− 2“.",
            ursache="konzept",
        ),
        Fehlerbild(
            antwort=str(2**hostbits - 1),
            warum="Abzuziehen sind zwei Adressen: Netzadresse und Broadcast.",
            ursache="rechenfehler",
        ),
    ]
    return [
        _ip_step("Erster Host", network + 1, f"Netzadresse + 1 → {ip_str(network + 1)}."),
        _ip_step("Letzter Host", broadcast - 1, f"Broadcast − 1 → {ip_str(broadcast - 1)}."),
        _num_step(
            "Nutzbare Hosts",
            usable_hosts(prefix),
            f"{hostbits} Hostbits: 2^{hostbits} − 2 = {usable_hosts(prefix)}.",
            hosts_wrong,
        ),
    ]


def _random_address(rng: random.Random, prefix: int) -> int:
    """Private Adresse, die nicht zufällig die Netz- oder Broadcastadresse ist."""
    base = rng.choice([(10 << 24), (172 << 24) | (16 << 16), (192 << 24) | (168 << 16)])
    while True:
        address = base | rng.randint(0, 2**16 - 1)
        host_part = address & ~mask(prefix) & ALL_ONES
        if 0 < host_part < 2 ** (32 - prefix) - 1:
            return address


BELEGE = (
    Beleg(
        titel="RFC 950: Internet Standard Subnetting Procedure", url="https://www.rfc-editor.org/rfc/rfc950"
    ),
    Beleg(
        titel="RFC 4632: Classless Inter-domain Routing (CIDR)", url="https://www.rfc-editor.org/rfc/rfc4632"
    ),
    Beleg(
        titel="RFC 1918: Address Allocation for Private Internets",
        url="https://www.rfc-editor.org/rfc/rfc1918",
    ),
)


@register
class Ipv4Subnetting(Generator):
    """Subnetzmaske, Netz, Broadcast, Host-Bereich und Subnetzbildung in vier Stufen."""

    id = "ipv4-subnetting"
    titel = "IPv4-Subnetting"
    stufen = (1, 2, 3, 4)
    status = "geprüft"
    quelle = "Generator „ipv4-subnetting“; jede Variante gegen Pythons Modul ipaddress getestet."
    belege = BELEGE

    def generate(self, rng: random.Random, stufe: Stufe, task_id: str, thema: str) -> Aufgabe:
        """Erzeugt eine Subnetting-Aufgabe der gewünschten Stufe."""
        builders = {1: self._mask, 2: self._network, 3: self._full, 4: self._split}
        steps, title, question, situation, hints = builders[stufe](rng)
        return Rechnung(
            typ="rechnung",
            id=task_id,
            thema=thema,
            stufe=stufe,
            titel=title,
            situation=situation,
            frage=question,
            hinweise=hints,
            loesungsweg="\n".join(f"{i + 1}. **{s.frage}:** {s.erklaerung}" for i, s in enumerate(steps)),
            schritte=steps,
            quelle=self.quelle,
            belege=list(self.belege),
            status=self.status,
        )

    def _mask(self, rng: random.Random) -> _Parts:
        prefix = rng.randint(9, 30)
        question = f"Wie lautet die Subnetzmaske zum Präfix **/{prefix}** in Punktschreibweise?"
        hints = [
            "Das Präfix gibt an, wie viele Bits von links zum Netzanteil gehören.",
            "Ein volles Oktett mit 8 Einsen ist 255; Teil-Oktette: 128, 192, 224, 240, 248, 252, 254.",
            f"{prefix // 8} volle Oktette mit 255, danach {prefix % 8} Einsen im nächsten Oktett."
            if prefix % 8
            else f"{prefix // 8} volle Oktette mit 255, danach nur noch Nullen.",
        ]
        return [_mask_step(prefix)], "Präfix → Subnetzmaske", question, None, hints

    def _network(self, rng: random.Random) -> _Parts:
        prefix = rng.randint(25, 30)
        address = _random_address(rng, prefix)
        question = (
            f"Ein Rechner hat die Adresse **{ip_str(address)}/{prefix}**. Bestimme Schritt für Schritt:"
        )
        steps = [_step_width_step(prefix), _network_step(address, prefix), _broadcast_step(address, prefix)]
        hints = [
            "Netzadresse: alle Hostbits 0. Broadcast: alle Hostbits 1.",
            "Schrittweite = 256 − Maskenwert im Grenz-Oktett; Netze beginnen bei Vielfachen davon.",
            f"Die Maske im 4. Oktett ist {octet(mask(prefix), 3)}.",
        ]
        return steps, "Netz- und Broadcastadresse", question, None, hints

    def _full(self, rng: random.Random) -> _Parts:
        prefix = rng.choice([p for p in range(17, 31) if p % 8 != 0])
        address = _random_address(rng, prefix)
        question = f"Gegeben ist **{ip_str(address)}/{prefix}**. Bestimme Schritt für Schritt:"
        steps = [
            _mask_step(prefix),
            _step_width_step(prefix),
            _network_step(address, prefix),
            _broadcast_step(address, prefix),
            *_host_range_steps(address, prefix),
        ]
        hints = [
            "Erst die Maske, dann das Grenz-Oktett finden – dort passiert alles Interessante.",
            "Schrittweite = 256 − Maskenwert; Broadcast = nächste Netzadresse − 1; Hosts = 2^h − 2.",
            f"Das Grenz-Oktett ist das {boundary_octet(prefix) + 1}. Oktett.",
        ]
        return steps, "Subnetz komplett bestimmen", question, None, hints

    def _split(self, rng: random.Random) -> _Parts:
        base_prefix = rng.randint(16, 24)
        new_prefix = rng.randint(base_prefix + 1, min(base_prefix + 6, 30))
        borrowed = new_prefix - base_prefix
        base = _random_address(rng, base_prefix) & mask(base_prefix)
        count = 2**borrowed
        by_hosts = rng.random() < 0.5
        number = rng.randint(2, count)
        target = base + (number - 1) * 2 ** (32 - new_prefix)
        if by_hosts:
            hosts = rng.randint(usable_hosts(new_prefix + 1) + 1, usable_hosts(new_prefix))
            need = f"Subnetze mit jeweils mindestens **{hosts} Hosts**"
            first = self._hostbits_step(hosts, new_prefix)
            count_step = _num_step(
                "Anzahl Subnetze",
                count,
                f"Geliehene Bits: {new_prefix} − {base_prefix} = {borrowed}; 2^{borrowed} = {count}.",
            )
        else:
            wanted = rng.randint(2 ** (borrowed - 1) + 1, count)
            need = f"mindestens **{wanted} gleich große Subnetze**"
            first = _num_step(
                "Geliehene Bits",
                borrowed,
                f"Kleinstes n mit 2^n ≥ {wanted}: 2^{borrowed} = {count}.",
                [
                    Fehlerbild(
                        antwort=str(borrowed + 1),
                        warum="Eins zu viel: schon 2^n ≥ Anzahl reicht.",
                        ursache="rechenfehler",
                    )
                ],
            )
            count_step = _num_step(
                "Nutzbare Hosts je Subnetz",
                usable_hosts(new_prefix),
                f"{32 - new_prefix} Hostbits: 2^{32 - new_prefix} − 2 = {usable_hosts(new_prefix)}.",
            )
        situation = (
            f"Die ArchivTech GmbH hat für ihren neuen Standort das Netz **{ip_str(base)}/{base_prefix}** "
            f"bekommen. Die Netzwerkabteilung braucht {need}."
        )
        question = f"Teile das Netz auf und bestimme die Werte für das **{number}. Subnetz**:"
        steps = [
            first,
            _num_step("Neues Präfix (Zahl hinter /)", new_prefix, f"Neues Präfix: /{new_prefix}."),
            _mask_step(new_prefix),
            _step_width_step(new_prefix),
            count_step,
            _ip_step(
                f"Netzadresse des {number}. Subnetzes",
                target,
                f"Ausgangsnetz + ({number} − 1) × {2 ** (32 - new_prefix)} Adressen je Subnetz "
                f"→ {ip_str(target)}.",
            ),
            _broadcast_step(target, new_prefix),
        ]
        hints = [
            "Subnetze gegeben → 2^n ≥ Anzahl. Hosts gegeben → 2^h − 2 ≥ Anzahl.",
            "Schrittweite = 256 − Maskenwert im Grenz-Oktett; das n-te Netz beginnt (n − 1) Schritte weiter.",
            f"Das Ausgangsnetz hat {32 - base_prefix} Hostbits, von denen du Bits leihst.",
        ]
        return steps, "Netz in Subnetze aufteilen", question, situation, hints

    @staticmethod
    def _hostbits_step(hosts: int, new_prefix: int) -> Rechenschritt:
        hostbits = 32 - new_prefix
        # Typischer Fehler: 2^h ≥ Hosts ohne „− 2“ gerechnet
        without_minus_two = max((hosts - 1).bit_length(), 1)
        falsch = [
            Fehlerbild(
                antwort=str(without_minus_two),
                warum="Ohne „− 2“ gerechnet: Netz- und Broadcastadresse brauchen auch Platz, "
                "also 2^h − 2 ≥ Hosts.",
                ursache="konzept",
            )
        ]
        return _num_step(
            "Hostbits",
            hostbits,
            f"Kleinstes h mit 2^h − 2 ≥ {hosts}: 2^{hostbits} − 2 = {usable_hosts(new_prefix)}.",
            falsch,
        )
