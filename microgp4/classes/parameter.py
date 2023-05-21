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

__all__ = ['ParameterABC', 'ParameterStructuralABC']

from abc import ABC, abstractmethod
from typing import Any

from networkx.classes import MultiDiGraph

from microgp4.user_messages import *
from microgp4.classes.pedantic import PedanticABC
from microgp4.classes.evolvable import EvolvableABC
from microgp4.classes.node_reference import NodeReference


class ParameterABC(EvolvableABC, PedanticABC, ABC):
    """Generic class for storing a Macro parameter"""

    __slots__ = ['target_variable']  # Preventing the automatic creation of __dict__

    COUNTER = 0

    def __init__(self):
        ParameterStructuralABC.COUNTER += 1
        self._key = ParameterStructuralABC.COUNTER

    @property
    def key(self):
        return self._key

    def __eq__(self, other: 'ParameterABC') -> bool:
        if type(self) != type(other):
            return False
        else:
            return self.key == other.key and self.value == other.value

    def __str__(self):
        return str(self.value)

    def __format__(self, format_spec):
        return format(self.value, format_spec)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        assert self.is_valid(new_value), \
            "ValueError: invalid value: {} (paranoia check)".format(new_value)
        self._value = new_value

    def is_valid(self, obj: Any) -> bool:
        if not super().is_valid(obj):
            return False
        if obj is None:
            return False
        return True


class ParameterStructuralABC(ParameterABC, ABC):
    """Generic class for storing a Macro structural parameter"""

    __slots__ = []  # Preventing the automatic creation of __dict__

    _node_reference: NodeReference | None

    def __init__(self):
        super().__init__()
        self._node_reference = None

    def _fasten(self, node_reference):
        assert check_valid_type(node_reference, NodeReference)
        assert check_valid_type(node_reference.graph, MultiDiGraph)
        assert check_valid_type(node_reference.node, int)
        assert node_reference.node in node_reference.graph
        self._node_reference = node_reference

    def _unfasten(self):
        self._node_reference = None

    @property
    def is_fastened(self) -> bool:
        return self._node_reference is not None

    @property
    def value(self):
        if self._node_reference is None:
            return None
        else:
            return next((v for u, v, k in self._node_reference.graph.edges(self._node_reference.node, keys=True)
                         if k == self.key), None)

    def drop_link(self):
        if self.value:
            self._node_reference.graph.remove_edge(self._node_reference.node, self.value, self.key)

    def __str__(self):
        return f'n{self.value}'

    def __format__(self, format_spec):
        return 'n' + format(self.value, format_spec)

    def is_valid(self, obj: Any) -> bool:
        assert check_valid_type(obj, int)
        if not super().is_valid(obj):
            return False
        if not self.is_fastened:
            return False
        # TODO: Da fare
        return True
