"""Lernplan: Phasen, Wochen, Machbarkeit und Zeitplan-Ampel (LP-04, LP-09, LP-10)."""

from __future__ import annotations

from nicegui import ui

from ap_trainer.core.models import PHASE_NAMES, LearningPlan
from ap_trainer.service import Trainer
from ap_trainer.ui.layout import AMPEL_COLORS, frame


def _feasibility_card(plan: LearningPlan, trainer: Trainer) -> None:
    check = plan.machbarkeit
    status = trainer.status()
    with ui.card().classes("w-full"):
        with ui.row().classes("items-center gap-3 flex-wrap"):
            ui.label("Machbarkeit").classes("text-lg font-medium")
            ui.badge(status.ampel, color=AMPEL_COLORS[status.ampel])
        ui.label(
            f"Bedarf {check.benoetigt_h:.0f} h · Aufbauphase {check.verfuegbar_aufbau_h:.0f} h · "
            f"bis zur Prüfung insgesamt {check.verfuegbar_gesamt_h:.0f} h"
        )
        if check.machbar:
            ui.label(f"Puffer: {check.puffer_h:.0f} Stunden. Der Plan geht auf.").classes("text-positive")
            return
        ui.label(f"Es fehlen {-check.puffer_h:.0f} Stunden.").classes("text-negative font-medium")
        ui.label(
            f"Vorschlag 1: Lernbudget um etwa {check.zusaetzlich_pro_woche_h:.1f} Stunden pro Woche erhöhen."
        )
        titles = {t.topic_id: t.titel for t in plan.themen}
        cut = ", ".join(titles.get(tid, tid) for tid in check.kuerzung[:8])
        more = " …" if len(check.kuerzung) > 8 else ""
        ui.label(f"Vorschlag 2: am wenigsten prüfungsrelevante Themen kürzen: {cut}{more}")


def _phases(plan: LearningPlan) -> None:
    with ui.row().classes("gap-2 flex-wrap"):
        for phase, start in plan.phasenbeginn.items():
            ui.chip(f"{PHASE_NAMES[phase]} ab {start:%d.%m.%Y}", icon="flag").props("outline")


def _weeks_table(plan: LearningPlan) -> None:
    titles = {t.topic_id: t.titel for t in plan.themen}
    rows = [
        {
            "nr": w.nummer,
            "woche": f"{w.montag:%d.%m.}",
            "phase": PHASE_NAMES[w.phase],
            "stunden": w.verfuegbar_h,
            "themen": ", ".join(titles[t] for t in w.themen) or "–",
        }
        for w in plan.wochen
    ]
    columns = [
        {"name": "nr", "label": "Woche", "field": "nr"},
        {"name": "woche", "label": "ab", "field": "woche"},
        {"name": "phase", "label": "Phase", "field": "phase"},
        {"name": "stunden", "label": "Stunden", "field": "stunden"},
        {
            "name": "themen",
            "label": "Themen",
            "field": "themen",
            "align": "left",
            "classes": "whitespace-normal",
        },
    ]
    ui.table(columns=columns, rows=rows, row_key="nr").classes("w-full").props("dense flat wrap-cells")


def _unplanned(plan: LearningPlan) -> None:
    missing = [t for t in plan.themen if not t.eingeplant]
    if missing:
        with ui.expansion(f"{len(missing)} Themen passen nicht mehr in die Aufbauphase", icon="warning"):
            for topic in missing:
                ui.label(f"{topic.titel} ({topic.stunden:.1f} h, Gewicht {topic.gewicht:.1f})")


def register(trainer: Trainer) -> None:
    """Registriert die Planseite."""

    @ui.page("/plan")
    def plan_page() -> None:
        plan = trainer.plan()
        with frame("Lernplan"):
            _feasibility_card(plan, trainer)
            _phases(plan)
            _weeks_table(plan)
            _unplanned(plan)
            ui.label(
                "Der Plan rechnet sich bei jedem Aufruf neu: verpasste Tage und ein geändertes Budget "
                "verschieben ihn automatisch."
            ).classes("text-sm opacity-70")
