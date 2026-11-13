"""Generator „ipv6“ gegen Pythons Modul ``ipaddress`` und eine eigene Bitrechnung (NF-07)."""

from __future__ import annotations

import ipaddress
import re

from ap_trainer.content.aufgaben import Rechenschritt, Rechnung
from ap_trainer.tasks.answers import parse_ipv6
from ap_trainer.tasks.generators import make
from ap_trainer.tasks.generators.ipv6 import blocks_of, compress, value_of
from tests.tasks.random_cases import random_cases

_CODE = re.compile(r"`([0-9a-f:./]+)`")


def _steps(task: Rechnung) -> dict[str, Rechenschritt]:
    return {step.frage: step for step in task.schritte}


@random_cases()
def test_compress_matches_ipaddress(seed: int) -> None:
    task = make("ipv6", 1, seed, "ipv6")
    assert isinstance(task, Rechnung)
    full = _CODE.search(task.frage).group(1)  # type: ignore[union-attr]
    address = ipaddress.IPv6Address(full)
    assert address.exploded == full
    assert task.schritte[0].antwort == address.compressed
    for error in task.schritte[0].falsch:
        assert error.antwort != address.compressed


@random_cases()
def test_expand_matches_ipaddress(seed: int) -> None:
    task = make("ipv6", 2, seed, "ipv6")
    assert isinstance(task, Rechnung)
    short = _CODE.search(task.frage).group(1)  # type: ignore[union-attr]
    address = ipaddress.IPv6Address(short)
    steps = _steps(task)
    assert steps["Volle Schreibweise"].antwort == address.exploded
    present = len([part for part in short.split(":") if part])
    assert int(steps["Anzahl Null-Blöcke für „::“"].antwort) == 8 - present


@random_cases()
def test_subnets_match_ipaddress(seed: int) -> None:
    task = make("ipv6", 3, seed, "ipv6")
    assert isinstance(task, Rechnung) and task.situation
    base = ipaddress.IPv6Network(re.search(r"\*\*([0-9a-f:]+/\d+)\*\*", task.situation).group(1))  # type: ignore[union-attr]
    number = int(re.search(r"\*\*(\d+)\. Subnetz", task.frage).group(1))  # type: ignore[union-attr]
    steps = _steps(task)
    assert int(steps["Bits für die Subnetz-ID"].antwort) == 64 - base.prefixlen
    assert int(steps["Anzahl /64-Subnetze"].antwort) == 2 ** (64 - base.prefixlen)
    # n-tes Subnetz direkt aus der Adresse berechnet, ohne alle Subnetze aufzuzählen
    expected = ipaddress.IPv6Network((int(base.network_address) + ((number - 1) << 64), 64))
    assert expected.subnet_of(base)
    answer = steps[f"Präfix des {number}. Subnetzes"].antwort
    assert ipaddress.IPv6Network(answer) == expected
    assert (
        int(steps[f"Subnetz-ID des {number}. Subnetzes (Hex, nur die Subnetz-Bits)"].antwort, 16)
        == number - 1
    )


def _reference_eui64(mac: str) -> int:
    """EUI-64 nach RFC 4291 Anhang A, unabhängig vom Generator als 64-Bit-Zahl gerechnet."""
    value = int(mac.replace(":", ""), 16)
    upper, lower = value >> 24, value & 0xFFFFFF
    eui = (upper << 40) | (0xFFFE << 24) | lower
    return eui ^ (1 << 57)  # Universal/Local-Bit: Bit 6 des ersten Oktetts von links (0-basiert)


@random_cases()
def test_eui64_matches_reference(seed: int) -> None:
    task = make("ipv6", 4, seed, "ipv6")
    assert isinstance(task, Rechnung) and task.situation
    mac = re.search(r"MAC-Adresse `([0-9a-f:]+)`", task.situation).group(1)  # type: ignore[union-attr]
    prefix = ipaddress.IPv6Network(re.search(r"Präfix `([0-9a-f:]+/64)`", task.situation).group(1))  # type: ignore[union-attr]
    iid = _reference_eui64(mac)
    steps = _steps(task)
    assert parse_ipv6(steps["Link-Local-Adresse"].antwort) == ((0xFE80 << 112) | iid, None)
    assert parse_ipv6(steps["Globale Adresse per SLAAC"].antwort) == (int(prefix.network_address) | iid, None)
    assert int(steps["Erstes Byte nach dem Umdrehen des 7. Bits (Hex)"].antwort, 16) == (iid >> 56) & 0xFF


def test_example_from_lesson() -> None:
    # Lektion ipv6-adressen und ipv6-subnetze-slaac
    full = "2001:0db8:0000:0000:0008:0800:200c:417a"
    blocks = blocks_of(int(ipaddress.IPv6Address(full)))
    assert compress(blocks) == "2001:db8::8:800:200c:417a"
    assert compress(blocks_of(int(ipaddress.IPv6Address("2001:db8:0:0:1:0:0:1")))) == "2001:db8::1:0:0:1"
    assert value_of(blocks) == int(ipaddress.IPv6Address(full))
    assert f"{_reference_eui64('3c:52:82:1a:7f:09'):016x}" == "3e5282fffe1a7f09"
