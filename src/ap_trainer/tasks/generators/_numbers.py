"""Hilfen für Generatoren mit Kommazahlen: exakt rechnen, deutsch anzeigen, eindeutig speichern.

Generatoren rechnen mit ``Fraction`` (keine Rundungsfehler). Für die Anzeige gibt es die deutsche
Schreibweise mit Tausenderpunkten („1.051,20“), für die gespeicherte Musterlösung eine eindeutige
ohne Tausenderpunkte („1051,2“) – „1.500“ wäre sonst zweideutig (siehe E-25).
Die Datei beginnt mit ``_``, damit die Registrierung sie nicht als Generator lädt.
"""

from __future__ import annotations

from fractions import Fraction

from ap_trainer.content.aufgaben import Fehlerbild, Fehlerursache, Rechenschritt

type Number = int | Fraction

# Erlaubte relative Abweichung, wenn die Musterlösung gerundet ist (0,5 %)
ROUNDED_TOLERANCE = 0.005


def rounded(value: Number, decimals: int = 2) -> Fraction:
    """Kaufmännisch gerundet (ab 5 aufrunden), exakt als Bruch."""
    factor = 10**decimals
    exact = Fraction(value)
    scaled = abs(exact) * factor
    whole = int(scaled)
    if scaled - whole >= Fraction(1, 2):
        whole += 1
    return Fraction(whole if exact >= 0 else -whole, factor)


def de(value: Number, decimals: int | None = None, max_places: int = 2) -> str:
    """Deutsche Schreibweise: Tausenderpunkte, Dezimalkomma.

    Ohne ``decimals`` so viele Nachkommastellen wie nötig (höchstens ``max_places``), sonst genau
    ``decimals``.
    """
    places = decimals if decimals is not None else _needed_places(Fraction(value), max_places)
    number = rounded(value, places)
    sign = "−" if number < 0 else ""
    number = abs(number)
    whole = int(number)
    text = f"{whole:,}".replace(",", ".")
    if places:
        fraction = round((number - whole) * 10**places)
        text += "," + str(fraction).rjust(places, "0")
    return sign + text


def answer(value: Number, places: int = 2) -> str:
    """Musterlösung ohne Tausenderpunkte, höchstens ``places`` Nachkommastellen, z. B. ``1051,2``."""
    number = rounded(value, places)
    text = de(number, max_places=places).replace(".", "")
    return text.rstrip("0").rstrip(",") if "," in text else text


def _needed_places(value: Fraction, max_places: int = 2) -> int:
    for places in range(max_places):
        if value * 10**places == int(value * 10**places):
            return places
    return max_places


def _distinct(value: Fraction, other: Fraction, tolerance: float) -> bool:
    """True, wenn ``value`` sicher außerhalb der Toleranz um ``other`` liegt."""
    if tolerance == 0:
        return value != other
    return abs(value - other) > abs(other) * Fraction(2 * tolerance) + Fraction(1, 100)


def number_step(
    frage: str,
    value: Number,
    erklaerung: str,
    einheit: str | None = None,
    falsch: list[tuple[Number, str, Fehlerursache]] | None = None,
    toleranz: float | None = None,
    places: int | None = None,
) -> Rechenschritt:
    """Rechenschritt mit Zahl als Antwort; gerundete Werte bekommen eine kleine Toleranz.

    ``falsch`` sind typische Fehlwerte mit Erklärung und Ursache. Fehlwerte, die (fast) dem
    richtigen Wert entsprechen oder doppelt vorkommen, werden verworfen. ``toleranz`` überschreibt
    die automatische Toleranz, z. B. wenn Zwischenergebnisse üblicherweise gerundet werden.
    ``places`` sind die Nachkommastellen der Musterlösung; ohne Angabe 2, bei Werten unter 1 aber 4,
    damit z. B. 0,018 kW nicht zu 0,02 kW wird.
    """
    exact = Fraction(value)
    digits = places if places is not None else (4 if 0 < abs(exact) < 1 else 2)
    tolerance = 0.0 if rounded(exact, digits) == exact else ROUNDED_TOLERANCE
    if toleranz is not None:
        tolerance = toleranz
    errors: list[Fehlerbild] = []
    seen: list[Fraction] = [rounded(exact, digits)]
    for wrong, why, cause in falsch or []:
        candidate = rounded(wrong, digits)
        if all(_distinct(candidate, other, tolerance) for other in seen):
            seen.append(candidate)
            errors.append(Fehlerbild(antwort=answer(candidate, digits), warum=why, ursache=cause))
    return Rechenschritt(
        frage=frage,
        antwort=answer(exact, digits),
        format="zahl",
        einheit=einheit,
        toleranz=tolerance,
        erklaerung=erklaerung,
        falsch=errors,
    )
