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

NUM_BITS = 100


# explicit: @ugp.fitness_function(type_=ugp.fitness.Integer)
@ugp.fitness_function
def fitness(genotype: str):
    """Vanilla 1-max"""
    return sum(b == '1' for b in genotype)


def single_array_parameter():
    macro = ugp.f.macro("{v}", v=ugp.f.array_parameter("01", NUM_BITS + 1))
    frame = ugp.f.sequence([macro])
    return frame


def multiple_distinct_bits():
    macro = ugp.f.macro("{v}", v=ugp.f.choice_parameter("01"))
    frame = ugp.f.bunch([macro], size=(NUM_BITS, NUM_BITS + 1))
    return frame


def main():
    ugp.microgp_logger.setLevel(logging.INFO)

    top_frame = multiple_distinct_bits()
    evaluator = ugp.evaluator.PythonFunction(fitness, strip_genome=True)
    population = ugp.ea.vanilla_ea(top_frame, evaluator, max_generation=10, max_fitness=fitness('1' * NUM_BITS))

    for i in population:
        print(i.describe(max_recursion=99))


if __name__ == '__main__':
    main()
