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


@ugp.fitness_function
def fitness(genotype: str):
    """Vanilla 1-max"""
    return sum(b == "1" for b in genotype)


def single_array_parameter():
    macro = ugp.f.macro("{v}", v=ugp.f.array_parameter("01", NUM_BITS + 1))
    frame = ugp.f.sequence([macro])
    return frame


def multiple_distinct_bits():
    macro = ugp.f.macro("{v}", v=ugp.f.choice_parameter("01"))
    frame = ugp.f.bunch([macro], size=(1, NUM_BITS + 1))
    # frame.add_node_check(lambda n: n.framework_out_degree % 2 == 0)
    return frame


def multiple_frames():
    macro = ugp.f.macro("{v}", v=ugp.f.choice_parameter("01"))
    link = ugp.f.macro(
        "[{_node}]=>[{l}]", l=ugp.f.global_reference(target_frame="blues", first_macro=True, creative_zeal=0.01)
    )
    frame = ugp.f.bunch([macro, link], size=(NUM_BITS // 10 // 10, NUM_BITS // 10 + 1), name="blues")
    return frame


def main():
    ugp.microgp_logger.setLevel(logging.INFO)

    top_frame = multiple_distinct_bits()
    evaluator = ugp.evaluator.PythonEvaluator(fitness, cook_genome=True)
    population = ugp.ea.vanilla_ea(top_frame, evaluator, max_generation=1, max_fitness=fitness("1" * NUM_BITS))

    population[0].as_forest(filename="forest.svg")
    population[0].as_lgp(filename="lgp.svg", zoom=1.0)
    with open("ind0.lst", "w") as out:
        out.write(population.dump_individual(0, {"$dump_node_info": True}))

    for _, i in population:
        print(i.describe(max_recursion=99))


if __name__ == "__main__":
    main()
