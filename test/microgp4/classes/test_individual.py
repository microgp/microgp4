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

from microgp4.global_symbols import FRAMEWORK, NODE_ZERO
from microgp4.classes.readymade_macros import MacroZero
from microgp4.classes.fitness import FitnessABC
from microgp4.classes.frame import FrameABC
import pytest
from unittest.mock import Mock
from microgp4.classes.individual import Individual
import networkx as nx

# def test_individual_creation():
#     G = nx.MultiDiGraph()
 
#     G.add_node(1)
#     G.add_node(2)
#     G.add_node(3)
 
#     G.add_edge(1, 2)
#     G.add_edge(2, 3)
#     G.add_edge(3, 1)
 
#     ind1 = Individual(top_frame=G)
#     ind2 = Individual(top_frame=G)
 
#     assert ind1.fitness == None
#     assert ind2.fitness == None
#     ind1.fitness = 42
#     ind2.fitness = 43
#     assert ind1.fitness == 42
#     assert ind2.fitness == 43
#     ind2.fitness = 42   
#     assert ind1.fitness == ind2.fitness
#     assert ind1.genome != ind2.genome
#     my_dict = {}
 
#     G = nx.MultiDiGraph()
#     G.add_nodes_from(range(100, 110))
#     ind1 = Individual(top_frame=G)
#     ind2 = Individual(top_frame=G)
 
#     assert ind1.fitness == None
#     assert ind2.fitness == None
 
#     my_dict = {}

import pytest
import networkx as nx
from microgp4.classes import Individual

def test_individual_properties():
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(100, 110))
    ind1 = Individual(top_frame=G)

def test_individual_fitness_setter():
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(100, 110))
    ind1 = Individual(top_frame=G)
    ind1.fitness = 42
    assert ind1.fitness == 42

def test_individual_str():
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(100, 110))
    ind1 = Individual(top_frame=G)
