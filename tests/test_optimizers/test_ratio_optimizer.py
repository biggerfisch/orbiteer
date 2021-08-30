#!/usr/bin/env python

from datetime import timedelta

import pytest

from orbiteer.optimizers import TimedeltaRatioOptimizer


@pytest.fixture
def simple_first() -> timedelta:
    return timedelta(seconds=30.0)


@pytest.fixture
def timedelta_ro(simple_first: timedelta) -> TimedeltaRatioOptimizer:
    return TimedeltaRatioOptimizer(goal=100.0, first_value=simple_first)


@pytest.fixture
def damped_timedelta_ro(simple_first: timedelta) -> TimedeltaRatioOptimizer:
    return TimedeltaRatioOptimizer(goal=100.0, first_value=simple_first, damper=0.5)


def test_compute_at_goal_changes_nothing(timedelta_ro: TimedeltaRatioOptimizer, simple_first: timedelta) -> None:
    next_range = timedelta_ro.compute_next(100.0)

    assert next_range == simple_first


def test_returns_first_value_if_measurement_is_None(
    timedelta_ro: TimedeltaRatioOptimizer,
    simple_first: timedelta,
) -> None:
    next_range = timedelta_ro.compute_next(None)

    assert next_range == simple_first


def test_measure_half_goal_doubles(timedelta_ro: TimedeltaRatioOptimizer, simple_first: timedelta) -> None:
    next_range = timedelta_ro.compute_next(50.0)

    assert next_range == (simple_first * 2)


def test_measure_double_halves(timedelta_ro: TimedeltaRatioOptimizer, simple_first: timedelta) -> None:
    next_range = timedelta_ro.compute_next(200.0)

    assert next_range == (simple_first / 2)


def test_measure_half_damped(damped_timedelta_ro: TimedeltaRatioOptimizer, simple_first) -> None:
    next_range = damped_timedelta_ro.compute_next(50.0)

    assert next_range == (simple_first * 1.5)


def test_measure_double_damped(damped_timedelta_ro: TimedeltaRatioOptimizer, simple_first) -> None:
    next_range = damped_timedelta_ro.compute_next(200.0)

    assert next_range == (simple_first * 0.75)
