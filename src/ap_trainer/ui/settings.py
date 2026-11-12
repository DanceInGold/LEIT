"""Einstellungen: Prüfungstermin, Lernbudget mit Wechseln, Lerntage, lernfreie Zeiten, Export.

Umsetzung von LP-01 (Budget-Presets 15/20/30 oder frei, jederzeit änderbar) und NF-03
(Lernstand als JSON exportieren und importieren).
"""

from __future__ import annotations

import datetime as dt
import json
from collections.abc import Callable
from typing import Any

from nicegui import events, ui
from pydantic import ValidationError

from ap_trainer.core.models import BudgetPeriod, DateRange, PlanSettings
from ap_trainer.service import Trainer
from ap_trainer.ui.layout import frame

WEEKDAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
PRESETS = [15, 20, 30]


def _date_input(label: str, row: dict[str, Any], key: str) -> None:
    ui.input(label).props("type=date dense").bind_value(row, key).classes("w-44")


def _row_actions(rows: list[dict[str, Any]], refresh: Callable[[], None]) -> tuple[Any, Any]:
    """Liefert Hilfsfunktionen zum Hinzufügen und Entfernen von Zeilen mit Neuzeichnen."""

    def add(row: dict[str, Any]) -> None:
        rows.append(row)
        refresh()

    def remove(index: int) -> None:
        rows.pop(index)
        refresh()

    return add, remove


def _budget_editor(state: dict[str, Any]) -> None:
    def set_hours(row: dict[str, Any], hours: int) -> None:
        row["stunden"] = hours
        rows.refresh()

    @ui.refreshable
    def rows() -> None:
        for index, row in enumerate(state["budget"]):
            with ui.row().classes("items-end gap-2 flex-wrap"):
                _date_input("ab", row, "ab")
                ui.number("Stunden/Woche", min=1, max=80, step=1).bind_value(row, "stunden").classes("w-36")
                for preset in PRESETS:
                    ui.button(str(preset), on_click=lambda r=row, p=preset: set_hours(r, p)).props(
                        "outline dense"
                    )
                if len(state["budget"]) > 1:
                    ui.button(icon="delete", on_click=lambda i=index: remove(i)).props("flat dense")

    add, remove = _row_actions(state["budget"], rows.refresh)
    ui.label("Lernbudget").classes("text-lg font-medium")
    ui.label(
        "Für einen späteren Wechsel (z. B. auf 30 Stunden) eine weitere Zeile mit Startdatum anlegen."
    ).classes("text-sm opacity-70")
    rows()
    ui.button(
        "Budgetwechsel hinzufügen",
        icon="add",
        on_click=lambda: add({"ab": dt.date.today().isoformat(), "stunden": 30}),
    ).props("flat")


def _holiday_editor(state: dict[str, Any]) -> None:
    @ui.refreshable
    def rows() -> None:
        for index, row in enumerate(state["lernfrei"]):
            with ui.row().classes("items-end gap-2 flex-wrap"):
                _date_input("von", row, "von")
                _date_input("bis", row, "bis")
                ui.input("Bezeichnung").props("dense").bind_value(row, "bezeichnung")
                ui.button(icon="delete", on_click=lambda i=index: remove(i)).props("flat dense")

    add, remove = _row_actions(state["lernfrei"], rows.refresh)
    ui.label("Lernfreie Zeiten").classes("text-lg font-medium")
    rows()
    today = dt.date.today().isoformat()
    ui.button(
        "Lernfreie Zeit hinzufügen",
        icon="add",
        on_click=lambda: add({"von": today, "bis": today, "bezeichnung": ""}),
    ).props("flat")


def _to_settings(state: dict[str, Any]) -> PlanSettings:
    return PlanSettings(
        pruefungsdatum=dt.date.fromisoformat(state["pruefungsdatum"]),
        lernbeginn=dt.date.fromisoformat(state["lernbeginn"]),
        budget=[
            BudgetPeriod(ab=dt.date.fromisoformat(r["ab"]), stunden_pro_woche=r["stunden"])
            for r in state["budget"]
        ],
        lerntage=[int(i) for i, on in state["tage"].items() if on],
        lernfrei=[
            DateRange(
                von=dt.date.fromisoformat(r["von"]),
                bis=dt.date.fromisoformat(r["bis"]),
                bezeichnung=r["bezeichnung"],
            )
            for r in state["lernfrei"]
        ],
        kalibrierung=state["kalibrierung"],
    )


def _from_settings(cfg: PlanSettings) -> dict[str, Any]:
    return {
        "pruefungsdatum": cfg.pruefungsdatum.isoformat(),
        "lernbeginn": cfg.lernbeginn.isoformat(),
        "budget": [{"ab": p.ab.isoformat(), "stunden": p.stunden_pro_woche} for p in cfg.budget],
        # Wörterbuch statt Liste, weil NiceGUI-Bindungen über Schlüssel arbeiten
        "tage": {str(i): i in cfg.lerntage for i in range(7)},
        "lernfrei": [
            {"von": r.von.isoformat(), "bis": r.bis.isoformat(), "bezeichnung": r.bezeichnung}
            for r in cfg.lernfrei
        ],
        "kalibrierung": cfg.kalibrierung,
    }


def _export_import(trainer: Trainer) -> None:
    ui.label("Lernstand sichern").classes("text-lg font-medium")

    def download() -> None:
        data = json.dumps(trainer.export(), ensure_ascii=False, indent=2).encode("utf-8")
        ui.download(data, f"lernstand-{dt.date.today().isoformat()}.json")

    def upload(event: events.UploadEventArguments) -> None:
        try:
            trainer.import_(json.loads(event.content.read().decode("utf-8")))
            ui.notify("Lernstand übernommen.", type="positive")
        except (ValueError, KeyError) as exc:
            ui.notify(f"Import fehlgeschlagen: {exc}", type="negative")

    with ui.row().classes("items-center gap-3 flex-wrap"):
        ui.button("Als JSON exportieren", icon="download", on_click=download)
        ui.upload(
            label="JSON importieren (ersetzt den aktuellen Stand)", on_upload=upload, auto_upload=True
        ).props("accept=.json")


def register(trainer: Trainer) -> None:
    """Registriert die Einstellungsseite."""

    @ui.page("/einstellungen")
    def settings_page() -> None:
        state = _from_settings(trainer.settings())
        with frame("Einstellungen"):
            with ui.row().classes("items-end gap-3 flex-wrap"):
                _date_input("Prüfungsdatum", state, "pruefungsdatum")
                _date_input("Lernbeginn", state, "lernbeginn")
            _budget_editor(state)
            ui.label("Lerntage").classes("text-lg font-medium")
            with ui.row().classes("gap-2 flex-wrap"):
                for index, name in enumerate(WEEKDAYS):
                    ui.checkbox(name).bind_value(state["tage"], str(index))
            _holiday_editor(state)
            max_reviews = ui.number(
                "Höchstens Wiederholungen pro Tag", value=trainer.max_reviews, min=5, max=500
            )

            def save() -> None:
                try:
                    trainer.save_settings(_to_settings(state))
                except (ValidationError, ValueError) as exc:
                    ui.notify(f"Bitte prüfen: {exc}", type="negative", multi_line=True)
                    return
                trainer.store.set_setting("max_wiederholungen", int(max_reviews.value or 60))
                ui.notify("Gespeichert – der Plan ist neu berechnet.", type="positive")

            ui.button("Speichern", icon="save", on_click=save).classes("mt-2")
            ui.separator()
            _export_import(trainer)
