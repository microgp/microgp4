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
# v1 / May 2023 / Squillero (GX)

__all__ = ['Scalar', 'Approximate', 'Vector']

from typing import Sequence, Any, Type
from math import isclose

from .fitness import FitnessABC
from microgp4.tools.names import _patch_class_info


class Scalar(FitnessABC, float):
    """A single numeric value -- Larger is better."""
    pass


class Integer(FitnessABC, int):
    """A single numeric value -- Larger is better."""
    pass


class Approximate(FitnessABC, float):
    """A single, floating-point value with approximate equality -- Larger is better."""

    def __init__(self, argument, rel_tol: float = 1e-09, abs_tol: float = 0):
        """See the documentation of math.isclose() and PEP485."""
        super(Approximate, self).__init__()
        self._rel_tol = rel_tol
        self._abs_tol = abs_tol

    def decorate(self) -> str:
        return str(float(self)) + '≈'

    def is_distinguishable(self, other: FitnessABC) -> bool:
        self.is_comparable(other)
        return not isclose(float(self), float(other), rel_tol=self._rel_tol, abs_tol=self._abs_tol)

    def is_fitter(self, other: FitnessABC) -> bool:
        self.is_comparable(other)
        return self != other and float(self) > float(other)

    def is_comparable(self, other: 'Approximate'):
        super().is_comparable(other)
        assert self._abs_tol == other._abs_tol, f"Can't is_fitter Fitness Floats with different absolute tolerance ({float(self)}±{self._abs_tol} vs. {float(other)}±{other._abs_tol})"
        assert self._rel_tol == other._rel_tol, f"Can't is_fitter Fitness Floats with different relative tolerance ({float(self)}±{self._rel_tol}r vs. {float(other)}±{other._rel_tol}r)"


# VECTORS


class Vector(FitnessABC):
    """A generic vector of Fitness values.

    fitness_type is the subtype, **kwargs are passed to fitness init

    Examples:
        f1 = sgx.fitness.Vector([23, 10], fitness_type=Approximate, abs_tol=.1)
        f2 = sgx.fitness.Vector([23, 10], fitness_type=Approximate, abs_tol=.001)

        f1 > sgx.fitness.Vector([23, 9.99], fitness_type=Approximate, abs_tol=.1) is False
        f2 > sgx.fitness.Vector([23, 9.99], fitness_type=Approximate, abs_tol=.001) is True

    """

    def __init__(self, value: Sequence, fitness_type: Type[FitnessABC] = Scalar, **kwargs):
        self._values = tuple(fitness_type(e, **kwargs) for e in value)
        self.run_paranoia_checks()

    def is_comparable(self, other: 'Vector'):
        super().is_comparable(other)
        assert len(self._values) == len(
            other._values), f"Can't is_fitter Fitness Vectors of different size ({self} vs. {other})"

    def is_distinguishable(self, other: 'Vector') -> bool:
        self.is_comparable(other)
        return any(e1 != e2 for e1, e2 in zip(self._values, other._values))

    def is_fitter(self, other: FitnessABC) -> bool:
        self.is_comparable(other)
        return Vector.compare_vectors(self._values, other._values) > 0

    @staticmethod
    def compare_vectors(v1: Sequence[FitnessABC], v2: Sequence[FitnessABC]) -> int:
        """Compare Fitness values in v1 and v2.

        Return -1 if v1 < v2; +1 if v1 > v2; 0 if v1 == v2"""
        for e1, e2 in zip(v1, v2):
            if e1 > e2:
                return 1
            elif e2 > e1:
                return -1
        return 0

    def decorate(self) -> str:
        return ', '.join(e.decorate() for e in self._values)

    def __iter__(self):
        return iter(self._values)

    def __hash__(self):
        return hash(self._values)


# Patch names

_patch_class_info(Scalar, 'Scalar', tag='fitness')
_patch_class_info(Integer, 'Integer', tag='fitness')
_patch_class_info(Approximate, 'Approximate', tag='fitness')
_patch_class_info(Vector, 'Vector', tag='fitness')
