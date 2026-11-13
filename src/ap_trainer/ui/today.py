"""Startseite „Heute“: Kennzahlen, die Tagesration und ein analytischer Überblick (LP-05, LP-10).

Oben vier Kennzahlen, darunter knapp, was heute dran ist, dann vier Diagramme:
Soll und Ist der Lernzeit, Fortschritt je Prüfungsbereich, Lernzeit der letzten Tage und
die Wiederholungen der kommenden Woche.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

from nicegui import ui

from ap_trainer.content.aufgaben import STUFEN_NAMEN
from ap_trainer.core.models import PHASE_NAMES
from ap_trainer.core.today import DailyRation
from ap_trainer.service import Trainer
from ap_trainer.ui import charts
from ap_trainer.ui.layout import AMPEL_COLORS, frame


def _setup_hint(trainer: Trainer) -> None:
    if trainer.is_configured():
        return
    with ui.card().classes("w-full bg-amber-100 dark:bg-amber-900"):
        ui.label("Willkommen! Lege zuerst Prüfungstermin und Lernbudget fest.").classes("font-medium")
        ui.button("Zu den Einstellungen", on_click=lambda: ui.navigate.to("/einstellungen"))


def _kpi(label: str, value: str, hint: str) -> None:
    with ui.card().classes("grow basis-36 gap-0"):
        ui.label(label).classes("text-xs uppercase tracking-wide opacity-60")
        ui.label(value).classes("kpi-value")
        ui.label(hint).classes("text-xs opacity-70")


def _kpi_row(trainer: Trainer, ration: DailyRation) -> None:
    numbers = trainer.kpis()
    status = trainer.status()
    with ui.row().classes("w-full gap-3 items-stretch"):
        _kpi("Bis zur Prüfung", f"{numbers.tage_bis_pruefung} Tage", PHASE_NAMES[ration.phase])
        _kpi("Stoff erledigt", f"{numbers.fortschritt:.0%}", f"Soll heute: {status.soll_anteil:.0%}")
        _kpi("Lernzeit Woche", f"{numbers.woche_ist_h:.1f} h", f"von {numbers.woche_soll_h:.0f} h geplant")
        _kpi("Karten fällig", str(numbers.karten_faellig), "heute")
    with ui.row().classes("items-center gap-2"):
        ui.badge(status.ampel, color=AMPEL_COLORS[status.ampel])
        ui.label(status.prognose).classes("text-sm opacity-80")


def _todo_item(icon: str, title: str, detail: str, action: tuple[str, str] | None) -> None:
    with ui.row().classes("items-center gap-3 w-full flex-nowrap"):
        ui.icon(icon, size="sm").classes("opacity-70")
        with ui.column().classes("grow gap-0"):
            ui.label(title).classes("font-medium")
            ui.label(detail).classes("text-sm opacity-70")
        if action:
            label, target = action
            ui.button(label, on_click=lambda: ui.navigate.to(target)).props("unelevated")


def _practice_item(trainer: Trainer, ration: DailyRation) -> None:
    """Übungsblock: Aufgaben zum aktuellen Thema, sonst zur Übersicht (LP-05)."""
    topic_id = ration.thema.topic_id if ration.thema else None
    pool = trainer.pools.get(topic_id) if topic_id else None
    if topic_id and pool is not None and not pool.is_empty():
        level = trainer.level(topic_id).stufe
        detail = f"{ration.thema.titel if ration.thema else ''} · Stufe {level} · {STUFEN_NAMEN[level]}"
        _todo_item("edit_note", "Üben", detail, ("Üben", f"/ueben/{topic_id}"))
        return
    _todo_item("edit_note", "Üben", "Aufgaben zu allen Themen mit Übungen", ("Übersicht", "/ueben"))


def _todo_card(ration: DailyRation, trainer: Trainer) -> None:
    with ui.card().classes("w-full"):
        ui.label(f"Heute dran · {ration.minuten_budget} Minuten").classes("text-lg font-medium")
        reviews = ration.wiederholungen
        _todo_item(
            "style",
            f"{reviews} Lernkarten wiederholen" if reviews else "Keine Karten fällig",
            "kommt vor neuem Stoff" if reviews else "Karten entstehen nach jedem gelesenen Kapitel",
            ("Starten", "/lernkarten") if reviews else None,
        )
        ui.separator()
        if ration.thema is None:
            _todo_item("celebration", "Alle Themen abgeschlossen", "Zeit für Vertiefung und Simulation", None)
        elif ration.lektion:
            _todo_item(
                "school",
                ration.lektion.titel,
                f"{ration.thema.titel} · ca. {ration.lektion.dauer_min} Min.",
                ("Öffnen", f"/lektion/{ration.lektion.id}"),
            )
        else:
            target = f"/thema/{ration.thema.topic_id}"
            _todo_item("hourglass_top", ration.thema.titel, "Kapitel sind in Arbeit", ("Thema", target))
        ui.separator()
        _practice_item(trainer, ration)


def _chart_card(title: str, options: dict[str, Any], height: str = "h-64") -> None:
    with ui.card().classes("w-full md:w-[calc(50%-0.375rem)] gap-1"):
        ui.label(title).classes("font-medium")
        ui.echart(options).classes(f"w-full {height}")


def _charts(trainer: Trainer) -> None:
    today = dt.date.today()
    ui.label("Überblick").classes("text-xl font-semibold mt-2")
    with ui.row().classes("w-full gap-3"):
        curve = charts.study_curve_chart(trainer.study_curve(today), today)
        _chart_card("Lernzeit: geplant und gelernt", curve)
        _chart_card("Fortschritt je Prüfungsbereich", charts.area_chart(trainer.area_progress()))
        _chart_card(
            "Lernminuten der letzten 14 Tage",
            charts.bar_chart(
                trainer.daily_minutes(today), "Minuten", target=trainer.daily_target_minutes(today)
            ),
            "h-52",
        )
        forecast = charts.bar_chart(trainer.review_forecast(), "Karten")
        _chart_card("Fällige Karten der nächsten 7 Tage", forecast, "h-52")


def register(trainer: Trainer) -> None:
    """Registriert die Startseite."""

    @ui.page("/")
    def today_page() -> None:
        with frame("Heute"):
            _setup_hint(trainer)
            ration = trainer.ration()
            _kpi_row(trainer, ration)
            _todo_card(ration, trainer)
            _charts(trainer)
