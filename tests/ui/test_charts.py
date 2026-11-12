"""Tests für die Diagramm-Optionen der Startseite (reine Daten, ohne Browser)."""

from __future__ import annotations

import datetime as dt

from ap_trainer.core.stats import AreaProgress, TimeSeries
from ap_trainer.ui import charts

MONDAY = dt.date(2026, 11, 16)


def test_day_label_is_german() -> None:
    assert charts.day_label(MONDAY) == "Mo 16.11."
    assert charts.day_label(MONDAY + dt.timedelta(days=6)) == "So 22.11."


def test_study_curve_marks_today_and_keeps_gaps() -> None:
    days = [MONDAY + dt.timedelta(days=i) for i in range(3)]
    curve = TimeSeries(tage=days, soll=[2.0, 4.0, 6.0], ist=[1.0, None, None])
    options = charts.study_curve_chart(curve, MONDAY)
    planned, learned = options["series"]
    assert planned["lineStyle"]["type"] == "dashed" and planned["lineStyle"]["color"] == charts.GREY
    assert learned["data"] == [1.0, None, None]
    assert learned["markLine"]["data"] == [{"xAxis": "16.11."}]
    assert options["legend"]["data"] == ["Geplant", "Gelernt"]


def test_study_curve_without_today_has_no_marker() -> None:
    curve = TimeSeries(tage=[MONDAY], soll=[1.0], ist=[None])
    options = charts.study_curve_chart(curve, MONDAY - dt.timedelta(days=1))
    assert options["series"][1]["markLine"]["data"] == []


def test_area_chart_stacks_three_states() -> None:
    area = AreaProgress(bereich_id="b03", bereich="IT-Systeme", erledigt_h=2, begonnen_h=1, offen_h=5)
    options = charts.area_chart([area])
    assert options["yAxis"]["data"] == ["IT-Systeme"]
    assert [s["data"] for s in options["series"]] == [[2], [1], [5]]
    assert {s["stack"] for s in options["series"]} == {"stand"}


def test_bar_chart_rounds_and_adds_target() -> None:
    points = [(MONDAY, 44.6), (MONDAY + dt.timedelta(days=1), 0.0)]
    options = charts.bar_chart(points, "Minuten", target=180)
    (series,) = options["series"]
    assert series["data"] == [45, 0]
    assert series["markLine"]["data"] == [{"yAxis": 180}]
    assert options["xAxis"]["data"] == ["Mo 16.11.", "Di 17.11."]


def test_bar_chart_without_target() -> None:
    options = charts.bar_chart([(MONDAY, 3)], "Karten")
    assert "markLine" not in options["series"][0]
