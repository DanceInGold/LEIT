"""Rauchtest: Das Paket lässt sich importieren und starten."""

from ap_trainer import __version__
from ap_trainer.__main__ import main


def test_version_is_semver() -> None:
    assert len(__version__.split(".")) == 3


def test_main_returns_zero() -> None:
    assert main() == 0
