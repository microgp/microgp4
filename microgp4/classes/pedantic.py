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

__all__ = ['Pedantic']

from abc import ABC, abstractmethod
from typing import Callable, Optional

from microgp4.user_messages import microgp_logger


class Pedantic:
    r"""Pedantic classes can check the validity of nodes references and of their own attributes.

    * Value checks can be added dynamically to a `Pedantic` class via the @classmethod `add_attributes_check`.

    * Node checks can be added dynamically to a `Pedantic` class via the @classmethod `add_node_check`.

    All checks, both value- and node- ones, can be later called from an instance with
    `object.is_valid(node_reference)`. If the class does not implement node checks, the parameter
    `node_reference` can be omitted or be explicitly ``None``.
    """

    __last_check_result: bool
    NODE_CHECKS: list[Callable] = list()
    ATTRIBUTE_CHECKS: list[Callable] = list()

    @classmethod
    def add_node_check(cls, function: Callable) -> None:
        try:
            cls.NODE_CHECKS.append(function)
        except AttributeError:
            cls.NODE_CHECKS = [function]

    @classmethod
    def add_attributes_check(cls, function: Callable) -> None:
        try:
            cls.ATTRIBUTE_CHECKS.append(function)
        except AttributeError:
            cls.ATTRIBUTE_CHECKS = [function]

    def is_valid(self, node: Optional['NodeReference'] = None) -> bool:
        r"""Checks the validity of a `NodeReference` and internal attributes"""
        self.__last_check_result = False
        if hasattr(self.__class__, 'NODE_CHECKS') and not all(f(node) for f in self.__class__.NODE_CHECKS):
            assert self._is_valid_debug(node)
            return False
        if hasattr(self.__class__, 'ATTRIBUTE_CHECKS') and not all(f(self) for f in self.__class__.ATTRIBUTE_CHECKS):
            assert self._is_valid_debug(node)
            return False
        self.__last_check_result = True
        return True

    def _is_valid_debug(self, node: 'NodeReference') -> None:
        if hasattr(self.__class__, 'NODE_CHECKS'):
            for f in self.__class__.NODE_CHECKS:
                microgp_logger.debug(f"NodeChecks: {f.__name__}({node}): {f(node)}")
        if hasattr(self.__class__, 'ATTRIBUTE_CHECKS'):
            for f in self.__class__.ATTRIBUTE_CHECKS:
                microgp_logger.debug(f"ValueChecks: {f.__name__}({self!r}): {f(self)}")
