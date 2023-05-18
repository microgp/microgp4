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

import random
import microgp4 as ugp

BATCH_SIZE = 4096


def test_reproducibility():
    seed = random.randint(0, 1_000_000)
    ugp.rrandom.seed(seed)
    v1 = [ugp.rrandom.random() for _ in range(BATCH_SIZE)]
    v2 = [ugp.rrandom.random() for _ in range(BATCH_SIZE)]
    ugp.rrandom.seed(seed)
    v3 = [ugp.rrandom.random() for _ in range(BATCH_SIZE)]
    assert v1 == v3
    assert v2 != v3

    ugp.rrandom.seed()
    v4 = [ugp.rrandom.random() for _ in range(BATCH_SIZE)]
    assert v1 != v4


def test_independence():
    seed = random.randint(0, 1_000_000)
    ugp.rrandom.seed(seed)
    v1 = [ugp.rrandom.random() for _ in range(BATCH_SIZE)]
    ugp.rrandom.seed(seed)
    v2_1 = [ugp.rrandom.random() for _ in range(BATCH_SIZE // 2)]
    z = [random.random() for _ in range(BATCH_SIZE)]
    v2_2 = [ugp.rrandom.random() for _ in range(BATCH_SIZE // 2)]
    assert v1 == v2_1 + v2_2
