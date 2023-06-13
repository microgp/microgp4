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
# v1 / May 2023 / Squillero (GX)

__all__ = ['Statistics', 'fitness_function', 'genetic_operator']

from typing import Callable
from dataclasses import dataclass

from functools import wraps
from inspect import signature
from copy import copy
import shelve
from pickle import HIGHEST_PROTOCOL
from collections import namedtuple

from microgp4.user_messages.checks import *
from microgp4.user_messages import *
from microgp4.global_symbols import *
from microgp4.classes.individual import Individual, Birth
from microgp4.classes.fitness import *
from microgp4 import fitness
from microgp4.fitness_log import *

FAMILYTREE_FILENAME = 'genealogy.db'
FITNESS_LOG_FILENAME = 'fitness.db'


def _genetic_operator_proto(*, strength=1.0) -> list[Individual] | None:
    """Example of signature for a genetic operator"""
    raise NotImplementedError


def _initializer_proto(top_frame) -> list[Individual] | None:
    """Example of signature for a genetic operator"""
    raise NotImplementedError


@dataclass
class Statistics:
    """Class for keeping stats of a genetic operator."""
    calls: int = 0
    aborts: int = 0
    total_offsprint: int = 0
    complete_failures: int = 0
    partial_failures: int = 0
    partial_successes: int = 0
    complete_successes: int = 0
    pass


def fitness_function(func: Callable[..., FitnessABC] | None = None,
                     /,
                     *,
                     type_: type[FitnessABC] = fitness.Scalar,
                     backend: str | None = 'list'):

    log_ = FitnessLog(backend)

    @wraps(func)
    def wrapper(*args, log=log_, **kwargs):
        result = type_(func(*args, **kwargs))
        log += result
        return result

    wrapper.microgp = UGP4_TAG
    wrapper.type = FITNESS_FUNCTION

    if func is None:
        # called with args... let's roll again
        return lambda f: fitness_function(f, type_=type_, backend=backend)
    else:
        return wrapper


def genetic_operator(*, num_parents: int = 1, family_tree: str | None = 'dict'):
    r"""Register a function as a "genetic operator" in MicroGP

    A genetic operator creates individual. A genetic operators is given `num_parents` individual and produces a list
    of new individuals (the offspring). If the operator return an empty list or `None`, or if it raises a
    `GeneticOperatorFailure` exception, it is considered to have aborted.

    Genetic operators gets any number of parents as arguments and the `strength` as mandatory keyword argument. That is:

    >>> def genetic_operator(*, strength=1.0) -> list[Individual] | None:

    Historically, genetic operators are classified either as *mutation operators*, when `num_parents == 1`,
    or *recombination operators*, when `num_parents >= 2`. MicroGP4 handles a third class: the *initializers*,
    when `num_parent == None`. Initializers are called before the first generation, when the population is empty,
    and gets as argument only the `top_frame` of individuals (that is: no *parent* is needed, as there are none
    available, yet). Also, the `strength` is missing. That is:

    >>> def initializer(top_frame) -> list[Individual] | None:

    If an operator does not require a parent, but it is supposed to be called after initialization, set `num_parents
    = 0`. It will be called with an empty individual as argument (ie. only NODE_ZERO)
    """

    assert num_parents is None or check_value_range(num_parents, 1)

    def decorator(func):

        if num_parents is None:
            assert set(p.name for p in signature(_initializer_proto).parameters.values()) == set(p.name for p in signature(func).parameters.values()), \
                f"TypeError: invalid signature for a population initializer '{func.__name__}{signature(func)}'"
        else:
            assert set(p.name for p in signature(_genetic_operator_proto).parameters.values()) <= set(p.name for p in signature(func).parameters.values()), \
                f"TypeError: invalid signature for a genetic operator '{func.__name__}{signature(func)}'"

        @wraps(func)
        def wrapper(*args: Individual, **kwargs):
            wrapper.stats.calls += 1
            try:
                offspring = func(*args, **kwargs)
            except GeneticOperatorAbort:
                offspring = list()

            if offspring is None:
                offspring = []
            elif isinstance(offspring, Individual):
                offspring = [offspring]

            offspring = [i for i in offspring if i.is_feasible]
            for i in offspring:
                i._birth = Birth(func.__module__ + '.' + func.__name__, tuple(args))
            wrapper.stats.total_offsprint += len(offspring)
            return offspring

        wrapper.microgp = UGP4_TAG
        wrapper.type = GENETIC_OPERATOR
        wrapper.num_parents = num_parents
        wrapper.stats = Statistics()

        return wrapper

    return decorator
