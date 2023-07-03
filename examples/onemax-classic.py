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


# explicit: @ugp.fitness_function(type_=ugp.fitness.Integer)
@ugp.fitness_function
def fitness(genotype: str):
    """Vanilla 1-max"""
    return sum(b == '1' for b in genotype)


def main():
    ugp.microgp_logger.setLevel(logging.DEBUG)

    macro = ugp.f.macro("{v}", v=ugp.f.array_parameter("01", 100))
    frame = ugp.f.sequence([macro])

    evaluator = ugp.evaluator.PythonFunction(fitness, strip_genome=True)
    population = ugp.ea.vanilla_ea(frame, evaluator)

    for i in population:
        print(i.describe(include_structure=False, max_recursion=99))


if __name__ == '__main__':
    main()
