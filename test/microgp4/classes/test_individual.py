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

# from microgp4.global_symbols import FRAMEWORK, NODE_ZERO
# from microgp4.classes.readymade_macros import MacroZero
# from microgp4.classes.fitness import FitnessABC
# from microgp4.classes.frame import FrameABC
# from microgp4.ea.graph import *
# import pytest
# from unittest.mock import Mock
# from microgp4.classes.individual import Individual
# import networkx as nx

from typing import Any, Type

import microgp4 as ugp
import networkx as nx

NODE_ZERO = 0
FRAMEWORK = "framework"

def test_individual_class():
    
    G1 = nx.MultiDiGraph()
    G2 = nx.MultiDiGraph()

    G1.add_node(NODE_ZERO, data='test')
    G2.add_node(NODE_ZERO, data='test')


    ind1 = ugp.classes.Individual(G1)
    ind2 = ugp.classes.Individual(G2)

    print(ind1)
    assert ind1 == ind2
    assert ind1 != None

    macro1a = ugp.f.macro('1')
    macro1b = ugp.f.macro('call {m1}', m1=ugp.f.global_reference('macrob'))
    frame1 = ugp.f.bunch([macro1a, macro1a, macro1a, macro1a, macro1b], name='frame1', size=10_000)
    frame2 = ugp.f.bunch([macro1a], name='frame2', size=10_000)
    ind = ugp.classes.Individual(top_frame=frame1)

    ind.G.add_edge(0, 1, kind=FRAMEWORK)
    ind.G.add_node(1, _macro=ugp.classes.readymade_macros.MacroZero)
    ind.G.add_node(0, _frame=ugp.classes.readymade_frames.SELF)
    print(len(ind.macros))

    assert str(ind.grammar_tree) == "DiGraph with 2 nodes and 1 edges"
    assert ind != ind1
    
    assert ind1.fitness == None
    assert ind2.fitness == None

    ind1.fitness = 42
    ind2.fitness = 43

    assert ind1.fitness == 42
    assert ind2.fitness == 43

    ind2.fitness = 42   

    assert ind1.fitness == ind2.fitness
    assert ind1.genome != ind2.genome


    assert len(ind.macros) == 2 # why not 1?

    assert ind.discard_useless_components() == None

    ind.G.add_edge(0, 2, kind=FRAMEWORK)
    ind.G.add_node(2, _macro=macro1b)
    ind.G.add_node(NODE_ZERO, _macro=ugp.classes.readymade_macros.MacroZero)
    print(ind.genome)
    print(ind.dump)

    
    assert len(ind.macros) == 3

    assert ind.as_forest(filename="somefile.jpg") == None
    
    # [MS] MARCO's try
    ind.G.add_edge(1,3, kind=FRAMEWORK)
    ind.G.add_edge(2,4, kind=FRAMEWORK)
    ind.G.add_node(3, _macro=macro1a)
    ind.G.add_node(4, _macro=macro1a)
    # [MS] ok but what if an individual has only two nodes? Is it invalid?
    # lgp correctly ignore the node 0. But if the only nodes existing are those connected to 0, they will be ignored because the function
    # focus on the edges and not on the nodes.
    print(ind.as_lgp())

    ind1.G.add_edge(0, 1, kind=FRAMEWORK)
    ind1.G.add_node(0, _frame=ugp.classes.readymade_macros.MacroZero)
    ind1.G.add_node(1, _macro=macro1a)
    ind1.check() # [MS] bug in individual.py lines 322, 325. Incorrect parameters passage.


    # print(ind.parameters)
    # [MS] I think that in graph.py in get_parameters it tries to access a .values that it can not exists.

    G1 = nx.MultiDiGraph()
    G1.add_edge(0, 1, kind=FRAMEWORK)

    ind1 = ugp.classes.Individual(top_frame=G1)
    ind1.G.add_node(1, _macro=macro1a)
    ind1.G.add_edge(0, 1, kind=FRAMEWORK)
    print(ind1.G.nodes(data=True))
    print("aywa")
    tree = ind1.grammar_tree

    expected_tree = nx.DiGraph()
    expected_tree.add_edge(1, 2)
    expected_tree.add_node(1)
    expected_tree.add_node(2)

    assert nx.is_isomorphic(tree, expected_tree)

    assert nx.is_branching(tree) and nx.is_weakly_connected(tree)
