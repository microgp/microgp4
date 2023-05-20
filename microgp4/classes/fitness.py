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

__all__ = ['FitnessABC', 'reverse_fitness']

from abc import ABC, abstractmethod
from functools import wraps, cache

from microgp4.classes.pedantic import PedanticABC
from microgp4.classes.paranoid import Paranoid
from microgp4.user_messages import *
from microgp4.tools.names import _patch_class_info


class FitnessABC(PedanticABC, Paranoid, ABC):
    """Fitness of a phenotype, handle multiple formats (eg. scalar, tuple).

    The class also redefines the relational operator in order to handle different types of optimization
    (eg. maximization, minimization) and to provide limited support to more complex scenarios
    (eg. multi-objective optimization)

    Equalities ('==' and '!=') are based on `is_distinguishable`.

    Single angular-bracket operators ('>', '<', '>=', and '<=') are based on `is_fitter` and may be randomized
    (ie. the result may not be reproducible).

    Double angular-bracket operators ('>>' and '<<') are based on `is_dominant` and the result is stable. By default,
    `is_dominant` is defined as `is_fitter`.

    When subclassing, one should only redefine `is_fitter`, and optionally `is_distinguishable` and `is_dominant`;
    `is_dominant` **must** be changed if `is_fitter` is randomized, making the result not reproducible.

    Additional sanity checks should be added to `is_comparable
    `. Subclasses may redefine the `decorate` method to
    change the value appearance.
    """

    @abstractmethod
    def is_fitter(self, other: 'FitnessABC') -> bool:
        """Check whether fitter than the other (result may be accidental)."""
        assert self.is_comparable(other)
        return super().__gt__(other)

    def is_dominant(self, other: 'FitnessABC') -> bool:
        """Check whether dominates the other (result is certain)."""
        return self.is_fitter(other)
    def is_comparable(self, other: 'FitnessABC'):
        assert str(self.__class__) == str(other.__class__), \
            f"ValueError: Can't compare different type of Fitness values: {self} and {other} (paranoia check)"
        return True


    def is_distinguishable(self, other: 'FitnessABC') -> bool:
        """Check whether some differences from the other Fitness may be perceived."""
        assert self.is_comparable(other)
        return super().__ne__(other)

    def is_comparable(self, other: 'FitnessABC'):
        assert str(self.__class__) == str(other.__class__), \
            f"ValueError: Can't compare different type of Fitness values: {self.__class__} and {other.__class__} (paranoia check)"
        return True

    def is_valid(self, fitness: 'FitnessABC') -> bool:
        try:
            self.is_comparable(fitness)
        except AssertionError:
            return False
        return True

    def decorate(self) -> str:
        """Represent the individual fitness value with a nice string."""
        return f"{super().__str__()}"

    # FINAL/WARNINGS

    def __eq__(self, other: 'FitnessABC') -> bool:
        return not self.is_distinguishable(other)

    def __ne__(self, other: 'FitnessABC') -> bool:
        return self.is_distinguishable(other)

    def __gt__(self, other: 'FitnessABC') -> bool:
        return self.is_fitter(other)

    def __lt__(self, other: 'FitnessABC') -> bool:
        return other.is_fitter(self)

    def __ge__(self, other: 'FitnessABC') -> bool:
        return not self.__lt__(other)

    def __le__(self, other: 'FitnessABC') -> bool:
        return not self.__gt__(other)

    def __rshift__(self, other: 'FitnessABC') -> bool:
        return self.is_dominant(other)

    def __lshift__(self, other: 'FitnessABC') -> bool:
        return other.is_dominant(self)

    def __str__(self):
        # Double parentheses: ⸨ ⸩  (U+2E28, U+2E29)
        # White parentheses: ⦅ ⦆  (U+2985, U+2986)
        # Fullwidth white parentheses:｟ ｠ (U+FF5F, U+FF60)
        # Math white square parentheses: ⟦ ⟧ (U+27E6, U+27E7)
        # Z notation binding bracket: ⦉ ⦊
        # Curved angled bracket: ⧼ ⧽

        return f"⸨{self.decorate()}⸩"

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self):
        return str(self)

    def run_paranoia_checks(self) -> bool:
        return super().run_paranoia_checks()


@cache
def reverse_fitness(fitness_class: type[FitnessABC]) -> type[FitnessABC]:
    """Reverse fitness class turning a maximization problem into a minimization one."""
    assert check_valid_type(fitness_class, FitnessABC, subclass=True)

    class T(fitness_class):

        def is_fitter(self, other: FitnessABC) -> bool:
            assert self.__class__ == other.__class__, \
                    f"TypeError: different types of fitness: '{self.__class__}' and '{other.__class__}'"
            return super(T, other).is_fitter(self)

        def is_dominant(self, other: FitnessABC) -> bool:
            assert self.__class__ == other.__class__, \
                    f"TypeError: different types of fitness: '{self.__class__}' and '{other.__class__}'"
            return super(T, other).is_dominant(self)

        def decorate(self) -> str:
            return f'ᴙ{fitness_class(self).decorate()}'

    _patch_class_info(T, f'reverse[{fitness_class.__name__}]', tag='fitness')

    return T
