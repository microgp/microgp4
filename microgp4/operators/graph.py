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

__all__ = ['unroll']

import networkx as nx

from microgp4.user_messages import *
from microgp4.global_symbols import *
from microgp4.tools.graph import *
from microgp4.classes import monitor
from microgp4.classes.parameter import ParameterABC
from microgp4.classes.individual import Individual
from microgp4.classes.node_view import NodeView, NodeReference
from microgp4.classes.frame import FrameABC
from microgp4.classes.macro import Macro
from microgp4.classes.parameter import ParameterStructuralABC


@monitor.failure_rate
def unroll(individual: Individual, top: type[FrameABC]) -> int | None:
    """
    Recursively unroll a Frame as a subtree inside the Individual's graph.

    Args:
        individual: The individual to unroll the frame into
        top: Frame type to unroll

    Returns:
        The root of the new subtree (an int)
    """

    assert check_valid_types(individual, Individual)
    assert check_valid_types(top, FrameABC, Macro, subclass=True)
    assert not individual.is_finalized, \
        f"ValueError: individual is finalized (paranoia check)"

    G = individual.genome
    new_node = recursive_unroll(top, G)
    if not new_node:
        return None
    G.add_edge(NODE_ZERO, new_node, _type=FRAMEWORK)

    parameters = get_all_parameters(G, new_node, node_id=True)
    for p, n in parameters:
        if isinstance(p, ParameterStructuralABC):
            p.mutate(1, NodeReference(G, n))
        else:
            p.mutate(1)

    # Initialize structural parameters
    # TODO???

    if individual.valid:
        return new_node
    else:
        return None


# NOTE[GX]: I'd love being reasonably generic and efficient in a recursive
# function, but I can't use `singledispatch` from `functools` because I'm
# choosing the implementation using the *value* of `top` -- it's a *type*,
def recursive_unroll(top: type[Macro | FrameABC], G: nx.classes.MultiDiGraph) -> int:
    """Unrolls a frame/macro over the graph."""

    if issubclass(top, FrameABC):
        new_node = _unroll_frame(top, G)
    elif issubclass(top, Macro):
        new_node = _unroll_macro(top, G)
    else:
        raise NotImplementedError(f"{top!r}")

    return new_node


def _unroll_frame(frame_class: type[FrameABC], G: nx.classes.MultiDiGraph) -> int:
    node_id = G.graph['node_count']
    G.graph['node_count'] += 1
    G.add_node(node_id)

    frame_instance = frame_class()
    G.nodes[node_id]['_type'] = FRAME_NODE
    G.nodes[node_id]['_selement'] = frame_instance
    for f in frame_instance.successors:
        new_node_id = recursive_unroll(f, G)
        G.add_edge(node_id, new_node_id, _type=FRAMEWORK)  # Checkout test/paranoia/networkx

    return node_id


def _unroll_macro(macro_class: type[Macro], G: nx.classes.MultiDiGraph) -> int:
    node_id = G.graph['node_count']
    G.graph['node_count'] += 1
    G.add_node(node_id)

    macro_instance = macro_class()
    G.nodes[node_id]['_type'] = MACRO_NODE
    G.nodes[node_id]['_selement'] = macro_instance
    for k, p in macro_instance.parameter_types.items():
        G.nodes[node_id][k] = p()

    return node_id
