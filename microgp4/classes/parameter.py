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

__all__ = ["ParameterABC", "ParameterStructuralABC"]

from abc import ABC, abstractmethod
from typing import Any

from networkx.classes import MultiDiGraph

from microgp4.global_symbols import *
from microgp4.user_messages import *
from microgp4.classes.selement import SElement
from microgp4.classes.paranoid import Paranoid
from microgp4.classes.node_reference import NodeReference


class ParameterABC(SElement, Paranoid, ABC):
    """Generic class for storing a Macro parameter"""

    __slots__ = ["target_variable"]  # Preventing the automatic creation of __dict__

    COUNTER = 0

    def __init__(self):
        ParameterStructuralABC.COUNTER += 1
        self._key = ParameterStructuralABC.COUNTER

    def __eq__(self, other: "ParameterABC") -> bool:
        if type(self) != type(other):
            return False
        else:
            return self.key == other.key and self.value == other.value

    def __str__(self):
        return str(self.value)

    def __format__(self, format_spec):
        return format(self.value, format_spec)

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        assert self.is_correct(new_value), f"{PARANOIA_VALUE_ERROR}: invalid value: {new_value}"
        self._value = new_value

    @abstractmethod
    def mutate(self, strength: float = 1.0, **kwargs) -> None:
        pass


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
    def graph(self):
        assert self.is_fastened, f"{PARANOIA_VALUE_ERROR}: structural parameter is not fastened"
        return self._node_reference.graph

    @property
    def node(self):
        assert self.is_fastened, f"{PARANOIA_VALUE_ERROR}: structural parameter is not fastened"
        return self._node_reference.node

    @property
    def is_fastened(self) -> bool:
        return self._node_reference is not None

    @property
    def value(self):
        if self._node_reference is None:
            return None
        return next(
            (v for u, v, k in self._node_reference.graph.edges(self._node_reference.node, keys=True) if k == self.key),
            None,
        )

    @value.setter
    def value(self, target_node):
        old_target_node = self.value
        if old_target_node is not None:
            self._node_reference.graph.remove_edge(self._node_reference.node, old_target_node, self.key)
        if target_node is not None:
            self._node_reference.graph.add_edge(self._node_reference.node, target_node, key=self.key, _type=LINK)

    def __str__(self):
        return format(self, '')

    def __format__(self, format_spec):
        target = self.value
        return "n" + format(self.value, format_spec) if target is not None else "*UNSET*"

    def is_correct(self, obj: Any) -> bool:
        assert check_valid_type(obj, int)
        if not super().is_correct(obj):
            return False
        if not self.is_fastened:
            return False
        # TODO: Da fare
        return True
