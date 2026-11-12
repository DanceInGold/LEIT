"""Rauchtests: Paket importierbar, Kommandozeile, Startabbruch bei fehlerhaften Inhalten."""

from __future__ import annotations

from pathlib import Path

import pytest

from ap_trainer import __version__
from ap_trainer.__main__ import main, parse_args


def test_version_is_semver() -> None:
    assert len(__version__.split(".")) == 3


def test_parse_args_defaults_and_lan() -> None:
    args = parse_args([])
    assert args.port == 8080 and not args.lan
    assert parse_args(["--lan", "--port", "9000"]).lan


def test_main_refuses_broken_content(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "paket.yaml").write_text("id: kaputt\n", encoding="utf-8")
    monkeypatch.setenv("AP_TRAINER_CONTENT", str(tmp_path))
    monkeypatch.setenv("AP_TRAINER_DATA", str(tmp_path / "db.sqlite"))
    assert main([]) == 2


def test_ui_pages_register(package_dir: Path, tmp_path: Path) -> None:
    """Nur mit installiertem NiceGUI (CI): alle Seiten lassen sich registrieren."""
    pytest.importorskip("nicegui")
    from ap_trainer.content.loader import load_package_or_raise
    from ap_trainer.service import Trainer
    from ap_trainer.storage.db import Store
    from ap_trainer.ui.app import build

    build(Trainer(load_package_or_raise(package_dir), Store(tmp_path / "db.sqlite")))
