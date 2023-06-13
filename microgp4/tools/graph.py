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

from collections.abc import Sequence
import networkx as nx

__all__ = [
    'get_predecessor', 'get_siblings', 'get_successors', 'set_successors_order', 'get_structure_tree', 'get_frames',
    'get_macros', 'get_parameters', 'get_node_color_dict', 'is_equal', '_get_first_macro'
]

from microgp4.user_messages.checks import *
from microgp4.global_symbols import *
from microgp4.classes.node_reference import NodeReference
from microgp4.classes.parameter import ParameterABC
from microgp4.tools.names import *


def _check_genome(G: nx.MultiDiGraph) -> bool:
    all_edges = G.edges(keys=True, data=True)
    assert all('kind' in d for u, v, k, d in all_edges), \
        "ValueError: missing 'kind' attribute (paranoia check)"
    tree_edges = [(u, v) for u, v, k, d in all_edges if d['kind'] == FRAMEWORK]
    assert len(tree_edges) == len(set(tree_edges)), \
        "ValueError: duplicated framework edge (paranoia check)"
    assert all(d['kind'] != FRAMEWORK or len(d) == 1 for u, v, k, d in all_edges), \
        "ValueError: unknown attribute in tree edge (paranoia check)"
    return True


def get_structure_tree(G: nx.MultiDiGraph) -> nx.DiGraph:
    tree = nx.DiGraph()
    tree.add_edges_from((u, v) for u, v, k in G.edges(data='kind') if k == FRAMEWORK)
    assert nx.is_branching(tree) and nx.is_weakly_connected(tree), \
        f"ValueError: Structure of {G!r} is not a valid tree (paranoia check)"
    return tree


def get_successors(ref: NodeReference) -> list[int]:
    G = ref.graph
    return [v for u, v, d in G.out_edges(ref.node, data='kind') if d == FRAMEWORK]


def get_predecessor(ref: NodeReference) -> int:
    return next((u for u, v, k in ref.graph.in_edges(ref.node, data='kind') if k == FRAMEWORK), 0)


def get_siblings(ref: NodeReference) -> list[int]:
    """
    Returns the list of all successors of node's only predecessor. That is, the node itself and its siblings.

    Args:
        ref: a NodeRef

    Returns:
        A list of node indexes
    """

    assert ref.node != NODE_ZERO, \
        f"ValueError: NODE_ZERO has ho siblings!"
    return get_successors(NodeReference(ref.graph, get_predecessor(ref)))


def set_successors_order(ref: NodeReference, new_order: Sequence[int]) -> None:
    assert check_valid_type(new_order, Sequence)
    G = ref.graph
    assert _check_genome(G)
    current = list((u, v, k) for u, v, k, d in G.out_edges(ref.node, keys=True, data='kind') if d == FRAMEWORK)
    assert {v for u, v, k in current} == set(new_order), \
        f"ValueError: mismatching new order: {[v for u, v, k in current]} vs. {new_order} (paranoia check)"

    for u, v, k in current:
        G.remove_edge(u, v, k)
    for v in new_order:
        G.add_edge(ref.node, v, kind=FRAMEWORK)


def get_frames(G: nx.MultiDiGraph, name: str | None = None):
    """
    Returns all nodes containing a frame instances with a given name through a DF visit

    Args:
        G: The individual's structure
        name: [Optional] returns only frames with a given name

    Returns:
        A list of node indexes
    """

    assert check_valid_types(G, nx.MultiDiGraph)
    assert name is None or check_valid_types(name, str)

    return [
        n for n in nx.dfs_preorder_nodes(get_structure_tree(G), source=NODE_ZERO) if '_frame' in G.nodes[n] and
        (name is None or uncanonize_name(G.nodes[n]['_frame'].__class__.__name__, user=True) == name)
    ]


def get_macros(G: nx.MultiDiGraph, root: int | None = None):
    """
    Returns all nodes containing a macro instances through a DF visit

    Args:
        G: The individual's structure

    Returns:
        A list of node indexes
    """
    if root is None:
        root = NODE_ZERO
    assert '_frame' in G.nodes[root], \
        f"ValueError: {root} is not a frame node"
    return [n for n in nx.dfs_preorder_nodes(get_structure_tree(G), source=root) if '_macro' in G.nodes[n]]


def get_parameters(G: nx.MultiDiGraph, root: int | None = None) -> list[ParameterABC]:
    """
    Returns all parameters of all macro instances through a DF visit

    Args:
        G: The individual's structure

    Returns:
        A list of ParameterABC
    """
    return [
        p for n in nx.dfs_preorder_nodes(get_structure_tree(G), source=NODE_ZERO) if '_macro' in G.nodes[n]
        for p in G.nodes[n]['_macro'].parameters.values()
    ]


def get_node_color_dict(G: nx.MultiDiGraph) -> dict[int, int]:
    """Assign an index to each node based on the name of the underlying macro."""
    known_labels = dict()
    colors = dict()
    for n in G:
        if '_macro' in G.nodes[n]:
            name = G.nodes[n]['_macro'].__class__.__name__
        else:
            name = G.nodes[n]['_frame'].__class__.__name__
        if name not in known_labels:
            known_labels[name] = len(known_labels)
        colors[n] = known_labels[name]
    return colors


def _get_first_macro(root: int, G: nx.MultiDiGraph, T: nx.DiGraph) -> int:
    """Quick n' dirty."""
    return next((n for n in nx.dfs_preorder_nodes(T, root) if '_macro' in G.nodes[n]), None)


def is_equal(ref1: NodeReference, ref2: NodeReference) -> bool:
    return ref1.graph.nodes[ref1.node] == ref2.graph.nodes[ref2.node]
