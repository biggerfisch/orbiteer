#!/usr/bin/env python

import enum
import time
import typing as t
from abc import ABC, abstractmethod

from typing_extensions import Protocol


class Stringable(Protocol):
    def __str__(self) -> str:
        ...


class TargetMeasurementStrategy(enum.Enum):
    DURATION = "duration"
    OUTPUT = "output"


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

    def run(self, range_parameters: t.Iterable[Stringable]) -> float:
        """
        Runs the target and returns the ...
        """
        time_before_run = time.time()
        output = self._run_target([str(rp) for rp in range_parameters])
        duration = time.time() - time_before_run

        if self.measurement_strategy == TargetMeasurementStrategy.DURATION:
            return duration
        elif self.measurement_strategy == TargetMeasurementStrategy.OUTPUT:
            if output is not None:
                return output
            else:
                return 0
        else:
            raise RuntimeError("Invalid measurement strategy")
