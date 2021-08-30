#!/usr/bin/env python

import typing as t

import orbiteer.iterators as iterators
import orbiteer.targets as targets
from orbiteer.shared_types import Calculatable

RT = t.TypeVar("RT")
IT = t.TypeVar("IT", bound=Calculatable)


class OrbiteerRunner:
    def __init__(
        self,
        iterator: iterators.AbstractRangeIterator[RT, IT],
        target: targets.AbstractTarget,
    ) -> None:
        self.iterator = iterator
        self.target = target

    def run(self) -> None:
        first_range = self.iterator.compute_next_range(None)
        next_range = first_range

        while not self.iterator.is_done:
            measurement = self.target.run(next_range)
            next_range = self.iterator.compute_next_range(measurement)
