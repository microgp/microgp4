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


def test_shared():
    p = ugp.f.integer_parameter(0, 10_000_000)
    for p in [
            ugp.f.integer_parameter(0, 10_000_000),
            ugp.f.float_parameter(0, 1.),
            ugp.f.choice_parameter(range(10_000)),
            ugp.f.array_parameter("01X", 256)
    ]:

        s = ugp.f.make_shared_parameter(p)
        i1 = s()
        i2 = s()
        assert i1.value == i2.value
        i1.mutate(1)
        assert i1.value == i2.value
        tmp = i1.value
        i2.mutate()
        assert i1.value == i2.value
        assert i1.value == tmp

        s2 = ugp.f.make_shared_parameter(p)
        i3 = s2()
        i3.mutate()
        assert i1.value == i2.value
        assert i1.value != i3.value
