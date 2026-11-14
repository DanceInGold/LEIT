"""Baut die Oberfläche aus den einzelnen Seiten zusammen."""

from __future__ import annotations

import datetime as dt

from ap_trainer.service import Trainer
from ap_trainer.ui import (
    exercise,
    glossary,
    layout,
    lesson,
    mixed,
    operators,
    plan,
    practice,
    progress,
    settings,
    simulation,
    today,
    topics,
)

# Einstellung im Lernstand: True = heller Modus
LIGHT_KEY = "oberflaeche_hell"


def build(trainer: Trainer) -> None:
    """Registriert alle Seiten für die übergebene Anwendungsschicht."""

    def exam_dates() -> tuple[dt.date, dt.date]:
        settings = trainer.settings()
        return settings.pruefungsdatum, settings.lernbeginn

    # Hell/Dunkel gilt für alle Seiten und überlebt den Neustart (Vorgabe: dunkel, E-43)
    layout.configure(
        exam_dates=exam_dates,
        get_light=lambda: bool(trainer.store.get_setting(LIGHT_KEY, False)),
        set_light=lambda value: trainer.store.set_setting(LIGHT_KEY, value),
    )
    for page in (
        today,
        lesson,
        topics,
        exercise,
        mixed,
        operators,
        simulation,
        progress,
        glossary,
        practice,
        plan,
        settings,
    ):
        page.register(trainer)
