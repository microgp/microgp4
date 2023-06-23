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

from microgp4.tools.names import *
import pytest

def test_canonize_name():
    assert canonize_name('foo', 'bar') == 'bar❬foo#1❭'
    assert canonize_name('foo', 'bar') == 'bar❬foo#2❭'
    assert canonize_name('baz', 'qux') == 'qux❬baz#1❭'
    
    assert canonize_name('foo', 'pippo', user=True) == 'pippo<foo>'
    
    assert canonize_name('thing', 'some', make_unique=False) == 'some❬thing❭'
    assert canonize_name('tag', 'some', make_unique=False) == 'some❬tag❭'
    
    assert canonize_name('foo', 'bar', user_space=True) == 'bar<foo#3>'
    assert canonize_name('foo', 'bar', user_space=True) == 'bar<foo#4>'
    


# user <>
# else ❬❭
def test_uncanonize_name():
    assert uncanonize_name('foo❬bar❭') == 'bar'
    assert uncanonize_name('foo❬bar#1❭') == 'bar'
    assert uncanonize_name('foo❬bar#1❭', keep_number=True) == 'bar#1'
    assert uncanonize_name('foo<bar>', user=True) == 'bar'
    assert uncanonize_name('foo<bar#1>') == ''
    assert uncanonize_name('foo<bar#1>', user=True, keep_number=True) == 'bar#1'
    assert uncanonize_name('foo<smth>', user=True) == 'smth'
    
    assert uncanonize_name('foo❬bar❭', user=False) == 'bar'
    assert uncanonize_name('foo<bar>', user=False) == ''
    assert uncanonize_name('foo<bar#1>', user=False) == ''
    assert uncanonize_name('foo❬bar#3❭', user=False, keep_number=True) == 'bar#3'
