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

ugp.builtins.SELF

m1 = ugp.macro("macro1")
m2 = ugp.macro("macro2")
m3 = ugp.macro("macro3")
f1 = ugp.framework.sequence([m1, m1], extra_parameters={'_comment': '@'})
f2 = ugp.framework.sequence([m2, m2], extra_parameters={'_comment': '#'})
f3 = ugp.framework.sequence([m1, m2, m3])
pf1 = ugp.framework.sequence([f1, f2, f3])
pf2 = ugp.framework.sequence([f2, f1, f3], extra_parameters={'_comment': '$'})
pf3 = ugp.framework.sequence([f1, f2, f3])

tot = ugp.framework.sequence([pf1, pf2, pf3])

P = ugp.Population(top_frame=tot, fitness_function=None)
P.add_random_individual()
text = P.dump_individual(0, extra_parameters={'$dump_node_info': True})
print(text)
