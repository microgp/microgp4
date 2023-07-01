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

# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
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

#############################################################################
# HISTORY
# v1 / July 2023 / Squillero (GX)

from microgp4.user_messages.checks import *
from microgp4.classes.individual import Individual
from microgp4.classes.population import Population
from microgp4.randy import rrandom


def tournament_selection(population: Population, tournament_size: float = 2) -> Individual:
    assert check_value_range(tournament_size, min_=1)
    candidates = [rrandom.choice(population.individuals) for _ in range(tournament_size)]
    if rrandom.boolean(p_true=tournament_size % 1):
        candidates.append(rrandom.choice(population.individuals))
    return max(candidates, key=lambda i: i.fitness)
