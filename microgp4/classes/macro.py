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

__all__ = ["Macro"]

from collections import defaultdict
from typing import Any

from microgp4.user_messages import *

from microgp4.classes.selement import SElement
from microgp4.classes.paranoid import Paranoid
from microgp4.classes.value_bag import USER_PARAMETER
from microgp4.classes.value_bag import ValueBag
from microgp4.classes.node_view import NodeView
from microgp4.classes.parameter import ParameterABC


class Macro(SElement, Paranoid):
    """Base class for all the different Macros."""

    TEXT: str
    PARAMETERS: dict[str, type[ParameterABC]]
    EXTRA_PARAMETERS: dict[str, Any]

    def __init__(self):
        self._dont_use_this_parameters = dict()

    def __eq__(self, other: "Macro") -> bool:
        if type(self) != type(other):
            return False
        elif self.text != other.text or self.parameter_types != other.parameter_types:
            return False
        # elif self.text != other.text or self.parameters != other.parameters:
        #    return False
        return True

    # PEDANTIC
    def is_correct(self, nv: Any) -> bool:
        """Checks a NodeView against a macro."""
        return True
        # assert check_valid_type(nv, NodeView)
        # return all(nv.attributes[n].is_correct(nv.attributes[n].value) for n, p in self.PARAMETERS.items())

    @property
    def text(self) -> str:
        return self.TEXT

    @property
    def extra_parameters(self) -> None:
        return self.EXTRA_PARAMETERS

    @property
    def parameter_types(self) -> dict[str, type[ParameterABC]]:
        return self.PARAMETERS

    # def __getitem__(self, parameter: str) -> Any:
    #    assert Macro.is_name_valid(parameter), \
    #        f"ValueError: invalid parameter name: {parameter} (paranoia check)"
    #    return self.parameters[parameter]

    def __str__(self):
        # BRACKETS: ⁅ ⁆ 〈 〉❬ ❭
        # return f'Macro❬{self.__class__.__name__}❭'
        return self.__class__.__name__

    def dump(self, extra_parameters: ValueBag) -> str:
        check_valid_type(extra_parameters, ValueBag)
        return self.text.format(**extra_parameters)

    @staticmethod
    def is_name_valid(name: str) -> bool:
        if not isinstance(name, str):
            return False
        return bool(USER_PARAMETER.fullmatch(name))
