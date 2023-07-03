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

import logging
from copy import deepcopy

try:
    import microgp4 as ugp
except ModuleNotFoundError as e:
    import sys, os
    sys.path.append(os.curdir)
    sys.path.append(os.pardir)
    import microgp4 as ugp

#ugp.set_logger_level(logging.INFO)

ugp.microgp_logger.setLevel(logging.DEBUG)
ugp.rrandom.seed(42)

register = ugp.f.choice_parameter(['ah', 'bh', 'ch', 'dh', 'al', 'bl', 'cl', 'dl'])
byte = ugp.f.integer_parameter(0, 2**8)
#test_10 = ugp.f.integer_parameter(1, 10)
#test_byte = ugp.f.integer_parameter(0, 255)
#test_byte = ugp.f.integer_parameter(2, 65536 + 1)
#test_byte = ugp.f.integer_parameter(1, 2**32)
#test_bool = ugp.f.integer_parameter(1, 2)
#register = register()
#byte = byte()
add = ugp.f.macro('add {r}, 0x{v:02x} {_comment} ie. {_node} adds {v} to register {r}', r=register, v=byte)
sub = ugp.f.macro('sub {r}, 0x{v:02x} {_comment} ie. {_node} subtracts {v} from register {r}', r=register, v=byte)
code_up = ugp.f.bunch([add, sub], size=(1, 4))
code_down = ugp.f.bunch([add, sub], size=(1, 4))

zap = ugp.f.sequence([(code_up, 2), (code_down, 3)])
pass

# REFERENCES
local_ref = ugp.f.local_reference(backward=True, loop=False, forward=True)
jmp = ugp.f.macro('branch {target}', target=local_ref)
test_jmp = ugp.f.bunch(jmp, size=(2, 4))

global_ref = ugp.f.global_reference('Program')
call = ugp.f.macro('jmp {target}', target=global_ref)
test_call = ugp.f.bunch(call, size=5)
mycode = ugp.f.sequence([code_up, test_call, code_down], name='MyCode')

prologue = ugp.f.bunch(ugp.f.macro('{_comment} PROLOGUE (node {_node.pathname})'))
epilogue = ugp.f.bunch([ugp.f.macro('{_comment} EPILOGUE (node {_node.pathname})')])

program = ugp.f.sequence([prologue, test_call, mycode, test_call, epilogue], name='Program')
#program = ugp.f.sequence([prologue, test_jmp, test_call, test_jmp, epilogue])

#program.add_check(lambda node: node.successors[1].framework_out_degree == node.successors[2].framework_out_degree)
#code_up.add_check(
#    lambda node: all(node.successors[i].macro.v < node.successors[i + 1].macro.v for i in range(node.out_degree - 1)))
#code_down.add_check(
#    lambda node: all(node.successors[i].macro.v > node.successors[i + 1].macro.v for i in range(node.out_degree - 1)))

population = ugp.classes.population.Population(top_frame=program)
population += ugp.operators.random_individual(program)
#population.individuals.clear()
#opulation.add_random_individual()

population.individuals.append(deepcopy(population.individuals[0]))
I0 = population.individuals[0]
I1 = population.individuals[1]

I0.as_forest(filename='structure-tree', figsize=(25, 15), bbox_inches='tight')
I0.as_lgp(filename='code.png', figsize=(25, 15), bbox_inches='tight')

ugp.rrandom.seed()
print(I0 == I1)
I1.G.nodes[19]['_macro'].parameters['target'].mutate(1)
print(I0 == I1)

with open('p0.s', 'w') as F:
    F.write(population.dump_individual(0, {'$dump_node_info': True}))
with open('p1.s', 'w') as F:
    F.write(population.dump_individual(1, {'$dump_node_info': True}))

pass
