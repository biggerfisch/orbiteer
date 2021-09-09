#!/usr/bin/env python

import pytest

from orbiteer.targets import CommandTarget, TargetMeasurementStrategy


@pytest.fixture
def command_target_duration() -> CommandTarget:
    return CommandTarget(TargetMeasurementStrategy.DURATION, ["echo"])


@pytest.fixture
def command_target_output() -> CommandTarget:
    return CommandTarget(TargetMeasurementStrategy.OUTPUT, ["echo"])


def test_command_target_duration_time_measured(command_target_duration: CommandTarget) -> None:
    duration = command_target_duration.run(["1"])

    assert duration > 0.0


def test_command_target_output_measurement(command_target_output: CommandTarget) -> None:
    duration = command_target_output.run(["1"])

    assert duration == 1


def test_run_bad_measurement_strat_raises(command_target_output: CommandTarget) -> None:
    # This is intentionally invalid
    command_target_output.measurement_strategy = "nope"  # type: ignore

    with pytest.raises(Exception):
        command_target_output.run(["1"])
