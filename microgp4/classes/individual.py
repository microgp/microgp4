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
from microgp4.global_symbols import FRAMEWORK, LINK
from microgp4.global_symbols import NODE_ZERO
from microgp4.tools.graph import *

from .fitness import FitnessABC
from microgp4.classes.evolvable import EvolvableABC
from microgp4.classes.value_bag import ValueBag
from microgp4.classes.node_reference import NodeReference
from microgp4.classes.node_view import NodeView
from microgp4.classes.frame import FrameABC
from microgp4.classes.readymade_macros import MacroZero


@dataclass(frozen=True)
class Birth:
    operator: Callable
    parents: tuple['Individual']


class Individual(EvolvableABC):
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
        self._genome = nx.MultiDiGraph(node_count=1, top_frame=top_frame)
        self._genome.add_node(NODE_ZERO, root=True, _macro=MacroZero())
        self._fitness = None
        self._str = ''
        self._grammar_tree = None

    def __del__(self) -> None:
        self._genome.clear()  # NOTE[GX]: I guess it's useless...

    def __str__(self):
        n_nodes = len(self.G)
        n_macros = sum('_macro' in self.G.nodes[n] for n in self.G) - 1
        n_frames = sum('_frame' in self.G.nodes[n] for n in self.G)
        n_links = sum(True for _, _, k in self.G.edges(data='kind') if k != FRAMEWORK)
        n_params = sum(True for p in chain.from_iterable(self.G.nodes[n]['_macro'].parameters.items()
                                                         for n in self.G
                                                         if '_macro' in self.G.nodes[n]))
        me = 'Individual with' + \
             f''' {n_frames} frames and {n_macros} macros''' + \
             f''' ({n_params:,} parameter{'s' if n_params != 1 else ''} total''' + \
             f''', {n_links:,} structural)'''
        return me

    def __eq__(self, other: 'Individual') -> bool:
        if type(self) != type(other):
            return False
        else:
            return all(
                is_equal(NodeReference(self.G, n1), NodeReference(other.G, n2)) for n1, n2 in zip_longest(
                    nx.dfs_preorder_nodes(self.G, NODE_ZERO), nx.dfs_preorder_nodes(other.G, NODE_ZERO)))

    # PROPERTIES

    @property
    def finalized(self):
        return self._fitness is not None

    @property
    def G(self):
        """Individual's underlying NetworkX MultiDiGraph."""
        return self._genome

    @property
    def genome(self):
        """Individual's genome (ie. the underlying NetworkX MultiDiGraph)."""
        return self._genome

    @property
    def grammar_tree(self) -> nx.classes.DiGraph:
        """A tree with the grammar tree of the individual (ie. only edges of `kind=FRAMEWORK`)."""

        if self._grammar_tree:
            return self._grammar_tree
        gt = get_grammar_tree(self._genome)
        if self.finalized:
            self._grammar_tree = gt
        return gt

    @property
    def fitness(self):
        """The fitness of the individual."""
        return self._fitness

    def _check_fitness(self, value):
        check_valid_types(value, FitnessABC)
        assert not self.finalized, \
            f"ValueError: Individual marked as final, fitness value already set to {self._fitness} (paranoia check)"
        return True

    @fitness.setter
    def fitness(self, value: FitnessABC):
        """The fitness of the individual."""
        assert self._check_fitness(value)
        self._fitness = value

    @property
    def macros(self):
        return [self._genome.nodes[n]['_macro'] for n in get_macros(self._genome)]

    @property
    def parameters(self):
        return get_parameters(self._genome)

    # REQUIRED ABSTRACT METHODS

    def is_valid(self, obj: Any) -> bool:
        # TODO: Add implementation
        raise NotImplementedError

    # PUBLIC METHODS
    def as_forest(self, *, figsize: tuple = (12, 10), filename: str | None = None, **kwargs) -> None:
        r"""Draw the grammar tree of the individual.

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

        if not plt:
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

    def mutate(self, strength: float = 1., **kwargs: Any) -> None:
        # TODO: Implement it!
        raise NotImplementedError

    def clone(self) -> "Individual":
        I = deepcopy(self)
        I._fitness = None
        return I

    def discard_useless_components(self):
        G = nx.MultiDiGraph()
        G.add_edges_from(self.G.edges)
        T = self.grammar_tree
        for v in list(T.successors(0))[1:]:
            G.remove_edge(0, v)
        ccomp = list(nx.weakly_connected_components(G))
        self.G.remove_nodes_from(chain.from_iterable(ccomp[1:]))

    def dump(self, extra_parameters: dict) -> str:
        if '$omit_banner' in extra_parameters and extra_parameters['$omit_banner']:
            deprecation('Removing the banner with $omit_banner is deprecated', stacklevel_offset=1)
            m0_text = MacroZero.text
            MacroZero.text = ''
        self._str = ''
        self._dump(NodeReference(self.G, 0), extra_parameters)
        if '$omit_banner' in extra_parameters and extra_parameters['$omit_banner']:
            MacroZero.text = m0_text
        return self._str

    def _dump(self, nr: NodeReference, parameters) -> None:

        local_parameters = parameters | nr.graph.nodes[nr.node] | {'_node': NodeView(nr)}
        if '_macro' in nr.graph.nodes[nr.node]:
            local_parameters |= nr.graph.nodes[nr.node]['_macro'].extra_parameters | \
                                nr.graph.nodes[nr.node]['_macro'].parameters
        if '_frame' in nr.graph.nodes[nr.node]:
            local_parameters |= nr.graph.nodes[nr.node]['_frame'].parameters
        bag = ValueBag(local_parameters)

        # GENERAL NODE HEADER
        self._str += '{_text_before_node}'.format(**bag)

        if nr.graph.in_degree(nr.node) > 1:
            self._str += bag['_label'].format(**bag)

        if '_macro' in nr.graph.nodes[nr.node]:
            self._str += '{_text_before_macro}'.format(**bag)
            self._str += nr.graph.nodes[nr.node]['_macro'].dump(bag)
            if bag['$dump_node_info']:
                self._str += '  {_comment}{_comment} {_node.pathname} ➜ {_node.name}'.format(**bag)
            self._str += '{_text_after_macro}'.format(**bag)
        elif '_frame' in nr.graph.nodes[nr.node]:
            self._str += '{_text_before_frame}'.format(**bag)
            if bag['$dump_node_info']:
                self._str += '{_comment}{_comment} {_node.pathname} ➜ {_node.name}{_text_after_macro}'.format(**bag)
            self._str += '{_text_after_frame}'.format(**bag)

        # GENERAL NODE FOOTER
        self._str += '{_text_after_node}'.format(**bag)

        successors = list(get_successors(nr))
        for n in successors:
            self._dump(NodeReference(nr.graph, n), bag)

    def check(self) -> bool:
        """Checks the syntax of the individual."""
        for n in nx.dfs_preorder_nodes(self.grammar_tree, source=NODE_ZERO):
            if '_frame' in self._genome.nodes[n]:
                if not self._genome.nodes[n]['_frame'].run_checks(NodeView(self._genome, n)):
                    return False
            elif '_macro' in self._genome.nodes[n]:
                if not self._genome.nodes[n]['_macro'].run_checks(NodeView(self._genome, n)):
                    return False
            elif 'root' in self._genome.nodes[n] and self._genome.nodes[n]['root'] is True:
                pass  # safe
            else:
                raise SyntaxWarning(f"Unknown node type: {self._genome.nodes[n]}")
        return True

    def _draw_forest(self, figsize) -> None:
        """Draw individual using multipartite_layout"""

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()

        ##############################################################################
        # get T
        T = nx.DiGraph()
        T.add_edges_from((u, v) for u, v, k in self.G.edges(data='kind') if k == FRAMEWORK)
        for n in T:
            T.nodes[n]['depth'] = len(nx.shortest_path(T, 0, n))
        pos = nx.multipartite_layout(T, subset_key="depth", align="horizontal")
        pos = {node: (-x, -y) for (node, (x, y)) in pos.items()}
        colors = get_node_color_dict(self.G)
        T.remove_node(0)
        # draw structure
        nx.draw_networkx_edges(T, pos, style=':', edge_color='lightgray', ax=ax)
        # draw macros
        nodelist = [n for n in T if '_macro' in self.G.nodes[n]]
        nx.draw_networkx_nodes(T,
                               pos,
                               nodelist=nodelist,
                               node_color=[colors[n] for n in nodelist],
                               cmap=plt.cm.tab20,
                               ax=ax)
        # draw frames
        nodelist = [n for n in self.G if '_frame' in self.G.nodes[n]]
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
        U.add_edges_from(
            (u, v) for u, v, k in self.G.edges(data='kind') if k == LINK and T.nodes[u]['depth'] == T.nodes[v]['depth'])
        nx.draw_networkx_edges(
            U,
            pos,
            edge_color=[
                Individual.SHARP_COLORS_PALETTE[n % Individual.SHARP_COLORS_NUM] for n in range(U.number_of_edges())
            ],
            connectionstyle='arc3,rad=-.3',
            ax=ax)
        U = nx.DiGraph()
        U.add_edges_from(
            (u, v) for u, v, k in self.G.edges(data='kind') if k == LINK and T.nodes[u]['depth'] != T.nodes[v]['depth'])
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
        T.add_edges_from((u, v) for u, v, k in self.G.edges(data='kind') if k == FRAMEWORK)
        prev = 0
        # get P
        P = nx.DiGraph()
        for n in nx.dfs_preorder_nodes(T, NODE_ZERO):
            if (0, n) in list(self.G.in_edges(n)):
                prev = None
            if prev:
                P.add_edge(prev, n)
            if '_macro' in self.G.nodes[n]:
                prev = n
        for u, v in list(P.edges):
            if '_frame' in self.G.nodes[v]:
                for succ in P.successors(v):
                    P.add_edge(u, succ)
        P.remove_nodes_from([0] + [n for n in P.nodes if '_macro' not in self.G.nodes[n]])
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
        U.add_edges_from((u, v) for u, v, k in self.G.edges(data='kind') if k == LINK and ccomp_lat[u] == ccomp_lat[v])
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
        U.add_edges_from((u, v) for u, v, k in self.G.edges(data='kind') if k == LINK and ccomp_lat[u] != ccomp_lat[v])
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
