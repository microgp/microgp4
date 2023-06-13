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

__all__ = ['vanilla_ea']

# noinspection PyUnresolvedReferences
from microgp4.operators import *
# noinspection PyUnresolvedReferences
from microgp4.fitness import *
from microgp4.sys import *
from microgp4.classes.population import Population
from microgp4.classes.frame import FrameABC
from microgp4.classes.evaluator import EvaluatorABC
from microgp4.randy import rrandom

from microgp4.registry import *


def vanilla_ea(top_frame: type[FrameABC], evaluator: EvaluatorABC, mu: int = 10, lambda_: int = 20):
    population = Population(top_frame)

    # Initialize population
    ops0 = [op for op in get_operators() if op.num_parents is None]
    while len(population) < mu:
        o = rrandom.choice(ops0)
        population += o(top_frame=top_frame)
    evaluator(population)
    print(population)

    # Let's roll
    for _ in range(100):
        ops = [op for op in get_operators() if op.num_parents is not None]
        new_individuals = list()
        for step in range(lambda_):
            op = rrandom.choice(ops)
            parent = rrandom.choice(population.individuals)
            new_individuals += op(parent, strength=.05)
        population += new_individuals
        evaluator(population)
        population.sort()
        population.individuals[mu:] = []
        print("\n")
        print(population)

    pass
