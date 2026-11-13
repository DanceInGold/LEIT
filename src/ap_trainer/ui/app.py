"""Baut die Oberfläche aus den einzelnen Seiten zusammen."""

from __future__ import annotations

from ap_trainer.service import Trainer
from ap_trainer.ui import exercise, glossary, lesson, plan, practice, settings, today, topics


def build(trainer: Trainer) -> None:
    """Registriert alle Seiten für die übergebene Anwendungsschicht."""
    for page in (today, lesson, topics, exercise, glossary, practice, plan, settings):
        page.register(trainer)
