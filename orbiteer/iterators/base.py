#!/usr/bin/env python

import typing as t
from abc import ABC, abstractmethod

from orbiteer.optimizers import AbstractOptimizer
from orbiteer.shared_types import Calculatable

RT = t.TypeVar("RT")  # RangeType - the type used to talk about the range values themselves
IT = t.TypeVar("IT", bound=Calculatable)  # ItervalType - the type used to talk about size of a chunk


class AbstractRangeIterator(t.Generic[RT, IT], ABC):
    def __init__(self, optimizer: AbstractOptimizer[IT], *args: t.Any, **kwargs: t.Any) -> None:
        self.optimizer = optimizer

    def compute_next_range(self, last_measurement: t.Optional[float]) -> t.Iterable[RT]:
        if not self.is_done:
            next_interval = self.optimizer.compute_next(last_measurement)
            return self._compute_next_range(next_interval)
        else:
            raise StopIteration

    @property
    def is_done(self) -> bool:
        """
        Whether or not there are more things to iterate over. Once false, should never become true again.
        """
        return self._is_done()

    @abstractmethod
    def _compute_next_range(self, next_interval: IT) -> t.Iterable[RT]:
        """
        Computes the next parameters to feed to the command for the next run
        """

    @abstractmethod
    def _is_done(self) -> bool:
        """
        Tells whether or not we are done iterating
        """
