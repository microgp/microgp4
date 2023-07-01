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


class MyFitness(ugp.classes.FitnessABC):

    def __init__(self, value):
        self.value = value

    def calculate(self, individual):
        pass

    @classmethod
    def is_fitter(cls, fitness1, fitness2):
        pass


def test_fitness_function():

    @ugp.decorators.fitness_function(MyFitness)
    def my_fitness_function():
        return MyFitness(42)

    fitness_object = my_fitness_function()

    assert isinstance(fitness_object, MyFitness)
