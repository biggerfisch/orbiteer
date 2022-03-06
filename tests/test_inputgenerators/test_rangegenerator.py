#!/usr/bin/env python

from datetime import datetime, timedelta

import pytest

from orbiteer.inputgenerators import DatetimeRangeGenerator
from orbiteer.optimizers import RatioOptimizer


@pytest.fixture
def ratio_optimizer() -> RatioOptimizer:
    return RatioOptimizer(goal=100.0, first_value=30.0)


@pytest.fixture
def jan_1() -> datetime:
    return datetime.fromisoformat("2021-01-01T00:00:00+00:00")


@pytest.fixture
def feb_1() -> datetime:
    return datetime.fromisoformat("2021-02-01T00:00:00+00:00")


@pytest.fixture
def datetime_generator(
    ratio_optimizer: RatioOptimizer,
    jan_1: datetime,
    feb_1: datetime,
) -> DatetimeRangeGenerator:
    return DatetimeRangeGenerator(ratio_optimizer, left=jan_1, right=feb_1)


def test_compute_next_one_day_interval(datetime_generator: DatetimeRangeGenerator, jan_1: datetime) -> None:
    next_interval = 1
    # Force next value
    datetime_generator.optimizer.min_value = next_interval
    datetime_generator.optimizer.max_value = next_interval

    next_range = list(datetime_generator.compute_next_input(1))

    assert next_range[0] == jan_1.isoformat()
    assert next_range[1] == (jan_1 + timedelta(seconds=next_interval)).isoformat()
    assert not datetime_generator.is_done
