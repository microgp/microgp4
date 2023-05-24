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

def test_value_bag():
    test_dict = {'$a':False, 'b':'b', '_a':1, '$1': True}
    vb1 = ugp.C.ValueBag(test_dict)
    vb2 = ugp.C.ValueBag(init=None, **test_dict)
    vb3 = ugp.C.ValueBag(init=vb1)
    with pytest.raises(ugp.user_messages.MicroGPException):
        wrong_dict = {'1a':'bar','z': 1, '$a':'a'}
        _ = ugp.C.ValueBag(wrong_dict)
    with pytest.raises(ugp.user_messages.MicroGPException):
        _ = ugp.C.ValueBag(init=None,**{'1a':'bar'})

    assert isinstance(vb1, ugp.C.ValueBag)
    assert len(vb1.keys()) == 2
    assert len(vb1._keys()) == 4
    assert vb1.keys() != vb1._keys()
    assert vb1['$a'] == False
    assert vb1['b'] == 'b'
    assert vb1.a != vb1['$a']
    assert vb1 == vb2
    assert vb3 == vb2
    assert vb1['1z'] == None    

    with pytest.raises(NotImplementedError):
        vb1['a'] = 1

    with pytest.raises(TypeError):
        vb1[1]