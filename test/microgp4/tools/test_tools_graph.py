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


# from microgp4.classes.node_reference import *
# from microgp4.global_symbols import *
# from microgp4.tools.graph import *
# from microgp4.tools.graph import _check_genome
# import pytest
# import networkx as nx
# from collections import abc
# import random

# def create_test_graph():
#     G = nx.MultiDiGraph()
#     nodes = [n for n in range(1, 10)]
#     random.shuffle(nodes)
#     G.add_node(NODE_ZERO, _frame='frame1')
#     for n in nodes:
#         G.add_node(str(n), _frame='frame1', _macro={'param1': 'value1', 'param2': 'value2'})
#         G.add_edge(NODE_ZERO, str(n), kind=FRAMEWORK)
#     return G


# def test_check_genome():
#     G = create_test_graph()
#     assert _check_genome(G) is True

# def test_get_grammar_tree():
#     G = create_test_graph()
#     tree = get_grammar_tree(G)
#     assert isinstance(tree, nx.DiGraph)

# def test_get_successors():
#     G = create_test_graph()
#     ref = NodeReference(G, NODE_ZERO)
#     assert isinstance(get_successors(ref), list)

# def test_get_predecessor():
#     G = create_test_graph()
#     ref = NodeReference(G, '1')
#     assert get_predecessor(ref) == NODE_ZERO

# def test_get_siblings():
#     G = create_test_graph()
#     ref = NodeReference(G, '1')
#     assert isinstance(get_siblings(ref), list)

# def test_set_successors_order():
#     G = create_test_graph()
#     ref = NodeReference(G, NODE_ZERO)
#     old_order = get_successors(ref)
#     new_order = old_order[::-1] 
#     set_successors_order(ref, new_order)
#     assert get_successors(ref) == new_order


# def test_get_frames():
#     G = create_test_graph()
#     assert isinstance(get_frames(G), list)

# def test_get_macros():
#     G = create_test_graph()
#     assert isinstance(get_macros(G), list)

# def test_get_parameters():
#     G = create_test_graph()
#     assert isinstance(get_parameters(G), list)

# def test_get_node_color_dict():
#     G = create_test_graph()
#     assert isinstance(get_node_color_dict(G), dict)

# def test_get_first_macro():
#     G = create_test_graph()
#     T = get_grammar_tree(G)
#     assert _get_first_macro(NODE_ZERO, G, T) is not None

# def test_is_equal():
#     G = create_test_graph()
#     ref1 = NodeReference(G, '1')
#     ref2 = NodeReference(G, '1')
#     assert is_equal(ref1, ref2) is True

# def test_check_genome_empty():
#     G = nx.MultiDiGraph()
#     with pytest.raises(AssertionError):
#         _check_genome(G)

# def test_get_grammar_tree_empty():
#     G = nx.MultiDiGraph()
#     with pytest.raises(AssertionError):
#         get_grammar_tree(G)

# def test_get_successors_no_successors():
#     G = create_test_graph()
#     ref = NodeReference(G, '1')
#     assert get_successors(ref) == []

# def test_get_predecessor_no_predecessor():
#     G = nx.MultiDiGraph()
#     G.add_node('1')
#     ref = NodeReference(G, '1')
#     assert get_predecessor(ref) == 0

# def test_set_successors_order_single_successor():
#     G = create_test_graph()
#     ref = NodeReference(G, NODE_ZERO)
#     set_successors_order(ref, ['1'])
#     assert get_successors(ref) == ['1']

# def test_get_frames_no_frames():
#     G = nx.MultiDiGraph()
#     assert get_frames(G) == []

# def test_get_macros_no_macros():
#     G = create_test_graph()
#     for node in G.nodes():
#         G.nodes[node].pop('_macro', None)
#     assert get_macros(G) == []

# def test_get_parameters_no_parameters():
#     G = create_test_graph()
#     for node in G.nodes():
#         G.nodes[node].pop('_macro', None)
#     assert get_parameters(G) == []

# def test_is_equal_different_nodes():
#     G = create_test_graph()
#     ref1 = NodeReference(G, '1')
#     ref2 = NodeReference(G, '3')
#     assert is_equal(ref1, ref2) is False

