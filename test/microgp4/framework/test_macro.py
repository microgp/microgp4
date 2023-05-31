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

def test_macro():
    p1 = ugp.f.integer_parameter(0,4)
    m1 = ugp.f.macro("test number {p1}", p1=p1)
    m2 = ugp.f.macro("test numbers {p1}", p1=p1)
    m3 = ugp.f.macro("test number {p2}", p2=p1)
    a = m1()
    b = m1()
    c = m2()
    d = m3()

    assert a is not None
    assert a == b
    assert a != c
    assert a != d

    assert a.parameters == {}
    assert list(a.parameter_types.keys()) == ['p1']
    assert a.text == "test number {p1}"

    # graph.py, mimic _unroll_macro, ln 125,126
    for k, p in a.parameter_types.items():
        a.parameters[k] = p()

    assert a.parameters['p1'].value == 0
    assert a != b
    a.mutate(1)
    assert a.parameters['p1'].value != 0

    with pytest.raises(ugp.user_messages.MicroGPError):
        ugp.f.macro(12)
