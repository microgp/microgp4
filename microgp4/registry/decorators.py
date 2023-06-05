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

__all__ = ['fitness_function', 'genetic_operator']

from functools import wraps

from microgp4.global_symbols import *
from microgp4.classes.fitness import *
from microgp4.classes import fitness_base

from .registrar import *
from .stats import *


# A really cool hack suggested by bj0 on Stackoverflow
# See "how-to-create-a-decorator-that-can-be-used-either-with-or-without-parameters"
def doublewrap(func):
    """A decorator decorator, allowing the decorator to be used with and without parameters"""

    @wraps(func)
    def decorator(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            assert callable(args[0]), f"TypeError: Incorrect use of decorator"
            return func(args[0])
        else:
            assert not args, f"TypeError: Incorrect use of decorator"
            return lambda realf: func(realf, *args, **kwargs)

    return decorator


@doublewrap
def fitness_function(func, *, type_: type[FitnessABC] | None = None, registry: Register | None = None):

    if not type_:
        type_ = fitness_base.Scalar
    if not registry:
        registry = GLOBAL_REGISTER
    log_ = FitnessLog()

    @wraps(func)
    def wrapper(*args, log=log_, **kwargs):
        result = type_(func(*args, **kwargs))
        log += result
        return result

    wrapper.microgp = UGP4_TAG
    wrapper.type = FITNESS_FUNCTION
    return wrapper


def genetic_operator(*, num_parents: int = 1, registry: Register | None = None):

    if not registry:
        registry = GLOBAL_REGISTER
    stats = OperatorStatistics()

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            stats.calls += 1
            try:
                result = func(*args, **kwargs)
            except:
                pass
            return result

        wrapper.microgp = UGP4_TAG
        wrapper.type = GENETIC_OPERATOR
        wrapper.num_parents = num_parents
        registry.register_operator(wrapper, stats)

        return wrapper

    return decorator
