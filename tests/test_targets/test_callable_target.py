#!/usr/bin/env python

import pytest

from orbiteer.targets import CallableTarget, TargetMeasurementStrategy


@pytest.fixture
def callable_target_duration() -> CallableTarget:
    return CallableTarget(TargetMeasurementStrategy.DURATION, to_call=lambda x: x)


@pytest.fixture
def callable_target_output() -> CallableTarget:
    return CallableTarget(TargetMeasurementStrategy.OUTPUT, to_call=lambda x: x)


def test_callable_target_duration_time_measured(callable_target_duration: CallableTarget) -> None:
    duration = callable_target_duration.run(["1"])

    assert duration > 0.0


def test_callable_target_output_measurement(callable_target_output: CallableTarget) -> None:
    duration = callable_target_output.run(["123"])

    assert duration == 123


def test_raises_with_no_to_call() -> None:
    with pytest.raises(ValueError):
        CallableTarget(TargetMeasurementStrategy.OUTPUT)
