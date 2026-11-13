"""Tests für das Laden und Prüfen der Aufgabendateien (AU-01, NF-08)."""

from __future__ import annotations

from pathlib import Path

from ap_trainer.content.checks import check_references
from ap_trainer.content.loader import load_package, load_package_or_raise
from ap_trainer.tasks.validate import check_tasks

REPO_CONTENT = Path(__file__).resolve().parents[2] / "content" / "ap1"


def test_tasks_and_generators_are_loaded(package_dir: Path) -> None:
    package, errors = load_package(package_dir)
    assert errors == [] and package is not None
    assert set(package.aufgaben) == {"zahlen-nibble"}
    assert package.aufgaben["zahlen-nibble"].thema == "zahlen"
    assert package.generatoren == {"zahlen": ["zahlensysteme"]}
    assert [t.id for t in package.tasks_for_topic("zahlen")] == ["zahlen-nibble"]
    assert check_tasks(package) == []


def test_real_tasks_are_valid() -> None:
    package = load_package_or_raise(REPO_CONTENT)
    assert package.aufgaben and check_tasks(package) == []


def test_wrong_topic_and_unknown_generator(package_dir: Path) -> None:
    file = package_dir / "aufgaben" / "zahlen.yaml"
    text = file.read_text(encoding="utf-8").replace("[zahlensysteme]", "[gibt-es-nicht]")
    file.write_text(text.replace("  - id: zahlen-nibble", "  - id: zahlen-nibble\n    thema: hardware"))
    package, errors = load_package(package_dir)
    assert any("thema passt nicht zum Dateinamen" in str(e) for e in errors)
    assert package is not None
    assert any("unbekannter Generator" in str(e) for e in check_tasks(package))


def test_tasks_for_dropped_topics_and_missing_sources(package_dir: Path) -> None:
    raid = (package_dir / "aufgaben" / "zahlen.yaml").read_text(encoding="utf-8")
    raid = raid.replace("zahlen-nibble", "raid-1").replace("    belege: [{titel: Testbeleg}]\n", "")
    (package_dir / "aufgaben" / "raid.yaml").write_text(raid, encoding="utf-8")
    package, errors = load_package(package_dir)
    assert errors == [] and package is not None
    messages = [str(e) for e in check_references(package)]
    assert any("entfallen" in m for m in messages)
    assert any("raid-1: belege fehlen" in m for m in messages)


def test_wrong_model_solution_is_reported(package_dir: Path) -> None:
    file = package_dir / "aufgaben" / "zahlen.yaml"
    file.write_text(
        file.read_text(encoding="utf-8")
        + """
  - id: zahlen-rechnung
    typ: rechnung
    stufe: 2
    titel: Rechnung
    frage: Rechne.
    schritte:
      - {frage: Wert, antwort: "zehn", erklaerung: x}
      - {frage: Dual, antwort: "101", format: dual, erklaerung: y, falsch: [{antwort: "0101", warum: z}]}
    loesungsweg: so
    quelle: neu
    belege: [{titel: Beleg}]
    status: ungeprüft
""",
        encoding="utf-8",
    )
    package, _ = load_package(package_dir)
    assert package is not None
    messages = [str(e) for e in check_tasks(package)]
    assert any("Schritt 1: Antwort „zehn“" in m for m in messages)
    assert any("Schritt 2: Falschantwort „0101“ zählt als richtig" in m for m in messages)
