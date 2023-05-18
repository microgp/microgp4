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
# v1 / April 2023 / Squillero (GX)

__all__ = ['FrameABC']

from typing import Union, Type
from types import NoneType
from abc import abstractmethod
from copy import copy

from microgp4.user_messages.checks import *

from microgp4.classes.macro import Macro
from microgp4.classes.evolvable import EvolvableABC
from microgp4.classes.value_bag import ValueBag
from microgp4.classes.checkable import Checkable


class FrameABC(EvolvableABC, Checkable):

    _registered_names = set()

    def __init__(self, parameters: dict | None = None) -> None:
        assert check_valid_types(parameters, dict, NoneType)
        super().__init__()
        self._checks = list()
        self._parameters = parameters if parameters is not None else dict()
        #self._values = list()

    def __eq__(self, other: 'FrameABC') -> bool:
        if type(self) != type(other):
            return False
        else:
            return self.name == other.name

    @property
    def parameters(self):
        return copy(self._parameters)

    @property
    @abstractmethod
    def successors(self) -> list[Type['FrameABC'] | Type[Macro]]:
        pass

    def dump(self, extra_parameters: ValueBag) -> str:
        check_valid_type(extra_parameters, ValueBag)
        return ''

    def is_valid(self, obj) -> bool:
        # TODO: Tupla Grafo/Nodo
        return True

    def run_paranoia_checks(self) -> bool:
        return super().run_paranoia_checks()

    @classmethod
    @property
    def name(cls):
        return (cls.__name__)

    @staticmethod
    def generate_unique_name(tag: str = 'Unknown') -> str:
        FrameABC._name_counter[tag] += 1
        return f'{tag}#{FrameABC._name_counter[tag]}'

    @staticmethod
    def register_name(name: str) -> bool:
        assert name not in FrameABC._registered_names, \
            f"ValueError: Frame name {name!r} already exists (paranoia check)"
        FrameABC._registered_names.add(name)
        return True
