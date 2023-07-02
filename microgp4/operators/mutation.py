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
# v1 / June 2023 / Squillero (GX)

from microgp4.user_messages import *
from microgp4.classes.frame import *
from microgp4.classes import Population, Individual
from microgp4.registry import *
from microgp4.functions import *
from microgp4.randy import rrandom


@genetic_operator(num_parents=1)
def single_parameter_mutation(parent: Individual, strength=1.0) -> list['Individual']:
    offspring = parent.clone
    param = rrandom.choice(offspring.parameters)
    mutate(param, strength=strength)
    return [offspring]


@genetic_operator(num_parents=1)
def add_macro_to_bunch(parent: Individual, strength=1.0) -> list['Individual']:
    offspring = parent.clone
    G = offspring.genome
    candidates = [n for n in offspring.nodes if isinstance(G.nodes[n]['_selement'], FrameMacroBunch) and G.out_degree[n] < G.nodes[n]['_selement'].SIZE[1]]
    if not candidates:
        raise GeneticOperatorAbort
    node = rrandom.choice(candidates)
    new_macro_type = rrandom.choice(G.nodes[node]['_selement'].POOL)
    new_macro_type

    raise GeneticOperatorAbort
    return [offspring]
