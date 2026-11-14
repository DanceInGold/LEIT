"""Fortschritt: Themenkarte mit Ampelfarben (FT-02) und Fehlerprotokoll (FT-04).

Die Themenkarte zeigt je Prüfungsbereich eine Kachel pro Thema mit Beherrschungsgrad (FT-01);
ein Klick führt direkt zum Üben. Das Fehlerprotokoll listet falsch gelöste Aufgaben nach
Fehlerursache und bietet an, jede Aufgabe noch einmal zu lösen.
"""

from __future__ import annotations

import datetime as dt
from urllib.parse import quote

from nicegui import ui

from ap_trainer.content.models import Thema
from ap_trainer.core.mastery import AMPEL_LABELS, GREEN_FROM, YELLOW_FROM, Ampel, Mastery
from ap_trainer.core.mistakes import MistakeEntry, MistakeGroup
from ap_trainer.service import Trainer
from ap_trainer.ui.layout import frame

AMPEL_ORDER: tuple[Ampel, ...] = ("grün", "gelb", "rot", "grau")
# CSS-Klasse je Ampelfarbe (Farben im Seitenrahmen, hell und dunkel lesbar)
AMPEL_CLASS: dict[Ampel, str] = {
    "grün": "ampel-gruen",
    "gelb": "ampel-gelb",
    "rot": "ampel-rot",
    "grau": "ampel-grau",
}
AMPEL_ICON: dict[Ampel, str] = {
    "grün": "check_circle",
    "gelb": "change_history",
    "rot": "error",
    "grau": "radio_button_unchecked",
}
CAUSE_ICON = {
    "rechenfehler": "calculate",
    "begriff": "swap_horiz",
    "konzept": "psychology",
    "unbekannt": "help",
}


def _weighted_average(trainer: Trainer, values: dict[str, Mastery]) -> int | None:
    """Nach Prüfungsgewicht gemittelter Grad; nicht geübte Themen zählen mit 0 %."""
    total = sum(trainer.weights[t] for t in values)
    if not total or all(m.grad is None for m in values.values()):
        return None
    return round(sum(trainer.weights[t] * (m.grad or 0) for t, m in values.items()) / total)


def _summary(trainer: Trainer, values: dict[str, Mastery]) -> None:
    """Kennzahlen: gewichteter Gesamtgrad und Zahl der Themen je Ampelfarbe."""
    average = _weighted_average(trainer, values)
    with ui.row().classes("gap-3 flex-wrap w-full"):
        with ui.card().classes("p-3"):
            ui.label("–" if average is None else f"{average} %").classes("kpi-value")
            ui.label("Beherrschung gesamt (nach Gewicht)").classes("text-sm opacity-70")
        for colour in AMPEL_ORDER:
            count = sum(m.ampel == colour for m in values.values())
            with ui.card().classes(f"p-3 {AMPEL_CLASS[colour]}"):
                with ui.row().classes("items-center gap-1"):
                    ui.icon(AMPEL_ICON[colour])
                    ui.label(str(count)).classes("kpi-value")
                ui.label(AMPEL_LABELS[colour]).classes("text-sm opacity-80")


def _tile(topic: Thema, value: Mastery, stufe: int) -> None:
    """Eine Kachel der Themenkarte; Farbe und Symbol tragen die Ampel (nicht nur die Farbe)."""
    detail = (
        f"Qualität {value.qualitaet:.0%} · Reichweite {value.reichweite:.0%} · Frische {value.frische:.0%}"
        if value.grad is not None
        else "Noch keine Aufgabe gelöst"
    )
    with (
        ui.card()
        .classes(f"p-2 cursor-pointer hover:shadow-md {AMPEL_CLASS[value.ampel]}")
        .on("click", lambda: ui.navigate.to(f"/ueben/{topic.id}"))
        .tooltip(detail)
    ):
        with ui.row().classes("items-center gap-1 w-full flex-nowrap"):
            ui.icon(AMPEL_ICON[value.ampel]).classes("text-lg")
            ui.label(topic.titel).classes("text-sm font-medium grow leading-tight")
        with ui.row().classes("items-baseline gap-2 w-full"):
            ui.label("–" if value.grad is None else f"{value.grad} %").classes("text-xl font-semibold")
            ui.label(f"Stufe {stufe} · {value.versuche} Versuche").classes("text-xs opacity-70")


def _legend() -> None:
    texts = {
        "grün": f"ab {GREEN_FROM} %",
        "gelb": f"{YELLOW_FROM}–{GREEN_FROM - 1} %",
        "rot": f"unter {YELLOW_FROM} %",
        "grau": "noch nicht geübt",
    }
    with ui.row().classes("gap-3 flex-wrap text-sm"):
        for colour in AMPEL_ORDER:
            with ui.row().classes(f"items-center gap-1 px-2 rounded {AMPEL_CLASS[colour]}"):
                ui.icon(AMPEL_ICON[colour])
                ui.label(f"{AMPEL_LABELS[colour]}: {texts[colour]}")


def _topic_map(trainer: Trainer, values: dict[str, Mastery]) -> None:
    """Themenkarte: je Prüfungsbereich ein Raster, schwächste Themen zuerst."""
    katalog = trainer.package.katalog
    levels = {p.thema.id: p.stufe for p in trainer.practice_topics()}
    for bereich in katalog.bereiche:
        topics = [t for t in katalog.themen if t.bereich == bereich.id and t.id in values]
        if not topics:
            continue
        ui.label(bereich.name).classes("text-lg font-semibold mt-2")
        # Schwächste zuerst, nicht geübte am Ende; bei Gleichstand das höhere Prüfungsgewicht
        topics.sort(key=lambda t: (values[t.id].grad is None, values[t.id].grad or 0, -trainer.weights[t.id]))
        with ui.element("div").classes("grid grid-cols-2 sm:grid-cols-3 gap-2 w-full"):
            for topic in topics:
                _tile(topic, values[topic.id], levels.get(topic.id, 1))


def _local(moment: dt.datetime) -> str:
    """Zeitpunkt in Ortszeit, deutsch formatiert."""
    aware = moment if moment.tzinfo else moment.replace(tzinfo=dt.UTC)
    return aware.astimezone().strftime("%d.%m.%Y %H:%M")


def _entry_row(trainer: Trainer, entry: MistakeEntry) -> None:
    topic = trainer.package.katalog.by_id().get(entry.thema)
    with ui.row().classes("items-center gap-2 w-full flex-nowrap py-1 border-b border-gray-500/20"):
        ui.icon(
            "check_circle" if entry.behoben else "cancel", color="positive" if entry.behoben else "negative"
        )
        with ui.column().classes("grow gap-0"):
            ui.label(trainer.task_title(entry.aufgabe_id, entry.thema)).classes("font-medium")
            info = f"{topic.titel if topic else entry.thema} · zuletzt falsch {_local(entry.zuletzt_falsch)}"
            if entry.fehlversuche > 1:
                info += f" · {entry.fehlversuche}× falsch"
            if entry.behoben:
                info += " · inzwischen richtig gelöst"
            ui.label(info).classes("text-xs opacity-70")
        target = f"/ueben/{entry.thema}?aufgabe={quote(entry.aufgabe_id, safe='')}"
        ui.button("Nochmal", icon="replay", on_click=lambda t=target: ui.navigate.to(t)).props("flat dense")


def _group(trainer: Trainer, group: MistakeGroup) -> None:
    caption = f"{group.titel} – {group.offen} offen" if group.offen else f"{group.titel} – alle behoben"
    with ui.expansion(caption, icon=CAUSE_ICON[group.ursache], value=group.offen > 0).classes(
        "w-full border rounded"
    ):
        for entry in group.eintraege:
            _entry_row(trainer, entry)


def register(trainer: Trainer) -> None:
    """Registriert Fortschrittsseite und Fehlerprotokoll."""

    @ui.page("/fortschritt")
    def progress_page() -> None:
        values = trainer.masteries()
        with frame("Fortschritt"):
            ui.label(
                "Beherrschungsgrad je Thema aus deinen Übungen: Trefferquote nach Stufe, Hilfen, höchste "
                "sicher gelöste Stufe und Abstand zum letzten Erfolg. Klick auf eine Kachel zum Üben."
            ).classes("text-sm opacity-80")
            _summary(trainer, values)
            _legend()
            open_mistakes = sum(g.offen for g in trainer.mistakes())
            with ui.row().classes("gap-2 flex-wrap items-center"):
                ui.button(
                    f"Fehlerprotokoll ({open_mistakes} offen)",
                    icon="report",
                    on_click=lambda: ui.navigate.to("/fehler"),
                ).props("outline")
                ui.button("Mischtest", icon="shuffle", on_click=lambda: ui.navigate.to("/mischtest")).props(
                    "outline"
                )
                history = trainer.mixed_test_history()
                if history:
                    last = history[-1]
                    ui.label(
                        f"Letzter Mischtest {dt.date.fromisoformat(last['datum']):%d.%m.}: "
                        f"{last['richtig']}/{last['gesamt']} richtig"
                    ).classes("text-sm opacity-70")
            _topic_map(trainer, values)

    @ui.page("/fehler")
    def mistakes_page(alle: bool = False) -> None:
        groups = trainer.mistakes(include_fixed=alle)
        with frame("Fehlerprotokoll"):
            with ui.row().classes("items-center gap-3 flex-wrap"):
                ui.link("← Fortschritt", "/fortschritt")
                ui.switch(
                    "Behobene Fehler anzeigen",
                    value=alle,
                    on_change=lambda e: ui.navigate.to("/fehler?alle=true" if e.value else "/fehler"),
                )
            if not groups:
                ui.label(
                    "Keine offenen Fehler. Weiter so!" if not alle else "Noch keine Aufgabe falsch gelöst."
                ).classes("opacity-70")
            for group in groups:
                _group(trainer, group)
