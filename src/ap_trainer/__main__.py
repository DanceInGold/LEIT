"""Einstieg des Programms (``uv run ap-trainer``).

In Phase 0 nur ein Platzhalter; die Oberfläche (NiceGUI) folgt in Phase 1.
"""

from ap_trainer import __version__


def main() -> int:
    """Startet den Lernbegleiter."""
    print(f"AP1-Lernbegleiter {__version__} – Gerüst aus Phase 0, die Oberfläche folgt in Phase 1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
