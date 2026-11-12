"""Startseite „Heute“: Tagesration mit Wiederholungen, nächster Lektion und Ampel (LP-05).

Die Tagesration ist mit einem Klick erreichbar, weil sie die Startseite ist (NF-05).
"""

from __future__ import annotations

from nicegui import ui

from ap_trainer.core.models import PHASE_NAMES, ScheduleStatus
from ap_trainer.core.today import DailyRation
from ap_trainer.service import Trainer
from ap_trainer.ui.layout import AMPEL_COLORS, frame


def _setup_hint(trainer: Trainer) -> None:
    if trainer.is_configured():
        return
    with ui.card().classes("w-full bg-amber-100 dark:bg-amber-900"):
        ui.label("Willkommen! Lege zuerst Prüfungstermin und Lernbudget fest.").classes("font-medium")
        ui.button("Zu den Einstellungen", on_click=lambda: ui.navigate.to("/einstellungen"))


def _status_card(ration: DailyRation, status: ScheduleStatus) -> None:
    with ui.card().classes("w-full"), ui.row().classes("items-center gap-4 flex-wrap"):
        ui.label(f"Noch {ration.tage_bis_pruefung} Tage bis zur Prüfung").classes("text-lg font-medium")
        ui.badge(PHASE_NAMES[ration.phase])
        ui.badge(status.ampel, color=AMPEL_COLORS[status.ampel])
        ui.label(f"Heute geplant: {ration.minuten_budget} Minuten").classes("text-sm opacity-80")
    ui.label(status.prognose).classes("text-sm opacity-80")


def _reviews_card(ration: DailyRation) -> None:
    with ui.card().classes("w-full"):
        ui.label("1 · Wiederholen").classes("text-lg font-medium")
        if ration.wiederholungen:
            ui.label(f"{ration.wiederholungen} Lernkarten sind fällig – die kommen vor neuem Stoff.")
            ui.button("Wiederholung starten", icon="style", on_click=lambda: ui.navigate.to("/lernkarten"))
        else:
            ui.label("Nichts fällig. Lernkarten entstehen, sobald du eine Lektion als gelesen markierst.")


def _lesson_card(ration: DailyRation) -> None:
    with ui.card().classes("w-full"):
        ui.label("2 · Neue Lektion").classes("text-lg font-medium")
        if ration.thema is None:
            ui.label("Alle Themen sind abgeschlossen – Zeit für Vertiefung und Simulationen.")
            return
        ui.label(f"Thema: {ration.thema.titel}")
        if ration.lektion:
            ui.label(f"{ration.lektion.titel} · ca. {ration.lektion.dauer_min} Min.").classes("opacity-80")
            target = f"/lektion/{ration.lektion.id}"
            ui.button("Lektion öffnen", icon="school", on_click=lambda: ui.navigate.to(target))
        elif ration.lektion_fehlt:
            ui.label(
                "Für dieses Thema ist die Lektion noch in Arbeit – sie kommt mit dem nächsten Update."
            ).classes("text-amber-700 dark:text-amber-300")


def _practice_card() -> None:
    with ui.card().classes("w-full"):
        ui.label("3 · Üben").classes("text-lg font-medium")
        ui.label("Aufgaben und Rechentrainer folgen in Phase 2. Bis dahin: Lernkarten und Merksätze.")


def register(trainer: Trainer) -> None:
    """Registriert die Startseite."""

    @ui.page("/")
    def today_page() -> None:
        with frame("Heute"):
            _setup_hint(trainer)
            ration = trainer.ration()
            _status_card(ration, trainer.status())
            _reviews_card(ration)
            _lesson_card(ration)
            _practice_card()
