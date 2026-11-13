"""Generator „IPv6“: kürzen, ausschreiben, /64-Subnetze bilden, Interface-ID nach EUI-64 (AU-03).

Stufen: 1 Adresse kürzen (RFC 5952), 2 gekürzte Adresse ausschreiben, 3 Subnetze aus einem
Provider-Präfix (/48 bis /60), 4 Handlungssituation SLAAC mit EUI-64 aus einer MAC-Adresse.
Kürzen, Ausschreiben und EUI-64 sind hier von Hand programmiert; die Tests prüfen gegen Pythons
Modul ``ipaddress`` und eine eigene Bitrechnung.
"""

from __future__ import annotations

import random

from ap_trainer.content.aufgaben import Aufgabe, Fehlerbild, Rechenschritt, Rechnung, Stufe
from ap_trainer.content.models import Beleg
from ap_trainer.tasks.generators import Generator, register

# Dokumentationspräfix aus RFC 3849 – Beispieladressen kollidieren so mit keinem echten Netz
DOC_PREFIX = (0x2001, 0x0DB8)

type _Parts = tuple[list[Rechenschritt], str, str, str | None, list[str]]


def blocks_of(value: int) -> list[int]:
    """Die acht 16-Bit-Blöcke einer Adresse, links beginnend."""
    return [(value >> (16 * (7 - i))) & 0xFFFF for i in range(8)]


def value_of(blocks: list[int]) -> int:
    """128-Bit-Zahl aus acht Blöcken."""
    result = 0
    for block in blocks:
        result = (result << 16) | block
    return result


def full_form(blocks: list[int]) -> str:
    """Volle Schreibweise: acht Blöcke mit je vier Hex-Ziffern."""
    return ":".join(f"{b:04x}" for b in blocks)


def zero_runs(blocks: list[int]) -> list[tuple[int, int]]:
    """Alle Folgen von Null-Blöcken als (Start, Länge), von links nach rechts."""
    runs: list[tuple[int, int]] = []
    start = None
    for index, block in enumerate([*blocks, 1]):
        if block == 0 and start is None:
            start = index
        elif block != 0 and start is not None:
            runs.append((start, index - start))
            start = None
    return runs


def _join(blocks: list[str], run: tuple[int, int] | None) -> str:
    if run is None:
        return ":".join(blocks)
    start, length = run
    return ":".join(blocks[:start]) + "::" + ":".join(blocks[start + length :])


def compress(blocks: list[int]) -> str:
    """Kürzeste Schreibweise nach RFC 5952: führende Nullen weg, längste Null-Folge (ab 2) als ``::``."""
    short = [f"{b:x}" for b in blocks]
    candidates = [run for run in zero_runs(blocks) if run[1] >= 2]
    # Längste Folge; bei Gleichstand die erste (max nimmt bei Gleichstand das erste Element)
    best = max(candidates, key=lambda run: run[1]) if candidates else None
    return _join(short, best)


def eui64_interface_id(mac: list[int]) -> list[int]:
    """Interface-ID nach EUI-64: ff:fe in die Mitte, im ersten Byte das 7. Bit umdrehen."""
    first = mac[0] ^ 0b0000_0010
    octets = [first, mac[1], mac[2], 0xFF, 0xFE, mac[3], mac[4], mac[5]]
    return [(octets[i] << 8) | octets[i + 1] for i in range(0, 8, 2)]


def _text_step(frage: str, value: str, erklaerung: str, falsch: list[Fehlerbild]) -> Rechenschritt:
    unique = {f.antwort: f for f in falsch if f.antwort != value}
    return Rechenschritt(
        frage=frage, antwort=value, format="text", erklaerung=erklaerung, falsch=list(unique.values())
    )


def _random_blocks(rng: random.Random) -> list[int]:
    """Adresse aus dem Dokumentationspräfix mit Null-Folgen, führenden und abschließenden Nullen."""
    while True:
        rest = []
        for _ in range(6):
            kind = rng.random()
            if kind < 0.4:
                rest.append(0)
            elif kind < 0.6:
                rest.append(rng.randint(1, 0xF) << rng.choice([4, 8]))  # z. B. 0800, 00a0
            elif kind < 0.8:
                rest.append(rng.randint(1, 0xFF))  # führende Nullen, z. B. 0008
            else:
                rest.append(rng.randint(0x1000, 0xFFFF))
        blocks = [*DOC_PREFIX, *rest]
        if any(length >= 2 for _, length in zero_runs(blocks)):
            return blocks


def _compress_errors(blocks: list[int]) -> list[Fehlerbild]:
    short = [f"{b:x}" for b in blocks]
    runs = [run for run in zero_runs(blocks) if run[1] >= 2]
    best = max(runs, key=lambda run: run[1])
    errors = [
        Fehlerbild(
            antwort=_join([f"{b:04x}" for b in blocks], best),
            warum="Die führenden Nullen in den Blöcken dürfen auch noch weg (Regel 1).",
            ursache="konzept",
        )
    ]
    for other in runs:
        if other != best:
            errors.append(
                Fehlerbild(
                    antwort=_join(short, other),
                    warum="Gekürzt wird die längste Null-Folge, bei Gleichstand die erste.",
                    ursache="konzept",
                )
            )
            # Zweites „::“ – ungültig, weil die Zahl fehlender Blöcke nicht mehr eindeutig ist
            errors.append(
                Fehlerbild(
                    antwort=_double_colon(short, best, other),
                    warum="„::“ darf nur einmal vorkommen, sonst ist unklar, wie viele Null-Blöcke "
                    "wo fehlen.",
                    ursache="konzept",
                )
            )
    stripped = [b.rstrip("0") or "0" for b in short]
    if stripped != short:
        errors.append(
            Fehlerbild(
                antwort=_join(stripped, best),
                warum="Nur führende Nullen dürfen weg. Nullen am Ende eines Blocks bleiben: 0800 → 800.",
                ursache="konzept",
            )
        )
    return errors


def _double_colon(short: list[str], first: tuple[int, int], second: tuple[int, int]) -> str:
    """Schreibweise mit zwei „::“ (ungültig), für das Fehlerbild."""
    left, right = sorted([first, second])
    middle = short[left[0] + left[1] : right[0]]
    head = ":".join(short[: left[0]])
    tail = ":".join(short[right[0] + right[1] :])
    return f"{head}::{':'.join(middle)}::{tail}"


BELEGE = (
    Beleg(
        titel="RFC 4291: IP Version 6 Addressing Architecture", url="https://www.rfc-editor.org/rfc/rfc4291"
    ),
    Beleg(
        titel="RFC 5952: A Recommendation for IPv6 Address Text Representation",
        url="https://www.rfc-editor.org/rfc/rfc5952",
    ),
    Beleg(
        titel="RFC 3849: IPv6 Address Prefix Reserved for Documentation",
        url="https://www.rfc-editor.org/rfc/rfc3849",
    ),
    Beleg(
        titel="RFC 4862: IPv6 Stateless Address Autoconfiguration",
        url="https://www.rfc-editor.org/rfc/rfc4862",
    ),
)


@register
class Ipv6(Generator):
    """Kürzen, Ausschreiben, Subnetze und EUI-64 in vier Stufen."""

    id = "ipv6"
    titel = "IPv6-Adressen"
    stufen = (1, 2, 3, 4)
    status = "geprüft"
    quelle = "Generator „ipv6“; jede Variante gegen Pythons Modul ipaddress getestet."
    belege = BELEGE

    def generate(self, rng: random.Random, stufe: Stufe, task_id: str, thema: str) -> Aufgabe:
        """Erzeugt eine IPv6-Aufgabe der gewünschten Stufe."""
        builders = {1: self._compress, 2: self._expand, 3: self._subnets, 4: self._eui64}
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

    def _compress(self, rng: random.Random) -> _Parts:
        blocks = _random_blocks(rng)
        rule1 = ":".join(f"{b:x}" for b in blocks)
        result = compress(blocks)
        explanation = (
            f"Regel 1 (führende Nullen weg): `{rule1}`. Regel 2 (längste Null-Folge → `::`): `{result}`."
        )
        step = _text_step("Gekürzte Schreibweise", result, explanation, _compress_errors(blocks))
        question = f"Schreibe die Adresse `{full_form(blocks)}` so kurz wie möglich."
        hints = [
            "Zwei Regeln: führende Nullen je Block weg, dann eine Null-Folge durch `::` ersetzen.",
            "`::` darf nur einmal vorkommen – nimm die längste Folge von Null-Blöcken, bei "
            "Gleichstand die erste.",
            f"Nach Regel 1 lautet die Adresse `{rule1}`.",
        ]
        return [step], "Adresse kürzen", question, None, hints

    def _expand(self, rng: random.Random) -> _Parts:
        blocks = _random_blocks(rng)
        short = compress(blocks)
        present = len([part for part in short.split(":") if part])
        missing = 8 - present
        count = Rechenschritt(
            frage="Anzahl Null-Blöcke für „::“",
            antwort=str(missing),
            format="zahl",
            erklaerung=f"Vorhanden sind {present} Blöcke, also 8 − {present} = {missing}.",
            falsch=[
                Fehlerbild(
                    antwort=str(present),
                    warum="Das ist die Zahl der vorhandenen Blöcke. Gesucht sind die fehlenden: 8 "
                    "minus vorhandene.",
                    ursache="rechenfehler",
                )
            ]
            if present != missing
            else [],
        )
        right_padded = ":".join(f"{b:x}".ljust(4, "0") if b else "0000" for b in blocks)
        full = _text_step(
            "Volle Schreibweise",
            full_form(blocks),
            f"Jeden Block links mit Nullen auf 4 Ziffern auffüllen, für `::` {missing} Blöcke `0000`.",
            [
                Fehlerbild(
                    antwort=right_padded,
                    warum="Die Nullen gehören nach links – gekürzt wurden führende Nullen, also "
                    "werden sie vorne ergänzt.",
                    ursache="konzept",
                )
            ],
        )
        question = f"Schreibe die gekürzte Adresse `{short}` vollständig aus (8 Blöcke à 4 Hex-Ziffern)."
        hints = [
            "Eine IPv6-Adresse hat immer 8 Blöcke mit je 4 Hex-Ziffern.",
            "Für `::` stehen so viele Null-Blöcke, wie zu 8 fehlen.",
            f"Zähle die vorhandenen Blöcke in `{short}`.",
        ]
        return [count, full], "Adresse ausschreiben", question, None, hints

    def _subnets(self, rng: random.Random) -> _Parts:
        prefix = rng.choice([48, 52, 56, 60])
        bits = 64 - prefix
        site = rng.randint(1, 0xFFFF)
        fourth = rng.randint(0, 0xFFFF) & ~((1 << bits) - 1) & 0xFFFF
        base = [*DOC_PREFIX, site, fourth, 0, 0, 0, 0]
        number = rng.randint(2, min(2**bits, 400))
        subnet = list(base)
        subnet[3] = fourth + number - 1
        base_text = f"{compress(base)}/{prefix}"
        steps = [
            Rechenschritt(
                frage="Bits für die Subnetz-ID",
                antwort=str(bits),
                format="zahl",
                erklaerung=f"Bis zum /64: 64 − {prefix} = {bits} Bit.",
                falsch=[
                    Fehlerbild(
                        antwort=str(128 - prefix),
                        warum="Gerechnet bis 128. Die letzten 64 Bit sind die Interface-ID, Subnetze "
                        "enden bei /64.",
                        ursache="konzept",
                    )
                ],
            ),
            Rechenschritt(
                frage="Anzahl /64-Subnetze",
                antwort=str(2**bits),
                format="zahl",
                erklaerung=f"2^{bits} = {2**bits:,}".replace(",", ".") + ".",
                falsch=[
                    Fehlerbild(
                        antwort=str(2**bits - 2),
                        warum="Bei IPv6-Subnetzen wird nichts abgezogen – es gibt keinen Broadcast, "
                        "und gezählt "
                        "werden Subnetze, nicht Hosts.",
                        ursache="konzept",
                    )
                ],
            ),
            Rechenschritt(
                frage=f"Subnetz-ID des {number}. Subnetzes (Hex, nur die Subnetz-Bits)",
                antwort=f"{number - 1:x}",
                format="hex",
                erklaerung=f"Gezählt wird ab 0: das {number}. Subnetz hat die ID {number - 1} = "
                f"{number - 1:x} (hex).",
                falsch=[
                    Fehlerbild(
                        antwort=f"{number:x}",
                        warum="Das erste Subnetz hat die ID 0 – das n-te also n − 1.",
                        ursache="rechenfehler",
                    ),
                    *(
                        [
                            Fehlerbild(
                                antwort=str(number - 1),
                                warum="Die Dezimalzahl wurde einfach als Hex geschrieben; erst umrechnen.",
                                ursache="konzept",
                            )
                        ]
                        if number - 1 >= 10 and str(number - 1) != f"{number - 1:x}"
                        else []
                    ),
                ],
            ),
            Rechenschritt(
                frage=f"Präfix des {number}. Subnetzes",
                antwort=f"{compress(subnet)}/64",
                format="ipv6",
                erklaerung=f"Subnetz-ID in die Subnetz-Bits des 4. Blocks: {fourth:04x} + {number - 1:x} → "
                f"`{compress(subnet)}/64`.",
                falsch=[
                    Fehlerbild(
                        antwort=f"{compress([*subnet[:3], subnet[3] + 1, 0, 0, 0, 0])}/64"
                        if subnet[3] < 0xFFFF
                        else f"{compress(base)}/64",
                        warum="Eins zu weit gezählt: das erste Subnetz hat die ID 0.",
                        ursache="rechenfehler",
                    )
                ],
            ),
        ]
        situation = (
            f"Die ArchivTech GmbH bekommt für einen Standort das Präfix **{base_text}**. "
            "Jedes VLAN soll ein eigenes /64-Subnetz erhalten, durchnummeriert ab dem ersten."
        )
        question = f"Bestimme Subnetz-Bits, Anzahl der /64-Subnetze und das **{number}. Subnetz**."
        hints = [
            "Ein IPv6-Subnetz ist immer /64; die Bits zwischen Präfix und /64 sind die Subnetz-ID.",
            "Anzahl Subnetze = 2^(64 − Präfixlänge). Die Subnetz-ID steckt im 4. Block.",
            f"Bei /{prefix} hast du {bits} Bit für Subnetze.",
        ]
        return steps, "Subnetze aus einem Präfix", question, situation, hints

    def _eui64(self, rng: random.Random) -> _Parts:
        mac = [rng.randint(0, 255) & 0b1111_1100] + [rng.randint(0, 255) for _ in range(5)]
        mac_text = ":".join(f"{b:02x}" for b in mac)
        flipped = mac[0] ^ 0b10
        iid = eui64_interface_id(mac)
        wrong_iid = [(mac[0] << 8) | mac[1], *iid[1:]]
        site = rng.randint(1, 0xFFFF)
        vlan = rng.randint(1, 0xFF)
        prefix = [*DOC_PREFIX, site, vlan]
        link_local = [0xFE80, 0, 0, 0, *iid]
        global_address = [*prefix, *iid]
        steps = [
            Rechenschritt(
                frage="Erstes Byte der MAC als Dualzahl",
                antwort=f"{mac[0]:08b}",
                format="dual",
                erklaerung=f"{mac[0]:02x} (hex) = {mac[0]:08b}.",
            ),
            Rechenschritt(
                frage="Erstes Byte nach dem Umdrehen des 7. Bits (Hex)",
                antwort=f"{flipped:02x}",
                format="hex",
                erklaerung=f"Das 7. Bit von links hat den Wert 2: {mac[0]:08b} → {flipped:08b} = "
                f"{flipped:02x}.",
                falsch=[
                    Fehlerbild(
                        antwort=f"{mac[0]:02x}",
                        warum="Das 7. Bit (Universal/Local-Bit) muss umgedreht werden – das wurde vergessen.",
                        ursache="konzept",
                    ),
                    Fehlerbild(
                        antwort=f"{mac[0] ^ 0b1:02x}",
                        warum="Das ist das 8. Bit. Gemeint ist das 7. Bit von links, Stellenwert 2.",
                        ursache="rechenfehler",
                    ),
                    Fehlerbild(
                        antwort=f"{mac[0] ^ 0b0100_0000:02x}",
                        warum="Von rechts gezählt. Das 7. Bit von links hat den Stellenwert 2.",
                        ursache="rechenfehler",
                    ),
                ],
            ),
            Rechenschritt(
                frage="Link-Local-Adresse",
                antwort=compress(link_local),
                format="ipv6",
                erklaerung=f"`ff:fe` in die Mitte der MAC, erstes Byte {flipped:02x}: Interface-ID "
                f"`{':'.join(f'{b:x}' for b in iid)}`, davor `fe80::` → `{compress(link_local)}`.",
                falsch=[
                    Fehlerbild(
                        antwort=compress([0xFE80, 0, 0, 0, *wrong_iid]),
                        warum="Das 7. Bit im ersten Byte wurde nicht umgedreht.",
                        ursache="konzept",
                    )
                ],
            ),
            Rechenschritt(
                frage="Globale Adresse per SLAAC",
                antwort=compress(global_address),
                format="ipv6",
                erklaerung="Präfix aus dem Router Advertisement + dieselbe Interface-ID → "
                f"`{compress(global_address)}`.",
            ),
        ]
        situation = (
            f"Ein neuer Archivserver der ArchivTech GmbH hat die MAC-Adresse `{mac_text}`. Er bildet seine "
            f"Interface-ID nach **EUI-64**; der Router kündigt das Präfix "
            f"`{compress([*prefix, 0, 0, 0, 0])}/64` an."
        )
        question = "Bestimme Schritt für Schritt die Link-Local-Adresse und die globale Adresse des Servers."
        hints = [
            "EUI-64: in die Mitte der MAC `ff:fe` einfügen und im ersten Byte das 7. Bit umdrehen.",
            "Link-Local-Präfix ist `fe80::/64`; bei SLAAC kommt das globale Präfix vom Router.",
            f"Das erste Byte `{mac[0]:02x}` ist dual {mac[0]:08b}.",
        ]
        return steps, "SLAAC mit EUI-64", question, situation, hints
