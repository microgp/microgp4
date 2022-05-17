# -*- coding: utf-8 -*-
#          __________                                                       #
#   __  __/ ____/ __ \__ __   This file is part of MicroGP4 v1.0a1 "Kiwi"   #
#  / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer   #
# / /_/ / /_/ / ____/ // /_   https://github.com/squillero/microgp4         #
# \__  /\____/_/   /__  __/                                                 #
#   /_/ --MicroGP4-- /_/      "You don't need a big goal, be μ-ambitious!"  #
#                                                                           #

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

import logging
from abc import abstractmethod
from typing import Any
from copy import copy
from math import isclose

logger = logging.getLogger(__name__)


class Base:
    """Base class for storing fitness.

    The different selection schemes are implemented simply by overriding is_equal,
    is_better, and is_dominant (see specific fitness classes for details). A fitness
    might be invalid (None).

    Use standard relational operators >, <=, ... to compare fitness values, use
    shift >>, << to check for (Pareto) dominance. Note that the first comparison
    may be stochastic, while the second is always reproducible. Equal and not-equal
    ==, != are also non-stochastic.

    Please note that, according to Spencer's 'Survival of the Fittest',
    the bigger, the better. Thus we are *maximizing* the fitness and not
    minimizing a mathematical function.
    """

    #----------------------------------------------------------------------
    # Default value

    def __init__(self, value: Any) -> None:
        self._value = value

    @property
    def value(self) -> Any:
        return copy(self._value)

    #----------------------------------------------------------------------
    # Abstract methods

    @abstractmethod
    def is_valid(self) -> bool:
        """True if valid"""
        return self._value is not None

    @abstractmethod
    def is_equal(self, other: "Base") -> bool:
        """True if fitness is indistinguishable (ie. no reason to chose it over the other)"""
        assert self.is_valid(), f"Can't compare an invalid fitness ({self})"
        assert other.is_valid(), f"Can't compare against an invalid fitness ({other})"

    @abstractmethod
    def is_fitter(self, other: "Base") -> bool:
        """True if fitter (ie. is preferable to)"""
        assert self.is_valid(), f"Can't compare an invalid fitness ({self})"
        assert other.is_valid(), f"Can't compare against an invalid fitness ({other})"

    @abstractmethod
    def is_dominant(self, other: "Base") -> bool:
        """True if unquestionably superior (ie. always preferable to)"""
        assert self.is_valid(), f"Can't compare an invalid fitness ({self})"
        assert other.is_valid(), f"Can't compare against an invalid fitness ({other})"

    #----------------------------------------------------------------------
    # Relational operators: == != > >= < <= >> <<

    def __bool__(self) -> bool:
        return self.is_valid()

    def __eq__(self, other: "Base") -> bool:
        return self.is_equal(other)

    def __ne__(self, other: "Base") -> bool:
        return not self.is_equal(other)

    def __gt__(self, other: "Base") -> bool:
        return self.is_fitter(other)

    def __ge__(self, other: "Base") -> bool:
        return self.is_fitter(other) or self.is_equal(other)

    def __lt__(self, other: "Base") -> bool:
        return other.is_fitter(self)

    def __le__(self, other: "Base") -> bool:
        return other.is_fitter(self) or other.is_equal(self)

    def __rshift__(self, other) -> bool:
        return self.is_dominant(other)

    def __lshift__(self, other) -> bool:
        return other.is_dominant(self)

    def __str__(self):
        #return f"{self.__module__}.{self.__class__.__name__}{{v={self._value}}}"
        return f"{self.__class__.__name__}{{v={self._value}}}"
