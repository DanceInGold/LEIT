"""Dunkelmodus: Flächenfarben kommen aus eigenen CSS-Klassen mit ``body--dark`` statt aus Tailwind."""

from __future__ import annotations

import re
from pathlib import Path

UI = Path(__file__).parents[2] / "src" / "ap_trainer" / "ui"


def test_no_tailwind_dark_variants() -> None:
    # Tailwinds dark:-Varianten griffen nicht (weiße Abgabeleiste im Dunkelmodus); eigene Klassen
    # in layout._CSS mit ".body--dark" stattdessen verwenden.
    offenders = [
        f"{path.name}: {match.group(0)}"
        for path in sorted(UI.glob("*.py"))
        for match in re.finditer(r"\bdark:(?:bg|text|border)-[\w\[\]#-]+", path.read_text(encoding="utf-8"))
    ]
    assert offenders == []


def test_light_surfaces_have_a_dark_counterpart() -> None:
    # Jede helle Fläche aus layout._CSS braucht eine Regel für den Dunkelmodus
    css = (UI / "layout.py").read_text(encoding="utf-8")
    for cls in ("seiten-hintergrund", "hinweis-karte"):
        assert f".{cls} {{" in css and f".body--dark .{cls} {{" in css
