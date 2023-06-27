#!/usr/bin/env python3
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
# SPDX-License-Identifier: Apache-2.0

from microgp4.classes.parameter import ParameterABC
from microgp4.global_symbols import FRAMEWORK, NODE_ZERO
from microgp4.tools.graph import _check_genome
from microgp4.tools.graph import *
import pytest
import networkx as nx
from microgp4.classes.node_reference import NodeReference
class Frame1:
    pass

class Frame2:
    pass

class Frame3:
    pass

def test_check_genome():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind='framework')
    assert _check_genome(G) == True

def test_get_grammar_tree():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind='framework')
    tree = get_grammar_tree(G)
    assert isinstance(tree, nx.DiGraph)
    assert list(tree.edges) == [(1, 2)]

def test_get_successors():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind='framework')
    G.add_edge(1, 3, kind='framework')
    ref = NodeReference(G, 1)
    assert get_successors(ref) == [2, 3]

def test_get_predecessor():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind='framework')
    G.add_edge(1, 3, kind='framework')
    ref = NodeReference(G, 2)
    assert get_predecessor(ref) == 1

def test_get_siblings():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind='framework')
    G.add_edge(1, 3, kind='framework')
    ref = NodeReference(G, 2)
    assert get_siblings(ref) == [2, 3]

def test_set_successors_order():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind='framework')
    G.add_edge(1, 3, kind='framework')
    ref = NodeReference(G, 1)
    set_successors_order(ref, [3, 2])
    assert list(G.successors(1)) == [3, 2]


def test_get_successors():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind='framework')
    G.add_edge(1, 3, kind='framework')

    node_ref = NodeReference(G, 1)
    successors = get_successors(node_ref)

    assert sorted(successors) == [2, 3]


def test_get_predecessor():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind='framework')
    G.add_edge(1, 3, kind='framework')

    node_ref = NodeReference(G, 2)
    predecessor = get_predecessor(node_ref)

    assert predecessor == 1


def test_set_successors_order():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind='framework')
    G.add_edge(1, 3, kind='framework')

    node_ref = NodeReference(G, 1)
    new_order = [3, 2]
    set_successors_order(node_ref, new_order)

    assert get_successors(node_ref) == new_order

def test_is_equal():
    G1 = nx.MultiDiGraph()
    G1.add_edge(1, 2, kind='framework')
    G1.add_edge(1, 3, kind='framework')

    G2 = nx.MultiDiGraph()
    G2.add_edge(1, 2, kind='framework')
    G2.add_edge(1, 3, kind='framework')

    node_ref1 = NodeReference(G1, 1)
    node_ref2 = NodeReference(G2, 1)

    assert is_equal(node_ref1, node_ref2)

def test_get_node_color_dict():
    G = nx.MultiDiGraph()
    G.add_node(1, _frame=Frame1())
    G.add_node(2, _frame=Frame2())
    G.add_node(3, _frame=Frame3())
    color_dict = get_node_color_dict(G)
    assert len(set(color_dict.values())) == len(G.nodes)
    assert color_dict == {1: 0, 2: 1, 3: 2}

def test_get_macros():
    G = nx.MultiDiGraph()
    G.add_node(NODE_ZERO, _frame='frame')
    G.add_node(1, _macro='macro1')
    G.add_node(2, _macro='macro2')
    G.add_node(3, _macro='macro3')
    G.add_edge(NODE_ZERO, 1, kind=FRAMEWORK)
    G.add_edge(NODE_ZERO, 2, kind=FRAMEWORK)
    G.add_edge(NODE_ZERO, 3, kind=FRAMEWORK)

    macros = get_macros(G)
    assert macros == [1, 2, 3]

def test_get_frames():
    G = nx.MultiDiGraph()
    G.add_node(NODE_ZERO, _frame='frame')
    G.add_node(1, _frame='frame1')
    G.add_node(2, _frame='frame2')
    G.add_node(3, _frame='frame3')
    G.add_edge(NODE_ZERO, 1, kind=FRAMEWORK)
    G.add_edge(NODE_ZERO, 2, kind=FRAMEWORK)
    G.add_edge(NODE_ZERO, 3, kind=FRAMEWORK)

    frames = get_frames(G)
    assert frames == [NODE_ZERO, 1, 2, 3]

class Parameter(ParameterABC):
    def mutate(self):
        pass

def test_get_parameters():
    G = nx.MultiDiGraph()
    G.add_node(NODE_ZERO, _frame='frame', _macro={'param1': Parameter()})
    G.add_node(1, _frame='frame1', _macro={'param2': Parameter()})
    G.add_node(2, _frame='frame2', _macro={'param3': Parameter()})
    G.add_node(3, _frame='frame3', _macro={'param4': Parameter()})
    G.add_edge(NODE_ZERO, 1, kind=FRAMEWORK)
    G.add_edge(NODE_ZERO, 2, kind=FRAMEWORK)
    G.add_edge(NODE_ZERO, 3, kind=FRAMEWORK)

    parameters = get_parameters(G)
    assert len(parameters) == 4
    assert all(isinstance(param, Parameter) for param in parameters)
def test_get_first_macro():
    G = nx.MultiDiGraph()
    T = nx.DiGraph()
    G.add_node(1, _macro='macro1')
    G.add_node(2, _frame='frame1')
    G.add_node(3, _frame='frame1')
    T.add_edge(1, 2)
    T.add_edge(2, 3)
    first_macro = _get_first_macro(1, G, T)
    assert first_macro == 1
