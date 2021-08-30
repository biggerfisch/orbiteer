#!/usr/bin/env python

import enum
import time
import typing as t
from abc import ABC, abstractmethod

from orbiteer.iterators import RT


class TargetMeasurementStrategy(enum.Enum):
    DURATION = "Duration"
    STDOUT = "stdout"


class AbstractTarget(ABC):
    def __init__(self, measurement_strategy: TargetMeasurementStrategy) -> None:
        self.measurement_strategy = measurement_strategy

    @property
    def measurement_strategy(self) -> TargetMeasurementStrategy:
        return self._measurement_strategy

    @measurement_strategy.setter
    def measurement_strategy(self, new_value: TargetMeasurementStrategy) -> None:
        self._measurement_strategy = new_value

    @abstractmethod
    def _run_target(self, range_parameters: t.Iterable[str]) -> t.Optional[float]:
        """
        Runs the target and returns its output
        """

    def run(self, range_parameters: t.Iterable[RT]) -> float:
        """
        Runs the target and returns the ...
        """
        time_before_run = time.time()
        stdout = self._run_target([str(rp) for rp in range_parameters])
        duration = time.time() - time_before_run

        if self.measurement_strategy == TargetMeasurementStrategy.DURATION:
            return duration
        elif self.measurement_strategy == TargetMeasurementStrategy.STDOUT:
            if stdout is not None:
                return stdout
            else:
                return 0
        else:
            raise RuntimeError("Invalid measurement strategy")
