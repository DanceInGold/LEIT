"""Mechanische Inventur von ``quellen/``: Dateiliste, Prüfsummen, Rohtext.

Das Modul bewertet nichts, ordnet nichts zu und pusht nichts. Es vergleicht
den aktuellen Stand von ``quellen/`` mit dem Manifest aus dem letzten Lauf
und meldet neue, geänderte, umbenannte und gelöschte Dateien (Kap. 6 der
Anforderungen, Schritt 1 der Pipeline).
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from tools.extract import extract_text, page_count

MANIFEST_VERSION = 1

# Dateien, die nie zum Material gehören (Betriebssystem-Reste).
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}


@dataclass(frozen=True)
class FileEntry:
    """Eine Datei in ``quellen/`` mit ihren mechanischen Kennzahlen."""

    path: str
    sha256: str
    size: int
    format: str
    pages: int | None = None


@dataclass
class Changes:
    """Unterschied zwischen Manifest und aktuellem Stand."""

    new: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    renamed: list[tuple[str, str]] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        """True, wenn sich nichts geändert hat."""
        return not (self.new or self.changed or self.deleted or self.renamed)

    def summary(self) -> str:
        """Kurzform für Issue-Titel, z. B. ``2 neu, 1 geändert``."""
        parts = []
        if self.new:
            parts.append(f"{len(self.new)} neu")
        if self.changed:
            parts.append(f"{len(self.changed)} geändert")
        if self.renamed:
            parts.append(f"{len(self.renamed)} umbenannt")
        if self.deleted:
            parts.append(f"{len(self.deleted)} gelöscht")
        return ", ".join(parts) if parts else "keine Änderungen"


def sha256_of(path: Path) -> str:
    """Berechnet die SHA-256-Prüfsumme einer Datei blockweise."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 16), b""):
            digest.update(block)
    return digest.hexdigest()


def iter_source_files(root: Path) -> Iterable[Path]:
    """Liefert alle Materialdateien unterhalb von ``root`` in stabiler Reihenfolge."""
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name not in IGNORED_NAMES:
            yield path


def scan(root: Path) -> list[FileEntry]:
    """Erfasst alle Dateien in ``root`` mit Prüfsumme, Größe, Format und Seitenzahl."""
    entries = []
    for path in iter_source_files(root):
        suffix = path.suffix.lower().lstrip(".") or "ohne"
        entries.append(
            FileEntry(
                path=path.relative_to(root).as_posix(),
                sha256=sha256_of(path),
                size=path.stat().st_size,
                format=suffix,
                pages=page_count(path),
            )
        )
    return entries


def load_manifest(path: Path) -> list[FileEntry]:
    """Liest das Manifest; fehlt es, gilt der Bestand als leer."""
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [FileEntry(**item) for item in data.get("files", [])]


def write_manifest(path: Path, entries: list[FileEntry]) -> None:
    """Schreibt das Manifest als lesbares, stabil sortiertes JSON."""
    data = {
        "version": MANIFEST_VERSION,
        "generated": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": [asdict(entry) for entry in sorted(entries, key=lambda e: e.path)],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def compare(old: list[FileEntry], new: list[FileEntry]) -> Changes:
    """Vergleicht zwei Bestände.

    Eine Datei, die unter neuem Pfad mit derselben Prüfsumme auftaucht, während
    der alte Pfad verschwunden ist, gilt als Umbenennung und nicht als neu.
    """
    old_by_path = {e.path: e for e in old}
    new_by_path = {e.path: e for e in new}
    changes = Changes()

    added = [p for p in new_by_path if p not in old_by_path]
    removed = [p for p in old_by_path if p not in new_by_path]
    changes.changed = sorted(
        p for p in new_by_path if p in old_by_path and new_by_path[p].sha256 != old_by_path[p].sha256
    )

    removed_by_hash: dict[str, list[str]] = {}
    for path in removed:
        removed_by_hash.setdefault(old_by_path[path].sha256, []).append(path)

    for path in sorted(added):
        candidates = removed_by_hash.get(new_by_path[path].sha256)
        if candidates:
            source = candidates.pop(0)
            changes.renamed.append((source, path))
            removed.remove(source)
        else:
            changes.new.append(path)

    changes.deleted = sorted(removed)
    return changes


def extract_all(root: Path, target: Path, paths: Iterable[str]) -> list[str]:
    """Legt den Rohtext der genannten Dateien unter ``target`` ab.

    Gibt die Pfade zurück, für die kein Text gewonnen werden konnte (z. B.
    Bilder oder Scans ohne Textebene) – diese muss Claude als Bild sichten.
    """
    without_text = []
    for rel in paths:
        text = extract_text(root / rel)
        if not text or not text.strip():
            without_text.append(rel)
            continue
        out = target / f"{rel}.txt"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    return without_text


def render_report(changes: Changes, entries: list[FileEntry]) -> str:
    """Erzeugt den Markdown-Bericht, der als Issue-Text dient."""
    lines = [f"## Inventur: {changes.summary()}", ""]
    sections = [
        ("Neu", changes.new),
        ("Geändert", changes.changed),
        ("Gelöscht", changes.deleted),
    ]
    for title, items in sections:
        if items:
            lines.append(f"### {title}")
            lines.extend(f"- `{item}`" for item in items)
            lines.append("")
    if changes.renamed:
        lines.append("### Umbenannt")
        lines.extend(f"- `{old}` → `{new}`" for old, new in changes.renamed)
        lines.append("")
    lines.append(f"Bestand insgesamt: {len(entries)} Dateien.")
    return "\n".join(lines) + "\n"
