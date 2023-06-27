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
import microgp4 as ugp 

@pytest.fixture
def macro():
    class TestMacro(ugp.classes.Macro):
        TEXT = 'test'
        PARAMETERS = {}
        EXTRA_PARAMETERS = {}

    return TestMacro()


@pytest.fixture
def parameter_abc():
    class TestParameterABC(ugp.classes.ParameterABC):
        def mutate(self, strength: float = 1., **kwargs) -> None:
            pass

    return TestParameterABC()


@pytest.fixture
def node_view():
    class TestNodeView(ugp.classes.NodeView):
        def __init__(self):
            pass

    return TestNodeView()


def test_macro_initialization(macro):
    assert isinstance(macro, ugp.classes.Macro)
    assert isinstance(macro, ugp.classes.EvolvableABC)
    assert isinstance(macro, ugp.classes.Checkable)
    assert macro.parameters == {}


def test_macro_eq(macro):
    same_macro = macro
    assert macro == same_macro

    different_macro = ugp.classes.Macro()
    assert macro != different_macro


def test_macro_is_valid(macro, node_view):
    assert macro.is_valid(node_view)


def test_macro_text(macro):
    assert macro.text == 'test'


def test_macro_extra_parameters(macro):
    assert macro.extra_parameters == {}


def test_macro_parameter_types(macro):
    assert macro.parameter_types == {}


def test_macro_str(macro):
    assert str(macro) == 'TestMacro'


def test_macro_dump(macro):
    extra_parameters = ugp.classes.ValueBag({'test': 'value'})
    assert macro.dump(extra_parameters) == 'test'


def test_macro_mutate(macro, parameter_abc):
    macro.parameters = {'test': parameter_abc}
    macro.mutate(0.5)  

def test_macro_is_name_valid():
    assert ugp.classes.Macro.is_name_valid('test') 
    assert not ugp.classes.Macro.is_name_valid(123)
