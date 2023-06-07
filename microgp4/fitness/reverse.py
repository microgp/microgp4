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

# Copyright 2022-23 Giovanni Squillero and Alberto Tonda
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

__all__ = ['reverse_fitness']

from abc import ABC, abstractmethod
from functools import cache

from microgp4.classes.fitness import FitnessABC
from microgp4.user_messages import *
from microgp4.tools.names import _patch_class_info


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

        def _decorate(self) -> str:
            #return 'ᴙ⟦' + fitness_class._decorate(self) + '⟧'
            return 'ᴙ' + fitness_class._decorate(self)

    _patch_class_info(T, f'reverse[{fitness_class.__name__}]', tag='fitness')

    return T
