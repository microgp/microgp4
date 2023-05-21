# !/usr/bin/env python3
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

from random import shuffle
import networkx as nx

import microgp4 as ugp


# NOTE[GX]: Dictionaries are the underlying data structure used for NetworkX graphs, and as of Python 3.7+ they
# maintain insertion order. We should obtain the same result each time you run Graph.edges()!
def test_edge_order():
    """Checks the order of the edges is reliable."""
    G = nx.MultiDiGraph()
    nodes = [n for n in range(1, 10_000)]
    shuffle(nodes)

    G.add_node(ugp.NODE_ZERO)
    for n in nodes:
        G.add_node(n)
        G.add_edge(ugp.NODE_ZERO, n)

    assert list(nodes) == list(G.successors(ugp.NODE_ZERO))

    for _ in range(100):
        # remove a node
        i = nodes[len(nodes) // 2]
        G.remove_node(nodes[i])
        nodes = nodes[:i] + nodes[i + 1:]
        assert list(nodes) == list(G.successors(ugp.NODE_ZERO))
