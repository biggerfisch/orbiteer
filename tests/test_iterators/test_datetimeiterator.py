#!/usr/bin/env python

from datetime import datetime, timedelta

import pytest

from orbiteer.iterators import DatetimeRangeIterator
from orbiteer.optimizers import TimedeltaRatioOptimizer


@pytest.fixture
def timedelta_ratio_optimizer() -> TimedeltaRatioOptimizer:
    return TimedeltaRatioOptimizer(goal=100.0, first_value=timedelta(seconds=30.0))


@pytest.fixture
def jan_1() -> datetime:
    return datetime.fromisoformat("2021-01-01T00:00:00+00:00")


@pytest.fixture
def feb_1() -> datetime:
    return datetime.fromisoformat("2021-02-01T00:00:00+00:00")


@pytest.fixture
def datetime_iter(
    timedelta_ratio_optimizer: TimedeltaRatioOptimizer,
    jan_1: datetime,
    feb_1: datetime,
) -> DatetimeRangeIterator:
    return DatetimeRangeIterator(timedelta_ratio_optimizer, left=jan_1, right=feb_1)


def test_compute_next_one_day_interval(datetime_iter: DatetimeRangeIterator, jan_1: datetime) -> None:
    next_interval = timedelta(days=1)
    # Force next value
    datetime_iter.optimizer.min_value = next_interval
    datetime_iter.optimizer.max_value = next_interval

    next_range = list(datetime_iter.compute_next_range(1))

    assert next_range[0] == jan_1
    assert next_range[1] == jan_1 + next_interval
    assert not datetime_iter.is_done
