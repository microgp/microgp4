# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#############################################################################
#           __________                                                      #
#    __  __/ ____/ __ \__ __   This file is part of MicroGP4 v4!2.0         #
#   / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer  #
#  / /_/ / /_/ / ____/ // /_   https://github.com/microgp/microgp4          #
#  \__  /\____/_/   /__  __/                                                #
#    /_/ --MicroGP4-- /_/      You don't need a big goal, be μ-ambitious!   #
#                                                                           #
#############################################################################
# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

from logging import WARNING
import microgp4 as ugp


@ugp.fitness_function
def fitness(genotype: str):
    """Vanilla 1-max"""
    return sum(b == "1" for b in genotype)


def test_onemax_base_take1():
    macro = ugp.f.macro("{v}", v=ugp.f.array_parameter("01", 50))
    frame = ugp.f.sequence([macro])
    evaluator = ugp.evaluator.PythonEvaluator(fitness, cook_genome=True)
    ugp.microgp_logger.setLevel(WARNING)

    ugp.rrandom.seed(42)
    p1 = ugp.ea.vanilla_ea(frame, evaluator, max_generation=10)

    p2 = ugp.ea.vanilla_ea(frame, evaluator, max_generation=10)

    ugp.rrandom.seed(42)
    p3 = ugp.ea.vanilla_ea(frame, evaluator, max_generation=10)

    assert any(i1[1].fitness != i2[1].fitness for i1, i2 in zip(p1, p2))
    assert all(i1[1].fitness == i3[1].fitness for i1, i3 in zip(p1, p3))


def test_onemax_base_take2():
    macro = ugp.f.macro("{v}", v=ugp.f.choice_parameter("01"))
    frame = ugp.f.bunch([macro], size=(10, 100 + 1))
    evaluator = ugp.evaluator.PythonEvaluator(fitness, cook_genome=True)
    ugp.microgp_logger.setLevel(WARNING)

    ugp.rrandom.seed(42)
    p1 = ugp.ea.vanilla_ea(frame, evaluator, max_generation=10)

    p2 = ugp.ea.vanilla_ea(frame, evaluator, max_generation=10)

    ugp.rrandom.seed(42)
    p3 = ugp.ea.vanilla_ea(frame, evaluator, max_generation=10)

    assert any(i1[1].fitness != i2[1].fitness for i1, i2 in zip(p1, p2))
    assert all(i1[1].fitness == i3[1].fitness for i1, i3 in zip(p1, p3))
