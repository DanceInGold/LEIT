"""Zufallsfälle für Generator-Tests: Hypothesis, wenn installiert, sonst eine feste Seed-Schleife.

In der CI ist Hypothesis installiert und sucht gezielt nach Gegenbeispielen (NF-07). In schlanken
Umgebungen ohne Hypothesis laufen dieselben Tests mit 1.000 festen Zufalls-Seeds – so bleibt das
Abnahmekriterium „1.000 Testläufe ohne falsche Lösung“ überall prüfbar.
"""

from __future__ import annotations

import random
from collections.abc import Callable

CASES = 1000
SEED_MAX = 2**32 - 1

type SeedTest = Callable[[int], None]


def random_cases(cases: int = CASES) -> Callable[[SeedTest], Callable[[], None]]:
    """Dekorator: ruft den Test mit ``cases`` verschiedenen Seeds auf (Parameter ``seed``)."""
    try:
        from hypothesis import HealthCheck, given, settings
        from hypothesis import strategies as st
    except ImportError:  # pragma: no cover - nur ohne Hypothesis
        return _seed_loop(cases)

    def decorate(test: SeedTest) -> Callable[[], None]:
        wrapped = given(seed=st.integers(0, SEED_MAX))(test)
        configured: Callable[[], None] = settings(
            max_examples=cases, deadline=None, suppress_health_check=[HealthCheck.too_slow]
        )(wrapped)
        return configured

    return decorate


def _seed_loop(cases: int) -> Callable[[SeedTest], Callable[[], None]]:
    def decorate(test: SeedTest) -> Callable[[], None]:
        def run() -> None:
            seeds = random.Random(20270224)
            for _ in range(cases):
                seed = seeds.randint(0, SEED_MAX)
                try:
                    test(seed)
                except AssertionError as exc:
                    raise AssertionError(f"Seed {seed}: {exc}") from exc

        run.__name__ = test.__name__
        run.__doc__ = test.__doc__
        return run

    return decorate
