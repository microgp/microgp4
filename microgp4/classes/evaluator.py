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
    "EvaluatorABC",
    "PythonEvaluator",
    "MakefileEvaluator",
    "ScriptEvaluator",
]

from typing import Callable, Sequence
from abc import ABC, abstractmethod

from itertools import zip_longest

import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

from microgp4.global_symbols import *

if joblib_available:
    import joblib

from microgp4.user_messages import *
from microgp4.classes.fitness import FitnessABC
from microgp4.fitness import make_fitness
from microgp4.classes.population import Population
from microgp4.registry import *
from microgp4.global_symbols import *


class EvaluatorABC(ABC):
    r"""Base abstract class for Evaluator

    The `Evaluator` classes evaluate individuals in the population without a valid fitness values and update them.

    All *evaluators* implement the function `evaluate_population`, that evaluates all individuals without a valid
    fitness and updates them. **Note**: the ``EvaluatorABC`` implements the ``__call__`` method, instances can be used as functions to
    execute the `evaluate_population`.

    >>> evaluator = ugp.evaluator.PythonEvaluator(fitness)
    >>> evaluator(population)
    >>> print(evaluator.fitness_calls)

    In all Evaluators, set option `strip_phenotypes` to convert the genotype into a single-line string: the header is
    removed; leading and trailing spaces in each line are removed; empty lines are ignored; the final newline is
    removed; newlines are converted into spaces. Eg.:

    | ``; Automagically generated by MicroGP⏎``
    | ``000⏎``
    | ``⏎``
    | ``XX      ⏎``
    | ``111⏎``

    is transfomed into the string ``'000 XX 111'``

    Attributes
    ----------
    fitness_calls
        Number of fitness calls required so far.
    """

    _fitness_calls: int = 0
    cook: Callable[[str], str]

    def __init__(self, strip_phenotypes: bool = False):
        r"""
        Parameters
        ----------
        strip_phenotypes: bool
            ``True`` to transform into single-line strings
        """
        if strip_phenotypes:
            self.cook = lambda g: EvaluatorABC.strip_phenotypes(g)
        else:
            self.cook = lambda g: g

    @abstractmethod
    def evaluate_population(self, population: Population) -> None:
        raise NotImplementedError

    @property
    def fitness_calls(self) -> int:
        return self._fitness_calls

    def __call__(self, population: Population) -> None:
        self.evaluate_population(population)

    @staticmethod
    def strip_phenotypes(raw_dump: str) -> str:
        """Yabba"""
        lines = list()
        for l in raw_dump.split('\n')[1:]:
            if not l.strip():
                continue
            lines.append(l.strip())
        return "\n".join(lines)


class PythonEvaluator(EvaluatorABC):
    r"""
    An  `Evaluator` based on a Python function.

    The `PythonEvaluator` uses a Python function to calculate the fitness values of individuals. The genome is a
    string; it is passed as the only argument to the function. The function has been registered as fitness function
    using the decorator ``@ugp.fitness``.

    `PythonEvaluators` allow a simplistic form of parallelism:

    *   thread-based (builtin): Multiple functions are evaluated in different threads. Threads are lightweight,
        but due to the GIL [1]_, this method is likely to be useful only if the fitness function accesses external
        resources (eg. files, REST APIs, databases, external tools).

    *   process-based (based on `joblib` [2]_): Multiple functions are evaluated in different processes.
        Processes-based paralelism does not suffer from the GIL limitation [1]_, but starting/stopping them
        introduces considerable overhead, thus this method is likely to be useful only when the fitness function
        is computationally intensive.

    The `backend` parameters select the type of parallelism: ``None`` for sequential evaluation, ```thread_pool``` for
    threads, ``'joblib'`` for processes.

    When the evaluation is parallel, the parameter `max_workers` control the maximum number of workers that are
    started in parallel. If ``None``, a *reasonable* value is used, that takes into consideration the characteristic of
    the microprocessor.

    Set option `strip_phenotypes` (see :py:class:`classes.evaluator.EvaluatorABC`) to convert the genotype into a
    single-line string.

    Examples
    --------
    Use as many threads as reasonably possible, strip (cleanup) the phenotype before calling the function

    >>> ugp.evaluator.PythonEvaluator(fitness, backend='thread_pool', strip_phenotypes=True)

    Notes
    -----
    The fitness function must have been declared with the ``@fitness`` decorator.

    References
    ----------
    .. [1] https://docs.python.org/3/glossary.html#term-global-interpreter-lock
    .. [2] https://joblib.readthedocs.io/en/stable/
    """

    _function: Callable
    _function_name: str

    def __init__(
        self, fitness_function: Callable[[str], FitnessABC], max_workers=None, backend: str | None = None, **kwargs
    ) -> None:
        r"""
        Parameters
        ----------
        fitness_function
            The Python function for calculating the fitness
        max_workers
            Maximum number of workers to start in parallel. If ``None``, a reasonable number is used.
        backend
            Parallelization backend. Possible values are ``None`` or `'thread_pool'` or `'joblib'`
        kwargs
            Extra parameters for :class:`classes.evaluator.EvaluatorABC` (ie. `strip_phenotypes`)
        """

        super().__init__(**kwargs)
        assert (
            get_microgp4_type(fitness_function) == FITNESS_FUNCTION
        ), f"TypeError: {fitness_function} has not be registered as a MicgroGP fitness function"

        if not backend or (max_workers is not None and max_workers < 2):
            backend = ""
            max_workers = 1
        assert max_workers is None or check_value_range(max_workers, 1)

        self._fitness_function = fitness_function
        self._max_workers = max_workers
        self._backend = backend
        self._fitness_function_name = fitness_function.__qualname__

    def __str__(self):
        if not self._backend:
            return f"{self.__class__.__name__}❬{self._fitness_function_name}❭"
        elif self._backend == 'thread_pool':
            return f"{self.__class__.__name__}/ThreadPool❬{self._fitness_function_name}❭"
        elif self._backend == 'joblib':
            return f"{self.__class__.__name__}/JobLib❬{self._fitness_function_name}❭"
        else:
            raise NotImplementedError

    def evaluate_population(self, population: Population) -> None:
        individuals = [(i, I, self.cook(population.dump_individual(i))) for i, I in population.not_finalized]

        if self._max_workers == 1 or not self._backend:
            # Simple, sequential, Python evaluator
            for _, I, P in individuals:
                self._fitness_calls += 1
                I.fitness = self._fitness_function(P)
        elif self._backend == 'thread_pool':
            with ThreadPoolExecutor(
                max_workers=self._max_workers, thread_name_prefix=self._fitness_function_name
            ) as pool:
                for I, f in zip(
                    (I for _, I, _ in individuals), pool.map(self._fitness_function, (P for _, _, P in individuals))
                ):
                    self._fitness_calls += 1
                    I.fitness = f
        elif self._backend == 'joblib':
            jobs = list(joblib.delayed(self._fitness_function)(P) for _, _, P in individuals)
            values = joblib.Parallel(n_jobs=self._max_workers if self._max_workers else -1, return_as="generator")(jobs)
            for I, f in zip((I for _, I, _ in individuals), values):
                self._fitness_calls += 1
                I.fitness = f
        else:
            raise NotImplementedError(self._backend)


class MakefileEvaluator(EvaluatorABC):
    r"""
    A parallel `Evaluator` exploiting the good old `make` [1]_.

    The `MakefileEvaluator` helps the use of an external evaluator based on the `make` command. For each
    individual to be evaluated: it creates a temporary directory; puts in the directory `Makefile` and all other
    necessary files; dumps the genome of the individual; enter the directory and calls `make`; gets the result from
    the standard output; destroys the temporary directory.

    Different individuals are evaluated in parallel by different threads. The GIL [2]_ creates no problem as each
    thread calls `subprocess.run` and then waits for its completion.

    Most of the parameters can be configured:

    *   `filename`: The name of the genotype. Usually also the prerequisite of some rule in the Makefile
    *   `make_command`: How make should be invoked in the current system
    *   `make_flags`: Flags for make. Default is just ``'-s'`` (be quiet)
    *   `makefile`: Name of the Makefile itself
    *   `required_files`: Additional files required to make the program that must be added to the temporary
        directory. The `makefile` is added by default. Files are added creating a symlink [3]_ (**note**: on Windows it
        may be necessary to give the user additional permission)

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Make_%28software%29
    .. [2] https://docs.python.org/3/glossary.html#term-global-interpreter-lock
    .. [3] https://en.wikipedia.org/wiki/Symbolic_link

    """

    _filename: str
    _max_workers: int | None
    _make_command: str
    _make_flags: tuple[str]
    _makefile: str
    _required_files: tuple[str]
    _microgp_base_dir: str

    def __init__(
        self,
        filename: str,
        *,
        max_workers: int | None = None,
        make_command='make',
        make_flags: Sequence[str] = ('-s',),
        makefile='Makefile',
        required_files: Sequence[str] = (),
        **kwargs,
    ) -> None:
        r"""
        Parameters
        ----------
        filename
            Name of the file containing the genome
        max_workers
            Maximum number of workers to start in parallel. If ``None``, a reasonable number is used.
        make_command
            Name of the make command.
        make_flags
            Flags for the make command
        makefile
            Name of the makefile
        required_files
            Files that need to be present for the makefile to work in addition to `makefile` and `filename`
        kwargs
            Extra parameters for :class:`classes.evaluator.EvaluatorABC` (ie. `strip_phenotypes`)
        """
        super().__init__(**kwargs)
        assert max_workers is None or check_value_range(max_workers)
        self._filename = filename
        self._max_workers = max_workers
        self._make_command = make_command
        self._make_flags = tuple(make_flags)
        self._makefile = makefile
        self._required_files = tuple(required_files)
        self._microgp_base_dir = os.getcwd()

    def __str__(self):
        return f"{self.__class__.__name__}❬{self._filename}❭"

    def evaluate(self, phenotype):
        with tempfile.TemporaryDirectory(prefix="ugp4_", ignore_cleanup_errors=True) as tmp_dir:
            for f in [self._makefile, *self._required_files]:
                os.symlink(os.path.join(self._microgp_base_dir, f), os.path.join(tmp_dir, f))
            with open(os.path.join(tmp_dir, self._filename), "w") as dump:
                dump.write(phenotype)
            # try:
            result = subprocess.run(
                [self._make_command, *self._make_flags],
                cwd=tmp_dir,
                universal_newlines=True,
                check=True,
                text=True,
                timeout=1,
                capture_output=True,
            )
            # except subprocess.CalledProcessError as problem:
            #    microgp_logger.debug("MakefileEvaluator:evaluate: CalledProcessError: %s", problem)
            #    result = None
            # except subprocess.TimeoutExpired:
            #    microgp_logger.debug("MakefileEvaluator:evaluate: TimeoutExpired")
            #   result = None

            if result is None:
                microgp_logger.debug("MakefileEvaluator:evaluate: Process failed (returned None)")
                result = None
            elif not result.stdout:
                microgp_logger.debug(
                    "MakefileEvaluator:evaluate: Process returned empty stdout (stderr: %s)", result.stderr
                )
                result = None
        return result

    def evaluate_population(self, population: Population) -> None:
        indexes = list()
        genomes = list()
        for i, g in population:
            if not g.is_finalized:
                indexes.append(i)
                genomes.append(self.cook(population.dump_individual(i)))

        with ThreadPoolExecutor(max_workers=self._max_workers, thread_name_prefix="ugp4") as pool:
            for i, result in zip(indexes, pool.map(self.evaluate, genomes)):
                self._fitness_calls += 1
                if result is None:
                    raise RuntimeError(f"Thread failed (returned None)")
                else:
                    value = [float(r) for r in result.stdout.split()]
                    if len(value) == 1:
                        value = value[0]
                    fitness = make_fitness(value)
                    population[i].fitness = fitness
                microgp_logger.debug(
                    f"eval: {population[i].describe(include_fitness=True, include_birth=True, include_structure=True)}"
                )


class ScriptEvaluator(EvaluatorABC):
    """
    A class to represent a person.

    ...

    Attributes
    ----------
    name
        first name of the person
    surname
        family name of the person
    age
        age of the person
    """

    _file_name: str
    _script_name: str

    def __init__(
        self,
        script_name: str,
        args: Sequence[str] | None = None,
        *,
        filename_format: str = "phenotype_{i:04x}.txt",
        **kwargs,
    ) -> None:
        r"""
        Parameters
        ----------
        script_name
            Name of the script (eg. ``'./fitness.sh'``)
        args
            Optional arguments before the list of files with genomes
        filename_format
            Genome file names (eg. ``'ind{i:010}.dat'``)
        kwargs
            Extra parameters for :class:`classes.evaluator.EvaluatorABC` (ie. `strip_phenotypes`)
        """
        super().__init__(**kwargs)
        self._script_name = script_name
        self._script_options = args if args else list()
        self._file_name = filename_format

    def __str__(self):
        return f"{self.__class__.__name__}❬{self._script_name}❭"

    def evaluate_population(self, population: Population) -> None:
        individuals = population.not_finalized
        files = list()
        for idx, ind in individuals:
            self._fitness_calls += 1
            files.append(self._file_name.format(i=population.individuals[idx].id))
            with open(files[-1], "w") as dump:
                dump.write(self.cook(population.dump_individual(idx)))

        try:
            result = subprocess.run(
                [self._script_name, *self._script_options, *files],
                universal_newlines=True,
                check=True,
                text=True,
                timeout=10,
                capture_output=True,
            )
        except subprocess.CalledProcessError as problem:
            microgp_logger.debug("MakefileEvaluator:evaluate: CalledProcessError: %s", problem)
            result = None
        except subprocess.TimeoutExpired:
            microgp_logger.debug("MakefileEvaluator:evaluate: TimeoutExpired")
            result = None

        if result is None:
            raise RuntimeError("Process failed (returned None)")
        elif not result.stdout:
            raise RuntimeError(f"Process returned empty stdout (stderr: '{result.stderr}')")
        else:
            results = list(filter(lambda s: bool(s), result.stdout.split("\n")))
            assert len(results) == len(
                individuals
            ), f"ValueError: number of results and number of individual mismatch (paranoia check): found {len(results)} expected {len(individuals)}"
            for ind, line in zip_longest(individuals, results):
                value = [float(r) for r in line.split()]
                if len(value) == 1:
                    value = value[0]
                fitness = make_fitness(value)
                ind[1].fitness = fitness

        for f in files:
            os.unlink(f)
