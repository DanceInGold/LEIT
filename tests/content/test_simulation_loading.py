"""Tests für das Laden von Prüfungssimulationen (PS-01)."""

from __future__ import annotations

from pathlib import Path

import yaml

from ap_trainer.content.loader import load_package, load_package_or_raise

REAL = Path(__file__).parents[2] / "content" / "ap1"


def _part(nr: str, punkte: int, thema: str = "zahlen") -> dict[str, object]:
    return {
        "nr": nr,
        "punkte": punkte,
        "aufgabe": {
            "typ": "lueckentext",
            "thema": thema,
            "titel": "T",
            "frage": "F",
            "text": "Antwort {{1}}",
            "luecken": [{"antworten": ["x"]}],
            "loesungsweg": "x",
        },
    }


def _write(package_dir: Path, aufgaben: list[dict[str, object]]) -> None:
    data = {
        "titel": "Test",
        "ausgangssituation": "Lage",
        "quelle": "q",
        "status": "geprüft",
        "belege": [{"titel": "Beleg"}],
        "aufgaben": aufgaben,
    }
    (package_dir / "simulationen").mkdir(exist_ok=True)
    (package_dir / "simulationen" / "sim-test.yaml").write_text(yaml.safe_dump(data, allow_unicode=True))


def test_real_simulations_load_with_ids_and_level_five() -> None:
    package = load_package_or_raise(REAL)
    sim = package.simulationen["sim-01"]
    assert sim.punkte == 100 and len(sim.aufgaben) == 4
    tasks = sim.tasks()
    assert tasks[0].id == "sim-01-1a" and all(t.stufe == 5 for t in tasks)
    assert set(package.sim_tasks()) >= {t.id for t in tasks}


def test_points_must_sum_to_hundred(package_dir: Path) -> None:
    _write(package_dir, [{"nr": n, "titel": "A", "teilaufgaben": [_part("a", 20)]} for n in (1, 2, 3, 4)])
    _package, errors = load_package(package_dir)
    assert any("Summe der Punkte ist 80" in str(e) for e in errors)


def test_task_points_between_twenty_and_thirty(package_dir: Path) -> None:
    tasks = [{"nr": 1, "titel": "A", "teilaufgaben": [_part("a", 10)]}]
    tasks += [{"nr": n, "titel": "A", "teilaufgaben": [_part("a", 30)]} for n in (2, 3, 4)]
    _write(package_dir, tasks)
    _package, errors = load_package(package_dir)
    assert any("Aufgabe 1 hat 10 Punkte" in str(e) for e in errors)


def test_valid_simulation_inherits_source_and_status(package_dir: Path) -> None:
    _write(
        package_dir,
        [{"nr": n, "titel": "A", "teilaufgaben": [_part("a", 15), _part("b", 10)]} for n in (1, 2, 3, 4)],
    )
    package = load_package_or_raise(package_dir)
    task = package.simulationen["sim-test"].tasks()[1]
    assert task.id == "sim-test-1b" and task.quelle == "q" and task.status == "geprüft" and task.belege
