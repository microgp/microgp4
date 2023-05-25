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

from networkx.classes import MultiDiGraph
from microgp4.classes.node_reference import NodeReference


def test_node_reference():
    G = MultiDiGraph()
    p1 = NodeReference(G,1)
    p2 = NodeReference(G,2)
    assert p1 is not None
    assert type(p1.graph) == type(G)
    assert p1.node == 1 
    assert p1 != p2
    assert p2.node != 3
    assert p1.graph == p2.graph

