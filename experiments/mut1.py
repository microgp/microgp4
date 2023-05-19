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

#ugp.rrandom.seed(42)

register = ugp.f.choice_parameter(['ah', 'bh', 'ch', 'dh', 'al', 'bl', 'cl', 'dl'])
word = ugp.f.integer_parameter(0, 2**16)
int_op = ugp.f.choice_parameter(['add', 'sub', 'and', 'or', 'xor'])
inst = ugp.f.macro('{op} {r}, 0x{v:02x}', op=int_op, r=register, v=word)

call = ugp.f.macro('call {sub}', sub=ugp.f.global_reference('Wazoo', first_macro=True, creative_zeal=1))

vanilla = ugp.f.bunch([inst, inst, call], size=(1, 6))
entry_point = ugp.f.macro('\nproc {_node} NEAR:', _label='')
proc = ugp.f.sequence([entry_point, vanilla, 'ret'], name='Wazoo')

#call = ugp.f.macro('call {sub}', sub=ugp.f.integer_parameter(0, 256))
body = ugp.f.bunch([inst, inst, inst, call], size=10)

#prologue = ugp.f.bunch(ugp.f.macro('{_comment} PROLOGUE (node {_node.pathname})'))
#epilogue = ugp.f.bunch([ugp.f.macro('{_comment} EPILOGUE (node {_node.pathname})')])

program = ugp.f.sequence([body])

population = ugp.classes.population.Population(top_frame=program, fitness_function=None)
population.add_random_individual()

print(population.dump_individual(0, {'$dump_node_info': True}))
I = population.individuals[0]
I.as_forest(filename='grammar-tree.png', figsize=(25, 15), bbox_inches='tight')
I.as_lgp(filename='code.png', figsize=(25, 15), bbox_inches='tight')

pass
