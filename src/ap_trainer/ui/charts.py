"""Diagramm-Optionen (ECharts) für den Überblick auf der Startseite – ohne NiceGUI, testbar.

Farben nach der Referenzpalette: Ist-Werte Blau, Soll-Werte Grau gestrichelt, Abstufungen
in hellerem Blau. Text bleibt neutral grau, damit er in hellem und dunklem Modus lesbar ist.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Sequence
from typing import Any

from ap_trainer.core.stats import AreaProgress, TimeSeries

BLUE = "#2a78d6"
BLUE_LIGHT = "#86b6ef"
GREY = "#8a8984"
TRACK = "rgba(138,137,132,0.25)"
WEEKDAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

# Kurzbezeichnungen der Katalogbereiche für die Achsenbeschriftung
AREA_SHORT = {
    "b01": "Planen & Projekte",
    "b02": "Kundenberatung",
    "b03": "IT-Systeme",
    "b04": "Einrichten & Programmieren",
    "b05": "Qualität",
    "b06": "Sicherheit & Datenschutz",
    "b07": "Leistungserbringung",
}


def _base() -> dict[str, Any]:
    return {
        "backgroundColor": "transparent",
        "textStyle": {"color": GREY},
        "grid": {"left": 8, "right": 16, "top": 36, "bottom": 8, "containLabel": True},
        "tooltip": {"trigger": "axis"},
    }


def _axis_style() -> dict[str, Any]:
    return {
        "axisLine": {"lineStyle": {"color": TRACK}},
        "axisTick": {"show": False},
        "splitLine": {"lineStyle": {"color": TRACK, "type": "dashed"}},
        "axisLabel": {"color": GREY},
    }


def day_label(day: dt.date) -> str:
    """Kurze deutsche Tagesbeschriftung, z. B. „Mo 16.11.“."""
    return f"{WEEKDAYS[day.weekday()]} {day:%d.%m.}"


def study_curve_chart(curve: TimeSeries, today: dt.date) -> dict[str, Any]:
    """Liniendiagramm: kumulierte Soll- gegen Ist-Lernstunden mit Markierung für heute."""
    labels = [f"{d:%d.%m.}" for d in curve.tage]
    options = _base()
    options.update(
        {
            "legend": {"data": ["Geplant", "Gelernt"], "top": 0, "textStyle": {"color": GREY}},
            "xAxis": {"type": "category", "data": labels, "boundaryGap": False, **_axis_style()},
            "yAxis": {"type": "value", "name": "Stunden", "nameTextStyle": {"color": GREY}, **_axis_style()},
            "series": [
                {
                    "name": "Geplant",
                    "type": "line",
                    "data": curve.soll,
                    "showSymbol": False,
                    "lineStyle": {"color": GREY, "width": 2, "type": "dashed"},
                    "itemStyle": {"color": GREY},
                },
                {
                    "name": "Gelernt",
                    "type": "line",
                    "data": curve.ist,
                    "showSymbol": False,
                    "lineStyle": {"color": BLUE, "width": 2},
                    "itemStyle": {"color": BLUE},
                    "markLine": {
                        "symbol": "none",
                        "label": {"formatter": "heute", "color": GREY},
                        "lineStyle": {"color": GREY, "type": "dotted"},
                        "data": [{"xAxis": f"{today:%d.%m.}"}] if today in curve.tage else [],
                    },
                },
            ],
        }
    )
    return options


def area_chart(areas: list[AreaProgress]) -> dict[str, Any]:
    """Gestapelte Balken je Prüfungsbereich: erledigt, begonnen, offen (in Stunden)."""
    names = [AREA_SHORT.get(a.bereich_id, a.bereich) for a in areas]
    options = _base()
    options["tooltip"] = {"trigger": "axis", "axisPointer": {"type": "shadow"}}
    options.update(
        {
            "legend": {"data": ["erledigt", "begonnen", "offen"], "top": 0, "textStyle": {"color": GREY}},
            "xAxis": {"type": "value", "name": "Stunden", "nameTextStyle": {"color": GREY}, **_axis_style()},
            "yAxis": {
                "type": "category",
                "data": names,
                "inverse": True,
                **_axis_style(),
                "splitLine": {"show": False},
            },
            "series": [
                _stack("erledigt", [a.erledigt_h for a in areas], BLUE),
                _stack("begonnen", [a.begonnen_h for a in areas], BLUE_LIGHT),
                _stack("offen", [a.offen_h for a in areas], TRACK),
            ],
        }
    )
    return options


def _stack(name: str, values: list[float], color: str) -> dict[str, Any]:
    return {
        "name": name,
        "type": "bar",
        "stack": "stand",
        "data": values,
        "barWidth": 14,
        "itemStyle": {"color": color, "borderColor": "transparent", "borderWidth": 1},
    }


def bar_chart(
    points: Sequence[tuple[dt.date, float]], unit: str, target: float | None = None
) -> dict[str, Any]:
    """Einfaches Säulendiagramm je Tag (Lernminuten oder fällige Karten), optional mit Ziellinie."""
    options = _base()
    options["grid"]["top"] = 16
    options["tooltip"] = {"trigger": "axis", "axisPointer": {"type": "shadow"}}
    series: dict[str, Any] = {
        "name": unit,
        "type": "bar",
        "data": [round(v) for _, v in points],
        "barMaxWidth": 22,
        "itemStyle": {"color": BLUE, "borderRadius": [4, 4, 0, 0]},
    }
    if target:
        series["markLine"] = {
            "symbol": "none",
            "label": {"formatter": f"Ziel {target:.0f}", "color": GREY},
            "lineStyle": {"color": GREY, "type": "dashed"},
            "data": [{"yAxis": round(target)}],
        }
    options.update(
        {
            "xAxis": {"type": "category", "data": [day_label(d) for d, _ in points], **_axis_style()},
            "yAxis": {"type": "value", "minInterval": 1, **_axis_style()},
            "series": [series],
        }
    )
    return options
