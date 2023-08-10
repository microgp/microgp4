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

__all__ = ['Individual', 'Lineage', 'Age']

from typing import Any, Callable, Optional
from itertools import chain, zip_longest
from copy import deepcopy
from dataclasses import dataclass
import operator

import networkx as nx

from microgp4.user_messages import *
from microgp4.global_symbols import *
from microgp4.tools.graph import *

if matplotlib_available:
    import matplotlib.pyplot as plt

from microgp4.global_symbols import *
from microgp4.classes.fitness import FitnessABC
from microgp4.classes.paranoid import Paranoid
from microgp4.classes.value_bag import ValueBag
from microgp4.classes.node_reference import NodeReference
from microgp4.classes.node_view import NodeView
from microgp4.classes.macro import Macro
from microgp4.classes.frame import FrameABC
from microgp4.classes.parameter import ParameterABC, ParameterStructuralABC
from microgp4.classes.readymade_macros import MacroZero


@dataclass(frozen=True, slots=True)
class Lineage:
    operator: Optional[Callable]
    parents: tuple

    def __str__(self):
        parents = list()
        for p in self.parents:
            try:
                parents.append(str(p))
            except ReferenceError:
                # ☠ ⚰ (coffin) ⚱ (urn) 💀 ✝
                parents.append("☠")

        return self.operator.__name__ + "(" + ", ".join(parents) + ")"


@dataclass(slots=True)
class Age:
    birth: int | None = None
    apparent_age: int = 0

    def __iadd__(self, generations):
        self.apparent_age += generations

    def __str__(self):
        return f'⚝ {self.birth}' + (f' (⌛ {self.apparent_age})' if self.apparent_age else '')


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
    _lineage: Lineage | None
    _age: Age
    _str: str

    # A rainbow color mapping using matplotlib's tableau colors
    SHARP_COLORS_NUM = 7
    SHARP_COLORS_PALETTE = [
        "tab:blue",  # 1f77b4
        "tab:orange",  # ff7f0e
        "tab:green",  # 2ca02c
        "tab:red",  # d62728
        "tab:purple",  # 9467bd
        #'tab:brown',  # 8c564b
        #'tab:pink',  # e377c2
        #'tab:gray',  # 7f7f7f
        "tab:olive",  # bcbd22
        "tab:cyan",  # 17becf
    ]

    def __init__(self, top_frame: type[FrameABC]) -> None:
        Individual.__COUNTER += 1
        self._id = Individual.__COUNTER
        self._genome = nx.MultiDiGraph(node_count=NODE_ZERO + 1, top_frame=top_frame)
        self._genome.add_node(NODE_ZERO, _selement=MacroZero(), _type=MACRO_NODE)
        self._fitness = None
        self._str = ""
        self._structure_tree = None
        self._lineage = None
        self._age = Age()

    def __del__(self) -> None:
        self._genome.clear()  # NOTE[GX]: I guess it's useless...

    def __str__(self):
        return f"𝕚{self._id}"

    def __eq__(self, other) -> bool:
        return (
            type(self) == type(other)
            and self._fitness == other._fitness
            and nx.isomorphism.is_isomorphic(
                self._genome, other._genome, node_match=operator.eq, edge_match=operator.eq
            )
        )

    def __hash__(self):
        return hash(self._id)

    # PROPERTIES

    @property
    def id(self):
        return self._id

    @property
    def is_finalized(self):
        return self._fitness is not None

    @property
    def valid(self) -> bool:
        return all(
            self.genome.nodes[n]["_selement"].is_valid(NodeView(NodeReference(self.genome, n)))
            for n in nx.dfs_preorder_nodes(self.genome)
        )

    @property
    def clone(self) -> "Individual":
        scratch = self._fitness, self._lineage
        self._fitness, self._lineage = None, None
        I = deepcopy(self)
        Individual.__COUNTER += 1
        I._id = Individual.__COUNTER
        self._fitness, self._lineage = scratch
        I._age = Age()
        I._lineage = Lineage(None, (self,))
        return I

    @property
    def dfs_nodes(self):
        """Return all node indexes in reliable order."""
        return list(nx.dfs_preorder_nodes(self.structure_tree))

    @property
    def macros(self):
        """Return all macro instances in unreliable order."""
        return [
            self._genome.nodes[n]["_selement"] for n in self._genome if self._genome.nodes[n]["_type"] == MACRO_NODE
        ]

    @property
    def frames(self):
        """Return all frame instances in unreliable order."""
        return [
            self._genome.nodes[n]["_selement"] for n in self._genome if self._genome.nodes[n]["_type"] == FRAME_NODE
        ]

    @property
    def parameters(self):
        """Return all parameter instances in unreliable order."""
        return [p for n in self._genome for p in self._genome.nodes[n].values() if isinstance(p, ParameterABC)]

    @property
    def OLDISH_valid(self) -> bool:
        """Checks the syntax of the individual."""
        for n in nx.dfs_preorder_nodes(self.structure_tree, source=NODE_ZERO):
            if "_frame" in self._genome.nodes[n]:
                if not self._genome.nodes[n]["_frame"].run_checks(NodeView(self._genome, n)):
                    return False
            elif "_macro" in self._genome.nodes[n]:
                if not self._genome.nodes[n]["_macro"].run_checks(NodeView(self._genome, n)):
                    return False
                if not all(p.valid for p in self._genome.nodes[n]["_macro"].parameters.values()):
                    return False
            elif "root" in self._genome.nodes[n] and self._genome.nodes[n]["root"] is True:
                pass  # safe
            else:
                raise SyntaxWarning(f"Unknown node type: {self._genome.nodes[n]}")
        return True

    @property
    def G(self):
        """Individual's underlying NetworkX MultiDiGraph."""
        # TODO DeprecationWarning?
        return self._genome

    @property
    def genome(self):
        """Individual's genome (ie. the underlying NetworkX MultiDiGraph)."""
        # TODO: Add paranoia check?
        return self._genome

    @property
    def structure_tree(self) -> nx.classes.DiGraph:
        """A tree with the structure tree of the individual (ie. only edges of `kind=FRAMEWORK`)."""

        if self._structure_tree:
            return self._structure_tree

        tree = nx.DiGraph()
        tree.add_nodes_from(self._genome.nodes)
        tree.add_edges_from((u, v) for u, v, k in self._genome.edges(data="_type") if k == FRAMEWORK)
        assert nx.is_branching(tree) and nx.is_weakly_connected(
            tree
        ), f"{PARANOIA_VALUE_ERROR}: Structure of {self!r} is not a valid tree"

        if self.is_finalized:
            self._structure_tree = tree
        return tree

    @property
    def lineage(self):
        return self._lineage

    @property
    def age(self):
        """The age of the individual"""
        return self._age

    @age.setter
    def age(self, value: int):
        assert value >= 0
        self._age = value

    @property
    def fitness(self):
        """The fitness of the individual."""
        assert self.is_finalized, f"{PARANOIA_VALUE_ERROR}: Individual not marked as final, fitness value not set"
        return self._fitness

    def _check_fitness(self, value):
        check_valid_types(value, FitnessABC)
        assert (
            not self.is_finalized
        ), f"{PARANOIA_VALUE_ERROR}: Individual marked as final, fitness value already set to {self._fitness}"
        return True

    @fitness.setter
    def fitness(self, value: FitnessABC):
        """Set the fitness of the individual and update operator stats"""
        assert self._check_fitness(value)
        self._fitness = value
        if any(value >> i.fitness for i in self._lineage.parents) and any(
            value >> i.fitness or not value.is_distinguishable(i.fitness) for i in self.lineage.parents
        ):
            self._lineage.operator.stats.successes += 1
        elif any(value << i.fitness for i in self.lineage.parents) and any(
            value << i.fitness or not value.is_distinguishable(i.fitness) for i in self.lineage.parents
        ):
            self._lineage.operator.stats.failures += 1
        microgp_logger.debug(
            # f"Individual: {self.describe(include_fitness=True, include_birth=True, include_structure=True)}"
            f"Individual: Fitness of {self} is {value}"
        )

    #######################################################################
    # PUBLIC METHODS
    def run_paranoia_checks(self) -> bool:
        assert self.valid, f"{PARANOIA_VALUE_ERROR}: Individual {self!r} is not valid"

        # check genome (structural)
        assert self.genome == self._genome, f"{PARANOIA_VALUE_ERROR}: Panic: genome != _genome"
        assert nx.is_weakly_connected(
            self._genome
        ), f"{PARANOIA_VALUE_ERROR}: genome of {self!r} is not a connected graph"

        # check tree (structural)
        assert nx.is_branching(self.structure_tree) and nx.is_weakly_connected(
            self.structure_tree
        ), f"{PARANOIA_VALUE_ERROR}: structure_tree of {self!r} is not a tree"
        assert (self._fitness is None and not self.is_finalized) or (
            self._fitness is not None and self.is_finalized
        ), f"Value Error (paranoia check): Mismatch fitness and is_finalized"

        # check edges (semantic)
        edges = self._genome.edges(keys=True, data=True)
        assert all("_type" in d for u, v, k, d in edges), "ValueError (paranoia check): missing '_type' attribute"
        assert all(
            d["_type"] != FRAMEWORK or len(d) == 1 for u, v, k, d in edges
        ), "ValueError (paranoia check): unknown attribute in tree edge"
        tree_edges = [(u, v) for u, v, k, d in edges if d["_type"] == FRAMEWORK]
        assert len(tree_edges) == len(set(tree_edges)), "ValueError (paranoia check): duplicated framework edge"

        # check nodes (semantic)
        assert all(
            n < self._genome.graph["node_count"] for n in self._genome
        ), f"{PARANOIA_VALUE_ERROR}: invalid 'node_count' attribute ({self._genome.graph['node_count']})"

        assert all('_selement' in d for n, d in self._genome.nodes(data=True)), f"{PARANOIA_VALUE_ERROR}:"
        assert all(
            (isinstance(d['_selement'], Macro) and d['_type'] == 'macro')
            or (isinstance(d['_selement'], FrameABC) and d['_type'] == 'frame')
            for n, d in self._genome.nodes(data=True)
        )

        assert all(
            p._node_reference == NodeReference(self._genome, n)
            for n in self._genome
            for p in self._genome.nodes[n].values()
            if isinstance(p, ParameterStructuralABC)
        ), f"{PARANOIA_VALUE_ERROR}: Incorrect node_reference in structural parameter"

        return True

    def describe(
        self,
        *,
        include_fitness: bool = True,
        include_structure: bool = True,
        include_age: bool = True,
        include_lineage: bool = True,
        max_recursion: int = 0,
        _indent_level: str = "",
    ):
        desc = str(self)
        delem = list()
        if include_fitness:
            delem.append(f"fitness: {self.fitness}")
        if include_structure:
            node_types = list(t for n, t in self.G.nodes(data="_type"))
            n_nodes = len(self.G)
            n_macros = node_types.count(MACRO_NODE) - 1
            n_frames = node_types.count(FRAME_NODE)
            n_links = sum(True for _, _, k in self.G.edges(data="_type") if k != FRAMEWORK)
            n_params = sum(
                True
                for p in chain.from_iterable(
                    self.G.nodes[n]["_selement"].parameter_types.items()
                    for n in self.G
                    if self.G.nodes[n]["_type"] == MACRO_NODE
                )
            )
            delem.append(
                f"""{n_frames} frame{'s' if n_frames != 1 else ''} and {n_macros} macro{'s' if n_frames != 1 else ''}"""
                + f""" ({n_params:,} parameter{'s' if n_params != 1 else ''} total"""
                + f""", {n_links:,} structural)"""
            )
        if include_age:
            delem.append(str(self.age))
        if include_lineage:
            delem.append(str(self.lineage))
        descr = f"""{_indent_level}{desc} ⇨ {' / '.join(delem)}"""
        if max_recursion is None or max_recursion > 0:
            if max_recursion is not None:
                max_recursion -= 1
            for p in self.lineage.parents:
                try:
                    descr += "\n" + p.describe(
                        include_fitness=include_fitness,
                        include_structure=include_structure,
                        include_lineage=include_lineage,
                        max_recursion=max_recursion,
                        _indent_level=_indent_level + "  ",
                    )
                except ReferenceError:
                    pass
        return descr

    def as_forest(self, filename: str | None = None, *, zoom: int = 1.0, **kwargs) -> None:
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

        if filename:
            fig = self._draw_forest(zoom)
            fig.savefig(filename, bbox_inches='tight', **kwargs)
            plt.close()
        else:
            self._draw_forest(zoom)

    def as_lgp(self, filename: str | None = None, *, zoom: int = 1.0, **kwargs) -> None:
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

        if filename:
            fig = self._draw_multipartite(zoom)
            fig.savefig(filename, bbox_inches='tight', **kwargs)
            plt.close()
        else:
            self._draw_multipartite(zoom)

    def discard_useless_components(self):
        G = nx.MultiDiGraph()
        G.add_edges_from(self.G.edges)
        T = self.structure_tree
        for v in list(T.successors(0))[1:]:
            G.remove_edge(0, v)
        ccomp = list(nx.weakly_connected_components(G))
        self.G.remove_nodes_from(chain.from_iterable(ccomp[1:]))

    def dump(self, extra_parameters: dict) -> str:
        self._str = ""
        for n in self.dfs_nodes:
            self._str += Individual.dump_node(NodeReference(self.genome, n), extra_parameters)
        return self._str

    @staticmethod
    def dump_node(nr: NodeReference, parameters) -> str:
        local_parameters = parameters | nr.graph.nodes[nr.node] | {"_node": NodeView(nr)}
        # local_parameters |= nr.graph.nodes[nr.node]['_selement'].parameters
        if hasattr(nr.graph.nodes[nr.node]["_selement"], "extra_parameters"):
            local_parameters |= nr.graph.nodes[nr.node]["_selement"].extra_parameters
        bag = ValueBag(local_parameters)

        # GENERAL NODE HEADER
        str = "{_text_before_node}".format(**bag)

        if nr.graph.in_degree(nr.node) > 1:
            str += bag["_label"].format(**bag)

        if nr.graph.nodes[nr.node]["_type"] == MACRO_NODE:
            str += "{_text_before_macro}".format(**bag)
            str += nr.graph.nodes[nr.node]["_selement"].dump(bag)
            if bag["$dump_node_info"]:
                str += "  {_comment} [µGP⁴] {_node.pathname} ➜ {_node.name}".format(**bag)
            str += "{_text_after_macro}".format(**bag)
        elif nr.graph.nodes[nr.node]["_type"] == FRAME_NODE:
            str += "{_text_before_frame}".format(**bag)
            if bag["$dump_node_info"]:
                str += "{_comment} [µGP⁴] {_node.pathname} ➜ {_node.name}{_text_after_macro}".format(**bag)
            str += "{_text_after_frame}".format(**bag)

        # GENERAL NODE FOOTER
        str += "{_text_after_node}".format(**bag)

        return str

    def _draw_forest(self, zoom) -> None:
        """Draw individual using multipartite_layout"""

        T = self.structure_tree.copy()
        for n in T:
            T.nodes[n]["depth"] = len(nx.shortest_path(T, 0, n))
        height = max(T.nodes[n]["depth"] for n in T.nodes)
        width = sum(1 for n in T if self.G.nodes[n]["_type"] == MACRO_NODE)
        fig = plt.figure(figsize=(10 + zoom * width * 0.8, zoom * height + width / 2))
        ax = fig.add_subplot()

        T.remove_node(0)
        pos = nx.multipartite_layout(T, subset_key="depth", align="horizontal")
        pos = {node: (-x, -y) for (node, (x, y)) in pos.items()}
        colors = get_node_color_dict(self.G)

        # draw structure
        nx.draw_networkx_edges(
            T, pos, style=":", edge_color="lightgray", arrowstyle="-|>,head_length=.6,head_width=0.2", ax=ax
        )
        # draw macros
        nodelist = [n for n in T if self.G.nodes[n]["_type"] == MACRO_NODE]
        nx.draw_networkx_nodes(
            T, pos, nodelist=nodelist, node_color=[colors[n] for n in nodelist], node_size=800, cmap=plt.cm.tab20, ax=ax
        )
        # draw frames
        nodelist = [n for n in self.G if self.G.nodes[n]["_type"] == FRAME_NODE]
        nx.draw_networkx_nodes(
            T,
            pos,
            nodelist=nodelist,
            node_shape="s",
            node_size=800,
            node_color=[colors[n] for n in nodelist],
            cmap=plt.cm.Pastel1,
            ax=ax,
        )
        nx.draw_networkx_labels(T, pos)

        ##############################################################################
        # Draw links
        T.remove_edges_from(list(T.edges))
        T.add_edges_from(
            (u, v)
            for u, v, k in self.G.edges(data="_type")
            if u != v and k == LINK and T.nodes[u]["depth"] == T.nodes[v]["depth"]
        )
        nx.draw_networkx_edges(
            T,
            pos,
            edge_color=[
                Individual.SHARP_COLORS_PALETTE[n % Individual.SHARP_COLORS_NUM] for n in range(T.number_of_edges())
            ],
            connectionstyle="arc3,rad=-.3",
            arrowstyle="-|>,head_length=1,head_width=0.6",
            ax=ax,
        )
        T.add_edges_from((u, v) for u, v, k in self.G.edges(data="_type") if u == v and k == LINK)
        nx.draw_networkx_edges(
            T,
            pos,
            edge_color=[
                Individual.SHARP_COLORS_PALETTE[n % Individual.SHARP_COLORS_NUM] for n in range(T.number_of_edges())
            ],
            arrowstyle="-",
            ax=ax,
        )

        T.remove_edges_from(list(T.edges))
        T.add_edges_from(
            (u, v) for u, v, k in self.G.edges(data="_type") if k == LINK and T.nodes[u]["depth"] != T.nodes[v]["depth"]
        )
        nx.draw_networkx_edges(
            T,
            pos,
            edge_color=[
                Individual.SHARP_COLORS_PALETTE[n % Individual.SHARP_COLORS_NUM] for n in range(T.number_of_edges())
            ],
            arrowstyle="-|>,head_length=1,head_width=0.6",
            ax=ax,
        )

        plt.title(f'{self}')
        plt.box(False)

        return fig

    def _draw_multipartite(self, zoom: int) -> None:
        """Draw individual using multipartite_layout"""

        G = nx.DiGraph()
        sub_graphs = list()
        for s, head in enumerate(n for _, n in self.structure_tree.edges(0)):
            nodes = [
                n for n in nx.dfs_preorder_nodes(self.structure_tree, head) if self.G.nodes[n]["_type"] == MACRO_NODE
            ]
            sub_graphs.append(nodes)
            G.add_nodes_from(nodes)
            for n1, n2 in zip(nodes, nodes[1:]):
                G.add_edge(n1, n2)
            for n in nodes:
                G.nodes[n]["subset"] = s
        pos = nx.multipartite_layout(G)
        colors = get_node_color_dict(self._genome)
        nodelist = list(G.nodes)

        # figsize
        fig = plt.figure(
            # layout='constrained',
            figsize=(7 + 5 * zoom + zoom * len(sub_graphs) * 2.0, zoom * max(len(s) for s in sub_graphs) * 1.2),
        )
        ax = fig.add_subplot()

        # draw heads
        heads = [s[0] for s in sub_graphs]
        nx.draw_networkx_nodes(G, pos, nodelist=heads[0:1], node_size=800, node_color="gold", ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=heads, node_size=600, node_color="yellow", ax=ax)
        nx.draw(
            G,
            pos,
            node_color=[colors[n] for n in nodelist],
            cmap=plt.cm.tab20,
            node_size=400,
            with_labels=True,
            edge_color="lightgray",
            style=":",
            ax=ax,
        )

        labels = dict()
        param = {k: '' for k in DEFAULT_EXTRA_PARAMETERS}
        for n in (_ for _ in pos if self.genome.nodes[n]['_type'] == MACRO_NODE):
            pos[n] = (pos[n][0], pos[n][1])
            d = Individual.dump_node(NodeReference(self.genome, n), param)
            labels[n] = '     ' + d.split('\n')[0].strip() + (' …' if '\n' in d else '')
        nx.draw_networkx_labels(G, pos, horizontalalignment='left', labels=labels)

        # draw "local" references
        G.remove_edges_from(list(G.edges))
        for s in sub_graphs:
            G.add_edges_from((u, v) for u, v, k in self.G.edges(data="_type") if k == LINK and u in s and v in s)
        nx.draw_networkx_edges(
            G,
            pos,
            edge_color=[
                Individual.SHARP_COLORS_PALETTE[n % Individual.SHARP_COLORS_NUM] for n in range(G.number_of_edges())
            ],
            width=2.0,
            alpha=0.5,
            connectionstyle="arc3,rad=-.4",
            arrowstyle="-|>,head_length=.6,head_width=0.2",
            ax=ax,
        )
        # draw "global" references
        G.remove_edges_from(list(G.edges))
        for s in sub_graphs:
            G.add_edges_from(
                (u, v)
                for u, v, k in self.G.edges(data="_type")
                if k == LINK and ((u in s and v not in s) or (u not in s and v in s))
            )
        nx.draw_networkx_edges(
            G,
            pos,
            edge_color=[
                Individual.SHARP_COLORS_PALETTE[n % Individual.SHARP_COLORS_NUM] for n in range(G.number_of_edges())
            ],
            width=2.0,
            alpha=0.5,
            connectionstyle="arc3,rad=-.1",
            arrowstyle="-|>,head_length=.7,head_width=0.3",
            ax=ax,
        )

        plt.title(f'Individual: {self}')
        plt.tight_layout()

        return fig
