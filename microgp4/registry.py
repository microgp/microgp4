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

from microgp4.user_messages import *
from microgp4.global_symbols import *
from microgp4.classes.fitness import *
from microgp4 import fitness
from microgp4.fitness_log import *

from copy import copy
import shelve
from pickle import HIGHEST_PROTOCOL
from collections import namedtuple

from microgp4.user_messages.checks import *

FAMILYTREE_FILENAME = 'genealogy.db'
FITNESS_LOG_FILENAME = 'fitness.db'


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

    A genetic operators accept any number (including 0) individuals as parents
    and yields a list of individuals (the offspring). Operators accept two optional
    keyword arguments:

    * strength (default 1.0). If applicable, the `strength` of the operator
    * top_frame (default `None`). The top frame of the generated individuals. If `None` is copied from the first parent

    The operator aborts if:
    * it returns `None`
    * it returns an empty list
    * it raises the exception `GeneticOperatorFailure`
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.stats.calls += 1
            try:
                offspring = func(*args, **kwargs)
            except GeneticOperatorAbort:
                offspring = list()

            if offspring:
                offspring = [i for i in offspring if i.feasible]
                wrapper.stats.total_offsprint += len(offspring)

            return offspring

        wrapper.microgp = UGP4_TAG
        wrapper.type = GENETIC_OPERATOR
        wrapper.num_parents = num_parents
        wrapper.stats = Statistics()

        return wrapper

    return decorator
