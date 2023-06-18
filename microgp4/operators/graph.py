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
from microgp4.global_symbols import FRAMEWORK, NODE_ZERO
from microgp4.tools.graph import *
from microgp4.classes import monitor
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
    G.add_edge(NODE_ZERO, new_node, kind=FRAMEWORK)

    parameters = get_all_parameters(G, new_node, nodes=True)
    for p, n in parameters:
        if isinstance(p, ParameterStructuralABC):
            p.mutate(1, NodeReference(G, n))
        else:
            p.mutate(1)

    # Initialize structural parameters

    tree = individual.structure_tree
    if all(
            c.is_correct(NodeView(NodeReference(individual.genome, n))) for c, n in ((
                G.nodes[n]['_frame'] if '_frame' in G.nodes[n] else G.nodes[n]['_macro'],
                n) for n in nx.dfs_preorder_nodes(tree, source=NODE_ZERO) if n)):
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


def _unroll_frame(top: type[FrameABC], G: nx.classes.MultiDiGraph) -> int:
    node_id = G.graph['node_count']
    G.graph['node_count'] += 1
    G.add_node(node_id)

    frame_instance = top()
    G.nodes[node_id]['_frame'] = frame_instance
    for f in frame_instance.successors:
        new_node_id = recursive_unroll(f, G)
        G.add_edge(node_id, new_node_id, kind=FRAMEWORK)  # Checkout test/paranoia/networkx

    return node_id


def _unroll_macro(top: type[Macro], G: nx.classes.MultiDiGraph) -> int:
    node_id = G.graph['node_count']
    G.graph['node_count'] += 1
    G.add_node(node_id)

    macro_instance = top()
    G.nodes[node_id]['_macro'] = macro_instance
    for k, p in macro_instance.parameter_types.items():
        macro_instance.parameters[k] = p()

    return node_id


def get_all_frames(G: nx.classes.MultiDiGraph, root: int = 0):
    """~Returns a list of all macros in the tree starting at `root`"""
    tree = nx.classes.DiGraph()
    tree.add_edges_from((u, v) for u, v, k in G.edges(data='kind') if k == FRAMEWORK)
    return [G.nodes[n]['_frame'] for n in nx.dfs_preorder_nodes(tree, root) if '_frame' in G.nodes[n]]


def get_all_macros(G: nx.classes.MultiDiGraph, root: int = 0, *, nodes: bool = False) -> list:
    """~Returns a list of all macros in the tree starting at `root`"""
    tree = nx.classes.DiGraph()
    tree.add_edges_from((u, v) for u, v, k in G.edges(data='kind') if k == FRAMEWORK)
    if nodes:
        return [(G.nodes[n]['_macro'], n) for n in nx.dfs_preorder_nodes(tree, root) if '_macro' in G.nodes[n]]
    else:
        return [G.nodes[n]['_macro'] for n in nx.dfs_preorder_nodes(tree, root) if '_macro' in G.nodes[n]]


def get_all_parameters(G: nx.classes.MultiDiGraph, root: int = 0, *, nodes: bool = False) -> list:
    """~Returns a list of all macros in the tree starting at `root`"""
    if nodes:
        return [(p, n) for m, n in get_all_macros(G, root, nodes=True) for p in m.parameters.values()]
    else:
        return [p for m in get_all_macros(G, root) for p in m.parameters.values()]
