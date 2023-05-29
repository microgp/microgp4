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

import microgp4 as ugp4

def test_integer():
    p1 = ugp4.f.integer_parameter(1,5)
    p2 = ugp4.f.integer_parameter(1,6)
    p3 = ugp4.f.integer_parameter(4,6)
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
    #controlla test di Squillero per parameters
    pass