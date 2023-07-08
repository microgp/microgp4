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
# v1 / June 2023 / Squillero (GX)

from microgp4.global_symbols import *
from microgp4.operators.unroll import *
from microgp4.user_messages import *
from microgp4.classes import *
from microgp4.registry import *
from microgp4.functions import *
from microgp4.randy import rrandom
from microgp4.tools.graph import *

import networkx as nx

@genetic_operator(num_parents=1)
def single_parameter_mutation(parent: Individual, strength=1.0) -> list['Individual']:
    offspring = parent.clone
    param = rrandom.choice(offspring.parameters)
    mutate(param, strength=strength)
    return [offspring]


@genetic_operator(num_parents=1)
def add_macro_to_bunch_mutation(parent: Individual, strength=1.0) -> list['Individual']:
    offspring = parent.clone
    G = offspring.genome
    candidates = [
        n for n in offspring.nodes
        if isinstance(G.nodes[n]['_selement'], FrameMacroBunch) and G.out_degree[n] < G.nodes[n]['_selement'].SIZE[1] -
        1
    ]
    if not candidates:
        raise GeneticOperatorAbort
    node = rrandom.choice(candidates)
    successors = get_successors(NodeReference(G, node))
    new_macro_type = rrandom.choice(G.nodes[node]['_selement'].POOL)
    new_macro = unroll_selement(new_macro_type, G)
    G.add_edge(node, new_macro, _type=FRAMEWORK)
    i = rrandom.randint(0, len(successors))
    set_successors_order(NodeReference(G, node), successors[:i] + [new_macro] + successors[i:])
    return [offspring]


@genetic_operator(num_parents=2)
def bunch_random_crossover(p1: Individual, p2: Individual, strength=1.0) -> list['Individual']:
    offspring = p1.clone

    # TODO: Cercare FRAME il cui tipo esiste in p2
    candidates = [f for f in p2.frames if (isinstance(f, FrameMacroBunch) and f in offspring.frames)]
    if not candidates:
        raise GeneticOperatorAbort
    chosen = rrandom.choice(candidates)
    # find a node in p2 where selected frame is
    start_locus = rrandom.choice([l for l in p2.genome.nodes if p2.genome._node[l]['_selement'] == chosen])
    # take the node and the children nodes
    sub_genome = p2.genome.subgraph(list(nx.dfs_preorder_nodes(p2.genome,start_locus)))
    # save to be removed node's actual position
    old_locus = rrandom.choice([ n for n in offspring.genome.nodes if offspring.genome._node[n]['_selement'] == chosen])
    # save to be removed node to perform later check
    old_node = offspring.genome._node[old_locus]
    # first position of the added nodes
    first_locus = len(offspring.genome)
    # adding nodes from p2
    offspring._genome = nx.disjoint_union(offspring.genome, sub_genome)
    # find the new position of the to be removed node
    new_locus = [ n for n in offspring.genome.nodes if offspring.genome._node[n] == old_node][0]
    # SUGGERIMENTO: **AGGIUNGI** UN ATTRIBUTO AL NODO E POI CANCELLALO
    # ALTERNATIVA: new_locus = next(n for n in offspring.genome.nodes if offspring.genome._node[n] == old_node)
    # save in going edges of aforementioned node
    attached_nodes = [e[0] for e in offspring.genome.edges if e[1] == new_locus]
    # deleting node with his children
    offspring.genome.remove_nodes_from(list(nx.dfs_preorder_nodes(offspring.genome,new_locus)))
    # recreating edges to the added nodes
    offspring.genome.add_edges_from([(l,first_locus) for l in attached_nodes])

    # TODO: Aggiungere _type negli archi

    return [offspring]