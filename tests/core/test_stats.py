"""Tests für die Auswertungen des Überblicks."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

from ap_trainer.content.loader import load_package
from ap_trainer.core.models import BudgetPeriod, PlanSettings, TopicProgress
from ap_trainer.core.stats import area_progress, daily_minutes, kpis, review_forecast, study_curve

MONDAY = dt.date(2026, 11, 16)
CFG = PlanSettings(
    pruefungsdatum=MONDAY + dt.timedelta(weeks=2),
    lernbeginn=MONDAY,
    budget=[BudgetPeriod(ab=MONDAY, stunden_pro_woche=10)],
)


def test_study_curve_soll_and_ist() -> None:
    minutes = {MONDAY: 90.0, MONDAY + dt.timedelta(days=1): 30.0}
    curve = study_curve(CFG, minutes, MONDAY + dt.timedelta(days=1))
    assert curve.soll[0] == 2.0 and curve.soll[4] == 10.0  # 10 h auf Mo–Fr
    assert curve.ist[:2] == [1.5, 2.0]
    assert curve.ist[2] is None  # Zukunft
    assert curve.soll[-1] == 20.0


def test_area_progress_counts_done_and_started(package_dir: Path) -> None:
    package, _ = load_package(package_dir)
    assert package is not None
    progress = {
        "zahlen": TopicProgress(topic_id="zahlen", zustand="fertig"),
        "subnetting": TopicProgress(topic_id="subnetting", zustand="laufend", minuten=60),
    }
    (area,) = area_progress(package.katalog, progress)
    # zahlen 2 h, subnetting 5 h, hardware 4 h, jeweils + 20 % Zuschlag; Zusatz und entfallen zählen nicht
    assert area.erledigt_h == 2.4
    assert area.begonnen_h == 1.0
    assert area.offen_h == pytest.approx(6.0 - 1.0 + 4.8)
    assert 0 < area.anteil < 1


def test_daily_minutes_and_forecast() -> None:
    rows = daily_minutes({MONDAY: 45.4}, MONDAY, days=3)
    assert rows == [(MONDAY - dt.timedelta(2), 0), (MONDAY - dt.timedelta(1), 0), (MONDAY, 45)]
    now = dt.datetime(2026, 11, 16, 9, tzinfo=dt.UTC)
    due = [now - dt.timedelta(days=3), now, now + dt.timedelta(days=1), now + dt.timedelta(days=30)]
    forecast = dict(review_forecast(due, now, days=7))
    assert forecast[MONDAY] == 2 and forecast[MONDAY + dt.timedelta(1)] == 1
    assert sum(forecast.values()) == 3


def test_kpis(package_dir: Path) -> None:
    package, _ = load_package(package_dir)
    assert package is not None
    wednesday = MONDAY + dt.timedelta(days=2)
    result = kpis(package.katalog, CFG, {}, {MONDAY: 60.0, wednesday: 30.0}, 4, wednesday)
    assert result.tage_bis_pruefung == 12
    assert result.woche_ist_h == 1.5 and result.woche_soll_h == 10
    assert result.fortschritt == 0 and result.karten_faellig == 4
