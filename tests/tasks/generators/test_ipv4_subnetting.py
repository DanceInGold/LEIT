"""Generator „ipv4-subnetting“ gegen Pythons Modul ``ipaddress`` als unabhängige Referenz (NF-07)."""

from __future__ import annotations

import ipaddress
import math
import re

from ap_trainer.content.aufgaben import Rechenschritt, Rechnung
from ap_trainer.tasks.generators import make
from tests.tasks.random_cases import random_cases

_ADDRESS = re.compile(r"\*\*(\d+\.\d+\.\d+\.\d+)/(\d+)\*\*")
_PREFIX = re.compile(r"\*\*/(\d+)\*\*")


def _steps(task: Rechnung) -> dict[str, Rechenschritt]:
    return {step.frage: step for step in task.schritte}


def _check_interface(steps: dict[str, Rechenschritt], net: ipaddress.IPv4Network) -> None:
    """Prüft alle Schritte, die zu einem Subnetz gehören, gegen ``ipaddress``."""
    if "Subnetzmaske" in steps:
        assert steps["Subnetzmaske"].antwort == str(net.netmask)
    if "Broadcastadresse" in steps:
        assert steps["Broadcastadresse"].antwort == str(net.broadcast_address)
    if "Netzadresse" in steps:
        assert steps["Netzadresse"].antwort == str(net.network_address)
    if "Erster Host" in steps:
        hosts = list(net.hosts())
        assert steps["Erster Host"].antwort == str(hosts[0])
        assert steps["Letzter Host"].antwort == str(hosts[-1])
        assert int(steps["Nutzbare Hosts"].antwort) == len(hosts)
    if "Schrittweite im Grenz-Oktett" in steps:
        octets = str(net.netmask).split(".")
        boundary = (net.prefixlen - 1) // 8
        assert int(steps["Schrittweite im Grenz-Oktett"].antwort) == 256 - int(octets[boundary])


@random_cases()
def test_mask_level(seed: int) -> None:
    task = make("ipv4-subnetting", 1, seed, "ipv4-subnetting")
    assert isinstance(task, Rechnung)
    prefix = int(_PREFIX.search(task.frage).group(1))  # type: ignore[union-attr]
    assert task.schritte[0].antwort == str(ipaddress.ip_network(f"0.0.0.0/{prefix}").netmask)


@random_cases()
def test_address_levels(seed: int) -> None:
    for level in (2, 3):
        task = make("ipv4-subnetting", level, seed, "ipv4-subnetting")
        assert isinstance(task, Rechnung)
        address, prefix = _ADDRESS.search(task.frage).groups()  # type: ignore[union-attr]
        interface = ipaddress.ip_interface(f"{address}/{prefix}")
        assert interface.ip not in (interface.network.network_address, interface.network.broadcast_address)
        assert interface.ip.is_private
        _check_interface(_steps(task), interface.network)


@random_cases()
def test_split_level(seed: int) -> None:
    task = make("ipv4-subnetting", 4, seed, "ipv4-subnetting")
    assert isinstance(task, Rechnung) and task.situation
    base = ipaddress.ip_network("/".join(_ADDRESS.search(task.situation).groups()))  # type: ignore[union-attr]
    steps = _steps(task)
    new_prefix = int(steps["Neues Präfix (Zahl hinter /)"].antwort)
    hosts_match = re.search(r"mindestens \*\*(\d+) Hosts", task.situation)
    if hosts_match:
        # Kleinstes Hostbit-h mit 2^h − 2 ≥ Hosts, unabhängig nachgerechnet
        hosts = int(hosts_match.group(1))
        hostbits = next(h for h in range(2, 33) if 2**h - 2 >= hosts)
        assert new_prefix == 32 - hostbits
    else:
        wanted = int(re.search(r"mindestens \*\*(\d+) gleich", task.situation).group(1))  # type: ignore[union-attr]
        assert new_prefix == base.prefixlen + math.ceil(math.log2(wanted))
    subnets = list(base.subnets(new_prefix=new_prefix))
    number = int(re.search(r"\*\*(\d+)\. Subnetz", task.frage).group(1))  # type: ignore[union-attr]
    target = subnets[number - 1]
    assert steps[f"Netzadresse des {number}. Subnetzes"].antwort == str(target.network_address)
    _check_interface({k: v for k, v in steps.items() if k != "Netzadresse"}, target)
    if "Anzahl Subnetze" in steps:
        assert int(steps["Anzahl Subnetze"].antwort) == len(subnets)
    else:
        assert int(steps["Nutzbare Hosts je Subnetz"].antwort) == target.num_addresses - 2


def test_example_from_lesson() -> None:
    # Beispiel 2 der Lektion: 172.16.48.0/20, mindestens 500 Hosts → /23, 8 Subnetze
    hostbits = next(h for h in range(2, 33) if 2**h - 2 >= 500)
    assert 32 - hostbits == 23
    assert len(list(ipaddress.ip_network("172.16.48.0/20").subnets(new_prefix=23))) == 8
