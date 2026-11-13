"""Generator „Zahlensysteme“: Umrechnen zwischen dezimal, dual und hexadezimal (AU-03).

Stufen: 1 ein Nibble (0–15), 2 ein Byte dual ↔ dezimal, 3 dezimal ↔ hexadezimal über den
Umweg Dualzahl (zwei geprüfte Schritte), 4 ein 16-Bit-Block aus einer IPv6-Adresse in einer
Handlungssituation. Die Umrechnung ist hier bewusst von Hand programmiert (Restwertmethode,
Viererblöcke); die Tests vergleichen mit Pythons eingebauten Funktionen als unabhängiger Referenz.
"""

from __future__ import annotations

import random

from ap_trainer.content.aufgaben import Aufgabe, Fehlerbild, Rechenschritt, Rechnung, Stufe
from ap_trainer.content.models import Beleg
from ap_trainer.tasks.generators import Generator, register

HEX_DIGITS = "0123456789ABCDEF"


def to_dual(value: int, width: int = 0) -> str:
    """Dualzahl per Restwertmethode, links mit Nullen auf ``width`` Stellen aufgefüllt."""
    digits: list[str] = []
    rest = value
    while rest > 0:
        digits.append(str(rest % 2))
        rest //= 2
    text = "".join(reversed(digits)) or "0"
    return text.rjust(width, "0")


def to_hex(value: int, width: int = 0) -> str:
    """Hexadezimalzahl über Viererblöcke der Dualzahl (je Block eine Hex-Ziffer)."""
    dual = to_dual(value)
    dual = dual.rjust((len(dual) + 3) // 4 * 4, "0")
    blocks = [dual[i : i + 4] for i in range(0, len(dual), 4)]
    text = "".join(HEX_DIGITS[dual_value(block)] for block in blocks).lstrip("0") or "0"
    return text.rjust(width, "0")


def dual_value(dual: str) -> int:
    """Wert einer Dualzahl: Summe der Stellenwerte unter den Einsen."""
    return sum(2**position for position, bit in enumerate(reversed(dual)) if bit == "1")


def hex_value(text: str) -> int:
    """Wert einer Hexadezimalzahl: Ziffernwert mal Potenz von 16."""
    return sum(HEX_DIGITS.index(d) * 16**pos for pos, d in enumerate(reversed(text.upper())))


def group(dual: str) -> str:
    """Dualzahl in Viererblöcken von rechts, z. B. ``1011 0111``."""
    padded = dual.rjust((len(dual) + 3) // 4 * 4, "0")
    return " ".join(padded[i : i + 4] for i in range(0, len(padded), 4))


def place_value_table(dual: str) -> str:
    """Markdown-Tabelle Stellenwert → Bit, wie in der Lektion."""
    weights = [str(2**p) for p in range(len(dual) - 1, -1, -1)]
    head = "| " + " | ".join(weights) + " |"
    rule = "|" + " ---: |" * len(dual)
    bits = "| " + " | ".join(dual) + " |"
    return f"{head}\n{rule}\n{bits}"


def _sum_of_ones(dual: str) -> str:
    parts = [str(2**p) for p, bit in enumerate(reversed(dual)) if bit == "1"]
    return " + ".join(reversed(parts)) or "0"


def _errors(correct: str, fmt_parse: dict[str, int], candidates: list[Fehlerbild]) -> list[Fehlerbild]:
    """Behält nur Fehlerbilder, die sich vom richtigen Wert und voneinander unterscheiden."""
    seen = {fmt_parse[correct]}
    kept: list[Fehlerbild] = []
    for error in candidates:
        value = fmt_parse.get(error.antwort)
        if value is not None and value not in seen:
            seen.add(value)
            kept.append(error)
    return kept


def _dual_to_decimal_step(dual: str) -> Rechenschritt:
    value = dual_value(dual)
    reversed_value = dual_value(dual[::-1])
    errors = _errors(
        str(value),
        {str(value): value, str(reversed_value): reversed_value},
        [
            Fehlerbild(
                antwort=str(reversed_value),
                warum="Die Stellenwerte wurden von links statt von rechts gezählt – das kleinste Bit (1) "
                "steht ganz rechts.",
                ursache="konzept",
            )
        ],
    )
    return Rechenschritt(
        frage="Dezimalwert",
        antwort=str(value),
        format="zahl",
        erklaerung=f"Stellenwerte unter den Einsen addieren: {_sum_of_ones(dual)} = {value}.",
        falsch=errors,
    )


def _decimal_to_dual_step(value: int, width: int) -> Rechenschritt:
    dual = to_dual(value, width)
    reversed_dual = dual.lstrip("0")[::-1]
    errors = _errors(
        dual,
        {dual: value, reversed_dual: dual_value(reversed_dual)},
        [
            Fehlerbild(
                antwort=reversed_dual,
                warum="Die Reste wurden von oben nach unten gelesen. Bei der Restwertmethode liest man "
                "die Reste von unten nach oben.",
                ursache="konzept",
            )
        ],
    )
    return Rechenschritt(
        frage=f"Dualzahl ({width} Bit)",
        antwort=group(dual),
        format="dual",
        erklaerung=f"{value} = {_sum_of_ones(dual)} → {group(dual)}.",
        falsch=errors,
    )


def _dual_to_hex_step(dual: str) -> Rechenschritt:
    value = dual_value(dual)
    hex_text = to_hex(value)
    trimmed = dual.lstrip("0") or "0"
    # Typischer Fehler: Viererblöcke von links statt von rechts gebildet
    left_blocks = trimmed.ljust((len(trimmed) + 3) // 4 * 4, "0")
    wrong = "".join(HEX_DIGITS[dual_value(left_blocks[i : i + 4])] for i in range(0, len(left_blocks), 4))
    errors = _errors(
        hex_text,
        {hex_text: value, wrong: hex_value(wrong)},
        [
            Fehlerbild(
                antwort=wrong,
                warum="Die Viererblöcke wurden von links gebildet. Immer von rechts gruppieren und links "
                "mit Nullen auffüllen.",
                ursache="konzept",
            )
        ],
    )
    blocks = group(dual).split()
    mapping = ", ".join(f"{b} = {HEX_DIGITS[dual_value(b)]}" for b in blocks)
    return Rechenschritt(
        frage="Hexadezimalzahl",
        antwort=hex_text,
        format="hex",
        erklaerung=f"Viererblöcke von rechts: {mapping} → {hex_text}.",
        falsch=errors,
    )


def _hex_to_dual_step(hex_text: str, width: int) -> Rechenschritt:
    value = hex_value(hex_text)
    dual = to_dual(value, width)
    mapping = ", ".join(f"{d} = {to_dual(HEX_DIGITS.index(d), 4)}" for d in hex_text)
    return Rechenschritt(
        frage=f"Dualzahl ({width} Bit)",
        antwort=group(dual),
        format="dual",
        erklaerung=f"Jede Hex-Ziffer ergibt genau 4 Bit: {mapping}.",
    )


def _hex_to_decimal_step(hex_text: str) -> Rechenschritt:
    value = hex_value(hex_text)
    # Typischer Fehler: Stellenwerte 10, 100 … statt 16, 256 … genommen
    wrong = sum(HEX_DIGITS.index(d) * 10**p for p, d in enumerate(reversed(hex_text)))
    errors = _errors(
        str(value),
        {str(value): value, str(wrong): wrong},
        [
            Fehlerbild(
                antwort=str(wrong),
                warum="Mit den Stellenwerten des Dezimalsystems (1, 10, 100) gerechnet. Im Hexsystem sind "
                "es Potenzen von 16: 1, 16, 256, 4096.",
                ursache="konzept",
            )
        ],
    )
    terms = " + ".join(
        f"{HEX_DIGITS.index(d)} × {16 ** (len(hex_text) - 1 - i)}" for i, d in enumerate(hex_text)
    )
    return Rechenschritt(
        frage="Dezimalwert",
        antwort=str(value),
        format="zahl",
        erklaerung=f"Ziffernwert mal Stellenwert (Potenzen von 16): {terms} = {value}.",
        falsch=errors,
    )


# Jede Stufe liefert: Schritte, Titel, Frage, Situation, Hinweise
type _Parts = tuple[list[Rechenschritt], str, str, str | None, list[str]]

BELEGE = (
    Beleg(titel="Lektion „Zahlensysteme umrechnen“ (Stellenwertsysteme)"),
    Beleg(
        titel="RFC 4291: IP Version 6 Addressing Architecture", url="https://www.rfc-editor.org/rfc/rfc4291"
    ),
)


@register
class NumberSystems(Generator):
    """Umrechnungen dual ↔ dezimal ↔ hexadezimal in vier Stufen."""

    id = "zahlensysteme"
    titel = "Zahlensysteme umrechnen"
    stufen = (1, 2, 3, 4)
    status = "ungeprüft"
    quelle = "Generator „zahlensysteme“; jede Variante gegen Pythons int()/format() getestet."
    belege = BELEGE

    def generate(self, rng: random.Random, stufe: Stufe, task_id: str, thema: str) -> Aufgabe:
        """Erzeugt eine Umrechnungsaufgabe der gewünschten Stufe."""
        builders = {1: self._nibble, 2: self._byte, 3: self._via_dual, 4: self._ipv6_block}
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

    def _nibble(self, rng: random.Random) -> _Parts:
        value = rng.randint(3, 15)
        dual = to_dual(value, 4)
        if rng.random() < 0.5:
            question = f"Wandle die Dualzahl `{dual}` in eine Dezimalzahl um."
            steps = [_dual_to_decimal_step(dual)]
            hints = ["Ein Nibble hat vier Stellen mit den Stellenwerten 8, 4, 2, 1."]
            return steps, "Nibble: dual → dezimal", question, None, hints
        question = f"Wandle die Dualzahl `{dual}` in eine Hexadezimalziffer um."
        steps = [_dual_to_hex_step(dual)]
        hints = ["Vier Bit ergeben genau eine Hex-Ziffer.", "Werte ab 10 schreibt man als A (10) bis F (15)."]
        return steps, "Nibble: dual → hexadezimal", question, None, hints

    def _byte(self, rng: random.Random) -> _Parts:
        value = rng.randint(16, 255)
        dual = to_dual(value, 8)
        if rng.random() < 0.5:
            question = f"Wandle die Dualzahl `{group(dual)}` in eine Dezimalzahl um."
            hints = [
                "Jede Stelle hat einen Stellenwert; rechts beginnt es mit 1.",
                "Stellenwerte eines Bytes: 128, 64, 32, 16, 8, 4, 2, 1.",
                f"Schreib die Stellenwerte über die Bits:\n\n{place_value_table(dual)}",
            ]
            return [_dual_to_decimal_step(dual)], "Byte: dual → dezimal", question, None, hints
        question = f"Wandle die Dezimalzahl **{value}** in eine 8-stellige Dualzahl um."
        largest = 2 ** (value.bit_length() - 1)
        hints = [
            "Zerlege die Zahl in Zweierpotenzen.",
            "Weg 1: Von links jeden Stellenwert (128, 64, …) abziehen, der noch hineinpasst.",
            f"Der größte Stellenwert, der in {value} passt, ist {largest}; Rest {value - largest}.",
        ]
        return [_decimal_to_dual_step(value, 8)], "Byte: dezimal → dual", question, None, hints

    def _via_dual(self, rng: random.Random) -> _Parts:
        value = rng.randint(256, 4095) if rng.random() < 0.4 else rng.randint(16, 255)
        width = 12 if value > 255 else 8
        if rng.random() < 0.5:
            question = f"Wandle die Dezimalzahl **{value}** in eine Hexadezimalzahl um – über die Dualzahl."
            dual = to_dual(value, width)
            steps = [_decimal_to_dual_step(value, width), _dual_to_hex_step(dual)]
            hints = [
                "Erst in die Dualzahl umrechnen, dann in Viererblöcke teilen.",
                "Eine Hex-Ziffer steht für genau 4 Bit.",
                f"Die Dualzahl hat {width} Stellen, also {width // 4} Viererblöcke.",
            ]
            return steps, "Dezimal → hexadezimal", question, None, hints
        hex_text = to_hex(value)
        question = f"Wandle die Hexadezimalzahl `{hex_text}` in eine Dezimalzahl um – über die Dualzahl."
        steps = [_hex_to_dual_step(hex_text, len(hex_text) * 4), _hex_to_decimal_step(hex_text)]
        hints = [
            "Erst jede Hex-Ziffer in 4 Bit übersetzen. Den Dezimalwert bekommst du über die Stellenwerte "
            "der Dualzahl oder über Potenzen von 16.",
            "A = 10, B = 11, C = 12, D = 13, E = 14, F = 15.",
            f"Die erste Ziffer {hex_text[0]} ergibt {to_dual(HEX_DIGITS.index(hex_text[0]), 4)}.",
        ]
        return steps, "Hexadezimal → dezimal", question, None, hints

    def _ipv6_block(self, rng: random.Random) -> _Parts:
        value = rng.randint(4096, 65535)
        hex_text = to_hex(value, 4)
        situation = (
            "Die ArchivTech GmbH dokumentiert ihr IPv6-Netz. In einer Firewall-Regel taucht der Block "
            f"`{hex_text.lower()}` der Adresse `2001:db8:{hex_text.lower()}::1` auf. Für eine Bitmaske "
            "brauchst du ihn als Dualzahl, für ein Skript als Dezimalzahl."
        )
        question = f"Rechne den Block `{hex_text}` in eine 16-stellige Dualzahl und in eine Dezimalzahl um."
        steps = [_hex_to_dual_step(hex_text, 16), _hex_to_decimal_step(hex_text)]
        hints = [
            "Ein IPv6-Block besteht aus 4 Hex-Ziffern, also 16 Bit.",
            "Jede Hex-Ziffer einzeln in 4 Bit übersetzen; für den Dezimalwert Potenzen von 16 nutzen.",
            f"{hex_text[0]} × 4096 ist der erste Summand des Dezimalwerts.",
        ]
        return steps, "IPv6-Block umrechnen", question, situation, hints
