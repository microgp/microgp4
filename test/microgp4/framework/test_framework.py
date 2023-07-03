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

def test_alternative():
    p1 = ugp.f.integer_parameter(0,4)
    m1 = ugp.f.macro("test number {p1}", p1=p1)
    m2 = ugp.f.macro("test number {p2}", p2=p1)
    m3 = ugp.f.macro("test number {p3}", p3=p1)
    a1 = ugp.f.alternative([m1,m2,m3])
    a2 = ugp.f.alternative([m1,m2])
    a3 = ugp.f.alternative([m1,m3])

    a = a1()
    b = a1()
    c = a2()
    d = a3()

    assert a != None
    assert a == b
    assert a.successors[0] == m1
    assert a.successors[0] in [m2,m3]

    assert a != c
    assert a != d
    assert c != d

    with pytest.raises(ugp.user_messages.MicroGPError):
        ugp.f.alternative(12)
    with pytest.raises(ugp.user_messages.MicroGPError):
        ugp.f.alternative('abc')
    with pytest.raises(ugp.user_messages.MicroGPError):
        ugp.f.alternative(p1)

def test_sequence():
    t1 = 'abc'
    p1 = ugp.f.integer_parameter(0,4)
    m1 = ugp.f.macro("test number {p1}", p1=p1)
    s1 = ugp.f.sequence([m1])
    s2 = ugp.f.sequence([s1])
    s3 = ugp.f.sequence([t1])

    a = s1()
    b = s1()
    c = s2()
    d = s3()
    assert a is not None
    assert len(a.successors) == 1
    assert a == b

    assert a != c
    assert len(c.successors) == 1
    for e in c.successors:
        assert e == s1
    
    assert a != d
    assert c != d
    assert len(d.successors) == 1
    for e in d.successors:
        assert type(t1) != type(e)
        assert type(e) == type(m1)
    
    with pytest.raises(ugp.user_messages.MicroGPError):
        ugp.f.sequence(12)

def test_bunch():
    p1 = ugp.f.integer_parameter(0,4)
    m1 = ugp.f.macro("test number {p1}", p1=p1)
    m2 = ugp.f.macro("test number {p2}", p2=p1)
    m3 = ugp.f.macro("test number {p3}", p3=p1)
    b1 = ugp.f.bunch(m1, (2,4))
    b2 = ugp.f.bunch(m1, (2,5))
    b3 = ugp.f.bunch(m1)
    b4 = ugp.f.bunch([m1,m2,m3], (4,7))

    a = b1()
    b = b1()
    c = b2()
    d = b3()
    e = b4()

    assert a is not None
    assert len(a.successors) in [2,3]
    assert a.successors[0] == m1
    assert a == b
    assert a != c
    assert len(d.successors) == 1
    assert all(i in [m1,m2,m3] for i in e.successors)

    with pytest.raises(ugp.user_messages.MicroGPError):
        ugp.f.bunch(p1)