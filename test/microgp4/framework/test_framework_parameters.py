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

import microgp4 as ugp

def test_integer():
    p1 = ugp.f.integer_parameter(1,5)
    p2 = ugp.f.integer_parameter(1,6)
    p3 = ugp.f.integer_parameter(4,6)
    a = p1()
    b = p2()
    c = p2()
    d = p3()
    assert a.value == 1
    assert b.value == a.value
    assert a != b
    assert c != b
    b.mutate(1)
    assert a.value != b.value
    assert b.value != c.value
    assert d.value != a.value

def test_float():
    p1 = ugp.f.float_parameter(0.1,2.2)
    p2 = ugp.f.float_parameter(0.1,3.2)
    p3 = ugp.f.float_parameter(1,2.2)
    a = p1()
    b = p2()
    c = p2()
    d = p3()
    assert a.value == 0.1
    assert b.value == a.value
    assert a != b
    assert c != b
    b.mutate(1)
    assert a.value != b.value
    assert b.value != c.value
    assert d.value != a.value

def test_choice():
    p1 = ugp.f.choice_parameter(['a','b','c','d'])
    p2 = ugp.f.choice_parameter(['a','x','y','z'])
    p3 = ugp.f.choice_parameter(range(4))
    a = p1()
    b = p2()
    c = p2()
    d = p3()
    assert a.value == 'a'
    assert b.value == a.value
    assert a != b
    assert c != b
    b.mutate(1)
    assert a.value != b.value
    assert b.value != c.value
    assert d.value != a.value

# def test_choice_mutation_working():
#     p5 = ugp4.f.choice_parameter(range(12))
#     f = p5()
#     assert f.value == 0
#     f.mutate(1)
#     assert f.value != 0

# def test_choice_mutation_no_generator():
#     p5 = ugp4.f.choice_parameter(range(4))
#     f = p5()
#     assert f.value == 0
#     f.mutate(0.5)
#     assert f.value != 0

# def test_choice_mutation_unexpected():
#     p5 = ugp4.f.choice_parameter(range(11))
#     f = p5()
#     assert f.value == 0
#     f.mutate(1)
#     # NOTE [MS]: this shouldn't be correct
#     # Test pass only if ran alone
#     assert f.value == 0
#     f.mutate(1)
#     assert f.value != 0

def test_array():
    p1 = ugp.f.array_parameter(['a','b','c','d'], 2)
    p2 = ugp.f.array_parameter(['a','x','y','z'], 2)
    p3 = ugp.f.array_parameter(['w','x','y','z'], 2)
    a = p1()
    b = p2()
    c = p2()
    d = p3()
    assert a.value == 'aa'
    assert b.value == a.value
    assert a != b
    assert c != b
    b.mutate(1)
    assert a.value != b.value
    assert b.value != c.value
    assert d.value != a.value