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

print(ugp.fit.Scalar(2))
print(ugp.fit.Integer(2))
print(ugp.fit.Float(2))
print(ugp.fit.reverse_fitness(ugp.fit.Scalar)(2))
print(ugp.fit.reverse_fitness(ugp.fit.Integer)(2))
print(ugp.fit.reverse_fitness(ugp.fit.Float)(2))

print(
    ugp.fit.Vector([
        ugp.fit.reverse_fitness(ugp.fit.Scalar)(2),
        ugp.fit.reverse_fitness(ugp.fit.Integer)(2),
        ugp.fit.reverse_fitness(ugp.fit.Float)(2)
    ]))

print(
    ugp.fit.reverse_fitness(ugp.fit.Vector)([
        ugp.fit.reverse_fitness(ugp.fit.Scalar)(2),
        ugp.fit.reverse_fitness(ugp.fit.Integer)(2),
        ugp.fit.reverse_fitness(ugp.fit.Float)(2)
    ]))
