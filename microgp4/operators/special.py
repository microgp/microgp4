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

# =[ HISTORY ]===============================================================
# v1 / June 2023 / Squillero (GX)

__all__ = ['random_individual']

from microgp4.user_messages import *
from microgp4.classes import Population, Individual
from microgp4.registry import *
from microgp4.operators.graph import *

# TODO: random individual non prende pop ma top frame
# TODO: mutate -> inizialize (senza strength!)
# TODO: mutation -> op gen


@genetic_operator(num_parents=None)
def random_individual(*, strength=1.0, top_frame=None) -> None:
    """Generate a valid random individual to the population."""

    new_root = None
    new_individual = None
    while new_root is None:
        new_individual = Individual(top_frame)
        try:
            new_root = unroll(new_individual, top_frame)
        except InvalidIndividual:
            new_root = None
    return new_individual