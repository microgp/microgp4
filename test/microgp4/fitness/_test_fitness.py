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

from math import sqrt
import pytest

import microgp4 as ugp


def test_simple():
    with pytest.raises(AssertionError):
        # TypeError: different types of fitness
        assert ugp.fit.Scalar(13) <= ugp.fit.Float(13)

    # SCALAR
    # nb. sqrt(2)**2 = 2.0000000000000004
    assert not ugp.fit.Float(2) == ugp.fit.Float(sqrt(2)**2)
    assert ugp.fit.Float(2) != ugp.fit.Float(sqrt(2)**2)
    assert not ugp.fit.Float(2) > ugp.fit.Float(sqrt(2)**2)
    assert not ugp.fit.Float(2) >= ugp.fit.Float(sqrt(2)**2)
    assert ugp.fit.Float(2) < ugp.fit.Float(sqrt(2)**2)
    assert ugp.fit.Float(2) <= ugp.fit.Float(sqrt(2)**2)
    #
    assert not ugp.fit.Float(13) == ugp.fit.Float(17)
    assert ugp.fit.Float(13) != ugp.fit.Float(17)
    assert not ugp.fit.Float(13) > ugp.fit.Float(17)
    assert not ugp.fit.Float(13) >= ugp.fit.Float(17)
    assert ugp.fit.Float(13) < ugp.fit.Float(17)
    assert ugp.fit.Float(13) <= ugp.fit.Float(17)

    # INTEGER
    assert ugp.fit.Integer(13) == ugp.fit.Integer(13)
    assert ugp.fit.Integer(13) == ugp.fit.Integer(13 + .01)
    assert ugp.fit.Integer(13) != ugp.fit.Integer(13 - .01)
    assert ugp.fit.Integer(17) > ugp.fit.Integer(13)
    assert ugp.fit.Integer(17) >= ugp.fit.Integer(13)
    assert not ugp.fit.Integer(17) < ugp.fit.Integer(13)
    assert not ugp.fit.Integer(17) <= ugp.fit.Integer(13)

    # SCALAR / APPROXIMATE
    # nb. sqrt(2)**2 = 2.0000000000000004
    assert ugp.fit.Scalar(2) == ugp.fit.Scalar(sqrt(2)**2)
    assert not ugp.fit.Scalar(2) != ugp.fit.Scalar(sqrt(2)**2)
    assert not ugp.fit.Scalar(2) > ugp.fit.Scalar(sqrt(2)**2)
    assert ugp.fit.Scalar(2) >= ugp.fit.Scalar(sqrt(2)**2)
    assert not ugp.fit.Scalar(2) < ugp.fit.Scalar(sqrt(2)**2)
    assert ugp.fit.Scalar(2) <= ugp.fit.Scalar(sqrt(2)**2)
    #
    assert not ugp.fit.Scalar(13) == ugp.fit.Scalar(17)
    assert ugp.fit.Scalar(13) != ugp.fit.Scalar(17)
    assert not ugp.fit.Scalar(13) > ugp.fit.Scalar(17)
    assert not ugp.fit.Scalar(13) >= ugp.fit.Scalar(17)
    assert ugp.fit.Scalar(13) < ugp.fit.Scalar(17)
    assert ugp.fit.Scalar(13) <= ugp.fit.Scalar(17)

    # REVERSE FITNESS (the smaller, the better -- ie. 2 > 3)
    rev_scalar = ugp.fit.reverse_fitness(ugp.fit.Float)
    assert not rev_scalar(2) == rev_scalar(sqrt(2)**2)
    assert rev_scalar(2) != rev_scalar(sqrt(2)**2)
    assert rev_scalar(2) > rev_scalar(sqrt(2)**2)
    assert rev_scalar(2) >= rev_scalar(sqrt(2)**2)
    assert not rev_scalar(2) < rev_scalar(sqrt(2)**2)
    assert not rev_scalar(2) <= rev_scalar(sqrt(2)**2)
    assert not rev_scalar(13) == rev_scalar(17)
    assert rev_scalar(13) != rev_scalar(17)
    assert rev_scalar(13) > rev_scalar(17)
    assert rev_scalar(13) >= rev_scalar(17)
    assert not rev_scalar(13) < rev_scalar(17)
    assert not rev_scalar(13) <= rev_scalar(17)
    #
    rev_approximate = ugp.fit.reverse_fitness(ugp.fit.Scalar)
    assert rev_approximate(2) == rev_approximate(sqrt(2)**2)
    assert not rev_approximate(2) != rev_approximate(sqrt(2)**2)
    assert not rev_approximate(2) > rev_approximate(sqrt(2)**2)
    assert rev_approximate(2) >= rev_approximate(sqrt(2)**2)
    assert not rev_approximate(2) < rev_approximate(sqrt(2)**2)
    assert rev_approximate(2) <= rev_approximate(sqrt(2)**2)
    assert not rev_approximate(13) == rev_approximate(17)
    assert rev_approximate(13) != rev_approximate(17)
    assert rev_approximate(13) > rev_approximate(17)
    assert rev_approximate(13) >= rev_approximate(17)
    assert not rev_approximate(13) < rev_approximate(17)
    assert not rev_approximate(13) <= rev_approximate(17)
    #
    with pytest.raises(AssertionError):
        # TypeError: different types of fitness
        assert rev_approximate(13) <= rev_scalar(13)

    # VECTOR of Scalars
    assert ugp.fit.Lexicographic([23, 2], ugp.fit.Float) == ugp.fit.Lexicographic([23, 2], ugp.fit.Float)
    assert not ugp.fit.Lexicographic([23, 2], ugp.fit.Float) != ugp.fit.Lexicographic([23, 2], ugp.fit.Float)
    assert not ugp.fit.Lexicographic([23, 2], ugp.fit.Float) == ugp.fit.Lexicographic([23, sqrt(2)**2], ugp.fit.Float)
    assert ugp.fit.Lexicographic([23, 2], ugp.fit.Float) != ugp.fit.Lexicographic([23, sqrt(2)**2], ugp.fit.Float)
    assert ugp.fit.Lexicographic([23, 10], ugp.fit.Float) == ugp.fit.Lexicographic([23, 10], ugp.fit.Float)
    assert not ugp.fit.Lexicographic([23, 10], ugp.fit.Float) == ugp.fit.Lexicographic([10, 23], ugp.fit.Float)
    assert ugp.fit.Lexicographic([23, 10], ugp.fit.Float) != ugp.fit.Lexicographic([10, 23], ugp.fit.Float)
    assert ugp.fit.Lexicographic([23, 10], ugp.fit.Float) > ugp.fit.Lexicographic([10, 23], ugp.fit.Float)
    assert ugp.fit.Lexicographic([23, 10], ugp.fit.Float) >= ugp.fit.Lexicographic([10, 23], ugp.fit.Float)
    assert not ugp.fit.Lexicographic([23, 10], ugp.fit.Float) < ugp.fit.Lexicographic([10, 23], ugp.fit.Float)
    assert not ugp.fit.Lexicographic([23, 10], ugp.fit.Float) <= ugp.fit.Lexicographic([10, 23], ugp.fit.Float)

    # VECTOR of Scalar
    assert ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar) == ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar)
    assert not ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar) != ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar)
    assert ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar) == ugp.fit.Lexicographic([23, sqrt(2)**2], ugp.fit.Scalar)
    assert not ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar) != ugp.fit.Lexicographic([23, sqrt(2)**2], ugp.fit.Scalar)
    assert not ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar) == ugp.fit.Lexicographic([sqrt(2)**2, 23], ugp.fit.Scalar)
    assert ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar) != ugp.fit.Lexicographic([sqrt(2)**2, 23], ugp.fit.Scalar)
    assert ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar) > ugp.fit.Lexicographic([sqrt(2)**2, 23], ugp.fit.Scalar)
    assert ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar) >= ugp.fit.Lexicographic([sqrt(2)**2, 23], ugp.fit.Scalar)
    assert not ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar) < ugp.fit.Lexicographic([sqrt(2)**2, 23], ugp.fit.Scalar)
    assert not ugp.fit.Lexicographic([23, 2], ugp.fit.Scalar) <= ugp.fit.Lexicographic([sqrt(2)**2, 23], ugp.fit.Scalar)

    f1 = ugp.fit.Vector([ugp.fit.Float(2), ugp.fit.Float(sqrt(2)**2)])
    f2 = ugp.fit.Vector([ugp.fit.Float(sqrt(2)**2), ugp.fit.Float(2)])
    assert f1 != f2
    assert f1 < f2
    f1 = ugp.fit.Vector([ugp.fit.reverse_fitness(ugp.fit.Float)(2), ugp.fit.Float(sqrt(2)**2)])
    f2 = ugp.fit.Vector([ugp.fit.reverse_fitness(ugp.fit.Float)(sqrt(2)**2), ugp.fit.Float(2)])
    assert f1 != f2
    assert f1 > f2

    f1 = ugp.fit.reverse_fitness(ugp.fit.Vector)([ugp.fit.Float(2), ugp.fit.Float(sqrt(2)**2)])
    f2 = ugp.fit.reverse_fitness(ugp.fit.Vector)([ugp.fit.Float(sqrt(2)**2), ugp.fit.Float(2)])
    assert f1 != f2
    assert f1 > f2
    print(f1)
