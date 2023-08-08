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
import platform
import argparse

import microgp4 as ugp

if platform.machine() == "arm64":
    import library_arm64 as library
else:
    raise NotImplementedError(f"Unknown machine type: {platform.machine()}")


SCRIPT_NAME = {"Linux": "./evaluate-all.sh", "Darwin": "./evaluate-all.sh", "Windows": "evaluate-all.cmd"}


def main():
    top_frame = library.define_frame()

    evaluator = ugp.evaluator.ScriptEvaluator(SCRIPT_NAME[platform.system()], filename_format="ind{i:06}.s")
    # evaluator = ugp.evaluator.MakefileEvaluator('onemax.s', required_files=['main.o'], timeout=5)
    population = ugp.ea.vanilla_ea(
        top_frame,
        evaluator,
        max_generation=100,
        max_fitness=ugp.fitness.make_fitness(5.0),
        population_extra_parameters={"_comment": library.COMMENT, '$dump_node_info': True},
    )

    with open('best-individual.s', 'w') as out:
        out.write(population.dump_individual(0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase log verbosity')
    parser.add_argument(
        '-d', '--debug', action='store_const', dest='verbose', const=2, help='log debug messages (same as -vv)'
    )
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
        ugp.logger.setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
        ugp.logger.setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)
        ugp.logger.setLevel(level=logging.DEBUG)

    main()
