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
import networkx as nx
# def local_reference(backward: bool = True, loop: bool = True, forward: bool = True) -> Type[ParameterStructuralABC]:

def test_local_reference():

    local_ref = ugp.f.local_reference(backward=False, loop=False, forward=False)
    assert issubclass(local_ref, ugp.classes.ParameterStructuralABC)
    assert not local_ref.BACKWARD
    assert not local_ref.SELF_LOOP
    assert not local_ref.FOREWARD

    local_ref = ugp.f.local_reference(backward=False, loop=False, forward=True)
    assert issubclass(local_ref, ugp.classes.ParameterStructuralABC)
    assert not local_ref.BACKWARD
    assert not local_ref.SELF_LOOP
    assert local_ref.FOREWARD

    local_ref = ugp.f.local_reference(backward=False, loop=True, forward=False)
    assert issubclass(local_ref, ugp.classes.ParameterStructuralABC)
    assert not local_ref.BACKWARD
    assert local_ref.SELF_LOOP
    assert not local_ref.FOREWARD

    local_ref = ugp.f.local_reference(backward=True, loop=False, forward=False)
    assert issubclass(local_ref, ugp.classes.ParameterStructuralABC)
    assert local_ref.BACKWARD
    assert not local_ref.SELF_LOOP
    assert not local_ref.FOREWARD

    local_ref = ugp.f.local_reference(backward=True, loop=True, forward=False)
    assert issubclass(local_ref, ugp.classes.ParameterStructuralABC)
    assert local_ref.BACKWARD
    assert local_ref.SELF_LOOP
    assert not local_ref.FOREWARD

    local_ref = ugp.f.local_reference(backward=True, loop=False, forward=True)
    assert issubclass(local_ref, ugp.classes.ParameterStructuralABC)
    assert local_ref.BACKWARD
    assert not local_ref.SELF_LOOP
    assert local_ref.FOREWARD

    local_ref = ugp.f.local_reference(backward=False, loop=True, forward=True)
    assert issubclass(local_ref, ugp.classes.ParameterStructuralABC)
    assert not local_ref.BACKWARD
    assert local_ref.SELF_LOOP
    assert local_ref.FOREWARD
