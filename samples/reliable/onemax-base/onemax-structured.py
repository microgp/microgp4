# -*- coding: utf-8 -*-
#############################################################################
#          __________                                                       #
#   __  __/ ____/ __ \__ __   This file is part of MicroGP4 v1.0 "Kiwi"     #
#  / / / / / __/ /_/ / // /   (!) by Giovanni Squillero and Alberto Tonda   #
# / /_/ / /_/ / ____/ // /_   https://github.com/squillero/microgp4         #
# \__  /\____/_/   /__  __/                                                 #
#   /_/ --MicroGP4-- /_/      "You don't need a big goal, be μ-ambitious!!" #
#                                                                           #
#############################################################################

# Copyright 2020-2021 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import sys

import microgp as ugp4

if __name__ == "__main__":
    ugp4.show_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase log verbosity")
    parser.add_argument("-d",
                        "--debug",
                        action="store_const",
                        dest="verbose",
                        const=2,
                        help="log debug messages (same as -vv)")
    args = parser.parse_args()
    if args.verbose == 0:
        microgp.utils.logging.DefaultLogger.setLevel(level=microgp.utils.logging.INFO)
    elif args.verbose == 1:
        microgp.utils.logging.DefaultLogger.setLevel(level=microgp.utils.logging.VERBOSE)
    elif args.verbose > 1:
        microgp.utils.logging.DefaultLogger.setLevel(level=microgp.utils.logging.DEBUG)
        microgp.utils.logging.debug("Verbose level set to DEBUG")
    microgp.utils.logging.log_cpu(microgp.utils.logging.INFO, "Program started")

    # Define a parameter of type ugp4.parameter.Categorical that can take two values: 0 or 1
    bit = ugp4.make_parameter(ugp4.parameter.Categorical, alternatives=[0, 1])

    # Define a macro that contains a parameter of type ugp4.parameter.Categorical
    word_macro = ugp4.Macro("{bit}", {'bit': bit})

    # Create a section containing 8 macros
    word_section = ugp4.make_section(word_macro, size=(32, 32), name='word_sec')

    # Create a constraints library
    library = ugp4.Constraints()
    library['main'] = [word_section]

    library.evaluator = ugp4.fitness.make_evaluator(evaluator=lambda s: s.count('1'), fitness_type=ugp4.fitness.Simple)

    # Create a list of operators with their arity
    operators = ugp4.Operators()
    # Add initialization operators
    operators += ugp4.GenOperator(ugp4.create_random_individual, 0)
    # Add mutation operators
    operators += ugp4.GenOperator(ugp4.hierarchical_mutation, 1)
    operators += ugp4.GenOperator(ugp4.flat_mutation, 1)
    # Add crossover operators
    operators += ugp4.GenOperator(ugp4.macro_pool_one_cut_point_crossover, 2)
    operators += ugp4.GenOperator(ugp4.macro_pool_uniform_crossover, 2)

    # Create the object that will manage the evolution
    mu = 10
    nu = 20
    strength = 0.7
    lambda_ = 7
    max_age = 10

    darwin = ugp4.Darwin(constraints=library,
                         operators=operators,
                         mu=mu,
                         nu=nu,
                         lambda_=lambda_,
                         strength=strength,
                         max_age=max_age,
                         max_generations=10)
    darwin.evolve()

    # That's all
    microgp.utils.logging.bare("Final archive:")
    for i in darwin.archive.individuals:
        ind = f"{i}".replace("\n", "-")
        microgp.utils.logging.bare(f"{i.id}: {ind} [{i.fitness}]")

    microgp.utils.logging.log_cpu(microgp.utils.logging.INFO, "Program completed")
    sys.exit(0)
