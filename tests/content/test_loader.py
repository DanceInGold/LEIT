"""Tests für Inhaltsmodell, Loader und Verweisprüfung."""

from __future__ import annotations

from pathlib import Path

import pytest

from ap_trainer.config import REPO_ROOT
from ap_trainer.content.checks import check_references
from ap_trainer.content.loader import (
    ContentLoadError,
    load_package,
    load_package_or_raise,
    split_frontmatter,
    split_sections,
)


def test_valid_package_loads(package_dir: Path) -> None:
    package, errors = load_package(package_dir)
    assert errors == []
    assert package is not None
    assert set(package.lektionen) == {"zahlen-1"}
    assert package.begriffe["bit"].langform == "Binary Digit"
    assert check_references(package) == []
    assert [les.id for les in package.lessons_for_topic("zahlen")] == ["zahlen-1"]


def test_real_content_package_is_valid() -> None:
    """Das echte Paket im Repo muss immer fehlerfrei laden (NF-08)."""
    package = load_package_or_raise(REPO_ROOT / "content" / "ap1")
    assert len(package.katalog.themen) > 50


def test_missing_section_is_reported(package_dir: Path) -> None:
    path = package_dir / "lektionen" / "zahlen-1.md"
    path.write_text(path.read_text(encoding="utf-8").replace("## Merksatz", "## Fazit"), encoding="utf-8")
    _, errors = load_package(package_dir)
    assert any("Pflichtabschnitte fehlen: Merksatz" in str(e) for e in errors)


def test_wrong_section_order_is_reported(package_dir: Path) -> None:
    path = package_dir / "lektionen" / "zahlen-1.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("## Worum geht es?\nZahlen.\n", "").replace(
        "## Merksatz", "## Worum geht es?\nZahlen.\n## Merksatz"
    )
    path.write_text(text, encoding="utf-8")
    _, errors = load_package(package_dir)
    assert any("Reihenfolge" in str(e) for e in errors)


def test_unknown_field_is_reported(package_dir: Path) -> None:
    path = package_dir / "glossar" / "bit.yaml"
    path.write_text(path.read_text(encoding="utf-8") + "farbe: blau\n", encoding="utf-8")
    _, errors = load_package(package_dir)
    assert any("farbe" in str(e) for e in errors)


def test_broken_references_are_reported(package_dir: Path) -> None:
    path = package_dir / "glossar" / "bit.yaml"
    text = path.read_text(encoding="utf-8").replace("verwandt: []", "verwandt: [byte]")
    path.write_text(text.replace("thema: zahlen", "thema: gibtsnicht"), encoding="utf-8")
    package, errors = load_package(package_dir)
    assert errors == [] and package is not None
    messages = [str(e) for e in check_references(package)]
    assert any("'byte' existiert nicht" in m for m in messages)
    assert any("unbekanntes Thema 'gibtsnicht'" in m for m in messages)


def test_dependency_cycle_is_reported(package_dir: Path) -> None:
    path = package_dir / "katalog.yaml"
    text = path.read_text(encoding="utf-8").replace(
        "stand_2025: aktiv, aufwand_h: 2}",
        "stand_2025: aktiv, voraussetzungen: [subnetting], aufwand_h: 2}",
        1,
    )
    path.write_text(text, encoding="utf-8")
    package, _ = load_package(package_dir)
    assert package is not None
    assert any("Zyklus" in str(e) for e in check_references(package))


def test_glossary_links_in_lessons_are_checked(package_dir: Path) -> None:
    path = package_dir / "lektionen" / "zahlen-1.md"
    path.write_text(path.read_text(encoding="utf-8").replace("glossar:bit", "glossar:byte"), encoding="utf-8")
    package, _ = load_package(package_dir)
    assert package is not None
    assert any("Glossar-Verweis 'byte'" in str(e) for e in check_references(package))


def test_load_or_raise_collects_all_errors(package_dir: Path) -> None:
    (package_dir / "paket.yaml").write_text("id: x\n", encoding="utf-8")
    with pytest.raises(ContentLoadError) as info:
        load_package_or_raise(package_dir)
    assert info.value.errors


def test_frontmatter_and_sections() -> None:
    head, body = split_frontmatter("---\na: 1\n---\n## Eins\nx\n## Zwei\ny\n")
    assert head == "a: 1"
    assert split_sections(body) == {"Eins": "x", "Zwei": "y"}
    with pytest.raises(ValueError):
        split_frontmatter("kein frontmatter")


def test_real_hardware_lessons_in_reading_order() -> None:
    package = load_package_or_raise(REPO_ROOT / "content" / "ap1")
    ids = [les.id for les in package.lessons_for_topic("hardware-komponenten")]
    assert ids == ["hardware-pc-aufbau", "hardware-cpu-ram", "hardware-netzteil-anschluesse"]
