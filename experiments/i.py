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

import pickle
import microgp4 as ugp


class Integer2(ugp.classes.FitnessABC, int):
    """A single numeric value -- Larger is better."""

    def __new__(cls, *args, **kw):
        return int.__new__(cls, *args, **kw)

    def _decorate(self):
        return str(int(self))


f = ugp.fit.make_fitness(4)
# f = Integer2(4)
print(pickle.dumps(f))
