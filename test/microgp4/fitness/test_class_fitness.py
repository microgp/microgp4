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

import pytest
import microgp4 as ugp


class ExampleFitness(ugp.classes.fitness.FitnessABC):
    def __init__(self, value: float):
        self.value = value

    def is_fitter(self, other: "ExampleFitness") -> bool:
        return self.value > other.value

    def is_dominant(self, other: "ExampleFitness") -> bool:
        return self.is_fitter(other)

    def is_distinguishable(self, other: "ExampleFitness") -> bool:
        return self.value != other.value

    def _decorate(self) -> str:
        return str(self.value)


def test_is_fitter():
    fitness1 = ExampleFitness(5.0)
    fitness2 = ExampleFitness(3.0)
    assert fitness1.is_fitter(fitness2)
    assert not fitness2.is_fitter(fitness1)


def test_is_dominant():
    fitness1 = ExampleFitness(5.0)
    fitness2 = ExampleFitness(3.0)
    assert fitness1.is_dominant(fitness2)
    assert not fitness2.is_dominant(fitness1)


def test_is_distinguishable():
    fitness1 = ExampleFitness(5.0)
    fitness2 = ExampleFitness(3.0)
    fitness3 = ExampleFitness(5.0)
    assert fitness1.is_distinguishable(fitness2)
    assert not fitness1.is_distinguishable(fitness3)


def test_decorate():
    fitness = ExampleFitness(5.0)
    assert fitness._decorate() == "5.0"


def test_reverse_fitness():
    reversed_fitness = ugp.fitness.reverse_fitness(ExampleFitness)
    reversed_fitness1 = reversed_fitness(5.0)
    reversed_fitness2 = reversed_fitness(3.0)

    assert reversed_fitness2.is_fitter(reversed_fitness1)
    assert not reversed_fitness1.is_fitter(reversed_fitness2)

    assert reversed_fitness1 != reversed_fitness2

    assert reversed_fitness1._decorate() == "ᴙ5.0"
    assert reversed_fitness2._decorate() == "ᴙ3.0"
