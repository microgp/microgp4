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
import logging

import _microgp4 as ugp


def test_random_individual():
    """Check the reproducibility of an individual of 1,000 random integers between -1M and +1M"""

    m = ugp.f.macro("{n}", n=ugp.f.integer_parameter(-1_000_000, 1_000_000 + 1))
    bunch = ugp.framework.bunch(m, size=1_000)
    population = ugp.classes.Population(top_frame=bunch, evaluator=None)

    ugp.rrandom.seed(42)
    population.add_random_individual()
    reference = population.dump_individual(0)

    population.add_random_individual()
    # Next individuals should be different
    assert reference != population.dump_individual(len(population.individuals) - 1)

    ugp.rrandom.seed(None)
    population.add_random_individual()
    assert reference != population.dump_individual(len(population.individuals) - 1)

    ugp.rrandom.seed(42)
    population.add_random_individual()
    assert reference == population.dump_individual(len(population.individuals) - 1)
