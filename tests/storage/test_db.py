"""Tests für den lokalen Lernstand: Migration, Fortschritt, Karten, Export/Import."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pytest

from ap_trainer.core.models import BudgetPeriod, PlanSettings, TopicProgress
from ap_trainer.storage.db import MIGRATIONS, Store

NOW = dt.datetime(2026, 11, 16, 8, 0, tzinfo=dt.UTC)


@pytest.fixture
def store(tmp_path: Path) -> Store:
    return Store(tmp_path / "lernstand.sqlite")


def test_migrations_set_schema_version(store: Store) -> None:
    assert store.schema_version == len(MIGRATIONS)
    store.migrate()  # zweimal ausführen ist harmlos
    assert store.schema_version == len(MIGRATIONS)


def test_settings_roundtrip(store: Store) -> None:
    assert store.load_plan_settings() is None
    cfg = PlanSettings(
        pruefungsdatum=dt.date(2027, 2, 24),
        lernbeginn=dt.date(2026, 11, 16),
        budget=[BudgetPeriod(ab=dt.date(2026, 11, 16), stunden_pro_woche=15)],
    )
    store.save_plan_settings(cfg)
    assert store.load_plan_settings() == cfg


def test_progress_and_lessons(store: Store) -> None:
    store.set_progress(TopicProgress(topic_id="zahlen", zustand="laufend", minuten=30))
    store.set_progress(TopicProgress(topic_id="zahlen", zustand="fertig", minuten=45))
    assert store.progress()["zahlen"].zustand == "fertig"
    store.mark_lesson_read("zahlen-1")
    store.mark_lesson_read("zahlen-1")
    assert store.read_lessons() == {"zahlen-1"}


def test_due_cards_ordered_and_limited(store: Store) -> None:
    store.put_card("a", NOW - dt.timedelta(days=2), {})
    store.put_card("b", NOW - dt.timedelta(days=1), {})
    store.put_card("c", NOW + dt.timedelta(days=1), {})
    assert store.due_cards(NOW, limit=10) == ["a", "b"]
    assert store.due_cards(NOW, limit=1) == ["a"]
    assert store.count_due(NOW) == 2


def test_export_import_roundtrip_on_other_device(store: Store, tmp_path: Path) -> None:
    """Abnahmekriterium: Export und Re-Import liefern identische Fortschrittswerte."""
    store.set_progress(TopicProgress(topic_id="zahlen", zustand="fertig", minuten=45))
    store.put_card("bit:def", NOW, {"x": 1})
    store.log_review("bit:def", 3, NOW)
    store.set_setting("max_wiederholungen", 40)
    exported = json.loads(json.dumps(store.export_json()))
    other = Store(tmp_path / "anderes-geraet.sqlite")
    other.import_json(exported)
    assert other.progress() == store.progress()
    assert other.get_card("bit:def") == store.get_card("bit:def")
    assert other.get_setting("max_wiederholungen") == 40
    assert other.export_json() == store.export_json()


def test_import_rejects_foreign_or_malicious_files(store: Store) -> None:
    with pytest.raises(ValueError):
        store.import_json({"format": "etwas anderes"})
    bad = store.export_json()
    bad["settings"] = [{"key": "a", "value": "1", "x); DROP TABLE cards; --": 1}]
    with pytest.raises(ValueError):
        store.import_json(bad)
    newer = store.export_json() | {"schema": 999}
    with pytest.raises(ValueError):
        store.import_json(newer)


def test_old_schema_is_migrated(tmp_path: Path) -> None:
    """NF-09: Ein Lernstand aus Version 1 bleibt nutzbar und bekommt die neue Spalte."""
    import sqlite3

    path = tmp_path / "alt.sqlite"
    conn = sqlite3.connect(path)
    conn.executescript(MIGRATIONS[0])
    conn.execute("PRAGMA user_version = 1")
    conn.execute("INSERT INTO study_log(day, minuten, art) VALUES('2026-11-16', 30, 'lektion')")
    conn.commit()
    conn.close()
    store = Store(path)
    assert store.schema_version == len(MIGRATIONS)
    store.log_study(0, "wiederholung", day=dt.date(2026, 11, 16), sekunden=90)
    assert store.minutes_by_day() == {dt.date(2026, 11, 16): 31.5}


def test_card_due_dates(store: Store) -> None:
    store.put_card("a", NOW, {})
    assert store.card_due_dates() == [NOW]
