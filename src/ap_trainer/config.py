"""Einstellungen des Programms: Pfade zu Inhalten und Lernstand.

Beide Pfade lassen sich über Umgebungsvariablen überschreiben, z. B. für Tests oder
einen zweiten Nutzer auf demselben Rechner.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class AppConfig:
    """Pfade, die das Programm braucht."""

    content_dir: Path
    data_file: Path


def load_config() -> AppConfig:
    """Liest die Pfade aus der Umgebung oder nimmt die Vorgaben.

    - ``AP_TRAINER_CONTENT``: Ordner des Inhaltspakets (Vorgabe: ``content/ap1`` im Repo)
    - ``AP_TRAINER_DATA``: Lernstand-Datei (Vorgabe: ``~/.ap-trainer/lernstand.sqlite``,
      also außerhalb des Repos, NF-04)
    """
    content = Path(os.environ.get("AP_TRAINER_CONTENT", REPO_ROOT / "content" / "ap1"))
    data = Path(os.environ.get("AP_TRAINER_DATA", Path.home() / ".ap-trainer" / "lernstand.sqlite"))
    return AppConfig(content_dir=content, data_file=data)
