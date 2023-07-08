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

from typing import Optional, Callable

from microgp4.user_messages import *


class SElement:
    r"""Syntactic Element (SElement)

    SElement classe is the building block of the syntax of the individual, the common ancestor of both `macros` and
    `frames`. SElements can check the validity of nodes references. Node checks can be added dynamically to a
    `Pedantic` class via the @classmethod `add_node_check`.

    All checks, both value- and node- ones, can be later called from an instance with
    `object.is_valid(node_reference)`. If the class does not implement node checks, the parameter
    `node_reference` can be omitted or be explicitly ``None``.
    """

    __last_check_result: bool
    # these are immutable to avoid any problem with aliasing
    NODE_CHECKS: tuple[Callable] = tuple()

    @classmethod
    def add_node_check(cls, function: Callable) -> None:
        cls.NODE_CHECKS = tuple([*cls.NODE_CHECKS, function])

    def is_valid(self, node: Optional['NodeReference'] = None) -> bool:
        r"""Checks the validity of a `NodeReference` and internal attributes"""
        self.__last_check_result = all(f(node) for f in self.__class__.NODE_CHECKS)
        return self.__last_check_result

    def _is_valid_debug(self, node: 'NodeReference') -> None:
        self.__last_check_result = True
        for f in self.__class__.NODE_CHECKS:
            if not f(node):
                microgp_logger.info(
                    f"NodeChecks: Failed check on genome 0x{id(node.genome):x}: {f.__qualname__}({node})")
                self.__last_check_result = False
        return self.__last_check_result
