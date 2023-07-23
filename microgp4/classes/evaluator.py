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

__all__ = [
    'EvaluatorABC', 'SequentialPythonEvaluator', 'ParallelPythonEvaluator', 'MakefileEvaluator', 'ScriptEvaluator'
]

from typing import Callable, Sequence
from abc import ABC, abstractmethod

import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

from microgp4.user_messages import *
from microgp4.classes.fitness import FitnessABC, InvalidFitness
from microgp4.fitness import make_fitness
from microgp4.classes.population import Population
from microgp4.tools.dump import _strip_genome
from microgp4.registry import *
from microgp4.global_symbols import *


class EvaluatorABC(ABC):
    """Base abstract class for Evaluator

    `fitness_calls` (``property``):
        Number of fitness calls required so far.

    All *evaluators* must implement:

    ``def evaluate_population(population)``:
        Evaluates all individuals without a valid fitness and updates them. Returns ``None``.

        **Note**: the ``EvaluatorABC`` implements the ``__call__`` method, instances can be used as functions to
        execute the `evaluate_population`.
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


class SequentialPythonEvaluator(EvaluatorABC):
    _function: Callable
    _function_name: str

    def __init__(self, function: Callable[[str], FitnessABC], strip_genome: bool = False) -> None:
        assert get_microgp4_type(function) == FITNESS_FUNCTION, \
                f"TypeError: {function} has not be registered as a MicgroGP fitness function"
        if strip_genome:
            self._function = lambda g: function(_strip_genome(g))
        else:
            self._function = function
        self._function_name = function.__qualname__

    def __str__(self):
        return f"{self.__class__.__name__}❬{self._function_name}❭"

    def evaluate_population(self, population: Population) -> None:
        for i, ind in filter(lambda x: not x[1].is_finalized, enumerate(population)):
            self._fitness_calls += 1
            fitness = self._function(population.dump_individual(i))
            ind.fitness = fitness
            microgp_logger.debug(
                f"eval: {ind.describe(include_fitness=True, include_birth=True, include_structure=True)}")


class ParallelPythonEvaluator(SequentialPythonEvaluator):

    def __init__(self, *args, max_workers=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._max_workers = max_workers

    def evaluate_population(self, population: Population) -> None:
        indexes = list()
        genomes = list()
        for i, g in enumerate(population):
            if not g.is_finalized:
                indexes.append(i)
                genomes.append(population.dump_individual(i))

        with ThreadPoolExecutor(max_workers=self._max_workers, thread_name_prefix=self._function_name) as pool:
            for i, f in zip(indexes, pool.map(self._function, genomes)):
                self._fitness_calls += 1
                population[i].fitness = f
                microgp_logger.debug(
                    f"eval: {population[i].describe(include_fitness=True, include_birth=True, include_structure=True)}")


class MakefileEvaluator(EvaluatorABC):
    _file_name: str
    _required_files: list[str]
    _max_workers: int | None
    _microgp_base_dir: str

    def __init__(self, file_name: str, max_workers: int | None = None, required_files: list[str] = None) -> None:
        if not required_files:
            required_files = ['makefile']
        self._file_name = file_name
        self._required_files = required_files
        self._max_workers = max_workers
        self._microgp_base_dir = os.getcwd()

    def evaluate(self, phenotype):
        with tempfile.TemporaryDirectory(prefix='ugp4_', ignore_cleanup_errors=True) as tmp_dir:
            #microgp_logger.debug(f"MakefileEvaluator:evaluate: Creating {tmp_dir}")
            for f in self._required_files:
                os.symlink(os.path.join(self._microgp_base_dir, f), os.path.join(tmp_dir, f))
            os.chdir(tmp_dir)
            with open(os.path.join(tmp_dir, self._file_name), 'w') as dump:
                dump.write(phenotype)
            try:
                result = subprocess.run(['make', '-s'],
                                        cwd=tmp_dir,
                                        universal_newlines=True,
                                        check=True,
                                        text=True,
                                        timeout=1,
                                        capture_output=True)
            except subprocess.CalledProcessError as problem:
                microgp_logger.debug("MakefileEvaluator:evaluate: CalledProcessError: %s", problem)
                result = None
            except subprocess.TimeoutExpired:
                microgp_logger.debug("MakefileEvaluator:evaluate: TimeoutExpired")
                result = None

            if result is None:
                microgp_logger.debug("MakefileEvaluator:evaluate: Process failed (returned None)")
                result = None
            elif not result.stdout:
                microgp_logger.debug("MakefileEvaluator:evaluate: Process returned empty stdout (stderr: %s)",
                                     result.stderr)
                result = None
        #microgp_logger.debug(f"MakefileEvaluator:evaluate: Leaving {tmp_dir}")
        return result

    def evaluate_population(self, population: Population) -> None:
        indexes = list()
        genomes = list()
        for i, g in enumerate(population):
            if not g.is_finalized:
                indexes.append(i)
                genomes.append(population.dump_individual(i))

        with ThreadPoolExecutor(max_workers=self._max_workers, thread_name_prefix='ugp4') as pool:
            for i, result in zip(indexes, pool.map(self.evaluate, genomes)):
                self._fitness_calls += 1
                if result is None:
                    population[i].fitness = InvalidFitness()
                else:
                    value = [float(r) for r in result.stdout.split()]
                    if len(value) == 1:
                        value = value[0]
                    fitness = make_fitness(value)
                    population[i].fitness = fitness
                microgp_logger.debug(
                    f"eval: {population[i].describe(include_fitness=True, include_birth=True, include_structure=True)}")


class ScriptEvaluator(EvaluatorABC):
    """
    A class to represent a person.

    ...

    Attributes
    ----------
    name : str
        first name of the person
    surname : str
        family name of the person
    age : int
        age of the person

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.

    hello
    """
    _file_name: str
    _script_name: str

    def __init__(self, script_name: str, file_name: str = 'phenotype_{i:04x}.txt') -> None:
        self._script_name = script_name
        self._file_name = file_name

    def evaluate_population(self, population: Population) -> None:
        ind_idxs = population.not_evaluated
        ind_files = list()
        for i in ind_idxs:
            self._fitness_calls += 1
            ind_files.append(self._file_name.format(i=population.individuals[i].id))
            with open(ind_files[-1], 'w') as dump:
                dump.write(population.dump_individual(i))

        try:
            result = subprocess.run([self._script_name, *ind_files],
                                    universal_newlines=True,
                                    check=True,
                                    text=True,
                                    timeout=10,
                                    capture_output=True)
        except subprocess.CalledProcessError as problem:
            microgp_logger.debug("MakefileEvaluator:evaluate: CalledProcessError: %s", problem)
            result = None
        except subprocess.TimeoutExpired:
            microgp_logger.debug("MakefileEvaluator:evaluate: TimeoutExpired")
            result = None

        if result is None:
            microgp_logger.debug("MakefileEvaluator:evaluate: Process failed (returned None)")
            population[i].fitness = InvalidFitness()
        elif not result.stdout:
            microgp_logger.debug("MakefileEvaluator:evaluate: Process returned empty stdout (stderr: %s)",
                                 result.stderr)
            population[i].fitness = InvalidFitness()
        else:
            results = list(filter(lambda s: bool(s), result.stdout.split('\n')))
            assert len(results) == len(ind_idxs), \
                f"ValueError: number of results and number of individual mismatch (paranoia check)"
            for i, line in zip(ind_idxs, results):
                value = [float(r) for r in line.split()]
                if len(value) == 1:
                    value = value[0]
                fitness = make_fitness(value)
                population.individuals[i].fitness = fitness

        for f in ind_files:
            os.remove(f)
