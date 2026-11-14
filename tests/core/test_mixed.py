"""Tests für den wöchentlichen Mischtest (WH-03)."""

from __future__ import annotations

import datetime as dt
import itertools
import random
from collections import Counter

from ap_trainer.core.mixed import mixed_test_due, mixed_topics, topic_weight


def test_weight_prefers_weak_and_heavy_topics() -> None:
    assert topic_weight(2.0, None) == 3.0
    assert topic_weight(2.0, 100) == 1.0
    assert topic_weight(4.0, 50) > topic_weight(2.0, 50)


def test_every_topic_once_before_repeating_and_never_twice_in_a_row() -> None:
    weights = {"a": 1.0, "b": 1.0, "c": 1.0, "d": 1.0}
    for seed in range(200):
        order = mixed_topics(weights, {}, random.Random(seed), size=10)
        assert len(order) == 10
        assert sorted(order[:4]) == ["a", "b", "c", "d"]
        assert all(x != y for x, y in itertools.pairwise(order))


def test_weak_topics_come_more_often() -> None:
    counts: Counter[str] = Counter()
    for seed in range(300):
        counts.update(
            mixed_topics({"stark": 1.0, "schwach": 1.0}, {"stark": 100, "schwach": 0}, random.Random(seed), 9)
        )
    assert counts["schwach"] > counts["stark"]


def test_no_topics_no_test() -> None:
    assert mixed_topics({}, {}, random.Random(1)) == []


def test_due_weekly_from_two_topics() -> None:
    today = dt.date(2027, 1, 18)
    assert not mixed_test_due(None, today, ["a"])
    assert mixed_test_due(None, today, ["a", "b"])
    assert not mixed_test_due(today - dt.timedelta(days=6), today, ["a", "b"])
    assert mixed_test_due(today - dt.timedelta(days=7), today, ["a", "b"])
