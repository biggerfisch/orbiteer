#!/usr/bin/env python

import typing as t
from datetime import timedelta

from .base import AbstractOptimizer, T


class RatioOptimizer(t.Generic[T], AbstractOptimizer[T]):
    def __init__(
        self,
        goal: float,
        first_value: T,
        max_value: t.Optional[T] = None,
        min_value: t.Optional[T] = None,
        damper: float = 1.0,  # Should be less than 1.0 to have damping effect
    ) -> None:
        # We need to specify all parent args in order for generic type checking to work
        super().__init__(goal, first_value, max_value, min_value)

        self.damper = damper

    def _compute_next(self, measurement: float) -> T:
        """
        Computes the direct ratio of where we are compared to where we want to be and uses it as a multiplier
        """
        last_output = self.outputs[-1]
        direct_ratio = self.goal / measurement

        # This damps and equalizes the ratio as required
        # Being damped by .X means that the change is only X% as strong. A damper of 0.5 would mean a 50% as strong mult
        multiplier = 1 + (direct_ratio - 1) * self.damper

        return last_output * multiplier


# Some defs with generics pre-filled to avoid detection issues
TimedeltaRatioOptimizer = RatioOptimizer[timedelta]
