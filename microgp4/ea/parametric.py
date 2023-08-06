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

# =[ HISTORY ]===============================================================
# v1 / July 2023 / Sacchet (MS)

__all__ = ["parametric_ea"]

from microgp4.operators import *
from microgp4.sys import *
from microgp4.classes.selement import *
from microgp4.classes.population import *
from microgp4.classes.frame import *
from microgp4.classes.evaluator import *
from microgp4.randy import rrandom
from microgp4.user_messages import *

from .selection import *


def _new_best(population: Population, evaluator: EvaluatorABC):
    microgp_logger.info(
        f"ParametricEA: 🍀 {population[0].describe(include_fitness=True, include_structure=False, include_birth=False)}"
        + f" [🕓 gen: {population.generation:,} / fcalls: {evaluator.fitness_calls:,}]")


def parametric_ea(top_frame: type[FrameABC],
                  evaluator: EvaluatorABC,
                  mu: int = 10,
                  lambda_: int = 20,
                  max_generation: int = 100,
                  max_fitness: FitnessABC | None = None,
                  top_n: int = 0,
                  lifespan: int = None,
                  operators: list[Callable] = None,
                  end_conditions: list[Callable] = None,
                  alpha: int = 10) -> Population:

    r"""A configurable evolutionary algorithm

    Parameters
    ----------
    top_frame
        The top_frame of individuals
    evaluator
        The evaluator used to evaluate individuals
    mu
        The size of the population
    lambda_
        The size the offspring
    top_n
        The size of champions population
    lifespan
        The number of generation an individual survive
    operators
        Which operetors you want to use
    alpha
        Parameter to reduce early failure penalty for operators
    Returns
    -------
    Population
        The last population
    """

    def take_operators(init: bool, operators_list: list[Callable]) -> list[Callable]:
        if operators_list is None or (flag := all((op.num_parents is not None) != init for op in operators_list)):
            ops = [op for op in get_operators() if (op.num_parents is None) == init]
        elif not flag:
            ops = [op for op in operators_list if (op.num_parents is None) == init]
        return ops

    def extimate_operator_probability(operators_list: list[Callable], iterations: int, alpha: int) -> list[float]:
        p0 = 1 / len(operators_list)
        if iterations <= alpha * len(operators_list):
            # list of equal probability for every operator
            return [p0] * len(operators_list)

        p_temp = list()
        delta_nomr = 0
        for op in operators_list:
            # penalty for the operator, normalized with number of iterations
            delta_p = (op.stats.aborts / op.stats.calls) * (1 / iterations)
            p_temp.append(delta_p)
            # to have sum(p) = 1 I need to add to all other probabilities how much I subtract from one
            delta_nomr += delta_p / (len(operators_list) - 1)
        # probability for every operator is equal to the starting probability minus the penalty plus the adding from every penalty minus the contribution from it's own penalty
        return [p0 - p + (delta_nomr - (p / (len(operators_list) - 1))) for p in p_temp]

    if end_conditions:
        stopping_conditions = end_conditions
    else:
        stopping_conditions = list()
        stopping_conditions.append(lambda: population.generation >= max_generation)
    if max_fitness:
        stopping_conditions.append(lambda: best.fitness == max_fitness or best.fitness >> max_fitness)

    # initialize population
    population = Population(top_frame)
    ops0 = take_operators(True, operators)

    gen0 = list()
    while len(gen0) < mu:
        o = rrandom.choice(ops0)
        gen0 += o(top_frame=top_frame)
    population += gen0
    evaluator(population)
    population.sort()
    best = population[0]
    _new_best(population, evaluator)

    all_individuals = set()
    ops = take_operators(False, operators)

    # begin evolution!
    count = 0
    while not any(s() for s in stopping_conditions):
        new_individuals = list()
        for step in range(lambda_):
            count += 1
            p = extimate_operator_probability(ops, count, alpha)
            op = rrandom.weighted_choice(ops, p)
            parents = list()
            for _ in range(op.num_parents):
                parents.append(tournament_selection(population, 1))
            new_individuals += op(*parents)

        population.aging()
        old = [i for i in population.individuals[top_n:] if i.age > lifespan]
        population -= old
        population += new_individuals

        evaluator(population)
        population.sort()

        all_individuals |= set(population)

        population.individuals[mu:] = []

        if best.fitness << population[0].fitness:
            best = population[0]
            _new_best(population, evaluator)

    microgp_logger.info("ParametricEA: Genetic operators statistics:")
    for op in get_operators():
        microgp_logger.info(f"ParametricEA: * {op.__qualname__}: {op.stats}")
    return population
