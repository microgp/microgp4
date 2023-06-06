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


@ugp.fitness_function
def fitness(individual: str):
    """xxx"""
    string = individual.split('\n')[1]
    return sum(b == '1' for b in string)


def main():
    macro = ugp.f.macro("{v}", v=ugp.f.array_parameter("01", 16))
    frame = ugp.f.sequence([macro])

    evaluator = ugp.eval.PythonFunction(fitness)
    population = ugp.C.Population(frame, evaluator)

    population.add_random_individual()
    population.add_random_individual()
    population.add_random_individual()
    population.evaluate()
    pass


if __name__ == '__main__':

    from pprint import pprint
    main()
