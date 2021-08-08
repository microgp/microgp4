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

from typing import List, Set, Dict, Sequence, Optional, Union, Any
from collections import Counter, defaultdict
import warnings

import networkx as nx

from .utils import random_generator
from .graph import NodesCollection, EdgesCollection, GraphToolbox
from .abstract import Paranoid, Pedantic
from .common_data_structures import Frame
from .constraints import Constraints, Section, RootSection, MacroPool
from .macro import Macro
from .node import NodeID
from .parameter.abstract import Structural
from .properties import Properties
from .simple_tree import SimpleTree, _SimpleNode
from .utils import logging


class Individual(Paranoid):
    # TODO: Double Check
    # TODO: Reove all these getters?
    """A solution encoded in MicroGP, the unit of selection in the evolutive
    process. Individuals are directed multigraph (`MultiDiGraph` in NetworkX),
    that is, more than one directed edges may connect the same pair of nodes.
    An individual must be finalized to be printed and copied, once it is
    finalized (individual._finalized == True) it can't be modified.

    *What an Individual contains*:

    - `node_id` (int): is the unique node_id of the individual

    - `_constraints` (Constraints): is a reference to the constraints used to generate them

    - `_graph` contains a reference to the nx MultiDiGraph. Inside it, node are identified by their unique node_id (`NodeID` object) and their data are stored as attributes:

        - `macro`: a reference to the macro

        - `parameters`: a dictionary with the actual parameters values

        - `frame_path`: path of the node in the constraints hierarchy

    - `_operator` (callable): contains the pointer to the operator with which it was created

    - `_parents` (Set[Individual] or None): set of parent individuals from which the individual was created. None if it has no parents

    - `_age` (int): count of how many epochs the individual lived

    - `_canonic_phenotype` (str): phenotype of the individual. It can be retrieved by printing the individual. It must be finalized

    Args:
        constraints: constraints of the individual
        copy_from: Individual to clone (if specified)

    **Examples:**

    - Create a new individual with its constraints

    >>> first_individual = Individual(constraints=constraints)

    - Clone an individual (same graph_manager, same parameter values, different NodeIDs and node_id)

    >>> copied_individual = Individual(constraints=first_individual.constraints, copy_from=first_individual)

    - Print the phenotype representation of an individual

    >>> print(first_individual)
    """

    _COUNTER = 0

    def __init__(self, constraints: Constraints, graph: nx.MultiDiGraph = None) -> None:
        """Individual builder"""
        self._id = Individual._COUNTER
        Individual._COUNTER += 1

        if not graph:
            graph = nx.MultiDiGraph()
        self._nx_graph = graph
        self._finalized = False
        self._valid = None
        self._frame_tree = SimpleTree(Frame('', RootSection()))
        self._age = 0
        self._operator = None
        self._canonic_phenotype = None
        self._graph_toolbox = GraphToolbox(self._nx_graph)
        self._constraints = constraints
        self._section_counter = Counter()
        self._parents = None
        self._canonic_phenotype = None
        self._parents = set()
        self._properties = defaultdict(Properties)

    @property
    def id(self) -> int:
        return self._id

    @property
    def valid(self) -> bool:
        """Test whole set of `checkers` to validate the individual

        Returns:
            True if the individual have passed all the tests, False otherwise
        """
        assert self._finalized, "Can't assess the validity of a non-finalized individual"
        if self._valid is None:
            self._valid = check_individual_validity(self)
        return self._valid

    @property
    def properties(self) -> Dict:
        return self._properties

    @property
    def graph_manager(self) -> GraphToolbox:
        return self._graph_toolbox

    @property
    def raw_nx_graph(self) -> nx.MultiDiGraph:
        warnings.warn("Direct access to nx.MultiDiGraph is deprecated and may lead to non-reproducibility",
                      DeprecationWarning,
                      stacklevel=2)
        return self._nx_graph

    @property
    def constraints(self) -> Constraints:
        return self._constraints

    @property
    def frame_tree(self) -> SimpleTree:
        return self._frame_tree

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        """Set the age of the individual"""
        assert value >= 0, "Age value must be >= 0"
        self._age = value

    @property
    def parents(self) -> Optional[Set['Individual']]:
        return self._parents

    @parents.setter
    def parents(self, parents: Optional[Set['Individual']]):
        """Set the set of individual parents"""
        self._parents = parents

    @property
    def operator(self) -> callable:
        return self._operator

    @operator.setter
    def operator(self, value):
        """Set the operator used to create this individual"""
        self._operator = value

    @property
    def root_frame(self) -> Frame:
        return self.frame_tree.root.frame

    @property
    def sections(self) -> Sequence[Section]:
        return tuple({f.section for f in self._frame_tree.node_dict})

    @property
    def entry_point(self) -> NodeID:
        entry_points = self.nodes(section_selector='main', heads_selector=True)
        assert len(entry_points) == 1, f"Multiple entry points: {entry_points}" # TODO please double check
        return entry_points[0]

    @property
    def unlinked_nodes(self):
        # TODO: CHANGE
        raise NotImplementedError
        return self._unlinked_nodes

    # LAZY PROPERTIES ##################################################################################################

    @property
    def fitness(self):
        return self.__fitness

    @property
    def fitness_comment(self) -> str:
        return self.__fitness_comment

    @property
    def nodes(self) -> NodesCollection:
        return self.__nodes

    @property
    def edges(self) -> EdgesCollection:
        return self.__edges

    def __getattr__(self, attribute: str) -> Any:
        """Lazy attributes 'fitness', 'fitness_comment' and 'nodes' are calculated only when needed"""

        if attribute == '_Individual__fitness' or attribute == '_Individual__fitness_comment':
            fitness, comment = self.constraints.evaluator(self)
            setattr(self, '_Individual__fitness', fitness)
            setattr(self, '_Individual__fitness_comment', comment)
            return getattr(self, attribute)
        elif attribute == '_Individual__nodes':
            nodes = NodesCollection(individual=self, nx_graph=self._nx_graph)
            if self._finalized:
                setattr(self, attribute, nodes)
            return nodes
        elif attribute == '_Individual__edges':
            edges = EdgesCollection(individual=self, nx_graph=self._nx_graph)
            if self._finalized:
                setattr(self, attribute, edges)
            return edges
        else:
            # can't raise AttributeError(f"Error: '{self.__class__.__name__}' has no attribute '{attribute}'")!
            return super().__getattribute__(attribute)

    def __hash__(self):
        assert self._finalized, f"Individual {self._id} is unhashable (not yet finalized)"
        return hash(str(self))

    def __lt__(self, other):
        return self.id < other.id

    def run_paranoia_checks(self) -> bool:
        assert self.graph_manager.run_paranoia_checks()
        entry_points = self.nodes(section_selector='main', heads_selector=True)
        assert len(entry_points) == 1, f"Found multiple entry points: {entry_points}"
        assert all(n.run_paranoia_checks() for n in self.nodes)
        return True

    # __________________________________________________________________________________________________________________

    def get_unique_frame_name(self, section: Union[Section, str]) -> str:
        """Get a name never used in the individual by any other frame

        Args:
            section (Section): section to which the frame refers (Section
                object or name of the section)

        Returns:
            The unique name of the new frame
        """
        if isinstance(section, Section):
            section = section.name
        self._section_counter[section] += 1
        return "%s_%d" % (section, self._section_counter[section])

    def draw(self, *args, edge_color=None, with_labels=True, node_size=700, node_color=None, **kwargs):
        """Draws the individual. All parameters are passed to nx.draw. If `node_color == None` then each `next-chain`
        will be colored with different colors (max 10 colors).
        """
        if not edge_color:
            edge_color = [col if col else 'red' for _, col in self.edges(data='color').items()]
        if not node_color:
            node_color = ['blue'] * len(self.nodes)
        # Node: try to dray with "spring"
        return nx.draw_circular(self._nx_graph,
                                *args,
                                edge_color=edge_color,
                                with_labels=with_labels,
                                node_size=node_size,
                                node_color=node_color,
                                font_color='white',
                                **kwargs)

    def add_node(self, parent_node: Optional[NodeID], macro: Macro, frame_path: Sequence[Frame]) -> NodeID:
        """Adds a node in the individual and chains it

        Args:
            parent_node (NodeID or None):  the previous block in the dump, if
            None the node will be the root of the individual
            macro (Macro):  the macro that the node will contain
            frame_path (Sequence of Frame): the full frame path to the section containing the node.

        Returns:
            The NodeID of the node just created
        """
        assert not self._finalized, "Individual has been finalized"

        # creates and links the new node
        new_node = NodeID()
        self.graph_manager.add_node(new_node)
        if parent_node:
            old_next = self.get_next(parent_node)
            if old_next:
                self.graph_manager.remove_edge(parent_node, old_next, 'next')
                self.graph_manager.add_edge(new_node, old_next, 'next')
            self.graph_manager.add_edge(parent_node, new_node, 'next')

        # add frame path information
        self.nodes[new_node].frame_path = frame_path  # OK

        # add macro information
        self.nodes[new_node].macro = macro
        self.nodes[new_node].parameters = None
        # that's all
        return new_node

    # noinspection PyArgumentList
    def remove_node(self, node_to_delete: NodeID) -> None:
        """Delete the node from the graph_manager and connect the edges of the currently connected nodes

        Args:
            node_to_delete (NodeID): Node to delete
        """
        assert isinstance(node_to_delete, NodeID), "The node to delete must be a NodeID"
        previous = self.graph_manager.get_predecessor(node_to_delete)
        successor = self.graph_manager.get_successor(node_to_delete)
        self.graph_manager.remove_node(node_to_delete)
        if previous and successor:
            self.graph_manager.add_edge(previous, successor, 'next')
        assert self.graph_manager.run_paranoia_checks()

    def get_section_heads(self) -> Dict[Section, NodeID]:
        internal_nodes = set(t for f, t, k in self.graph_manager.edges(keys=True) if k == 'next')
        return {d[1].section: n for n, d in self.graph_manager.graph.nodes('frame_path') if n not in internal_nodes}

    def stringify_node(self, node: NodeID) -> str:
        """Generates the string with the node's current parameters

        Args:
            node: NodeID of the node to be converted into string

        Returns:
            The string that describes the macro and its parameters of the selected node
        """
        vars_ = dict()
        for parameter_name, parameter in self.nodes[node].parameters.items():
            vars_[parameter_name] = parameter.value
        if self.graph_manager.get_referring_nodes(node):
            label = self.nodes[node].section.label_format.format(node=node)
        else:
            label = ''
        return label + self.nodes[node].macro.text.format(**vars_)

    def get_next(self, node: NodeID) -> NodeID:
        """Get the successor of node (ie. the next block in the dump)

        Args:
            node (NodeID): NodeID of the node of which I need the next

        Returns:
            NodeID of the next node, None if it is the last one in the graph_manager
        """
        assert isinstance(node, NodeID), "Parameter must be of class 'Node' not %s" % (type(node),)
        assert node.run_paranoia_checks()
        # TODO: Re-enable assert len([to for _, to, key in self.edges(node, keys=True) if key == 'next']) <= 1, "Found more than one next"
        # pretty weird use of a generator, but it could be efficient...
        # return next((to for _, to, key in self.graph_manager.edges(node, keys=True) if key == 'next'), None)
        return self.nodes[node].next

    # def get_successors(self, node: NodeID) -> List[NodeID]:
    #     """Get the list of al successors of a given node (following next's)
    #
    #     Args:
    #         node (NodeID): NodeID of the node of which I need the successors
    #
    #     Returns:
    #         The list of NodeID of subsequent nodes, None if there are none
    #     """
    #     assert isinstance(node, NodeID), "Node is not a Node!"
    #
    #     successors = list()
    #     n = list(tmp_g.successors(node))
    #     while n:
    #         assert len(n) == 1, "Found more than one next"
    #         assert isinstance(n[0], NodeID), "Node is not a Node!"
    #         successors += n
    #         n = list(tmp_g.successors(n[0]))
    #     return successors

    def get_predecessors(self, node: NodeID) -> List[NodeID]:
        """Get the list of al predecessors of a given node (following next's)

        Args:
            node (NodeID): NodeID of the node of which I need the predecessors

        Returns:
            The list of NodeID of preceding nodes, None if there are none
        """
        assert isinstance(node, NodeID), "node is not a Node!"
        tmp_g = nx.MultiDiGraph(((f, t) for f, t, k in self.graph_manager.edges(keys=True) if k == 'next'))
        if node not in tmp_g.nodes:
            return []
        predecessors = list()
        n = list(tmp_g.predecessors(node))
        while n:
            assert len(n) == 1, "Found more than one next"
            assert isinstance(n[0], NodeID), "Node is not a Node!"
            predecessors += n
            n = list(tmp_g.predecessors(n[0]))
        return predecessors

    def frames(self, section: Section = None, section_name: str = None) -> Set[Frame]:
        """Get all frames of an individual belonging to a given section

        Args:
            section (Section): limit to frames belonging to the section
            section_name (str): limit to frames belonging to the section (name)

        Returns:
            A set of frames
        """
        return get_frames(self, section=section, section_name=section_name)

    def _initialize_frames(self) -> None:
        """Initialize the frame tree using the frame paths of the nodes"""
        assert all([p for p in self.nodes(data='frame_path').values()]), "One or more nodes have frame_path == None"
        # Calculate paths
        for p in self.nodes(data='frame_path').values():
            self._frame_tree.add_path(p)

        # Add properties for frames
        for frame in self.frames():
            self.properties[frame].update(frame.section.properties)
            self.properties[frame].checkers.update(frame.section.make_default_checkers())

        # Add properties for macros
        for frame in (frame for frame in self.frames() if isinstance(frame.section, MacroPool)):
            for macro in (m for m in frame.section.macro_pool if m.properties):
                logging.debug(f"Copying props: {frame} <- {macro}")
                logging.debug(macro.properties)
                self.properties[frame].update(macro.properties)

        # Add root properties
        self.properties[self.root_frame].update(self.constraints.global_properties)
        for section in (s for s in self.sections if s != self.root_frame.section and getattr(s, 'instances', None)):
            sec = section.name
            (min_instances, max_instances) = section.instances
            self.properties[self.root_frame].add_checker(
                lambda section_counter_cumulative, **v: section_counter_cumulative[sec] >= min_instances)
            self.properties[self.root_frame].add_checker(
                lambda section_counter_cumulative, **v: section_counter_cumulative[sec] <= max_instances)

    def randomize_macros(self) -> None:
        """Randomize the values of the parameters inside the macros"""

        uninitialized_nodes = [n for n in self.nodes if self.nodes[n].parameters is None]
        random_generator.shuffle(uninitialized_nodes)
        while uninitialized_nodes:
            node = uninitialized_nodes.pop(0)
            macro = self.nodes[node].macro
            parameters = dict()
            for parameter_name, parameter_type in macro.parameters_type.items():
                kwargs = dict()
                if issubclass(parameter_type, Structural):
                    kwargs['node'] = node
                    kwargs['individual'] = self
                parameters[parameter_name] = parameter_type(name=parameter_name, **kwargs)
                parameters[parameter_name].initialize()
            self.nodes[node].parameters = parameters

    def finalize(self) -> None:
        """Final setup of an individual: manage the pending movable nodes, remove non-visitable nodes from the graph_manager,
            initialize the frame tree and the properties, set the canonical representation of an individual.
            :return: """
        assert not self._finalized, "Individual already finalized"

        all_nodes = set(self._nx_graph.nodes)
        reachable_nodes = set(nx.dfs_tree(self._nx_graph, self.entry_point))
        self._nx_graph.remove_nodes_from(all_nodes - reachable_nodes)

        self._initialize_frames()
        self.properties[self.root_frame].add_base_builder(
            lambda individual, **v:
            {'macro_list_global': [(d['macro'], d['path']) for n, d in individual.nodes(data=True).items()]})
        self.set_canonical()
        assert self.run_paranoia_checks()
        self._finalized = True

    def __str__(self) -> str:
        """Get the phenotype of an individual (string)"""
        assert self._finalized, "Individual can't be converted to str because it is not finalized"
        return self._stringify()
        # return self._canonic_phenotype

    def _stringify(self):
        lines = list()
        heads = [self.entry_point]
        known_heads = set(heads)
        while heads:
            new_heads = set()
            first_node = heads.pop(0)
            for node in [first_node] + self.graph_manager.get_all_successors(first_node):
                new_heads |= {n for n in self.graph_manager.get_referred_nodes(node) if self.graph_manager.is_head(n)}
                lines.append(self.stringify_node(node))
            heads += list(new_heads - known_heads)
        return "\n".join(lines)

    def set_canonical(self) -> None:
        """Set the canonical representation of an individual (`self._canonic_phenotype`)"""
        return
        assert not self._canonic_phenotype, "Canonical phenotype already set"
        node_counter = 1
        heads = self.check_entry_point()
        known_heads = set(heads)
        # TODO: Rewrite!!!!
        while heads:
            node = heads.pop(0)
            while node:
                node._canonical = node_counter
                successors = [(label, target) for _, target, label in self.graph_manager.edges(node, keys=True)]
                node = None
                for label, target in successors:
                    if label == 'next':
                        assert node is None, "Multiple next edges"
                        node = target
                    elif self.graph_manager.is_head(target) and target not in known_heads:
                        heads.append(target)
                        known_heads.add(target)
                node_counter += 1
        macros = list()
        heads = [self._entry_point]
        known_heads = set(heads)
        while heads:
            node = heads.pop(0)
            while node:
                macros.append(self.stringify_node(node))
                # from .parameter.reference import ExternalReference
                # for parameter in self.graph_manager.raw_nodes[node]['parameters'].values():
                #     if isinstance(parameter, ExternalReference):
                #         self.graph_manager.raw_nodes[parameter.value]
                successors = [(label, target) for _, target, label in self.graph_manager.edges(node, keys=True)]
                node = None
                for label, target in successors:
                    if label == 'next':
                        assert node is None, "Multiple next edges"
                        node = target
                    elif self.graph_manager.is_head(target) and target not in known_heads:
                        heads.append(target)
                        known_heads.add(target)
        self._canonic_phenotype = "\n".join(macros)

    def link_movable_nodes(self) -> Optional[bool]:
        """Set the value of the parameters of type LocalReference and ExternalReference when the node is movable"""
        if len(self._unlinked_nodes.keys()) == 0:
            return
        # This is the phase in which I setup the nodes of the copied frame/proc and then set the edges from the nodes
        #   already inside the current individual
        # self._unlinked_nodes is a dict containing as key the NodeID of the first node of the next-chain of the nodes
        #   structure to be moved. The value is the tuple containing:
        #   - [0] The NodeID of the node that must have as next the first node of the structure to be moved
        #   - [1] The NodeID of the first node after the structure to be moved
        #   - [2] The frame path that all nodes of next-chain structure will have
        for head in self._unlinked_nodes.keys():
            parent, first_outside, frame_path = self._unlinked_nodes[head]
            # I want to move a set of nodes
            was_entry_point = False
            if parent:
                node_id_to_delete = self.get_next(parent)
            else:
                # Check if the structure to delete is the first part of the main
                if self.graph_manager[self._entry_point]['frame_path'] == frame_path:
                    node_id_to_delete = self._entry_point
                    was_entry_point = True
                else:
                    return False
            if first_outside:
                # Find the last node of the movable nodes chain
                tmp = head
                while self.get_next(tmp):
                    tmp = self.get_next(tmp)
                last = tmp

            # Save the list of node node_id of the nodes to delete
            nodes_to_delete = list()
            while node_id_to_delete and node_id_to_delete != first_outside:
                nodes_to_delete.append(node_id_to_delete)
                node_id_to_delete = self.get_next(node_id_to_delete)

            # Convert into offsets the LocalReferences that have as destination the nodes to delete
            # Save in node_id_with_params_to_change the list of NodeIDs that have parameters to be changed
            from microgp.parameter import LocalReference
            for node in self.graph_manager.nodes(frame=frame_path[1]):
                assert self.graph_manager[node]['frame_path'], f"Invalid frame_path in node{node}"
                for parameter_name, parameter in self.graph_manager[node]['parameters'].items():
                    if isinstance(parameter, LocalReference):  # and parameter.value in nodes_to_delete:
                        parameter.offset = parameter.value_to_offset()

            for node in nodes_to_delete:
                self.remove_node(node)

            if parent:
                if first_outside:
                    self.graph_manager.remove_edge_DELETED(parent, first_outside)
                self.graph_manager.add_edge_DELETED(parent, head, 'next', color='black')
            else:
                if was_entry_point:
                    self._entry_point = head
            if first_outside:
                self.graph_manager.add_edge_DELETED(last, first_outside, 'next', color='black')

            # Set the frame path for the movable nodes [[and link the local references if there are any]]
            movable_node_id = head
            while movable_node_id and movable_node_id != first_outside:
                self.nodes[movable_node_id].frame_path = frame_path  ## PROBLEMA!!!!!!!!!!!!!!!!
                movable_node_id = self.get_next(movable_node_id)

            # Change the destinations of the local references that have been changed after the deletion of the nodes
            for node in self.graph_manager.nodes(frame=frame_path[1]):
                for parameter_name, parameter in self.graph_manager[node]['parameters'].items():
                    if isinstance(parameter, LocalReference) and parameter.offset:
                        parameter.value = parameter.offset_to_value(parameter.offset)
                        if not parameter.value:
                            logging.bare("This individual will ever be not valid")
                            pass
        self._unlinked_nodes = dict()

    def arrange_movable_proc(self, nodes_to_copy_from, source_individual, first_movable_node):
        # The source proc frame will be used as unique key for self._unlinked_procs dict
        # source_proc_frame = source_individual.nodes[nodes_to_copy_from[0]]['frame_path'][1]
        # individual._imported_procs[source_proc_frame] = first_movable_node

        # Build the frame path of each node in the proc
        source_frame_paths = list()
        for source_node_id in nodes_to_copy_from:
            source_frame_paths.append(source_individual.nodes[source_node_id].frame_path)

        # Set the frame path of each node in the proc
        nodes_count = 0
        node = first_movable_node
        frame_translation = dict()
        while node:
            assert source_frame_paths and len(source_frame_paths) > 0, "No more frame paths available"
            source_frame_path = source_frame_paths.pop(0)
            frame_path = [self.frame_tree.root.frame]
            source_frame_path = source_frame_path[1:]
            for frame in source_frame_path:
                if not frame_translation.get(frame, None):
                    section = frame.section
                    new_frame = Frame(self.get_unique_frame_name(section), section)
                    frame_translation[frame] = new_frame
                frame_path = tuple(frame_path) + tuple([frame_translation[frame]])
            self.nodes[node].frame_path = frame_path
            node = self.get_next(node)
            nodes_count += 1

    def copy_section_node_structure(self, source_individual: 'Individual', source_head: NodeID = None) -> \
            Dict[NodeID, NodeID]:
        """Copy the structure of a section from the `source_individual` to `self`. Used by the builder of the Individual
        when `copy_from` is not `None`.

        Args:
            source_individual (Individual): Individual from which to copy the section structure
            source_head (NodeID): NodeID of the head of the `next-chain` (section)

        Returns:
            The correspondences between source `NodeID`s and destination `NodeID`s
        """
        assert source_individual, "source_individual can't be None"
        assert self._finalized is not True, "Destination individual can't be finalized"

        if not source_head:
            heads = source_individual.check_entry_point()
        else:
            heads = [source_head]
        # node_translation contains as keys the source_individual NodeIDs and as value the correspondent destination
        #   individual NodeIDs
        node_translation = dict()
        known_heads = set(heads)
        while heads:
            source_node_id = heads.pop(0)
            parent = None
            while source_node_id:
                source_node = source_individual.nodes[source_node_id]
                frame_path = source_node.frame_path
                # Create the node and add it in the graph_manager
                destination_node_id = self.add_node(parent, source_node.macro, frame_path)
                node_translation[source_node_id] = destination_node_id
                parent = destination_node_id
                # Pick the next node
                successors = [(label, target) for _, target, label in source_individual.edges(source_node_id, keys=True)
                             ]
                source_node_id = None
                for label, target in successors:
                    if label == 'next':
                        assert source_node_id is None, "Multiple next edges"
                        source_node_id = target
                    elif source_individual.graph_manager.is_head(target) and target not in known_heads:
                        heads.append(target)
                        known_heads.add(target)
        if source_head == source_individual._entry_point or not source_head:
            self._entry_point = node_translation[source_head]
        return node_translation

    def fill_nodes_with_parameters(self, source_individual: 'Individual', node_translation: Dict[NodeID, NodeID],
                                   destination_nodes: Set[NodeID]):
        # TODO: THIS IS THE CAUSE OF NON-REPRODUCIBILITY!
        # Copy parameters values
        nodes_tot = destination_nodes
        uninitialized_nodes = set(nodes_tot)
        while uninitialized_nodes:
            for destination_node_id in sorted(uninitialized_nodes):  # !!!!!!!!!!!!!!!!!!!!!!
                # Create parameters and copy their values
                l = len(self.graph_manager.nodes())
                parameters = self.copy_parameters(source_individual, node_translation, destination_node_id)
                assert len(self.graph_manager.nodes()) == l, f"Parameters: {parameters}, DestNodeID: {destination_node_id}, " \
                                               f"SrcNodeID: {[k for k, v in node_translation.items() if v == destination_node_id][0]}"
                self.graph_manager[destination_node_id]['parameters'] = parameters
            uninitialized_nodes = destination_nodes - nodes_tot
            nodes_tot = destination_nodes

    def copy_parameters(self, source_individual: 'Individual', node_translation: Dict[NodeID, NodeID],
                        destination_node_id: NodeID):
        """Create parameters of the given node and copy their values from the original node (=``node_translation.keys()``)

        Args:
            source_individual (Individual): individual that contains the parameter values of the nodes to copy
            node_translation (Dict[NodeID, NodeID]): correspondences between source node ids and destination node ids
            destination_node_id (NodeID): NodeID of the node to copy

        Returns:
            Dictionary that contains the parameters of the new copied node
        """
        raise NotImplementedError
        assert isinstance(source_individual, Individual), "source_individual must be an Individual object"
        parameters = dict()
        # Get the node to be copied
        source_node_id = [k for k, v in node_translation.items() if v == destination_node_id][0]
        source_node = source_individual.graph_manager[source_node_id]
        from microgp.parameter import ExternalReference
        # Iterate for each node parameter in the original individual node
        for parameter_name, parameter in source_node['parameters'].items():
            data = dict()
            data['name'] = parameter_name
            if isinstance(parameter, Structural):
                data['individual'] = self
                data['node'] = destination_node_id
                if type(parameter) == Information:
                    pass
                else:
                    # Get the correspondent new NodeID
                    reference_destination = parameter.value
                    assert reference_destination in node_translation.keys(), "Something wrong"
                    # Get the correspondent NodeID belonging to the destination individual
                    new_value = node_translation[reference_destination]
                    if isinstance(parameter, ExternalReference):
                        data['do_not_init'] = True
            else:
                new_value = parameter.value
            new_parameter = type(parameter)(**data)
            if not isinstance(parameter, Information):
                new_parameter.value = new_value
                assert new_parameter.value == new_value, "Something went wrong"
            parameters[parameter_name] = new_parameter
        return parameters

    def create_movable_nodes(self,
                             source_individual: 'Individual',
                             nodes_to_copy_from: List[NodeID],
                             is_new_proc: bool = False) -> NodeID:
        first_node_id = None
        parent = None
        for source_node_id in nodes_to_copy_from:
            source_node = source_individual.graph_manager[source_node_id]
            new_node_id = self.add_node(parent, source_node['macro'], None)
            self.copy_parameters_movable(source_individual, new_node_id, source_node_id)
            if not first_node_id:
                first_node_id = new_node_id
                if is_new_proc is True:
                    assert first_node_id not in self._imported_procs.values(
                    ), "Node already in self._imported_procs.values()"
                    source_proc_frame = source_individual.nodes[source_node_id].frame_path[1]
                    self._imported_procs[source_proc_frame] = first_node_id
            parent = new_node_id
        return first_node_id

    def copy_parameters_movable(self, source_individual: 'Individual', new_node_id: NodeID, source_node_id: NodeID):
        from .parameter import ExternalReference, LocalReference
        source_node = source_individual.graph_manager[source_node_id]
        parameters = dict()
        for parameter_name, parameter in source_node['parameters'].items():
            data = dict()
            data['name'] = parameter_name
            if issubclass(type(parameter), Structural):
                data['individual'] = self
                data['node'] = new_node_id
                from .parameter import Special
                if issubclass(type(parameter), Special):
                    # NOTE: do not use the same Information, otherwise the set_canonical() will not work properly
                    parameter = type(parameter)(**data)
                elif isinstance(parameter, ExternalReference):
                    # If the parameter is an ExternalReference, then the new proc must be copied
                    first_source_proc_node = parameter.value

                    source_proc_frame = source_individual.nodes[first_source_proc_node].frame_path[1]
                    if source_proc_frame in self._imported_procs.keys():
                        # Proc already copied, link the current node to the first node of the proc
                        first_movable_node = self._imported_procs[source_proc_frame]
                    else:
                        # Create the structure of the new procedure
                        # nodes_to_copy_from = get_nodes_visit_order(source_individual, first_source_proc_node)
                        chosen_frame = source_individual.nodes[first_source_proc_node].frame_path[1]
                        nodes_to_copy_from = get_nodes_in_frame(source_individual, chosen_frame)

                        # Create movable nodes of the selected proc
                        first_movable_node = self.create_movable_nodes(source_individual,
                                                                       nodes_to_copy_from,
                                                                       is_new_proc=True)
                        assert first_movable_node, "Ops, something went wrong in creation of movable nodes"

                        self.arrange_movable_proc(nodes_to_copy_from, source_individual, first_movable_node)

                    # Set the final_destination of the external reference of the selected node__________________________
                    parameter = type(parameter)(**data)
                    parameter.value = first_movable_node
                elif isinstance(parameter, LocalReference):
                    # Save relative references that will be copied in a second phase. This because if I copy
                    offset = parameter.value_to_offset()
                    if not offset:
                        exit("This should not happen")
                    # Save the offset. The availability of a a valid target for the destination_node will be checked in
                    #   second phase, when the parameter will be created and the nodes structure will be fully created
                    data['offset'] = offset
                    parameter = type(parameter)(**data)
                else:
                    exit("This should not happen")
            else:
                # The non-Structural parameters must be copied in value
                new_value = source_node['parameters'][parameter_name].value
                # data["copy_from"] = new_value
                parameter = type(parameter)(**data)
                parameter.value = new_value
            parameters[parameter_name] = parameter
        self.graph_manager[new_node_id]['parameters'] = parameters

    def __eq__(self, other: 'Individual'):
        assert self._finalized and other._finalized, "One or more individuals are not finalized"
        return self._canonic_phenotype == other._canonic_phenotype


def get_nodes_in_frame(individual: Individual, frame: Frame, frame_path_limit: int = None) -> List[NodeID]:
    """Gets all nodes of an individual inside a given frame

    Args:
        individual (Individual): the individual
        frame (Frame): the frame
        frame_path_limit (int): how deep is the path for matching (positive: from root, negative: from leaf)

    Returns:
        A list of of Nodes
    """
    node_list = list()
    for node, data in individual.graph_manager.nodes(data='frame_path').items():
        #TODO: assert data, f"Invalid frame_path for node {node}: {data}"
        if frame_path_limit:
            if frame_path_limit > 0:
                data = data[0:frame_path_limit]
            else:
                data = data[len(data) + frame_path_limit:]
        #TODO: assert data, "Missing frame path"
        if data and frame in data:
            node_list.append(node)
    return node_list


def get_nodes_in_section(individual: Individual,
                         section: Section,
                         frame_path_limit: int = None,
                         head: bool = False) -> List[NodeID]:
    """Gets all nodes of an individual inside a given frame

    If `frame_path_limit` is set to N with N > 0, only the first N frames are
    considered for the match. If With N < 0, only the last N frames are
    considered for the match.

    Args:
        individual (Individual): the individual
        section (Section): the section
        frame_path_limit (int): limit the frame path
        head (bool): returns only the head of the section

    Returns:
        The list of nodes in the selected section
    """

    node_list = list()
    for node, data in individual.graph_manager.nodes(data='frame_path').items():
        if frame_path_limit:
            if frame_path_limit > 0:
                data = data[0:frame_path_limit]
            else:
                data = data[len(frame_path_limit) + frame_path_limit:]
        if section in (f.section for f in data):
            node_list.append(node)
    assert all(individual.graph_manager[n]['frame_path'] for n in node_list), "Illegal frame_path in individual's node"
    return node_list


def get_frames(individual: Individual, section: Section = None, section_name: str = None) -> Set[Frame]:
    """Gets all frames of an individuals belonging to a given section

    Args:
        individual (Individual): the individual
        section (Section): limit to frames belonging to the section
        section_name (str): limit to frames belonging to the section (name)

    Returns:
        A set of frames
    """

    assert not section or not section_name, "section and section_name cannot be both specified"

    if isinstance(section, str):
        section = individual.sections[section]

    frames = set()
    for path in individual.nodes(data='frame_path').values():
        if path:
            for frame in path:
                if section_name and frame.section.name == section_name:
                    frames.add(frame)
                elif section and frame.section == section:
                    frames.add(frame)
                elif not section and not section_name:
                    frames.add(frame)
    assert frames, "Internal panik"
    return frames


def get_macro_pool_nodes_count(individual: Individual, frames: Set[Frame] = None) -> Dict[Frame, int]:
    """Get a dict containing {Frame: number_of_macros}. Selects only MacroPools

    Args:
        frames (Set[Frame]): set of frames of which I want the number of nodes
        individual (Frame): Individual from which count the nodes

    Returns:
        Dictionary containing the amount of nodes (value) for each Frame (key)

    :meta private:
    """
    frame_count = dict()
    for node_id, value in individual.graph_manager.nodes(data=True).items():
        # Get the last frame (it is always a MacroPool)
        macro_pool = value['frame_path'][len(value['frame_path']) - 1]
        # Save the number of nodes in that frame
        if not frames or macro_pool in frames:
            frame_count[macro_pool] = len(get_nodes_in_frame(individual, frame=macro_pool))
    return frame_count


def get_nodes_in_frame(individual: 'Individual', frame: Frame, frame_path_limit: int = None) -> List[NodeID]:
    # TODO: Double Check
    """Gets all nodes of an individual inside a given frame

    Args:
        individual (Individual): the individual
        frame (Frame): the frame
        frame_path_limit (int): how deep is the path for matching (positive: from root, negative: from leaf)

    Returns:
        A list of of Nodes
    """
    warnings.warn("Functions is going to be removed", DeprecationWarning, stacklevel=2)
    return individual.nodes(frame_selector=frame)


def get_nodes_in_section(individual: 'Individual',
                         section: Section,
                         frame_path_limit: int = None,
                         head: bool = False) -> List[NodeID]:
    # TODO: Double Check
    """Gets all nodes of an individual inside a given frame

    If `frame_path_limit` is set to N with N > 0, only the first N frames are
    considered for the match. If With N < 0, only the last N frames are
    considered for the match.

    Args:
        individual (Individual): the individual
        section (Section): the section
        frame_path_limit (int): limit the frame path
        head (bool): returns only the head of the section

    Returns:
        The list of nodes in the selected section
    """

    node_list = list()
    for node, data in individual.nodes(data='frame_path').items():
        if frame_path_limit:
            if frame_path_limit > 0:
                data = data[0:frame_path_limit]
            else:
                data = data[len(frame_path_limit) + frame_path_limit:]
        if section in (f.section for f in data):
            node_list.append(node)
    assert all(individual.nodes[n].frame_path for n in node_list), "Illegal frame_path in individual's node"
    return node_list


def get_macro_pool_nodes_count(individual: 'Individual', frames: Set[Frame] = None) -> Dict[Frame, int]:
    # TODO: Double Check
    """Get a dict containing {Frame: number_of_macros}. Selects only MacroPools

    Args:
        frames (Set[Frame]): set of frames of which I want the number of nodes
        individual (Frame): individual from which count the nodes

    Returns:
        Dictionary containing the amount of nodes (value) for each Frame (key)

    :meta private:
    """
    frame_count = dict()
    for node_id, value in individual.nodes(data=True).items():
        # Get the last frame (it is always a MacroPool)
        macro_pool = value['frame_path'][len(value['frame_path']) - 1]
        # Save the number of nodes in that frame
        if not frames or macro_pool in frames:
            frame_count[macro_pool] = len(individual.nodes(frame_selector=macro_pool))
    return frame_count


def check_individual_validity(individual: 'Individual') -> bool:
    # TODO: Double Check
    """Check an individual against its constraints.

    Check the validity of all parameters (e.g., range), then the default
    `Properties` (e.g., number of macros in sections), and finally all the
    custom `Properties` added by the user.

    The result is cached, as individuals must be `finalized` to be checked

    Args:
        individual (Individual): the individual to be checked

    Returns:
        The validity as a boolean value
    """
    # examine all frames in the individual
    values = dict()
    for node, data in individual.nodes(data=True).items():
        if not all(p.is_valid(p.value) for p in data['parameters'].values()):
            return False
    # logging.debug("*** Checking individual %r" % (individual,))

    for frame in individual.frame_tree.post_order_visit():
        cumulative_values = dict()
        for f in individual.frame_tree.get_sub_frames(frame):
            for k, v in individual.properties[f].cumulative_values.items():
                if k not in cumulative_values:
                    cumulative_values[k] = v
                else:
                    # logging.debug("(merge sibling) %s: %s + %s:%s -> %s" % (k, cumulative_values[k], f.name, v, cumulative_values[k] + v))
                    # Note for a C geek: "cumulative_values[k] += v" did not work -- remember why?
                    cumulative_values[k] = cumulative_values[k] + v
        individual.properties[frame].update_values(individual=individual,
                                                   frame=frame,
                                                   cumulative_values=cumulative_values)

    for frame in individual.frame_tree.post_order_visit():
        # logging.debug("Checking %s" % (frame,))
        # logging.debug("%s" % (individual.properties[frame],))
        if not individual.properties[frame].run_checks():
            return False

    return True


def _update_values(individual: 'Individual', node: _SimpleNode) -> None:
    # TODO: Double Check
    assert False, "Don't use this function!"
    cumulative_values = dict()
    for n in node.children:
        _update_values(individual, n)
        for k, v in individual.properties[n.frame].cumulative_values.items():
            if k not in cumulative_values:
                cumulative_values[k] = v
            else:
                # logging.debug("(merge sibling) %s: %s + %s -> %s" % (k, cumulative_values[k], v, cumulative_values[k] + v))
                cumulative_values[k] += v
        # logging.debug("After %s: cumulative = %s" % (n.frame.name, cumulative_values))

    # logging.debug("REC Checking %s" % (node.frame,))
    # logging.debug("In %s: cumulative_values = %s" % (node.frame.name, cumulative_values))
    individual.properties[node.frame].update_values(individual=individual,
                                                    frame=node.frame,
                                                    cumulative_values=cumulative_values)


def clone_individual(individual: 'Individual') -> 'Individual':
    # TODO: Double Check
    """Creates a new individual that clones the structure of the given one"""
    mapping = {o: n for o, n in zip(individual.nodes, [NodeID() for _ in range(len(individual.nodes))])}
    new_graph = nx.MultiDiGraph()
    new_graph.add_nodes_from(mapping.values())
    new_graph.add_edges_from(
        (mapping[f], mapping[t], k, d) for f, t, k, d in individual._nx_graph.edges(keys=True, data=True))
    clone = Individual(individual.constraints, graph=new_graph)

    for n in individual.nodes:
        cn = mapping[n]  # n: node in source, cn: cloned node
        ###print(f"Clone map: {n} -> {cn}")
        clone._nx_graph.nodes[cn]['macro'] = individual._nx_graph.nodes[n]['macro']
        clone._nx_graph.nodes[cn]['frame_path'] = individual._nx_graph.nodes[n]['frame_path']

        parameters = dict()
        for parameter_name, parameter_type in individual._nx_graph.nodes[n]['macro'].parameters_type.items():
            if issubclass(parameter_type, Structural):
                # Structural parameters do not need to be initialized as values are stored as edges
                parameters[parameter_name] = parameter_type(name=parameter_name, node=cn, individual=clone)
            else:
                # Non-structural parameters need to be initialized, but do not need node individual/node references
                parameters[parameter_name] = parameter_type(name=parameter_name)
                parameters[parameter_name].initialize(individual._nx_graph.nodes[n]['parameters'][parameter_name].value)
        clone._nx_graph.nodes[cn]['parameters'] = parameters
    return clone
