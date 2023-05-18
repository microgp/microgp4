# -*- coding: utf-8 -*-
#############################################################################
#           __________                                                      #
#    __  __/ ____/ __ \__ __   This file is part of MicroGP v4!2.0          #
#   / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer  #
#  / /_/ / /_/ / ____/ // /_   https://github.com/microgp/microgp4          #
#  \__  /\____/_/   /__  __/                                                #
#    /_/ --MicroGP4-- /_/      You don't need a big goal, be μ-ambitious!   #
#                                                                           #
#############################################################################

# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

# =[ HISTORY ]===============================================================
# v1 / April 2023 / Squillero (GX)

__all__ = ['Scalar', 'ScalarInteger', 'ScalarExact', 'Vector', 'Sequence']

from collections.abc import Sequence
from copy import deepcopy
from math import isclose
from numbers import Number

from classes.ea.fitness import Fitness


class Scalar(Fitness, float):
    """A single, floating-point value with approximate equality -- see math.isclose."""

    def __init__(self, argument):
        super(Scalar, self).__init__()

    def is_distinguishable(self, other: 'Scalar') -> bool:
        assert self.run_comparable_check(other)
        return not isclose(float(self), float(other))

    def is_fitter(self, other: 'Scalar') -> bool:
        assert self.run_comparable_check(other)
        return self != other and float(self) > float(other)

    def run_comparable_check(self, other: 'Scalar'):
        assert super().run_comparable_check(other)
        return True

    def decorate(self) -> str:
        return f'{self:g}'


class ScalarExact(Fitness, float):
    """A single, floating-point sharp value."""

    def decorate(self) -> str:
        return f'{float(self)}♯'


class ScalarInteger(Fitness, int):
    """A single, integer value."""

    def decorate(self) -> str:
        return f'{self:,}𝕚'


class Vector(Fitness):
    """A vector of floating-point value with approximate equality -- see math.isclose."""

    def __init__(self, seq: Sequence) -> None:
        assert all(isinstance(f, Number) for f in seq), \
            f"TypeError: non-numeric element: {seq} (paranoia check)"
        self._data = tuple(float(f) for f in seq)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __str__(self):
        return self.decorate()

    def is_distinguishable(self, other: 'Scalar') -> bool:
        assert self.run_comparable_check(other)
        return not all(isclose(s, o) for s, o in zip(self, other))

    def is_fitter(self, other: 'Scalar') -> bool:
        # Simple lexicographic: compare the first pair of different elements
        assert self.run_comparable_check(other)
        s, o = next(((s, o) for s, o in zip(self, other) if s != o), (4.2, 4.2))
        return s > o

    def run_comparable_check(self, other: 'Scalar'):
        assert super().run_comparable_check(other)
        assert len(self) == len(other), \
            f"TypeError: different length: {self} vs. {other} (paranoia check)"
        return True

    def decorate(self) -> str:
        return "⟦" + ", ".join(str(f) for f in self._data) + "⟧"


class Sequence(Fitness):
    """A generic sequence of Fitness values."""

    def __init__(self, seq: 'Sequence') -> None:
        assert all(isinstance(f, Fitness) for f in seq), \
            f"TypeError: non-Fitness element: {seq} (paranoia check)"
        self._data = deepcopy(seq)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def is_distinguishable(self, other: 'Sequence') -> bool:
        assert self.run_comparable_check(other)
        return not all(s == o for s, o in zip(self, other))

    def is_fitter(self, other: 'Sequence') -> bool:
        # Simple lexicographic: compare the first pair of different elements
        assert self.run_comparable_check(other)
        s, o = next(((s, o) for s, o in zip(self, other) if s != o), (42, 42))
        return s > o

    def run_comparable_check(self, other: 'Sequence'):
        assert super().run_comparable_check(other)
        assert len(self) == len(other), \
            f"TypeError: different length: {self} vs. {other} (paranoia check)"
        assert all(s.run_comparable_check(o) for s, o in zip(self, other))
        return True

    def decorate(self) -> str:
        return ", ".join(f.decorate() for f in self._data)
