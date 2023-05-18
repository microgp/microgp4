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
# =[ HISTORY ]===============================================================
# v1 / April 2023 / Squillero (GX)

__all__ = ['PedanticABC']

from abc import ABC, abstractmethod
from typing import Any


class PedanticABC(ABC):
    """Abstract class: Pedantic classes do implement the `is_valid(x)` method."""

    @abstractmethod
    def is_valid(self, obj: Any) -> bool:
        """Checks an object against the specifications.

        The function checks the validity of an object against a Pedantic class, for example the current value of a
        parameter against the parameter definition (eg. type, range), or a node against a Frame definition.

        Args:
            obj: Any object

        Returns:
            True if the object is valid, False otherwise
        """
        return True
