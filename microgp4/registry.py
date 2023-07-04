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

# NOTE[GX]: This file contains code that some programmer may find upsetting

__all__ = ['Statistics', 'fitness_function', 'genetic_operator', 'get_microgp4_type']

from typing import Callable
from dataclasses import dataclass

from functools import wraps
from inspect import signature
import weakref
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


def get_microgp4_type(object):
    if not hasattr(object, 'microgp') or object.microgp != UGP4_TAG or not hasattr(object, 'type'):
        return None
    return object.type


@dataclass
class Statistics:
    """Class for keeping stats of a genetic operator."""
    calls: int = 0
    aborts: int = 0
    offspring: int = 0
    failures: int = 0
    successes: int = 0

    @staticmethod
    def nice(number, tag):
        if number == 0:
            return f'no {tag}s'
        elif number == 1:
            return f'1 {tag}'
        else:
            return f'{number:,} {tag}s'

    def __str__(self):
        return Statistics.nice(self.calls, 'call') + '; ' + Statistics.nice(self.aborts, 'abort') + \
            '; ' + Statistics.nice(self.offspring, 'new individual') + \
            ( f' ({self.successes:,}👍 {self.failures:,}👎)' if self.successes or self.failures else '' )


def fitness_function(func: Callable[..., FitnessABC] | None = None,
                     /,
                     *,
                     type_: type[FitnessABC] = None,
                     backend: str | None = 'list'):

    if type_ is None:
        type_ = lambda f: fitness.make_fitness(f)
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

            assert all(isinstance(i, Individual) for i in offspring), \
                f"TypeError: offspring {offspring!r}: expected list['Individual']"
            offspring = [i for i in offspring if i.valid]
            for i in offspring:
                i._birth = Birth(wrapper, tuple(weakref.proxy(a) for a in args))
            if offspring:
                wrapper.stats.offspring += len(offspring)
            else:
                wrapper.stats.aborts += 1
            return offspring

        wrapper.microgp = UGP4_TAG
        wrapper.type = GENETIC_OPERATOR
        wrapper.num_parents = num_parents
        wrapper.stats = Statistics()

        return wrapper

    return decorator
