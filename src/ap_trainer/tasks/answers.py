"""Eingaben lesen und vergleichen: Zahlen (deutsch und englisch), Dual, Hex, IPv4, Text.

Wer in der Prüfung „1.500,5“, „1500.5“ oder „62 Hosts“ schreibt, meint dasselbe wie die
Musterlösung. Diese Datei sorgt dafür, dass solche Schreibweisen als richtig zählen, ohne
falsche Antworten durchzulassen.
"""

from __future__ import annotations

import re

from ap_trainer.content.aufgaben import Antwortformat

# Zahl am Anfang der Eingabe; Einheiten oder Wörter danach („62 Hosts“, „4,5 s“) werden ignoriert
_NUMBER = re.compile(r"^[+-]?[\d.,]+")
_THOUSANDS = re.compile(r"^\d{1,3}(\.\d{3})+$")
_SPACES = re.compile(r"[\s  ]+")


def normalize_text(raw: str) -> str:
    """Kleinschreibung, überflüssige Leerzeichen und Satzzeichen am Ende entfernt."""
    text = _SPACES.sub(" ", raw).strip().casefold()
    return text.rstrip(".!")


def number_candidates(raw: str) -> list[float]:
    """Alle sinnvollen Lesarten einer Zahl.

    „1.500“ ist im Deutschen 1500, im Englischen 1,5 – beide Lesarten werden geliefert,
    der Vergleich nimmt die passende. Ein Komma ist immer Dezimalzeichen, wenn kein Punkt dabei ist.
    """
    text = _SPACES.sub("", raw).replace("−", "-")
    match = _NUMBER.match(text)
    if not match:
        return []
    token = match.group(0).rstrip(".,")
    variants: list[str] = []
    if "," in token and "." in token:
        # Das spätere Zeichen ist das Dezimalzeichen: 1.234,5 (deutsch) oder 1,234.5 (englisch)
        if token.rfind(",") > token.rfind("."):
            variants.append(token.replace(".", "").replace(",", "."))
        else:
            variants.append(token.replace(",", ""))
    elif "," in token:
        variants.append(token.replace(",", "."))
    elif "." in token:
        variants.append(token)
        if _THOUSANDS.match(token.lstrip("+-")):
            variants.append(token.replace(".", ""))
    else:
        variants.append(token)
    result: list[float] = []
    for variant in variants:
        try:
            result.append(float(variant))
        except ValueError:
            continue
    return result


def parse_dual(raw: str) -> int | None:
    """Dualzahl wie ``1100 0000``, ``0b11000000`` oder ``11000000₂``."""
    text = _SPACES.sub("", raw).casefold().removeprefix("0b").removesuffix("₂")
    return int(text, 2) if text and set(text) <= {"0", "1"} else None


def parse_hex(raw: str) -> int | None:
    """Hexadezimalzahl wie ``C0``, ``0xc0``, ``C0h`` oder ``C0₁₆``."""
    text = _SPACES.sub("", raw).casefold().removeprefix("0x").removesuffix("₁₆").removesuffix("h")
    return int(text, 16) if text and all(c in "0123456789abcdef" for c in text) else None


def parse_ipv4(raw: str) -> int | None:
    """IPv4-Adresse oder Maske als 32-Bit-Zahl; ``None`` bei ungültiger Schreibweise."""
    parts = _SPACES.sub("", raw).split(".")
    if len(parts) != 4 or not all(p.isdigit() and len(p) <= 3 for p in parts):
        return None
    octets = [int(p) for p in parts]
    if any(o > 255 for o in octets):
        return None
    return (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]


def is_valid(fmt: Antwortformat, raw: str) -> bool:
    """True, wenn ``raw`` im Format ``fmt`` lesbar ist (für die Inhaltsprüfung)."""
    if fmt == "zahl":
        return bool(number_candidates(raw))
    if fmt == "text":
        return bool(normalize_text(raw))
    return {"dual": parse_dual, "hex": parse_hex, "ipv4": parse_ipv4}[fmt](raw) is not None


def same_answer(fmt: Antwortformat, given: str, expected: str, tolerance: float = 0.0) -> bool:
    """Vergleicht eine Eingabe mit der erwarteten Antwort im angegebenen Format.

    ``tolerance`` ist die erlaubte relative Abweichung bei Zahlen (0.01 = 1 %).
    """
    if fmt == "zahl":
        targets = number_candidates(expected)
        if not targets:
            return False
        target = targets[0]
        allowed = max(abs(target) * tolerance, 1e-9)
        return any(abs(value - target) <= allowed for value in number_candidates(given))
    if fmt == "text":
        return normalize_text(given) == normalize_text(expected)
    parser = {"dual": parse_dual, "hex": parse_hex, "ipv4": parse_ipv4}[fmt]
    value = parser(given)
    return value is not None and value == parser(expected)
