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

byte = ugp.f.integer_parameter(0, 256)
reg = ugp.f.choice_parameter(["ax", "bx", "cx"])
macro1 = ugp.f.macro("{reg} = {val:#x}  ; hey {reg}", reg=reg, val=byte)
macro2 = ugp.f.macro("jmp {target}", target=ugp.f.local_reference(backward=False, loop=False))
sub = ugp.f.bunch([macro1], size=(5, 11), name="xxx")
macro3 = ugp.f.macro("call {target}", target=ugp.f.global_reference("xxx"))
prog = ugp.f.bunch([macro1, macro2, macro3], size=20)
pop = ugp.classes.Population(prog, None)
pop.add_random_individual()
pop.individuals[0]
