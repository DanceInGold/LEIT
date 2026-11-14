"""Beispiel-Lernstand für die Bildschirmfotos: wird befüllt, ohne die Oberfläche zu starten."""

from __future__ import annotations

from pathlib import Path

from ap_trainer.storage.db import Store
from tools.screenshots import LIGHT_PAGES, MOBILE_PAGES, PAGES, seed


def test_seed_fills_settings_attempts_study_time_and_a_simulation(tmp_path: Path) -> None:
    data = tmp_path / "lernstand.sqlite"
    seed(data)
    store = Store(data)
    assert store.load_plan_settings() is not None
    assert store.attempts() and store.sim_runs()
    store.close()


def test_light_and_mobile_pages_are_part_of_the_page_list() -> None:
    names = {name for name, _path in PAGES}
    assert names.issuperset(LIGHT_PAGES | MOBILE_PAGES)
    assert len(names) == len(PAGES)
