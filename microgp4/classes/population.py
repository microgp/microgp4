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

__all__ = ['Population']

from collections.abc import Sequence
from typing import Callable, Any
from copy import copy

from microgp4.classes.fitness import FitnessABC
from microgp4.classes.individual import Individual
from microgp4.classes.frame import FrameABC
from microgp4.user_messages import *


class Population:
    _top_frame: type[FrameABC]
    _fitness_function: Callable[[Any], FitnessABC]
    _individuals: list[Individual]
    _mu: int
    _lambda: int

    DEFAULT_EXTRA_PARAMETERS = {
        '_comment': ';',
        '_label': '{_node}:\n',
        '$dump_node_info': False,
        '_text_before_macro': '',
        '_text_after_macro': '\n',
        '_text_before_frame': '',
        '_text_after_frame': '',
        '_text_before_node': '',
        '_text_after_node': '',
    }

    def __init__(self, top_frame: type[FrameABC], extra_parameters: dict | None = None):
        assert check_valid_types(top_frame, FrameABC, subclass=True)
        assert extra_parameters is None or check_valid_type(extra_parameters, dict)
        self._top_frame = top_frame
        if extra_parameters is None:
            extra_parameters = dict()
        self._extra_parameters = Population.DEFAULT_EXTRA_PARAMETERS | extra_parameters
        self._individuals = list()

    #def get_new_node(self) -> int:
    #    self._node_count += 1
    #    return self._node_count

    @property
    def top_frame(self):
        return self._top_frame

    @property
    def individuals(self) -> list[Individual]:
        return self._individuals

    @property
    def parameters(self) -> dict:
        return copy(self._extra_parameters)

    def __getitem__(self, item):
        return self._individuals[item]

    def __len__(self):
        return len(self._individuals)

    def __iadd__(self, individual):
        if isinstance(individual, Sequence):
            assert all(check_valid_types(i, Individual) for i in individual)
            assert all(i.valid for i in individual), \
                f"ValueError: invalid individual"
            self._individuals.extend(individual)
        else:
            assert check_valid_types(individual, Individual)
            assert individual.valid, \
                f"ValueError: invalid individual"
            self._individuals.append(individual)
        return self

    def __iter__(self):
        return iter(self._individuals)

    def __str__(self):
        return f'{self.__class__.__name__} @ {hex(id(self))} (top frame: {self.top_frame.__name__})' + \
            '\n• ' + \
            '\n• '.join(str(i) for i in self._individuals)

    def dump_individual(self, ind: int | Individual, extra_parameters: dict | None = None) -> str:
        if isinstance(ind, int):
            ind = self.individuals[ind]
        if extra_parameters is not None:
            assert extra_parameters is None or check_valid_type(extra_parameters, dict)
            return ind.dump(self.parameters | extra_parameters)
        else:
            return ind.dump(self.parameters)

    def evaluate(self):
        whole_pop = [self.dump_individual(i) for i in self.individuals]
        result = self._evaluator.evaluate(whole_pop)
        if microgp_logger.level <= logging.DEBUG:
            for i, f in enumerate(result):
                microgp_logger.debug(f"evaluate: Individual {i:2d}: {f}")
        for i, f in zip(self.individuals, result):
            i.fitness = f

    def sort(self):
        fronts = list()
        sorted_ = list()
        individuals = set(self._individuals)

        while individuals:
            pareto = set(i1 for i1 in individuals
                         if all(i1.fitness == i2.fitness or i1.fitness >> i2.fitness for i2 in individuals))
            fronts.append(pareto)
            individuals -= pareto
            sorted_ += sorted(pareto, key=lambda i: (i.fitness, -i.id))

        self._individuals = sorted_
