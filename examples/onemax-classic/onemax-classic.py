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
import microgp4 as ugp

NUM_BITS = 50


@ugp.fitness_function
def fitness(genotype: str):
    """Vanilla 1-max"""
    return sum(b == '1' for b in genotype)


def main():
    ugp.microgp_logger.setLevel(logging.INFO)

    macro = ugp.f.macro('{v}', v=ugp.f.array_parameter('01', NUM_BITS + 1))
    top_frame = ugp.f.sequence([macro])

    # evaluator = ugp.evaluator.PythonEvaluator(fitness, cook_genome=True, backend=None)
    # evaluator = ugp.evaluator.PythonEvaluator(fitness, cook_genome=True, backend='thread_pool')
    # evaluator = ugp.evaluator.PythonEvaluator(fitness, cook_genome=True, backend='joblib')
    # evaluator = ugp.evaluator.ScriptEvaluator('./onemax-shell.sh', args=['-f'])
    evaluator = ugp.evaluator.MakefileEvaluator('genome.dat', required_files=['onemax-shell.sh'])

    population = ugp.ea.vanilla_ea(top_frame, evaluator, max_generation=1_000, lambda_=20, mu=30)


if __name__ == "__main__":
    main()
