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

import pytest
import networkx as nx
import microgp4 as ugp


class ConcreteParameter(ugp.classes.ParameterABC):

    def mutate(self, strength: float = 1., **kwargs) -> None:
        self.value = self.value + strength


class ConcreteStructuralParameter(ugp.classes.ParameterStructuralABC):

    def mutate(self, strength: float = 1., **kwargs) -> None:
        if self.is_fastened:
            self._node_reference.node += strength


def test_ParameterABC():
    parameter_abc = ConcreteParameter()
    parameter_abc.value = 5

    assert parameter_abc.key is not None
    assert parameter_abc.value == 5

    parameter_abc2 = ConcreteParameter()
    parameter_abc2.value = 5

    assert parameter_abc != parameter_abc2

    assert type(parameter_abc) == type(parameter_abc2) and parameter_abc.value == parameter_abc2.value


def test_ParameterStructuralABC():
    graph = nx.MultiDiGraph()
    graph.add_node(1)
    node_ref = ugp.classes.NodeReference(graph, 1)

    parameter_structural_abc = ConcreteStructuralParameter()
    parameter_structural_abc._fasten(node_ref)

    assert parameter_structural_abc.is_fastened
    assert parameter_structural_abc.value is None

    graph.add_edge(1, 2, key=parameter_structural_abc.key)
    assert parameter_structural_abc.value == 2

    parameter_structural_abc.drop_link()
    assert not graph.has_edge(1, 2, key=parameter_structural_abc.key)
