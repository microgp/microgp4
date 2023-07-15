# -*- coding: utf-8 -*-
#############################################################################
#           __________                                                      #
#    __  __/ ____/ __ \__ __   This file is part of MicroGP4 v4!2.0         #
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
# v1 / May 2023 / Squillero

__all__ = ['EvaluatorABC', 'PythonFunction', 'ParallelPythonFunction']

import logging
from typing import Callable, Sequence
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from microgp4.user_messages import *
from microgp4.classes.fitness import FitnessABC
from microgp4.classes.population import Population
from microgp4.tools.dump import _strip_genome
from microgp4.registry import *
from microgp4.global_symbols import *
from microgp4.classes.individual import Individual


class EvaluatorABC(ABC):
    """Hey
    """

    _fitness_calls: int = 0

    @abstractmethod
    def evaluate_population(self, population: Population) -> None:
        raise NotImplementedError

    @property
    def fitness_calls(self) -> int:
        return self._fitness_calls

    def __call__(self, population: Population) -> None:
        self.evaluate_population(population)


class PythonFunction(EvaluatorABC):

    def __init__(self, function: Callable[[str], FitnessABC], strip_genome: bool = False) -> None:
        assert get_microgp4_type(function) == FITNESS_FUNCTION, \
                f"TypeError: {function} has not be registered as a MicgroGP fitness function"
        if strip_genome:
            self._function = lambda g: function(_strip_genome(g))
        else:
            self._function = function

    def __str__(self):
        return f"PurePythonEvaluator❬{self._function.__module__}.{self._function.__name__}❭"

    def evaluate_population(self, population: Population) -> None:
        for i, ind in [_ for _ in enumerate(population) if _[1].is_finalized is False]:
            fitness = self._function(population.dump_individual(i))
            self._fitness_calls += 1
            ind.fitness = fitness
            microgp_logger.debug(
                f"eval: {ind.describe(include_fitness=True, include_birth=True, include_structure=True)}")


class Script(EvaluatorABC):

    def __init__(self) -> None:
        raise NotImplementedError


class ParallelPythonFunction(EvaluatorABC):

    def __init__(self, function: Callable[[str], FitnessABC], strip_genome: bool = False) -> None:
        assert get_microgp4_type(function) == FITNESS_FUNCTION, \
                f"TypeError: {function} has not be registered as a MicgroGP fitness function"
        if strip_genome:
            self._cook = lambda g: _strip_genome(g)
        else:
            self._cook = lambda g: g
        self._function = function

    def __str__(self):
        return f"PurePythonEvaluator_parallel❬{self._function.__module__}.{self._function.__name__}❭"

    def evaluate_population(self, population: Population) -> None:
        indexes = list()
        genomes = list()
        for i, g in enumerate(population):
            if not g.is_finalized:
                indexes.append(i)
                genomes.append(self._cook(population.dump_individual(i)))

        with ProcessPoolExecutor() as pool:
            for i, f in zip(indexes, pool.map(self._function, genomes)):
                self._fitness_calls += 1
                population[i].fitness = f
                microgp_logger.debug(
                    f"eval: {population[i].describe(include_fitness=True, include_birth=True, include_structure=True)}")


def shutup_logger():
    print(f"{microgp_logger.name} @ {id(microgp_logger):x} -> {microgp_logger.parent}")
    #microgp_logger.setLevel(logging.WARNING)
