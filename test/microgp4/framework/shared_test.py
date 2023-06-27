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
from microgp4.framework.shared import make_shared_parameter


def test_make_shared_parameter():
    for p in [
            ugp.f.integer_parameter(0, 10_000_000),
            ugp.f.float_parameter(0, 1.),
            ugp.f.choice_parameter(range(10_000)),
            ugp.f.array_parameter("01X", 256)
    ]:

        SharedParameter = make_shared_parameter(p)
        shared_param1 = SharedParameter()
        shared_param2 = SharedParameter()

        assert shared_param1.value == shared_param2.value

        tmp = shared_param1.value
        shared_param1.mutate(1)
        assert shared_param1.value == shared_param2.value
        assert shared_param1.value != tmp

        SharedParameter2 = make_shared_parameter(p)
        shared_param3 = SharedParameter2()

        tmp2 = shared_param3.value
        shared_param3.mutate()
        assert shared_param3.value != tmp2

        assert shared_param1.value != shared_param3.value
        assert shared_param2.value != shared_param3.value
