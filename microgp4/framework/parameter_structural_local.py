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

from itertools import chain
from functools import cache

from microgp4.user_messages import *
from microgp4.global_symbols import *

from microgp4.classes.parameter import ParameterStructuralABC
from microgp4.classes.node_reference import NodeReference
from microgp4.randy import rrandom

from microgp4.tools.graph import *
from microgp4.tools.names import canonize_name, _patch_class_info

__all__ = ["local_reference"]


@cache
def _local_reference(
    backward: bool = True, self_loop: bool = True, forward: bool = True
) -> type[ParameterStructuralABC]:
    """

    Args:
        backward:
        self_loop:
        forward:

    Returns:

    """

    class T(ParameterStructuralABC):
        __slots__ = []  # Preventing the automatic creation of __dict__

        BACKWARD = backward
        SELF_LOOP = self_loop
        FORWARD = forward

        @property
        def potential_targets(self):
            siblings = get_siblings(self._node_reference)
            i = siblings.index(self._node_reference.node)
            r = list()
            if T.BACKWARD:
                r += siblings[:i]
            if T.SELF_LOOP:
                r += [siblings[i]]
            if T.FORWARD:
                r += siblings[i + 1 :]
            return r

        def mutate(self, strength: float = 1.0, node_reference: NodeReference | None = None, *args, **kwargs) -> None:
            if node_reference is not None:
                self._fasten(node_reference)
            pt = self.potential_targets
            if not pt:
                raise GeneticOperatorFail

            if strength == 1 or self.value is None:
                self.value = rrandom.sigma_choice(pt, None, 1)
            else:
                self.value = rrandom.sigma_choice(pt, pt.index(self.value), strength)

    _patch_class_info(
        T,
        f"""LocalReference[{'<' if backward else '≮'}{'=' if self_loop else '≠'}{'>' if forward else '≯'}]""",
        tag="parameter",
    )
    return T


def local_reference(backward: bool = True, loop: bool = True, forward: bool = True) -> type[ParameterStructuralABC]:
    # TODO: Add checks
    return _local_reference(bool(backward), bool(loop), bool(forward))
