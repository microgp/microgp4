# -*- coding: utf-8 -*-
#############################################################################
#          __________                                                       #
#   __  __/ ____/ __ \__ __   This file is part of MicroGP4 v1.0 "Kiwi"     #
#  / / / / / __/ /_/ / // /   (!) by Giovanni Squillero and Alberto Tonda   #
# / /_/ / /_/ / ____/ // /_   https://github.com/squillero/microgp4         #
# \__  /\____/_/   /__  __/                                                 #
#   /_/ --MicroGP4-- /_/      "You don't need a big goal, be μ-ambitious!!" #
#                                                                           #
#############################################################################

# Copyright 2020 Giovanni Squillero and Alberto Tonda
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

import inspect
from collections.abc import Callable

from .individual import Individual

# TODO: Check. Urgent. (fall 2020)
# TODO: Change name!?!?! (get rid of Gen)
class GenOperator:
    # TODO: Double Check
    """Wrapper of a method that implements the algorithm manipulating or
    building one or more individuals. This class will also manage (in the
    future versions) the statistics applied to the assigned method. The method
    wrapped in the GenOperator must have **kwargs in its parameters.

    **Examples:**

    - Build three genetic operators passing the method and the arity

    >>> init_op1 = ugp4.GenOperator(ugp4.create_random_individual, 0)
    >>> mutation_op1 = ugp4.GenOperator(ugp4.remove_node_mutation, 1)
    >>> crossover_op1 = ugp4.GenOperator(ugp4.switch_proc_crossover, 2)
    >>> crossover_op2 = ugp4.GenOperator(ugp4.five_individuals_crossover, 5)

    - Call the method inside the genetic operator

    >>> selected_crossover_genoperator(individual1, individual2)
    >>> selected_mutation_genoperator(individual, strength=0.7, constraints=constraints))
    >>> individuals = tuple(ind1, ind2, ind3, ind4, ind5)
    >>> kwargs = {'param1': var1, 'param2': var2, 'param3': [a, b, c, d, e]}
    >>> selected_crossover_5_individuals(*individuals, kwargs)
    """

    def __init__(self, function: Callable, arity: int):
        """GenOperator builder. Set the method and how many individuals it
        will manipulate (arity)."""

        assert function, "Function can't be None"
        assert callable(function), "Function must be a callable object"
        assert arity >= 0, "Arity can't be < 0"
        assert inspect.Parameter.VAR_KEYWORD in (p.kind for p in inspect.signature(function).parameters.values()),\
            "The passed method doesn't have **kwargs"

        self._function = function
        self._arity = arity
        self._succeses = list()
        self._results = list()

    def __call__(self, *args, **kwargs):
        return self._function(*args, **kwargs)

    def __lt__(self, other) -> bool:
        # required for reproducibility
        return self._function.__name__ < other._function.__name__

    def update_successes(self, successes: int):
        assert successes >= 0, "Success parameter must be >= 0"
        self._succeses.append(successes)

    def update_results(self, individual: Individual):
        # TODO: implement in future implementations
        pass

    @property
    def function(self):
        return self._function

    @property
    def arity(self):
        return self._arity
