# -*- coding: utf-8 -*-
#############################################################################
#          __________                                                       #
#   __  __/ ____/ __ \__ __   This file is part of MicroGP4 v1.0 "Kiwi"     #
#  / / / / / __/ /_/ / // /   (!) by Giovanni Squillero and Alberto Tonda   #
# / /_/ / /_/ / ____/ // /_   https://github.com/squillero/microgp4         #
# \__  /\____/_/   /__  __/                                                 #
#   /_/ --MicroGP4-- /_/      "You don't need a big goal, be μ-ambitious!!" #
#                                                                           #
#############################################################################

# Copyright 2020 Giovanni Squillero and Alberto Tonda
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

from typing import List, Dict, Optional, Union, Any, Collection, Tuple, Set
from collections import abc, namedtuple

import networkx as nx

from .utils import logging
from .abstract import Paranoid, Pedantic
from .common_data_structures import Frame
from .constraints import Section
from .node import NodeID


# TODO: Check. (fall 2020)
class NodeWrapper(Paranoid):
    # TODO: Double Check
    """Wrapper class for working with nodes inside Individual"""

    def __init__(self, node_id: NodeID, graph: nx.MultiDiGraph) -> None:
        # Can't use self. as it would recurse __setattr__
        self.__dict__['_node_id'] = node_id
        self.__dict__['_graph'] = graph
        self.__dict__['_data'] = graph.nodes[node_id]

    @property  # dynamically-created, read-only attribute
    def _id(self, other):
        # TODO: For debug only -- To be removed
        raise NotImplementedError

    @property  # dynamically-created, read-only attribute
    def id(self, other):
        # TODO: For debug only -- To be removed
        raise NotImplementedError

    @property  # dynamically-created, read-only attribute
    def node_id(self):
        return self.__dict__['_node_id']

    @property  # dynamically-created, read-only attribute
    def section(self):
        return self.frame_path[-1].section

    @property  # dynamically-created, read-only attribute
    def path(self) -> Optional[str]:
        if self._data['frame_path'][0] is not None:
            assert self._data['frame_path'][
                0].name == '', f"Internal error: <ROOT> frame is not '' but '{self._data['frame_path'][0]}'"
            return '/'.join(p.name for p in self._data['frame_path'])
        else:
            return None  # floating node!

    def __str__(self):
        return f"Node({self.node_id})"

    def __getattr__(self, attribute: str) -> Any:
        """Lazy attributes: calculated only if requested."""
        if attribute == 'successors':
            self.__dict__[attribute] = GraphToolbox(self._graph).get_all_successors(self.node_id)
        elif attribute == 'predecessors':
            self.__dict__[attribute] = GraphToolbox(self._graph).get_all_predecessors(self.node_id)
        elif attribute in self.__dict__['_data']:
            self.__dict__[attribute] = self._data[attribute]
        else:
            logging.debug(f"Creating empty attribute {attribute} in node {self.node_id}")
            self.__dict__[attribute] = None
        return self.__dict__[attribute]

    def __setattr__(self, attribute: str, value: Any) -> None:
        """Store attribute is nthe dictionary. Quite useful if the node is inside a finalized Individual."""
        self._data[attribute] = value

    def __getitem__(self, parameter_name: str) -> Any:
        """Access attributes as n['name'] and parameters as n['$name']."""
        assert isinstance(parameter_name, str), f"Parameter name should be string (found: {type(parameter_name)})"
        if parameter_name[0] == '$':
            # parameter inside the macro
            assert 'parameters' in self._data, "Missing 'parameters'. Uninitialized macro?"
            if self._data['parameters'] is not None and parameter_name[1:] in self._data['parameters']:
                return self._data['parameters'][parameter_name[1:]].value
            else:
                return None
        else:
            return getattr(self, parameter_name)

    def __setitem__(self, parameter_name: str, value: Any) -> None:
        """Set attribute n['name']=v or a parameter n['$name']=v."""
        assert isinstance(parameter_name, str), f"Parameter should be a string (found: {type(parameter_name)})"
        if parameter_name[0] == '$':
            assert 'parameters' in self._data, "Missing 'parameters' in NodeWrapper. Uninitialized macro?"
            self._data['parameters'][parameter_name[1:]].value = value
        else:
            self._data[parameter_name] = value

    def run_paranoia_checks(self) -> bool:
        # TODO: Implements checks
        return True


# TODO: Check. (fall 2020)
class NodesCollection(abc.Mapping, abc.Set, abc.Callable):
    # TODO: Double Check
    """Collection of nodes of an individual; quite but not completely different from a NetworkX node view.

    When used as a dictionary it allows read-only access to NodeViews. E.g.,

        >>> for n in ind.node_list;
        >>>     print(ind.node_list[n]['foo'])
        >>>     ind.node_list[n]['bar'] = 41    # nodes can be modified as a dictionary
        >>>     ind.node_list[n].baz += 1       # or as properties

    When `NodesCollection` is used as a function it allows to select nodes using various filters, e.g.,

        >>> ind.node_list(section_selector='main', heads_selector=False, data=True)

    Args:
        data: When data is ``None``, the return value is a list of :meth:`microgp.node.NodeID`. When data is ``True``,
            the return value is dictionary of dictionaries ``{node_id: {<all node properties>}}``. When data is the key
            of a node property, the return value is a dictionary ``{node_id: <the specified field>}``

        default: When property selected by data does not exists, the node is included in the result withe the specified
            value. If ``default`` is ``None``, the node is not included in the result.

        select_section (str or Section): Only include nodes belonging to the specified section.

        select_frame  (str or Frame): Only include nodes belonging to the specified frame.

        select_heads (None or bool): if specified, return only nodes that are heads of sections (``True``); or nodes that
            are internal to sections (``False``)

    Returns:
        Either a list or a dictionary, see `data`
    """

    # See <https://stackoverflow.com/questions/472000/usage-of-slots>
    __slots__ = ('_individual', '_nx_graph', '_nodes')

    def __getstate__(self):
        return {'_individual': self._individual, '_graph': self._nx_graph, '_nodes': self._nodes}

    def __setstate__(self, state):
        self._individual = state['_individual']
        self._nx_graph = state['_graph']
        self._nodes = state['_nodes']

    def __init__(self, individual: "Individual", nx_graph: nx.MultiDiGraph) -> None:
        self._individual = individual
        self._nx_graph = nx_graph
        self._nodes = {n: NodeWrapper(n, nx_graph) for n in sorted(self._nx_graph.nodes)}
        for n1, n2 in self._nx_graph.edges(keys='next'):
            self._nodes[n1]['next'] = n2
            self._nodes[n2]['prev'] = n1

    # Mapping methods
    def __len__(self):
        return len(self._nodes)

    def __iter__(self):
        return iter(self._nodes)

    def __getitem__(self, key):
        if not isinstance(key, NodeID):
            key = NodeID(key)
        assert key in self._nodes, f"Node {key} not in the individual ({list(self._nodes)})"
        return NodeWrapper(node_id=key, graph=self._nx_graph)

    # Set methods
    def __contains__(self, n):
        return n in self._nodes

    # NodeWrapper
    def __call__(self,
                 nodes: Collection[Union[NodeID, int]] = None,
                 data: Union[str, bool] = False,
                 section_selector: Union[Section, str] = None,
                 frame_selector: Union[Frame, str] = None,
                 heads_selector: Optional[bool] = None) -> Union[List[NodeID], Dict[NodeID, Any]]:
        assert not (section_selector and frame_selector), "Can't filter both by frame and section"

        # let's filter node list
        selected_node = list(self)

        if section_selector:
            if isinstance(section_selector, str):
                section_selector = self._individual.constraints.sections[section_selector]
            selected_node = [
                n for n in selected_node if section_selector in (f.section for f in self._nodes[n]['frame_path'])
            ]

        if frame_selector:
            if isinstance(frame_selector, Frame):
                selected_node = [n for n in selected_node if frame_selector in self._nodes[n]['frame_path']]
            else:
                selected_node = [
                    n for n in selected_node if frame_selector in (f.name for f in self._nodes[n]['frame_path'])
                ]

        if heads_selector is not None:
            internal_nodes = set(t for f, t, k in self._nx_graph.edges(selected_node, keys=True) if k == 'next')
            if heads_selector:
                selected_node = [n for n in selected_node if n not in internal_nodes]
            else:
                selected_node = [n for n in selected_node if n in internal_nodes]

        if nodes:
            if not isinstance(nodes, abc.Iterable):
                nodes = (nodes,)
            selected_node = [n for n in selected_node if n in {NodeID(n) for n in nodes}]

        # data is False: return a list of NodeID
        if data is False:
            return selected_node

        # data is either True or str: return a dict NodeID -> Any
        node_dict = dict()
        for n in selected_node:
            if data is True:
                node_dict[n] = self._nodes[n]
            else:
                node_dict[n] = self._nodes[n][data]
        return node_dict


# TODO: Check. (fall 2020)
EdgeWrapper = namedtuple('EdgeWrapper', ['src', 'dst', 'key', 'data'])
# TODO: Double Check


# TODO: Check. (fall 2020)
class EdgesCollection(abc.Mapping):
    # TODO: Double Check
    """Collection of nodes of an individual; quite but not completely different from a NetworkX node view.
    """

    __slots__ = ('_individual', '_nx_graph', '_edges')

    def __getstate__(self):
        return {'_individual': self._individual, '_graph': self._nx_graph, '_edges': self._nodes}

    def __setstate__(self, state):
        self._individual = state['_individual']
        self._nx_graph = state['_graph']
        self._edges = state['_edges']

    def __init__(self, individual: "Individual", nx_graph: nx.MultiDiGraph) -> None:
        self._individual = individual
        self._nx_graph = nx_graph
        self._edges = {(src, dst, key): EdgeWrapper(src, dst, key, data)
                       for src, dst, key, data in sorted(self._nx_graph.edges(data=True, keys=True))}

    # Mapping methods
    def __len__(self) -> int:
        return len(self._edges.values())

    def __iter__(self):
        return iter(self._edges.values())

    def __getitem__(self, key) -> EdgeWrapper:
        return self._edges[key]

    def __call__(self,
                 src: NodeID = None,
                 dst: NodeID = None,
                 key: str = None,
                 data: Union[str, bool] = False) -> List[Tuple[NodeID, NodeID, str, Any]]:
        edges = list(self)

        if src:
            edges = [e for e in edges if e.src == src]
        if dst:
            edges = [e for e in edges if e.dst == dst]
        if key:
            edges = [e for e in edges if e.key == key]

        if not data:
            return list(edges)
        elif data is True:
            return {(s, d, k): a for s, d, k, a in edges}
        else:
            result = dict()
            for s, d, k, a in edges:
                if data in a:
                    result[s, d, k] = a[data]
                else:
                    result[s, d, k] = None
            return result


# TODO: Check. (fall 2020)
class GraphToolbox(Paranoid):
    # TODO: Double Check
    """A safe wrapper around common operation on a NetworkX MultiDiGraph"""

    __slots__ = ('_nx_graph',)

    def __getstate__(self):
        return {'_graph': self._nx_graph}

    def __setstate__(self, state):
        self._nx_graph = state['_graph']

    def __init__(self, graph: nx.MultiDiGraph) -> None:
        self._nx_graph = graph

    def add_node(self, node: NodeID, **attributes) -> None:
        assert isinstance(node, NodeID), f"Parameter is not NodeID but {type(node)}"
        self._nx_graph.add_node(node, **attributes)

    def remove_node(self, node: NodeID) -> None:
        self._nx_graph.remove_node(node)

    def add_edge(self, src: NodeID, dst: NodeID, key: str, **attributes):
        assert src in self._nx_graph, f"Can't find source node '{src}' ({type(src)})"
        assert dst in self._nx_graph, f"Can't find destination node '{dst}' ({type(dst)})"
        if 'color' not in attributes:
            if key == 'next':
                attributes['color'] = 'black'
            else:
                attributes['color'] = 'green'
        self._nx_graph.add_edge(u_for_edge=src, v_for_edge=dst, key=key, **attributes)
        assert self.run_paranoia_checks()

    def remove_edge(self, src: NodeID, dst: NodeID, key: str):
        # TODO: Check key validity
        self._nx_graph.remove_edge(u=src, v=dst, key=key)

    def in_degree(self, node: NodeID) -> int:
        return self._nx_graph.in_degree(node)

    def out_degree(self, node: NodeID) -> int:
        return self._nx_graph.out_degree(node)

    def degree(self, node: NodeID) -> int:
        return self._nx_graph.degree(node)

    def get_referring_nodes(self, node: NodeID) -> Set[NodeID]:
        """List nodes that refer node in some parameter"""
        return {s for s, d, k in self._nx_graph.edges(keys=True) if d == node and k[0] == '$'}

    def get_referred_nodes(self, node: NodeID) -> Set[NodeID]:
        """List nodes that are referred by node in some parameter"""
        return {d for s, d, k in self._nx_graph.edges(node, keys=True) if k[0] == '$'}

    def is_referenced(self, node: NodeID, parameter: str) -> bool:
        """Check if node is the target of '$parameter'"""
        assert parameter[0] == '$', f"Parameter name should start with '$' (found: '{parameter}')"
        in_parameters = {k for s, d, k in self._nx_graph.edges(keys=True) if d == node}
        return parameter in in_parameters

    def is_head(self, node: NodeID) -> bool:
        """Check if node is not the target of a 'next' edge"""
        return not bool([s for s, d, k in self._nx_graph.edges(keys=True) if d == node and k == 'next'])

    def is_tail(self, node: NodeID) -> bool:
        """Check if node contains a 'next'"""
        return not bool([d for s, d, k in self._nx_graph.edges(node, keys=True) if k == 'next'])

    def is_internal(self, node: NodeID) -> bool:
        raise NotImplementedError

    def get_parameter(self, node: Union[NodeWrapper, NodeID], parameter_name: str) -> Optional[NodeID]:
        assert isinstance(node, NodeID) or isinstance(
            node, NodeWrapper), f"node is neither NodeID nor NodeWrapper ({type(node)})"
        assert parameter_name[0] == '$', f"Parameter name should start with '$' (found: '{parameter_name}')"
        if isinstance(node, NodeWrapper):
            node = node.node_id
        return next((d for s, d, k in self._nx_graph.edges(node, keys=True) if k == parameter_name), None)

    def get_predecessor(self, node: NodeID) -> Optional[NodeID]:
        return next((f for f, t, k in self._nx_graph.edges(node, keys=True) if k == 'next' and f != node), None)

    def get_all_predecessors(self, node: NodeID) -> List[NodeID]:
        predecessors = GraphToolbox._walk_filler(
            node, {n2: n1 for n1, n2, k in self._nx_graph.edges(keys=True) if k == 'next'})
        return predecessors[1:]

    def get_successor(self, node: NodeID) -> Optional[NodeID]:
        return next((t for f, t, k in self._nx_graph.edges(node, keys=True) if k == 'next'), None)

    def get_all_successors(self, node: NodeID) -> List[NodeID]:
        successors = GraphToolbox._walk_filler(node,
                                               {n1: n2 for n1, n2, k in self._nx_graph.edges(keys=True) if k == 'next'})
        return successors[1:]

    def run_paranoia_checks(self) -> bool:
        assert all(isinstance(n, NodeID) for n in self._nx_graph.nodes), "Fond non-NodeID in Individual structure"
        temporary_graph = nx.DiGraph((n1, n2) for n1, n2, k in self._nx_graph.edges(keys=True) if k == 'next')
        cycles = list(nx.simple_cycles(temporary_graph))
        assert not cycles, f"Individual structure is not a forest of DAGs: Cycles = {cycles}"
        return True

    @staticmethod
    def _walk_filler(start: NodeID, edges: Dict[NodeID, NodeID]):
        result = [start]
        while result[-1] in edges:
            result.append(edges[result[-1]])
        return result
