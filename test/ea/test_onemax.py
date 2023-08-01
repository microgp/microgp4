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
    return sum(b == '1' for b in genotype)


def test_onemax():
    ugp.microgp_logger.setLevel(WARNING)
    macro = ugp.f.macro('{v}', v=ugp.f.array_parameter('01', 50))
    frame = ugp.f.sequence([macro])

    # sequential evaluator
    evaluator = ugp.evaluator.PythonEvaluator(fitness, strip_phenotypes=True)

    # seed 42
    ugp.rrandom.seed(42)
    reference_population = ugp.ea.vanilla_ea(frame, evaluator, mu=10, max_generation=10)

    # seed not 42 (result should be !=)
    other_population = ugp.ea.vanilla_ea(frame, evaluator, mu=10, max_generation=10)
    assert any(r[1].fitness != o[1].fitness for r, o in zip(reference_population, other_population))

    # seed 42 again (result should be ==)
    ugp.rrandom.seed(42)
    other_population = ugp.ea.vanilla_ea(frame, evaluator, mu=10, max_generation=10)
    assert all(r[1].fitness == o[1].fitness for r, o in zip(reference_population, other_population))

    # multi-thread parallel evaluator & seed 42 (result should be ==)
    evaluator = ugp.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, max_jobs=None, backend='thread_pool')
    ugp.rrandom.seed(42)
    other_population = ugp.ea.vanilla_ea(frame, evaluator, mu=10, max_generation=10)
    assert all(r[1].fitness == o[1].fitness for r, o in zip(reference_population, other_population))

    # multi-process parallel evaluator & seed 42 (result should be ==)
    evaluator = ugp.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, max_jobs=None, backend='joblib')
    ugp.rrandom.seed(42)
    other_population = ugp.ea.vanilla_ea(frame, evaluator, mu=10, max_generation=10)
    assert all(r[1].fitness == o[1].fitness for r, o in zip(reference_population, other_population))
