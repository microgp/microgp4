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

import microgp4 as ugp


def test_simple():
    assert ugp.fit.Scalar(2) == ugp.fit.Scalar(2)
    assert ugp.fit.Scalar(2) != ugp.fit.Scalar(sqrt(2)**2)
    assert ugp.fit.Scalar(2) >= ugp.fit.Scalar(2)
    assert ugp.fit.Scalar(2) <= ugp.fit.Scalar(2)
    assert ugp.fit.Scalar(2) > ugp.fit.Scalar(1)
    assert ugp.fit.Scalar(2) >= ugp.fit.Scalar(1)
    assert not ugp.fit.Scalar(2) <= ugp.fit.Scalar(1)
    assert not ugp.fit.Scalar(2) < ugp.fit.Scalar(1)

    assert ugp.fit.Approximate(2) == ugp.fit.Approximate(2)
    assert ugp.fit.Approximate(2) == ugp.fit.Approximate(sqrt(2)**2)
    assert ugp.fit.Approximate(2) >= ugp.fit.Approximate(2)
    assert ugp.fit.Approximate(2) <= ugp.fit.Approximate(2)
    assert ugp.fit.Approximate(2) > ugp.fit.Approximate(1)
    assert ugp.fit.Approximate(2) >= ugp.fit.Approximate(1)
    assert not ugp.fit.Approximate(2) <= ugp.fit.Approximate(1)
    assert not ugp.fit.Approximate(2) < ugp.fit.Approximate(1)

