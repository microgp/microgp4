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

# NOTE[GX]: This file contains code that some programmer may find upsetting

__all__ = ['Individual']

from typing import Any, Callable
from itertools import chain, zip_longest
from copy import deepcopy
from dataclasses import dataclass

import networkx as nx

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError as e:
    plt_errror = e
    plt = None

from microgp4.user_messages import *
from microgp4.global_symbols import *
from microgp4.tools.graph import *

from microgp4.classes.fitness import FitnessABC
from microgp4.classes.paranoid import Paranoid
from microgp4.classes.value_bag import ValueBag
from microgp4.classes.node_reference import NodeReference
from microgp4.classes.node_view import NodeView
from microgp4.classes.frame import FrameABC
from microgp4.classes.readymade_macros import MacroZero


@dataclass(frozen=True)
class Birth:
    operator: Callable
    parents: tuple


class Individual(Paranoid):
    """
    MicroGP individual, that is, a genotype and its fitness

    An Individual is a forest stored in a NetworkX MultiDiGraph, each tree representing a chunk of code,
    plus the framework definition to check its structural correctness.

    All tree root nodes are connected to "Node Zero" -- thus, technically, it is not a forest, but a single tree :$

    Edges of `kind=FRAMEWORK` store the structure, while edges of `kind=LINK` store parameters and other references
    -- thus, technically, the individual is not even a tree, but a weekly-connected multigraph that may contains
    loops ://)

    Individuals are created by passing a reference to the top frame. Please note that frames are types, and their
    instances (ie. the objects) are stored as attributes inside the tree nodes.

    Individuals are managed by a `Population` class.
    """

    __COUNTER: int = 0

    _genome: nx.classes.MultiDiGraph
    _fitness: FitnessABC | None
    _str: str

    # A rainbow color mapping using matplotlib's tableau colors
    SHARP_COLORS_NUM = 7
    SHARP_COLORS_PALETTE = [
        'tab:blue',  # 1f77b4
        'tab:orange',  # ff7f0e
        'tab:green',  # 2ca02c
        'tab:red',  # d62728
        'tab:purple',  # 9467bd
        #'tab:brown',  # 8c564b
        #'tab:pink',  # e377c2
        #'tab:gray',  # 7f7f7f
        'tab:olive',  # bcbd22
        'tab:cyan'  # 17becf
    ]

    def __init__(self, top_frame: type[FrameABC]) -> None:
        Individual.__COUNTER += 1
        self._id = Individual.__COUNTER
        self._genome = nx.MultiDiGraph(node_count=1, top_frame=top_frame)
        self._genome.add_node(NODE_ZERO, root=True, _selement=MacroZero(), _type=MACRO_NODE)
        self._fitness = None
        self._str = ''
        self._structure_tree = None
        self._birth = None

    @property
    def clone(self) -> 'Individual':
        scratch = self._fitness, self._birth
        self._fitness, self._birth = None, None
        I = deepcopy(self)
        Individual.__COUNTER += 1
        I._id = Individual.__COUNTER
        self._fitness, self._birth = scratch
        return I

    @property
    def nodes(self):
        """Generate nodes in a depth-first-search pre-ordering visit of individual."""
        return nx.dfs_preorder_nodes(self.structure_tree, source=NODE_ZERO)

    def __del__(self) -> None:
        self._genome.clear()  # NOTE[GX]: I guess it's useless...

    def __str__(self):
        node_types = list(t for n, t in self.G.nodes(data='_type'))
        n_nodes = len(self.G)
        n_macros = node_types.count(MACRO_NODE) - 1
        n_frames = node_types.count(FRAME_NODE)
        n_links = sum(True for _, _, k in self.G.edges(data='_type') if k != FRAMEWORK)
        n_params = sum(True for p in chain.from_iterable(self.G.nodes[n]['_selement'].parameter_types.items()
                                                         for n in self.G
                                                         if self.G.nodes[n]['_type'] == MACRO_NODE))
        me = f'𝕚{self._id}:' + \
             f''' {n_frames} frame{'s' if n_frames != 1 else ''} and {n_macros} macro{'s' if n_frames != 1 else ''}''' + \
             f''' ({n_params:,} parameter{'s' if n_params != 1 else ''} total''' + \
             f''', {n_links:,} structural)''' + \
             f''' ⇨ {self.fitness}'''
        return me

    def __eq__(self, other: 'Individual') -> bool:
        if type(self) != type(other):
            return False
        else:
            return all(
                is_equal(NodeReference(self.G, n1), NodeReference(other.G, n2))
                for n1, n2 in zip_longest(self.nodes, other.nodes))

    def __hash__(self):
        return hash(self._id)

    # PROPERTIES

    @property
    def id(self):
        return self._id

    @property
    def is_finalized(self):
        return self._fitness is not None

    # PEDANTIC
    @property
    def valid(self) -> bool:
        return all(self.genome.nodes[n]['_selement'].is_valid(NodeView(NodeReference(self.genome, n)))
                   for n in nx.dfs_preorder_nodes(self.structure_tree, source=NODE_ZERO))

    @property
    def OLDISH_valid(self) -> bool:
        """Checks the syntax of the individual."""
        for n in nx.dfs_preorder_nodes(self.structure_tree, source=NODE_ZERO):
            if '_frame' in self._genome.nodes[n]:
                if not self._genome.nodes[n]['_frame'].run_checks(NodeView(self._genome, n)):
                    return False
            elif '_macro' in self._genome.nodes[n]:
                if not self._genome.nodes[n]['_macro'].run_checks(NodeView(self._genome, n)):
                    return False
                if not all(p.valid for p in self._genome.nodes[n]['_macro'].parameters.values()):
                    return False
            elif 'root' in self._genome.nodes[n] and self._genome.nodes[n]['root'] is True:
                pass  # safe
            else:
                raise SyntaxWarning(f"Unknown node type: {self._genome.nodes[n]}")
        return True

    @property
    def G(self):
        """Individual's underlying NetworkX MultiDiGraph."""
        return self._genome

    @property
    def genome(self):
        """Individual's genome (ie. the underlying NetworkX MultiDiGraph)."""
        return self._genome

    @property
    def structure_tree(self) -> nx.classes.DiGraph:
        """A tree with the structure tree of the individual (ie. only edges of `kind=FRAMEWORK`)."""

        if self._structure_tree:
            return self._structure_tree
        gt = get_structure_tree(self._genome)
        if self.is_finalized:
            self._structure_tree = gt
        return gt

    @property
    def birth(self):
        return self._birth

    @property
    def fitness(self):
        """The fitness of the individual."""
        return self._fitness

    def _check_fitness(self, value):
        check_valid_types(value, FitnessABC)
        assert not self.is_finalized, \
            f"ValueError: Individual marked as final, fitness value already set to {self._fitness} (paranoia check)"
        return True

    @fitness.setter
    def fitness(self, value: FitnessABC):
        """Set the fitness of the individual and update operator stats"""
        assert self._check_fitness(value)
        self._fitness = value
        if any(value >> i.fitness for i in self._birth.parents) and \
                any(value >> i.fitness or not value.is_distinguishable(i.fitness) for i in self.birth.parents):
            self._birth.operator.stats.successes += 1
        elif any(value << i.fitness for i in self.birth.parents) and \
                any(value << i.fitness or not value.is_distinguishable(i.fitness) for i in self.birth.parents):
            self._birth.operator.stats.failures += 1

    @property
    def macros(self):
        return [self._genome.nodes[n]['_macro'] for n in get_all_macros(self._genome)]

    @property
    def parameters(self):
        return get_all_parameters(self._genome)

    # PUBLIC METHODS
    def as_forest(self, *, figsize: tuple = (12, 10), filename: str | None = None, **kwargs) -> None:
        r"""Draw the structure tree of the individual.

        Generate a figure representing the individual using NetworkX's `multipartite_layout` [1]_
        with layers corresponding to the depth of nodes in the tree structure.

        The `figsize` argument is forwarded to pyplot's `figure`.

        If `filename` is not None, instead of displaying it, the figure is saved using pyplot's savefig [2]_.
        The format is chosen by the extension.

        Possible `kwargs`, are passed to pyplot's ``savefig``.

        Notes
        -----
            Consider using ``bbox_inches='tight'`` to trim the empty border.

        Parameters
        ----------
        figsize: tuple
            pyplot's ``figsize`` in inches
        filename: str
            name of the file (format based on extension)
        kwargs:
            optional arguments for pyplot's ``savefig``

        References
        ----------
        .. [1] https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.multipartite_layout.html
        .. [2] https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html

        """

        if plt is None:
            user_warning(f"Rendering of individuals not available: {plt_errror}")
            return

        if filename:
            fig = self._draw_forest(figsize)
            fig.savefig(filename, **kwargs)
            plt.close()
        else:
            self._draw_forest(figsize)

    def as_lgp(self, *, figsize: tuple = (12, 10), filename: str | None = None, **kwargs) -> None:
        r"""Draw the individual as a LGP genome.

        Generate a figure representing the individual using NetworkX's `multipartite_layout` [1]_ showing only the
        macros. The representation resembles those of an individual in a Linear Genetic Programming [2]_
        framework, composed of multiple linear segments.

        The `figsize` argument is forwarded to pyplot's `figure`.

        If `filename` is not None, instead of displaying it, the figure is saved using pyplot's savefig [3]_.
        The format is chosen by the extension.

        Possible `kwargs`, are passed to pyplot's ``savefig``.

        Notes
        -----
            Consider using ``bbox_inches='tight'`` to trim the empty border.

        Parameters
        ----------
        figsize: tuple
            pyplot's ``figsize`` in inches
        filename: str
            name of the file (format based on extension)
        kwargs:
            optional arguments for pyplot's ``savefig``

        References
        ----------
        .. [1] https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.multipartite_layout.html
        .. [2] https://en.wikipedia.org/wiki/Linear_genetic_programming
        .. [3] https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html

        """

        if not plt:
            user_warning(f"Rendering of individuals not available: {plt_errror}")
            return

        if filename:
            fig = self._draw_multipartite(figsize)
            fig.savefig(filename, **kwargs)
            plt.close()
        else:
            self._draw_multipartite(figsize)

    def discard_useless_components(self):
        G = nx.MultiDiGraph()
        G.add_edges_from(self.G.edges)
        T = self.structure_tree
        for v in list(T.successors(0))[1:]:
            G.remove_edge(0, v)
        ccomp = list(nx.weakly_connected_components(G))
        self.G.remove_nodes_from(chain.from_iterable(ccomp[1:]))

    def dump(self, extra_parameters: dict) -> str:
        self._str = ''
        for n in self.nodes:
            self._str += Individual._dump_node(NodeReference(self.genome, n), extra_parameters)
        return self._str

    @staticmethod
    def _dump_node(nr: NodeReference, parameters) -> str:
        local_parameters = parameters | nr.graph.nodes[nr.node] | {'_node': NodeView(nr)}
        #local_parameters |= nr.graph.nodes[nr.node]['_selement'].parameters
        if hasattr(nr.graph.nodes[nr.node]['_selement'], 'extra_parameters'):
            local_parameters |= nr.graph.nodes[nr.node]['_selement'].extra_parameters
        bag = ValueBag(local_parameters)

        # GENERAL NODE HEADER
        str = '{_text_before_node}'.format(**bag)

        if nr.graph.in_degree(nr.node) > 1:
            str += bag['_label'].format(**bag)

        if nr.graph.nodes[nr.node]['_type'] == MACRO_NODE:
            str += '{_text_before_macro}'.format(**bag)
            str += nr.graph.nodes[nr.node]['_selement'].dump(bag)
            if bag['$dump_node_info']:
                str += '  {_comment}{_comment} {_node.pathname} ➜ {_node.name}'.format(**bag)
            str += '{_text_after_macro}'.format(**bag)
        elif nr.graph.nodes[nr.node]['_type'] == FRAME_NODE:
            str += '{_text_before_frame}'.format(**bag)
            if bag['$dump_node_info']:
                str += '{_comment}{_comment} {_node.pathname} ➜ {_node.name}{_text_after_macro}'.format(**bag)
            str += '{_text_after_frame}'.format(**bag)

        # GENERAL NODE FOOTER
        str += '{_text_after_node}'.format(**bag)

        return str

    def _draw_forest(self, figsize) -> None:
        """Draw individual using multipartite_layout"""

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()

        ##############################################################################
        # get T
        T = nx.DiGraph()
        T.add_edges_from((u, v) for u, v, k in self.G.edges(data='_type') if k == FRAMEWORK)
        for n in T:
            T.nodes[n]['depth'] = len(nx.shortest_path(T, 0, n))
        pos = nx.multipartite_layout(T, subset_key="depth", align="horizontal")
        pos = {node: (-x, -y) for (node, (x, y)) in pos.items()}
        colors = get_node_color_dict(self.G)
        T.remove_node(0)
        # draw structure
        nx.draw_networkx_edges(T, pos, style=':', edge_color='lightgray', ax=ax)
        # draw macros
        nodelist = [n for n in T if self.G.nodes[n]['_type'] == MACRO_NODE]
        nx.draw_networkx_nodes(T,
                               pos,
                               nodelist=nodelist,
                               node_color=[colors[n] for n in nodelist],
                               cmap=plt.cm.tab20,
                               ax=ax)
        # draw frames
        nodelist = [n for n in self.G if self.G.nodes[n]['_type'] == FRAME_NODE]
        nx.draw_networkx_nodes(T,
                               pos,
                               nodelist=nodelist,
                               node_shape='s',
                               node_color=[colors[n] for n in nodelist],
                               cmap=plt.cm.Pastel1,
                               ax=ax)
        nx.draw_networkx_labels(T, pos)

        ##############################################################################
        # Draw links
        U = nx.DiGraph()
        U.add_edges_from((u, v)
                         for u, v, k in self.G.edges(data='_type')
                         if k == LINK and T.nodes[u]['depth'] == T.nodes[v]['depth'])
        nx.draw_networkx_edges(
            U,
            pos,
            edge_color=[
                Individual.SHARP_COLORS_PALETTE[n % Individual.SHARP_COLORS_NUM] for n in range(U.number_of_edges())
            ],
            connectionstyle='arc3,rad=-.3',
            ax=ax)
        U = nx.DiGraph()
        U.add_edges_from((u, v)
                         for u, v, k in self.G.edges(data='_type')
                         if k == LINK and T.nodes[u]['depth'] != T.nodes[v]['depth'])
        nx.draw_networkx_edges(
            U,
            pos,
            edge_color=[
                Individual.SHARP_COLORS_PALETTE[n % Individual.SHARP_COLORS_NUM] for n in range(U.number_of_edges())
            ],
            ax=ax)

        return fig

    def _draw_multipartite(self, figsize) -> None:
        """Draw individual using multipartite_layout"""

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()

        ##############################################################################
        # get T
        T = nx.DiGraph()
        T.add_edges_from((u, v) for u, v, k in self.G.edges(data='_type') if k == FRAMEWORK)
        prev = 0
        # get P
        P = nx.DiGraph()
        for n in nx.dfs_preorder_nodes(T, NODE_ZERO):
            if (0, n) in list(self.G.in_edges(n)):
                prev = None
            if prev:
                P.add_edge(prev, n)
            if self.G.nodes[n]['_type'] == MACRO_NODE:
                prev = n
        for u, v in list(P.edges):
            if self.G.nodes[n]['_type'] == MACRO_NODE:
                for succ in P.successors(v):
                    P.add_edge(u, succ)
        P.remove_nodes_from([0] + [n for n in P.nodes if self.G.nodes[n]['_type'] != MACRO_NODE])
        # get components
        ccomp = list(nx.weakly_connected_components(P))
        ccomp_lat = {n: pi for pi, part in enumerate(ccomp) for n in part}
        for n, p in [(n, next(i for i, p in enumerate(ccomp) if n in p)) for n in P]:
            P.nodes[n]['subset'] = p
        pos = nx.multipartite_layout(P)
        colors = get_node_color_dict(self.G)
        nodelist = list(P.nodes)
        # draw heads
        nx.draw_networkx_nodes(P, pos, nodelist=[nodelist[0]], node_size=800, node_color='gold', ax=ax)
        nodelist = [_get_first_macro(v, self.G, T) for u, v in T.edges(NODE_ZERO)]
        nx.draw_networkx_nodes(P, pos, nodelist=nodelist, node_size=600, node_color='yellow', ax=ax)
        nodelist = list(P.nodes)
        # draw chunks
        nx.draw(P,
                pos,
                nodelist=nodelist,
                node_color=[colors[n] for n in nodelist],
                cmap=plt.cm.tab20,
                node_size=400,
                with_labels=True,
                edge_color='lightgray',
                style=':',
                ax=ax)

        ##############################################################################
        # Draw links
        U = nx.DiGraph()
        U.add_edges_from((u, v) for u, v, k in self.G.edges(data='_type') if k == LINK and ccomp_lat[u] == ccomp_lat[v])
        nx.draw_networkx_edges(
            U,
            pos,
            edge_color=[
                Individual.SHARP_COLORS_PALETTE[n % Individual.SHARP_COLORS_NUM] for n in range(U.number_of_edges())
            ],
            width=2.0,
            alpha=.5,
            connectionstyle='arc3,rad=-.4',
            ax=ax)
        U = nx.DiGraph()
        U.add_edges_from((u, v) for u, v, k in self.G.edges(data='_type') if k == LINK and ccomp_lat[u] != ccomp_lat[v])
        nx.draw_networkx_edges(
            U,
            pos,
            edge_color=[
                Individual.SHARP_COLORS_PALETTE[n % Individual.SHARP_COLORS_NUM] for n in range(U.number_of_edges())
            ],
            width=2.0,
            alpha=.5,
            ax=ax)

        return fig
