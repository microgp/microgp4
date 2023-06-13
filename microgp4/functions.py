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
from microgp4.classes.parameter import ParameterABC

__all__ = ['mutate']


def mutate(parameter: ParameterABC, /, strength: float) -> None:
    """Mutates a parameter

    The function tries at least 100 times to change the parameter by calling `mutate` with the given strength.
    However, if `strength` is 0, `mutate` is not called at all and the parameter is left untouched.

    Parameters
    ----------
    parameter
        the parameter to mutate

    strength
        the strength of the mutation
    """

    counter = 0
    old_value = parameter.value

    while strength > 0 and parameter.value == old_value and counter < 100:
        counter += 1
        parameter.mutate(strength=strength)

    assert parameter.value != old_value or counter < 100 or strength < .01 or \
           performance(f"Failed to mutate {parameter.__class__.__name__} with strength {strength} after {counter:,} attempts",
        stacklevel_offset=1)
