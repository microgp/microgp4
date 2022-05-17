# -*- coding: utf-8 -*-
#############################################################################
#          __________                                                       #
#   __  __/ ____/ __ \__ __   This file is part of MicroGP4 v1.0a1 "Kiwi"   #
#  / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer   #
# / /_/ / /_/ / ____/ // /_   https://github.com/squillero/microgp4         #
# \__  /\____/_/   /__  __/                                                 #
#   /_/ --MicroGP4-- /_/      "You don't need a big goal, be μ-ambitious!"  #
#                                                                           #
#############################################################################

# Copyright 2022 Giovanni Squillero and Alberto Tonda
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

from numbers import Number
from typing import Sequence
from math import isclose

from .base import Base


class Simple(Base):
    """The simplest possible fitness: a single value"""

    def is_valid(self) -> bool:
        return super().is_valid()

    def is_equal(self, other: "Simple") -> bool:
        super(Simple, self).is_equal(other)
        return isclose(self._value, other._value)

    def is_fitter(self, other: "Simple") -> bool:
        super(Simple, self).is_fitter(other)
        return self._value > other._value and not isclose(self._value, other._value)

    def is_dominant(self, other: "Simple") -> bool:
        super(Simple, self).is_dominant(other)
        return self.is_fitter(other)


class Numeric(Base):
    """A very simply fitness: a single real number"""

    def is_valid(self) -> bool:
        assert self.value is None or isinstance(self.value,
                                                Number), f"Value must be None or a number ({type(self.value)})"
        return super().is_valid()

    def is_equal(self, other: "Numeric") -> bool:
        super(Numeric, self).is_equal(other)
        return isclose(self._value, other._value)

    def is_fitter(self, other: "Numeric") -> bool:
        super(Numeric, self).is_fitter(other)
        return self._value > other._value and not isclose(self._value, other._value)

    def is_dominant(self, other: "Numeric") -> bool:
        super(Numeric, self).is_dominant(other)
        return self.is_fitter(other)


class Tuple(Base):
    """A simple fitness: a tuple of values using lexicographic comparison"""

    def __init__(self, value: Sequence) -> None:
        self._value = tuple(value)

    def is_valid(self) -> bool:
        return all(v is not None for v in self._value)

    def is_equal(self, other: "Tuple") -> bool:
        super(Tuple, self).is_equal(other)
        return self._value == other._value

    def is_fitter(self, other: "Tuple") -> bool:
        super(Tuple, self).is_fitter(other)
        return self._value > other._value

    def is_dominant(self, other: "Tuple") -> bool:
        super(Tuple, self).is_dominant(other)
        return self.is_fitter(other)


class NumericTuple(Base):
    """A simple fitness: a tuple of real numbers using lexicographic comparison"""

    def __init__(self, value: Sequence) -> None:
        self._value = tuple(value)

    def is_valid(self) -> bool:
        assert isinstance(self.value, Tuple), f"Value must be a tuple ({type(self.value)})"
        assert all(v is None or isinstance(v, Number)
                   for v in self.value), f"All tuple elements must be None or numbers ({type(self.value)})"
        return all(v is not None for v in self._value)

    def is_equal(self, other: "NumericTuple") -> bool:
        super(NumericTuple, self).is_equal(other)
        return all(isclose(s, o) for s, o in zip(self._value, other._value))

    def is_fitter(self, other: "NumericTuple") -> bool:
        super(NumericTuple, self).is_fitter(other)
        return all(s > o and not isclose(s, o) for s, o in zip(self._value, other._value))

    def is_dominant(self, other: "NumericTuple") -> bool:
        super(NumericTuple, self).is_dominant(other)
        return self.is_fitter(other)
