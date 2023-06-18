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

#############################################################################
# =[ HISTORY ]===============================================================
# v1 / April 2023 / Squillero (GX)

__all__ = ['PedanticABC']

from abc import ABC, abstractmethod
from typing import Callable

from microgp4.user_messages import microgp_logger
from microgp4.global_symbols import *
from microgp4.classes.node_view import NodeReference


class PedanticABC:
    """Abstract class: Pedantic classes do implement the `is_correct(x)` method.

    Pedantic classes also allow to `add_check` and `run_checks`.
    """



    @property
    def valid(self) -> bool:
        """Checks an object against its specifications.

        The property checks the validity of the object against its definition.

        Returns:
            True if the object is valid, False otherwise
        """
        raise NotImplementedError

    @classmethod
    def add_node_check(cls, function: Callable) -> None:
        try:
            cls.NODE_CHECKS.append(function)
        except AttributeError:
            cls.NODE_CHECKS = [function]

    @classmethod
    def add_value_check(cls, function: Callable) -> None:
        try:
            cls.VALUE_CHECKS.append(function)
        except AttributeError:
            cls.VALUE_CHECKS = [function]

    def is_correct(self, node: NodeReference | None = None) -> bool:
        if hasattr(self.__class__, 'NODE_CHECKS') and not all(f(node) for f in self.NODE_CHECKS):
            microgp_logger.debug(f"CheckFail: Fail NodeCheck: {self.__class__.NODE_CHECKS}")
            return False
        if hasattr(self.__class__, 'VALUE_CHECKS') and not all(f(self) for f in self.VALUE_CHECKS):
            microgp_logger.debug(f"CheckFail: Fail ValueCheck: {self.__class__.VALUE_CHECKS}")
            return False
        return True
