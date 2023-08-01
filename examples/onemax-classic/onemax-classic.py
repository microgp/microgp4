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
import itertools

import microgp4 as ugp

NUM_BITS = 100


@ugp.fitness_function
def fitness(genotype):
    """Vanilla 1-max"""
    return sum(b == '1' for b in genotype)


def main():
    ugp.microgp_logger.setLevel(logging.INFO)

    macro = ugp.f.macro('{v}', v=ugp.f.array_parameter('01', NUM_BITS + 1))
    top_frame = ugp.f.sequence([macro])

    evaluators = list()
    evaluators.append(ugp.evaluator.PythonEvaluator(fitness, strip_phenotypes=True))
    evaluators.append(ugp.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='thread_pool'))
    evaluators.append(ugp.evaluator.PythonEvaluator(fitness, strip_phenotypes=True, backend='joblib'))
    evaluators.append(ugp.evaluator.ScriptEvaluator('./onemax-shell.sh', args=['-f']))
    evaluators.append(ugp.evaluator.MakefileEvaluator('genome.dat', required_files=['onemax-shell.sh']))

    populations = list()
    for e in evaluators:
        ugp.rrandom.seed(42)
        ugp.logger.info("main: Using %s", e)
        populations.append(ugp.ea.vanilla_ea(top_frame, e, max_generation=1000, lambda_=200, mu=300))
        pass

    for p1, p2 in itertools.combinations(populations, 2):
        for i1, i2 in zip(populations[0], populations[1]):
            assert i1[1].fitness == i2[1].fitness, f"Mismatch! {i1[1]} vs. {i2[1]}"
    ugp.logger.info("main: Results are identitcal!")


if __name__ == "__main__":
    main()
