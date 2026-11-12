"""Tests für die mechanische Inventur (tools/inventory.py und tools/cli.py)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import cli, inventory


def _write(root: Path, rel: str, content: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_scan_ignores_os_leftovers(tmp_path: Path) -> None:
    _write(tmp_path, "eigene/a.md", "# A")
    _write(tmp_path, "eigene/.DS_Store", "x")
    entries = inventory.scan(tmp_path)
    assert [e.path for e in entries] == ["eigene/a.md"]
    assert entries[0].format == "md"
    assert entries[0].pages is None


def test_compare_detects_new_changed_deleted(tmp_path: Path) -> None:
    _write(tmp_path, "a.md", "eins")
    _write(tmp_path, "b.md", "zwei")
    old = inventory.scan(tmp_path)
    _write(tmp_path, "a.md", "eins geändert")
    (tmp_path / "b.md").unlink()
    _write(tmp_path, "c.md", "drei")
    changes = inventory.compare(old, inventory.scan(tmp_path))
    assert changes.new == ["c.md"]
    assert changes.changed == ["a.md"]
    assert changes.deleted == ["b.md"]
    assert changes.renamed == []
    assert changes.summary() == "1 neu, 1 geändert, 1 gelöscht"


def test_compare_detects_rename_by_checksum(tmp_path: Path) -> None:
    _write(tmp_path, "scan_0034.md", "DHCP")
    old = inventory.scan(tmp_path)
    (tmp_path / "scan_0034.md").rename(tmp_path / "lf03-dhcp.md")
    changes = inventory.compare(old, inventory.scan(tmp_path))
    assert changes.renamed == [("scan_0034.md", "lf03-dhcp.md")]
    assert changes.new == [] and changes.deleted == []


def test_no_changes_is_empty(tmp_path: Path) -> None:
    _write(tmp_path, "a.md", "eins")
    entries = inventory.scan(tmp_path)
    changes = inventory.compare(entries, inventory.scan(tmp_path))
    assert changes.is_empty
    assert changes.summary() == "keine Änderungen"


def test_cli_check_writes_nothing(tmp_path: Path) -> None:
    quellen = tmp_path / "quellen"
    _write(quellen, "a.md", "eins")
    manifest = tmp_path / "docs" / "manifest.json"
    code = cli.main(
        [
            "inventur",
            "--check",
            "--quellen",
            str(quellen),
            "--manifest",
            str(manifest),
            "--extrakte",
            str(tmp_path / "build"),
        ]
    )
    assert code == 0
    assert not manifest.exists()
    assert not (tmp_path / "build").exists()


def test_cli_run_writes_manifest_and_extracts(tmp_path: Path) -> None:
    quellen = tmp_path / "quellen"
    _write(quellen, "eigene/a.md", "Inhalt")
    manifest = tmp_path / "manifest.json"
    build = tmp_path / "build"
    args = ["inventur", "--quellen", str(quellen), "--manifest", str(manifest), "--extrakte", str(build)]
    assert cli.main(args) == 0
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert [f["path"] for f in data["files"]] == ["eigene/a.md"]
    assert (build / "eigene" / "a.md.txt").read_text(encoding="utf-8") == "Inhalt"


def test_cli_github_output(tmp_path: Path) -> None:
    quellen = tmp_path / "quellen"
    _write(quellen, "a.md", "eins")
    out = tmp_path / "gh_output"
    cli.main(
        [
            "inventur",
            "--check",
            "--quellen",
            str(quellen),
            "--manifest",
            str(tmp_path / "m.json"),
            "--github-output",
            str(out),
        ]
    )
    text = out.read_text(encoding="utf-8")
    assert "changed=true" in text
    assert "summary=1 neu" in text


def test_cli_check_reports_content_status(package_dir: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["check", "--paket", str(package_dir)]) == 0
    assert "Inhalte in Ordnung" in capsys.readouterr().out
    (package_dir / "glossar" / "bit.yaml").write_text("id: bit\n", encoding="utf-8")
    assert cli.main(["check", "--paket", str(package_dir)]) == 1
