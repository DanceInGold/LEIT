"""Rohtext und Seitenzahl aus PDF, HTML und Markdown gewinnen.

Die Bibliotheken für PDF und HTML sind optional importiert: Fehlen sie,
liefert das Modul ``None`` statt abzubrechen, damit die Inventur auch in
einer schlanken Umgebung (z. B. der GitHub Action) Prüfsummen bilden kann.
"""

from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)
# pypdf meldet reparierbare Strukturfehler (z. B. aus Browser-Drucken) sehr ausführlich.
logging.getLogger("pypdf").setLevel(logging.ERROR)

TEXT_FORMATS = {".md", ".txt", ".csv", ".yaml", ".yml"}


def page_count(path: Path) -> int | None:
    """Seitenzahl einer PDF-Datei, sonst ``None``."""
    if path.suffix.lower() != ".pdf":
        return None
    try:
        from pypdf import PdfReader
    except ImportError:  # pragma: no cover - abhängig von der Umgebung
        return None
    try:
        return len(PdfReader(str(path)).pages)
    except Exception as exc:  # beschädigte oder verschlüsselte PDF
        log.warning("Seitenzahl nicht lesbar: %s (%s)", path, exc)
        return None


def extract_text(path: Path) -> str | None:
    """Rohtext einer Datei oder ``None``, wenn das Format keinen Text hat."""
    suffix = path.suffix.lower()
    if suffix in TEXT_FORMATS:
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".pdf":
        return _pdf_text(path)
    if suffix in {".html", ".htm"}:
        return _html_text(path)
    if suffix == ".xlsx":
        return _xlsx_text(path)
    return None


def _pdf_text(path: Path) -> str | None:
    try:
        import pdfplumber
    except ImportError:  # pragma: no cover - abhängig von der Umgebung
        return None
    try:
        with pdfplumber.open(str(path)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
    except Exception as exc:
        log.warning("PDF-Text nicht lesbar: %s (%s)", path, exc)
        return None
    return "\n\n".join(f"--- Seite {i} ---\n{text}" for i, text in enumerate(pages, start=1))


def _html_text(path: Path) -> str | None:
    try:
        from bs4 import BeautifulSoup
    except ImportError:  # pragma: no cover - abhängig von der Umgebung
        return None
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    lines = (line.strip() for line in soup.get_text("\n").splitlines())
    return "\n".join(line for line in lines if line)


def _xlsx_text(path: Path) -> str | None:
    try:
        import openpyxl
    except ImportError:  # pragma: no cover - abhängig von der Umgebung
        return None
    try:
        workbook = openpyxl.load_workbook(str(path), read_only=True, data_only=False)
    except Exception as exc:
        log.warning("Tabelle nicht lesbar: %s (%s)", path, exc)
        return None
    blocks = []
    for sheet in workbook.worksheets:
        rows = []
        for row in sheet.iter_rows(values_only=True):
            cells = ["" if value is None else str(value) for value in row]
            if any(cells):
                rows.append(" | ".join(cells).rstrip(" |"))
        blocks.append(f"--- Blatt {sheet.title} ---\n" + "\n".join(rows))
    workbook.close()
    return "\n\n".join(blocks)
