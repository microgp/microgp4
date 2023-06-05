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

#print(ugp.GLOBAL_REGISTER[foo])
for x in ugp.GLOBAL_REGISTER.operators:
    print(x, ugp.GLOBAL_REGISTER.operators[x])
x = foo('x')
print(x)
for x in ugp.GLOBAL_REGISTER.operators:
    print(x, ugp.GLOBAL_REGISTER.operators[x])

print(onemax1(1234.2))
print(onemax1(1234.2))
print(onemax1(1234.2))

from pprint import pprint

#print(ugp.GLOBAL_REGISTER[onemax2]['log'])

from microgp4.sysinfo import *
x = SysInfo()


o = x.operators
print(f"Genetic operators: {o}")

pass