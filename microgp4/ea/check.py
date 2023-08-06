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

from microgp4.operators import *
from microgp4.sys import *


def check() -> None:
    print("## GENETIC OPERATORS")
    print("\n### INIT\n")
    for op in [o for o in get_operators() if o.num_parents is None]:
        print(f"* {op.__qualname__} [{op.stats}]")
    print("\n### MUTATION\n")
    for op in [o for o in get_operators() if o.num_parents is not None and o.num_parents == 1]:
        print(f"* {op.__qualname__} [{op.stats}]")
    print("\n### CROSSOVER\n")
    for op in [o for o in get_operators() if o.num_parents is not None and o.num_parents > 1]:
        print(f"* {op.__qualname__} [{op.stats}]")
