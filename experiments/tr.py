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

#@ugp.genetic_operator(num_parents=1)
#def foo():
#    pass


@ugp.fitness_function
def onemax1(x):
    return x


@ugp.fitness_function(type_=ugp.fitness.UniformVector)
def onemax2(x):
    return x, 1, x


@ugp.genetic_operator(num_parents=1)
def foo(x):
    return x


print(f"Genetic operators: {ugp.sysinfo.genetic_operators}")
print(foo.stats)
x = foo('x')
print(f"Genetic operators: {ugp.sysinfo.genetic_operators}")
print(foo.stats)

print(onemax1(1234.2))
print(onemax1(1234.2))
print(onemax1(1234.2))

print(f"Genetic operators: {ugp.sysinfo.genetic_operators}")
print(f"Fitness functions: {ugp.sysinfo.fitness_functions}")

ugp.sysinfo.show(foo)
ugp.sysinfo.show('foo')
ugp.sysinfo.show(print)
pass

i = ugp.classes.Individual(None)
i.fitness = ugp.fitness.Scalar(3)
#i.fitness = ugp.fitness.Scalar(3)
