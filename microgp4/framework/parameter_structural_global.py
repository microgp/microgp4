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

from typing import Type

from itertools import chain
from functools import cache
from numbers import Number

import networkx as nx

from microgp4.user_messages import *
from microgp4.randy import rrandom
from microgp4.global_symbols import *

from microgp4.classes.parameter import ParameterStructuralABC
from microgp4.ea.graph import recursive_unroll, get_all_parameters
from microgp4.classes.node_reference import NodeReference
from microgp4.classes.frame import FrameABC

from microgp4.tools.graph import *
from microgp4.tools.names import canonize_name, _patch_class_info

__all__ = ['global_reference']


@cache
def _global_reference(*,
                      target_name: str | None = None,
                      target_frame: Type[FrameABC] | None = None,
                      first_macro: bool = True,
                      creative_zeal: Number = 0) -> Type[ParameterStructuralABC]:

    class T(ParameterStructuralABC):

        __slots__ = ['_target_frame']  # Preventing the automatic creation of __dict__

        if target_frame:

            def __init__(self):
                super().__init__()
                self._target_frame = target_frame
        else:

            def __init__(self):
                super().__init__()
                self._target_frame = FRAMEWORK_DIRECTORY[canonize_name(target_name,
                                                                       tag='Frame',
                                                                       user=True,
                                                                       warn_duplicates=False)]

        def get_potential_targets(self, suitable_frames: list | None = None):
            G = self._node_reference.graph
            if suitable_frames:
                suitable_frames_ = suitable_frames
            else:
                suitable_frames_ = [
                    n for n in nx.dfs_preorder_nodes(get_grammar_tree(G), source=NODE_ZERO)
                    if '_frame' in G.nodes[n] and isinstance(G.nodes[n]['_frame'], self._target_frame)
                ]
            if first_macro:
                targets = list(chain.from_iterable(get_macros(G, f)[:1] for f in suitable_frames_))
            else:
                targets = list(chain.from_iterable(get_macros(G, f) for f in suitable_frames_))

            if suitable_frames:
                pass
            elif not targets and creative_zeal > 0:
                targets = [None]
            elif isinstance(creative_zeal, int):
                # Add N = creative_zeal 'creation slots'
                targets += [None] * creative_zeal
            elif rrandom.boolean(p_true=creative_zeal):
                # Force creation with p = creative_zeal
                targets = [None]

            if not targets:
                raise MicroGPInvalidIndividual
            return targets

        def mutate(self, strength: float = 1., node_reference: NodeReference | None = None, *args, **kwargs) -> None:
            if node_reference is not None:
                self._fasten(node_reference)

            self.drop_link()

            # first try
            target = rrandom.sigma_choice(self.get_potential_targets(), self.value, strength)
            if target is None:
                new_node = recursive_unroll(self._target_frame, self._node_reference.graph)
                self._node_reference.graph.add_edge(NODE_ZERO, new_node, kind=FRAMEWORK)

                parameters = get_all_parameters(self._node_reference.graph, new_node, nodes=True)
                for p, n in parameters:
                    if isinstance(p, ParameterStructuralABC):
                        p.mutate(1, NodeReference(self._node_reference.graph, n))
                    else:
                        p.mutate(1)

                # second and last try
                target = rrandom.sigma_choice(self.get_potential_targets([new_node]), self.value, strength)

            if not target:
                raise MicroGPInvalidIndividual
            self._node_reference.graph.add_edge(self._node_reference.node, target, key=self.key, kind=LINK)

    _patch_class_info(T, f'GlobalReference[{target_frame}]', tag='parameter')
    return T


def global_reference(target_frame: str | Type[FrameABC],
                     first_macro: bool = False,
                     creative_zeal=0) -> Type[ParameterStructuralABC]:
    assert isinstance(creative_zeal, int) or 0 < creative_zeal < 1, \
        f"ValueError: creative zeal is integer or 0 <= float < 1: found {creative_zeal}"
    if isinstance(target_frame, str):
        return _global_reference(target_name=target_frame, first_macro=bool(first_macro), creative_zeal=creative_zeal)
    else:
        return _global_reference(target_frame=target_frame, first_macro=bool(first_macro), creative_zeal=creative_zeal)