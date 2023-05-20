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

rev_scalar = ugp.fit.reverse_fitness(ugp.fit.Scalar)
# in a reversed fitness, the smaller, the better -- ie. 2 > 3
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

rev_approximate = ugp.fit.reverse_fitness(ugp.fit.Approximate)
# in a reversed fitness, the smaller, the better -- ie. 2 > 3
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

with pytest.raises(AssertionError):
    assert rev_approximate(13) <= rev_scalar(13)
