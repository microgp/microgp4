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

from math import isclose
from numbers import Number
from typing import Sequence, Tuple
import logging

from .. import reproducible_random
from .base import Base

logger = logging.getLogger(__name__)


class Chromatic(Base):
    """A tuple of real values, using Chromatic selection."""

    def __init__(self, value: Sequence) -> None:
        self._value = tuple(value)

    def is_valid(self) -> bool:
        assert isinstance(self.value, Tuple), f"Value must be a tuple ({type(self.value)})"
        assert all(v is None or isinstance(v, Number)
                   for v in self.value), f"All tuple elements must be None or numbers ({type(self.value)})"
        return all(v is not None for v in self._value)

    def is_equal(self, other: "Chromatic") -> bool:
        super(Chromatic, self).is_equal(other)
        return all(isclose(s, o) for s, o in zip(self._value, other._value))

    def is_fitter(self, other: "Chromatic") -> bool:
        super(Chromatic, self).is_fitter(other)
        diff = [(abs(s - o)) for s, o in zip(self._value, other._value)]
        prob = [v / sum(diff) for v in diff]
        i = reproducible_random.np_choice(range(len(self._value)), p=prob)
        logger.debug(f"Comparing on feature i={i}")
        return self._value[i] > other._value[i] and not isclose(self._value[i], other._value[i])

    def is_dominant(self, other: "Chromatic") -> bool:
        super(Chromatic, self).is_dominant(other)
        return any(s > o and not isclose(s, o) for s, o in zip(self._value, other._value)) and all(
            s > o or isclose(s, o) for s, o in zip(self._value, other._value))
