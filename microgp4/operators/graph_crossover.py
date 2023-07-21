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

# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
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

#############################################################################
# HISTORY
# v1 / July 2023 / Sacchet (MS)

from microgp4.global_symbols import *
from microgp4.operators.unroll import *
from microgp4.user_messages import *
from microgp4.classes import *
from microgp4.registry import *
from microgp4.functions import *
from microgp4.randy import rrandom
from microgp4.tools.graph import *

import networkx as nx


@genetic_operator(num_parents=2)
def bunch_random_crossover(p1: Individual, p2: Individual, strength=1.0) -> list['Individual']:
    offspring = p1.clone
    candidates = [
        f for f in p2.frames if (isinstance(f, FrameMacroBunch) and type(f) in [type(fr) for fr in offspring.frames])
    ]
    if not candidates:
        raise GeneticOperatorAbort
    chosen = rrandom.choice(candidates)
    # find a node in p2 where selected frame is
    start_locus = rrandom.choice([l for l in p2.genome.nodes if type(p2.genome.nodes[l]['_selement']) == type(chosen)])
    # take the node and the children nodes
    sub_genome = p2.genome.subgraph(list(nx.dfs_preorder_nodes(p2.genome, start_locus)))
    # save to be removed node's actual position
    old_locus = rrandom.choice(
        [n for n in offspring.genome.nodes if type(offspring.genome.nodes[n]['_selement']) == type(chosen)])
    # mark the to be removed node
    offspring.genome.nodes[old_locus]['to_be_removed'] = True
    # first position of the added nodes
    first_locus = len(offspring.genome)
    # adding nodes from p2
    offspring._genome = nx.disjoint_union(offspring.genome, sub_genome)
    # find the new position of the to be removed node
    new_locus = next(n for n in offspring.genome.nodes if 'to_be_removed' in offspring.genome.nodes[n])
    # save in going edges (with parameters) of aforementioned node
    attached_nodes = [(e[0], e[2]) for e in offspring.genome.edges.data() if e[1] == new_locus]
    # deleting node with his children
    offspring.genome.remove_nodes_from(list(nx.dfs_preorder_nodes(offspring.genome, new_locus)))
    # recreating edges to the added nodes
    for ed in attached_nodes:
        offspring.genome.add_edge(ed[0], first_locus, **ed[1])
    #offspring._Individual__COUNTER == max(offspring.genome.nodes)

    return [offspring]
