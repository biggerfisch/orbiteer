#!/usr/bin/env python

import typing as t
from abc import ABC, abstractmethod

from orbiteer.shared_types import Calculatable

T = t.TypeVar("T", bound=Calculatable)


class AbstractOptimizer(t.Generic[T], ABC):
    def __init__(
        self,
        goal: float,
        first_value: T,
        max_value: t.Optional[T] = None,
        min_value: t.Optional[T] = None,
    ) -> None:
        self.goal = goal
        self.max_value = max_value
        self.min_value = min_value
        self.outputs = [first_value]

    def compute_next(self, measurement: t.Optional[float]) -> T:
        if measurement is None:
            return self.outputs[0]

        next_value = self._compute_next(measurement)
        next_value = self.limit_value(next_value)
        self.outputs.append(next_value)

        return next_value

    @abstractmethod
    def _compute_next(self, measurement: float) -> T:
        """
        Computes the next raw size of the rangeiterator, without limits
        """

    def limit_value(self, next_value: T) -> T:
        if self.max_value is not None:
            next_value = min(self.max_value, next_value)
        if self.min_value is not None:
            next_value = max(self.min_value, next_value)
        return next_value
