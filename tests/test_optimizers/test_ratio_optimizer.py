#!/usr/bin/env python

import pytest

from orbiteer.optimizers import RatioOptimizer


@pytest.fixture
def simple_first() -> float:
    return 30.0


@pytest.fixture
def simple_ro(simple_first: float) -> RatioOptimizer:
    return RatioOptimizer(goal=100.0, first_value=simple_first, round_places=False)


@pytest.fixture
def rounded_ro(simple_first: float) -> RatioOptimizer:
    return RatioOptimizer(goal=100.0, first_value=simple_first)


@pytest.fixture
def damped_ro(simple_first: float) -> RatioOptimizer:
    return RatioOptimizer(goal=100.0, first_value=simple_first, damper=0.5, round_places=False)


def test_compute_at_goal_changes_nothing(simple_ro: RatioOptimizer, simple_first: float) -> None:
    next_range = simple_ro.compute_next(100.0)

    assert next_range == simple_first


def test_returns_first_value_if_measurement_is_None(
    simple_ro: RatioOptimizer,
    simple_first: float,
) -> None:
    next_range = simple_ro.compute_next(None)

    assert next_range == simple_first


def test_measure_half_goal_doubles(simple_ro: RatioOptimizer, simple_first: float) -> None:
    next_range = simple_ro.compute_next(50.0)

    assert next_range == (simple_first * 2)


def test_measure_double_halves(simple_ro: RatioOptimizer, simple_first: float) -> None:
    next_range = simple_ro.compute_next(200.0)

    assert next_range == (simple_first / 2)


def test_measure_half_damped(damped_ro: RatioOptimizer, simple_first: float) -> None:
    next_range = damped_ro.compute_next(50.0)

    assert next_range == (simple_first * 1.5)


def test_measure_double_damped(damped_ro: RatioOptimizer, simple_first: float) -> None:
    next_range = damped_ro.compute_next(200.0)

    assert next_range == (simple_first * 0.75)


def test_measure_0_returns_last(simple_ro: RatioOptimizer, simple_first: float) -> None:
    next_range = simple_ro.compute_next(0)

    assert next_range == simple_first


def test_rounded_ro(rounded_ro: RatioOptimizer, simple_ro: RatioOptimizer) -> None:
    measurement = 80

    next_range_rounded = rounded_ro.compute_next(measurement)
    next_range_raw = simple_ro.compute_next(measurement)

    assert next_range_rounded == 38.0
    assert next_range_raw == 37.5
