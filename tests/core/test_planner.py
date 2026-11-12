"""Tests für Gewichtung, Wochenplan, Machbarkeit und Zeitplan-Ampel."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

from ap_trainer.content.loader import ContentPackage, load_package
from ap_trainer.core.models import BudgetPeriod, DateRange, PlanSettings, TopicProgress
from ap_trainer.core.planner import build_plan, daily_hours, needed_hours, order_topics, schedule_status
from ap_trainer.core.weighting import compute_weights

MONDAY = dt.date(2026, 11, 16)


@pytest.fixture
def pkg(package_dir: Path) -> ContentPackage:
    package, errors = load_package(package_dir)
    assert package is not None and not errors
    return package


def settings(weeks: int = 4, hours: float = 10, **extra: object) -> PlanSettings:
    return PlanSettings(
        pruefungsdatum=MONDAY + dt.timedelta(weeks=weeks),
        lernbeginn=MONDAY,
        budget=[BudgetPeriod(ab=MONDAY, stunden_pro_woche=hours)],
        **extra,  # type: ignore[arg-type]
    )


def test_weights_sum_to_100_and_dropped_is_zero(pkg: ContentPackage) -> None:
    weights = compute_weights(pkg.katalog)
    assert sum(weights.values()) == pytest.approx(100, abs=0.01)
    assert weights["raid"] == 0
    # Subnetting hat 30 Einzelpunkte, Zahlensysteme bekommt den Clusterrest 30 → gleich schwer
    assert weights["subnetting"] == pytest.approx(weights["zahlen"])
    assert weights["hardware"] > weights["extra"] > 0


def test_prerequisites_come_first_even_with_lower_weight(pkg: ContentPackage) -> None:
    weights = {"zahlen": 1.0, "subnetting": 90.0, "hardware": 50.0, "extra": 0.1}
    relevant = [t for t in pkg.katalog.themen if t.is_relevant]
    order = [t.id for t in order_topics(relevant, weights)]
    assert order.index("zahlen") < order.index("subnetting")
    # Zahlensysteme erbt die Priorität von Subnetting und kommt deshalb vor Hardware
    assert order[:2] == ["zahlen", "subnetting"]
    assert order[-1] == "extra"


def test_needed_hours_includes_review_bonus_and_known_topics(pkg: ContentPackage) -> None:
    topic = pkg.katalog.by_id()["subnetting"]
    assert needed_hours(topic, None, pkg.katalog, 1.0) == 6.0
    known = TopicProgress(topic_id="subnetting", bekannt=True)
    assert needed_hours(topic, known, pkg.katalog, 1.0) == pytest.approx(1.8)
    started = TopicProgress(topic_id="subnetting", minuten=120)
    assert needed_hours(topic, started, pkg.katalog, 1.0) == 4.0


def test_daily_hours_respect_study_days_and_holidays() -> None:
    cfg = settings(weeks=1, hours=10, lerntage=[0, 2], lernfrei=[DateRange(von=MONDAY, bis=MONDAY)])
    days = dict(daily_hours(cfg, MONDAY))
    assert days[MONDAY] == 0  # lernfrei
    assert days[MONDAY + dt.timedelta(days=2)] == 5  # Mittwoch
    assert days[MONDAY + dt.timedelta(days=1)] == 0  # Dienstag ist kein Lerntag


def test_plan_phases_and_feasibility(pkg: ContentPackage) -> None:
    plan = build_plan(pkg.katalog, settings(weeks=4, hours=10), {}, MONDAY)
    assert plan.phasenbeginn["aufbau"] == MONDAY
    assert plan.phasenbeginn["aufbau"] < plan.phasenbeginn["vertiefung"] < plan.phasenbeginn["pruefung"]
    # 40 h verfügbar, Aufbau 60 % = 24 h, Bedarf (2+5+4+1) * 1,2 = 14,4 h
    assert plan.machbarkeit.verfuegbar_gesamt_h == 40
    assert plan.machbarkeit.verfuegbar_aufbau_h == 24
    assert plan.machbarkeit.benoetigt_h == pytest.approx(14.4)
    assert plan.machbarkeit.machbar
    assert all(t.eingeplant for t in plan.themen)
    assert "raid" not in [t.topic_id for t in plan.themen]
    assert len(plan.wochen) == 4


def test_shortfall_suggests_budget_and_cuts_optional_first(pkg: ContentPackage) -> None:
    plan = build_plan(pkg.katalog, settings(weeks=2, hours=5), {}, MONDAY)
    assert not plan.machbarkeit.machbar
    assert plan.machbarkeit.zusaetzlich_pro_woche_h > 0
    assert plan.machbarkeit.kuerzung[0] == "extra"
    assert any(not t.eingeplant for t in plan.themen)


def test_budget_switch_without_restart(pkg: ContentPackage) -> None:
    low = settings(weeks=4, hours=5)
    switched = low.model_copy(
        update={
            "budget": [*low.budget, BudgetPeriod(ab=MONDAY + dt.timedelta(weeks=2), stunden_pro_woche=20)]
        }
    )
    assert switched.hours_per_week(MONDAY) == 5
    assert switched.hours_per_week(MONDAY + dt.timedelta(weeks=3)) == 20
    before = build_plan(pkg.katalog, low, {}, MONDAY).machbarkeit
    after = build_plan(pkg.katalog, switched, {}, MONDAY).machbarkeit
    assert after.verfuegbar_gesamt_h > before.verfuegbar_gesamt_h


def test_missed_days_shift_plan(pkg: ContentPackage) -> None:
    """Abnahmekriterium: Nach 3 verpassten Tagen passt sich der Plan an und warnt."""
    cfg = settings(weeks=2, hours=10)
    on_time = build_plan(pkg.katalog, cfg, {}, MONDAY)
    late = build_plan(pkg.katalog, cfg, {}, MONDAY + dt.timedelta(days=3))
    assert late.themen[0].beginn == MONDAY + dt.timedelta(days=3)
    assert late.machbarkeit.verfuegbar_gesamt_h < on_time.machbarkeit.verfuegbar_gesamt_h
    tight = settings(weeks=2, hours=12.5)  # 25 h gesamt, Aufbau 15 h ≥ Bedarf 14,4 h
    assert build_plan(pkg.katalog, tight, {}, MONDAY).machbarkeit.machbar
    assert not build_plan(pkg.katalog, tight, {}, MONDAY + dt.timedelta(days=3)).machbarkeit.machbar


def test_done_topics_leave_the_plan(pkg: ContentPackage) -> None:
    progress = {"zahlen": TopicProgress(topic_id="zahlen", zustand="fertig")}
    plan = build_plan(pkg.katalog, settings(), progress, MONDAY)
    assert "zahlen" not in [t.topic_id for t in plan.themen]
    assert plan.current_topic(set()) is not None


def test_schedule_status_traffic_light(pkg: ContentPackage) -> None:
    cfg = settings(weeks=4, hours=10)
    start = schedule_status(pkg.katalog, cfg, {}, MONDAY)
    assert start.ampel == "im Plan"
    later = MONDAY + dt.timedelta(days=14)
    assert schedule_status(pkg.katalog, cfg, {}, later).ampel == "im Verzug"
    all_done = {t: TopicProgress(topic_id=t, zustand="fertig") for t in ("zahlen", "subnetting", "hardware")}
    assert schedule_status(pkg.katalog, cfg, all_done, later).ampel == "im Plan"


def test_settings_validation() -> None:
    with pytest.raises(ValueError):
        settings(lerntage=[7])
    with pytest.raises(ValueError):
        PlanSettings(
            pruefungsdatum=MONDAY, lernbeginn=MONDAY, budget=[BudgetPeriod(ab=MONDAY, stunden_pro_woche=5)]
        )
