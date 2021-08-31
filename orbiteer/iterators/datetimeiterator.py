#!/usr/bin/env python

import typing as t
from datetime import datetime, timedelta

from .base import AbstractRangeIterator


class DatetimeRangeIterator(AbstractRangeIterator[datetime, timedelta]):
    def __init__(self, *args: t.Any, left: datetime, right: datetime, **kwargs: t.Any) -> None:
        # default is new to old == left -> right
        self.reverse_order = kwargs.pop("reverse_order", False)
        self.left = left
        self.right = right

        if not self.reverse_order:
            self.end = self.right
            self.right = self.left
        else:
            self.end = self.left
            self.left = self.right

        super().__init__(*args, **kwargs)

    def _compute_next_range(self, next_interval: timedelta) -> t.Tuple[datetime, datetime]:
        if not self.reverse_order:
            self.left = self.right
            self.right = min(self.left + next_interval, self.end)
        else:
            self.right = self.left
            self.left = max(self.right - next_interval, self.end)

        return self.left, self.right

    def _is_done(self) -> bool:
        if not self.reverse_order:
            return self.left >= self.end
        else:
            return self.right <= self.end
