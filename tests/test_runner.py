#!/usr/bin/env python

import unittest.mock as mock
from datetime import datetime

import pytest

from orbiteer.inputgenerators import DatetimeRangeGenerator
from orbiteer.optimizers import RatioOptimizer
from orbiteer.runner import OrbiteerRunner
from orbiteer.targets import CommandTarget, TargetMeasurementStrategy


@pytest.fixture
def ratio_optimizer() -> RatioOptimizer:
    return RatioOptimizer(goal=100.0, first_value=60.0)


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


@pytest.fixture
def command_target_output() -> CommandTarget:
    return CommandTarget(TargetMeasurementStrategy.OUTPUT, command_line=["echo"])


@pytest.fixture
def runner(datetime_generator: DatetimeRangeGenerator, command_target_output: CommandTarget) -> OrbiteerRunner:
    return OrbiteerRunner(datetime_generator, command_target_output)


def test_runner(runner: OrbiteerRunner, jan_1: datetime, feb_1: datetime) -> None:
    # A constant return value of 50 (which is half the target of 100) will cause an ever increasing range
    with mock.patch.object(runner.target, "run", return_value=50.0) as target_run:
        runner.run()

        # 30 days, starting with 60s, will double each time due to the return value
        # count:    1  2  3  4   5   6    7    8     9     10    11      12       13       14       15       16
        # duration: 1m 2m 4m 8m  16m 32m  1h4m 2h8m  4h16m 8h32m 17h4m   1d10h8m  2d20h16m 5d16h32m 11d9h4m  22d18h8m
        # total:    1m 3m 7m 15m 31m 1h3m 2h7m 4h15m 8h31m 17h3m 1d10h7m 2d20h15m 5d16h31m 11d9h3m  22d18h7m >30d
        assert target_run.call_count == 16
        # 0th call, 1st type of argument, 0th arg, first instance of the tuple
        assert target_run.mock_calls[0][1][0][0] == jan_1.isoformat()
        # LAST call, 1st type of argument, 0th arg, last instance of the tuple
        assert target_run.mock_calls[-1][1][0][1] == feb_1.isoformat()
