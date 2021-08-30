#!/usr/bin/env python

import typing as t

C = t.TypeVar("C", bound="Calculatable")


class Calculatable(t.Protocol):
    """
    Used to signify types that can have basic mathematic calculations done on them
    """

    def __add__(self: C, other: C) -> C:
        ...

    def __sub__(self: C, other: C) -> C:
        ...

    def __mul__(self: C, other: float) -> C:
        ...

    def __truediv__(self: C, other: C) -> float:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...


IT = t.TypeVar("IT", bound=Calculatable)  # ItervalType - the type used to talk about size of a chunk
