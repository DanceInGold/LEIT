"""Lokaler Lernstand in einer SQLite-Datei je Nutzer, mit Migrationen und JSON-Export.

Umsetzung von NF-03 (eine Datei, Export/Import als JSON, Backup durch Kopieren) und
NF-09 (Lernstand bleibt über Updates gültig: Schema-Migrationen mit Versionsnummer).
Bewusst mit der Standardbibliothek ``sqlite3`` statt SQLModel (siehe docs/entscheidungen.md).
"""

from __future__ import annotations

import datetime as dt
import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from ap_trainer.core.models import PlanSettings, TopicProgress

# Jede Migration hebt das Schema um genau eine Version an. Nie ändern, nur anhängen.
MIGRATIONS: list[str] = [
    """
    CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
    CREATE TABLE topic_progress (
        topic_id TEXT PRIMARY KEY,
        zustand TEXT NOT NULL DEFAULT 'offen',
        bekannt INTEGER NOT NULL DEFAULT 0,
        minuten INTEGER NOT NULL DEFAULT 0,
        geaendert TEXT NOT NULL
    );
    CREATE TABLE lesson_read (lesson_id TEXT PRIMARY KEY, gelesen_am TEXT NOT NULL);
    CREATE TABLE cards (
        card_id TEXT PRIMARY KEY,
        due TEXT NOT NULL,
        data TEXT NOT NULL
    );
    CREATE TABLE reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_id TEXT NOT NULL,
        grade INTEGER NOT NULL,
        reviewed_at TEXT NOT NULL
    );
    CREATE TABLE study_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT NOT NULL,
        minuten INTEGER NOT NULL,
        art TEXT NOT NULL,
        ref TEXT
    );
    """,
]

EXPORT_TABLES = ("settings", "topic_progress", "lesson_read", "cards", "reviews", "study_log")


def _now() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds")


class Store:
    """Zugriff auf die Lernstand-Datei. Eine Instanz je Programmlauf."""

    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self.migrate()

    def close(self) -> None:
        """Schließt die Datenbankverbindung."""
        self._conn.close()

    @contextmanager
    def _tx(self) -> Iterator[sqlite3.Connection]:
        with self._conn:
            yield self._conn

    @property
    def schema_version(self) -> int:
        """Aktuelle Schemaversion der Datei."""
        version: int = self._conn.execute("PRAGMA user_version").fetchone()[0]
        return version

    def migrate(self) -> None:
        """Spielt alle noch fehlenden Migrationen ein."""
        for number, script in enumerate(MIGRATIONS, start=1):
            if self.schema_version < number:
                with self._tx() as conn:
                    conn.executescript(script)
                    conn.execute(f"PRAGMA user_version = {number}")

    # --- Einstellungen -----------------------------------------------------------
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Liest eine Einstellung (JSON-Wert)."""
        row = self._conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return json.loads(row["value"]) if row else default

    def set_setting(self, key: str, value: Any) -> None:
        """Speichert eine Einstellung als JSON."""
        with self._tx() as conn:
            conn.execute(
                "INSERT INTO settings(key, value) VALUES(?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, json.dumps(value, ensure_ascii=False)),
            )

    def load_plan_settings(self) -> PlanSettings | None:
        """Plan-Einstellungen oder ``None``, wenn noch nicht eingerichtet."""
        raw = self.get_setting("plan")
        return PlanSettings.model_validate(raw) if raw else None

    def save_plan_settings(self, settings: PlanSettings) -> None:
        """Speichert die Plan-Einstellungen (LP-01, jederzeit änderbar)."""
        self.set_setting("plan", settings.model_dump(mode="json"))

    # --- Fortschritt -------------------------------------------------------------
    def progress(self) -> dict[str, TopicProgress]:
        """Lernstand aller Themen, die schon einmal angefasst wurden."""
        rows = self._conn.execute("SELECT topic_id, zustand, bekannt, minuten FROM topic_progress")
        return {
            r["topic_id"]: TopicProgress(
                topic_id=r["topic_id"], zustand=r["zustand"], bekannt=bool(r["bekannt"]), minuten=r["minuten"]
            )
            for r in rows
        }

    def set_progress(self, item: TopicProgress) -> None:
        """Speichert den Lernstand eines Themas."""
        with self._tx() as conn:
            conn.execute(
                "INSERT INTO topic_progress(topic_id, zustand, bekannt, minuten, geaendert) "
                "VALUES(?, ?, ?, ?, ?) ON CONFLICT(topic_id) DO UPDATE SET "
                "zustand = excluded.zustand, bekannt = excluded.bekannt, "
                "minuten = excluded.minuten, geaendert = excluded.geaendert",
                (item.topic_id, item.zustand, int(item.bekannt), item.minuten, _now()),
            )

    def mark_lesson_read(self, lesson_id: str) -> None:
        """Merkt sich, dass eine Lektion gelesen wurde."""
        with self._tx() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO lesson_read(lesson_id, gelesen_am) VALUES(?, ?)", (lesson_id, _now())
            )

    def read_lessons(self) -> set[str]:
        """IDs aller gelesenen Lektionen."""
        return {r[0] for r in self._conn.execute("SELECT lesson_id FROM lesson_read")}

    def log_study(self, minuten: int, art: str, ref: str | None = None, day: dt.date | None = None) -> None:
        """Protokolliert Lernzeit (Grundlage für FT-05 und LP-11)."""
        with self._tx() as conn:
            conn.execute(
                "INSERT INTO study_log(day, minuten, art, ref) VALUES(?, ?, ?, ?)",
                ((day or dt.date.today()).isoformat(), minuten, art, ref),
            )

    # --- Lernkarten --------------------------------------------------------------
    def card_ids(self) -> set[str]:
        """IDs aller angelegten Karten."""
        return {r[0] for r in self._conn.execute("SELECT card_id FROM cards")}

    def put_card(self, card_id: str, due: dt.datetime, data: dict[str, Any]) -> None:
        """Legt eine Karte an oder aktualisiert ihren Zustand."""
        with self._tx() as conn:
            conn.execute(
                "INSERT INTO cards(card_id, due, data) VALUES(?, ?, ?) "
                "ON CONFLICT(card_id) DO UPDATE SET due = excluded.due, data = excluded.data",
                (card_id, due.isoformat(), json.dumps(data)),
            )

    def get_card(self, card_id: str) -> tuple[dt.datetime, dict[str, Any]] | None:
        """Fälligkeit und Zustand einer Karte."""
        row = self._conn.execute("SELECT due, data FROM cards WHERE card_id = ?", (card_id,)).fetchone()
        return (dt.datetime.fromisoformat(row["due"]), json.loads(row["data"])) if row else None

    def due_cards(self, now: dt.datetime, limit: int) -> list[str]:
        """Fällige Karten, die am längsten überfälligen zuerst (WH-02)."""
        rows = self._conn.execute(
            "SELECT card_id FROM cards WHERE due <= ? ORDER BY due LIMIT ?", (now.isoformat(), limit)
        )
        return [r[0] for r in rows]

    def count_due(self, now: dt.datetime) -> int:
        """Anzahl fälliger Karten."""
        row = self._conn.execute("SELECT COUNT(*) FROM cards WHERE due <= ?", (now.isoformat(),)).fetchone()
        count: int = row[0]
        return count

    def log_review(self, card_id: str, grade: int, at: dt.datetime) -> None:
        """Protokolliert eine Bewertung."""
        with self._tx() as conn:
            conn.execute(
                "INSERT INTO reviews(card_id, grade, reviewed_at) VALUES(?, ?, ?)",
                (card_id, grade, at.isoformat()),
            )

    # --- Export / Import ---------------------------------------------------------
    def export_json(self) -> dict[str, Any]:
        """Kompletter Lernstand als JSON-fähiges Wörterbuch (NF-03)."""
        data: dict[str, Any] = {"format": "ap-trainer-lernstand", "schema": self.schema_version}
        for table in EXPORT_TABLES:
            rows = self._conn.execute(f"SELECT * FROM {table}").fetchall()
            data[table] = [dict(r) for r in rows]
        return data

    def import_json(self, data: dict[str, Any]) -> None:
        """Ersetzt den Lernstand durch einen Export. Ältere Exporte bleiben lesbar."""
        if data.get("format") != "ap-trainer-lernstand":
            raise ValueError("Keine Lernstand-Datei des AP-Trainers")
        if int(data.get("schema", 0)) > self.schema_version:
            raise ValueError("Export stammt aus einer neueren Programmversion – bitte erst aktualisieren")
        with self._tx() as conn:
            for table in EXPORT_TABLES:
                allowed = {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}
                conn.execute(f"DELETE FROM {table}")
                for row in data.get(table, []):
                    if not set(row) <= allowed:
                        raise ValueError(f"Unbekannte Spalten in Tabelle {table}: {set(row) - allowed}")
                    cols = ", ".join(row)
                    marks = ", ".join("?" for _ in row)
                    conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({marks})", tuple(row.values()))
