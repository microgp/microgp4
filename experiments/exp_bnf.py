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

ugp.rrandom.seed()
var = ugp.f.macro("{v}", v=ugp.f.choice_parameter("abcde"))
num = ugp.f.macro("{n}", n=ugp.f.integer_parameter(0, 100 + 1))
terminal = ugp.f.alternative([var, num])
open = ugp.f.macro("(")
close = ugp.f.macro(")")
operations = ugp.f.macro("{op}", op=ugp.f.choice_parameter("+-*/"))

bnf = ugp.f.bnf([[terminal], [open, ugp.f.SELF, operations, ugp.f.SELF, close]],
                extra_parameters={'_text_after_macro': ''})

SEED = 59
ugp.rrandom.seed(SEED)
P = ugp.classes.Population(top_frame=bnf, fitness_function=None)
P.add_random_individual()
print(P.dump_individual(len(P.individuals) - 1, extra_parameters={'$omit_banner': True}))

exit()

zap = list()
P = ugp.Population(top_frame=bnf, fitness_function=None)
for x in tqdm(range(10)):
    ugp.rrandom.seed(SEED)
    P.add_random_individual()
    txt = P.dump_individual(len(P.individuals) - 1,
                            extra_parameters={
                                '$dump_node_info': False,
                                '_text_after_macro': ' '
                            })
    zap.append(txt)

assert all(i == zap[0] for i in zap)

pass
