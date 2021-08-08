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
# Copyright 2020 Giovanni Squillero and Alberto Tonda
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

import warnings
from typing import Union, Set, List, Optional

from .archive import Archive
from .constraints import Constraints
from .individual import Individual
from .genetic_operators import order_by_fitness
from .operators import Operators
from .population import Population
from .utils import logging

# TODO: Check. Urgent. (fall 2020)

class Darwin:
    # TODO: Double Check
    """This class manages the evolution, stores the genetic operators, the
    population, and the archive. You can set some evolution parameters
    (`lambda, tau, nu, strength, mu`) and a list of stopping conditions.
    A `microgp.population.Population` and a `microgp.population.Archive`
    objects are also initialized.

    Args:
        constraints (Constraints): Constraints object that each individual managed by Darwin must have.
        operators (Operators): operators object that contains the set of GenOperators that will manipulate the individuals.
        mu (int): Population size.
        lambda_ (int): Number of operators to pick at each generation (except when the population is empty).
        nu (int): Number of initialization operators to pick when the population is empty. None if you want mu individuals.
        tau (float): Selection pressure. Default value: 2.0
        strength (float): Probability and strength of the mutation (to be passed to the mutation GenOperators).
        max_age (int): Maximum age that an individual in the population can have. None if you don't want to filter individuals by age.
        stopping_conditions:

    **Examples:**

    - Initialize a `Darwin`_ object:

        >>> mu = 10
        >>> nu = 20
        >>> strength = 0.2
        >>> lambda_ = 7
        >>> max_age = 10
        >>> darwin = ugp4.Darwin(
        >>>     constraints=library,
        >>>     operators=operators,
        >>>     mu=mu,
        >>>     nu=nu,
        >>>     lambda_=lambda_,
        >>>     strength=strength,
        >>>     max_age=max_age)

    - Evolve, print results (`Population`_):

        >>> darwin.evolve()
        >>> logging.bare("This is the population:")
        >>> for individual in darwin.population:
        >>>     msg = 'Printing individual ' + individual.id
        >>>     ugp4.print_individual(individual, msg=msg, plot=True)
        >>>     ugp4.logging.bare(individual.fitness)

    - Print the `Archive`_ that contains the best eve individuals

        >>> logging.bare("These are the best ever individuals:")
        >>> ugp4.print_individual(darwin.archive)
    """
    _WARN_POP_SIZE = "The population contains a number of individual lower than mu"

    def __init__(self,
                 constraints: Constraints,
                 operators: Operators,
                 mu: int,
                 lambda_: int,
                 nu: int = None,
                 tau: float = 2.0,
                 strength: float = 0.5,
                 max_age: Optional[int] = None,
                 max_generations: Optional[int] = 42,
                 stopping_conditions: Optional[list] = None) -> None:

        assert constraints, "constraints parameter can't be None"
        assert operators, "operators parameter can't be None"
        assert mu, "mu can't be None"
        assert mu > 0, "mu must be > 0"
        assert nu is None or nu > 0, "nu must be > 0 or None"
        assert lambda_ > 0, "lambda_ must be > 0"
        assert tau > 0, "tau must be > 0"
        assert 0 <= strength <= 1, "strength must be in [0, 1]"
        assert max_age is None or max_age > 0, "max_age must be > 0 or None"

        self._constraints = constraints
        self._operators = operators
        self._population = Population()
        self._archive = Archive()

        self._strength = strength
        self._max_age = max_age
        # Set population size
        self._mu = mu
        # Set initial generation population size
        self._nu = nu if nu else self._mu
        # Set the number of operators to pick for each generation
        self._lambda = lambda_
        # Set selection pressure
        self._tau = tau

        self._generation = 0
        if stopping_conditions is None:
            self._stopping_conditions = list()  # TODO: for future implementations
        else:
            self._stopping_conditions = stopping_conditions

        if max_generations:
            self._stopping_conditions.append(lambda: self.generation >= max_generations)

    @property
    def mu(self):
        return self._mu

    @property
    def lambda_(self):
        return self._lambda

    @property
    def generation(self) -> int:
        return self._generation

    def evolve(self) -> None:
        """Evolve the population until at least one of the stopping conditions
         becomes True"""
        # TODO: uncomment next line in future implementations
        # assert self._stopping_conditions and len(self._stopping_conditions) > 0, "No stopping conditions specified"

        # Continue until one or more of the stopping condition in the list is true
        # while all((not f(self) for f in self._stopping_conditions)):
        while all(not s() for s in self._stopping_conditions):
            self.do_generation()

    def do_generation(self) -> None:
        # TODO: Rewrite!
        """Perform a generation of the evolution. Pick lambda (or nu)
        operators, clean the resulting set of individuals given by the
        operators, join it to population and keep the best mu individuals"""

        # Initialize the list of individuals that compose the offspring of the current generation
        offspring = list()

        for l in range(self.lambda_):
            if len(self._population) == 0:
                # Use generation operators only
                operator = self._operators.select(max_arity=0)
            else:
                operator = self._operators.select(min_arity=1)

            # Create the list of parent individual
            parents = [self._population.select(tau=self._tau) for _ in range(operator.arity)]

            # Generate the offspring with the selected GenOperator
            temporary_offspring = operator(*parents, strength=self._strength, constraints=self._constraints)
            # TODO: Incomplete!
            assert issubclass(type(temporary_offspring),
                              list) or temporary_offspring is None, "temporary_offspring must be a list"

            # Filter the None individuals and manage the Allopatric Selection
            # [ ind1, ind2, [ ind11, ind12, ind13], [ ind21, [ ind211, ind212], ind23] ], ind4 ]
            final_offspring = self.filter_offspring(temporary_offspring)
            #from microgp.node import NodeID
            #from microgp import graph
            #o = final_offspring[0]
            #from microgp.individual import clone_individual
            #clone = clone_individual(o)
            #o2 = final_offspring[0]

            # if not final_offspring:
            #     logging.warning(f'Operator {operator.function} has not produced a valid individual')
            # elif parents:
            #     print_individual(parents[0])
            #     print_individual(final_offspring[0])

            # Update the number of successes of the selected GenOperator
            if final_offspring: # is not None: this is never None (see r. 250)
                ln = len(final_offspring)
                offspring += final_offspring
            else:
                ln = 0
            operator.update_successes(ln)

            # Update stats and join offspring to population (if valid)
            # offspring = self.update_stats_and_offspring(operator, temporary_offspring)
            # offspring += offspring

        # if len(self._population) == 0:
        #     print_individual(offspring)

        # Add the offspring to the population
        self._population += set(offspring)

        # Remove some individuals based on, for instance, their age, whether or not they are clones, etc.
        self._population.filter_by_age(max_age=self._max_age)
        self._population.filter_clones()

        # Keep in the population the best mu (or less) individuals
        self.keep_at_most_mu()

        # Insert in archive the best individuals (and remove the no more good enough individuals)
        self.update_archive()

        # Increment the age of the individuals in the population (and not in archive)
        if self._max_age is not None:
            self._population.grow_old(self._population - self.archive.individuals)
        self._generation += 1


    def filter_offspring(self, temporary_offspring: Optional[List[Optional[Individual]]]) \
            -> Optional[List[Optional[Individual]]]:
        """Remove "None" elements and choose the best element in sublist recursively

        Args:
            temporary_offspring: the list of individuals to just generated by the operator

        Returns:
            List of valid individuals
        """
        if temporary_offspring is None:
            return None
        filtered_offspring = list()
        for individual in temporary_offspring:
            if issubclass(type(individual), list):
                individual = self.get_best_unpacking(individual)
            if individual is not None and individual.valid:
                filtered_offspring += [individual]
        return filtered_offspring

    def get_best_unpacking(self, individuals: list) -> Optional[Individual]:
        """Find the best value in the given list (recursive)"""
        temp = list()
        for individual in individuals:
            if issubclass(type(individual), list):
                temp += self.get_best_unpacking(individual)
            elif individual is not None and individual.valid:
                temp += individual
        if len(temp) > 0:
            return order_by_fitness(temp)[0]
        else:
            return None

    def keep_at_most_mu(self) -> None:
        """Keep in the population at most mu individuals removing the worst"""
        # If there are too many individuals in the population -> keep only the best mu individuals
        mu = len(self._population)
        if len(self._population) < self.mu:
            warnings.warn(self._WARN_POP_SIZE, RuntimeWarning)
        ordered_individuals = order_by_fitness(self._population.individuals)
        self._population._individuals = set(ordered_individuals[:self.mu])

    def update_archive(self) -> None:
        """Insert in archive the best individuals (and remove the no more good enough individuals)"""
        for individual in self._population.individuals:
            self._archive += individual

    @property
    def population(self) -> Set[Individual]:
        return self._population.individuals

    @property
    def archive(self) -> Archive:
        return self._archive
