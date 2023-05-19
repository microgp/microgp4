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

try:
    import microgp4 as ugp
except ModuleNotFoundError as e:
    import sys, os
    sys.path.extend(['..', '../..'])
    import microgp4 as ugp


def main():
    register = ugp.f.choice_parameter([f'x{n}' for n in range(4)])
    int8 = ugp.f.integer_parameter(0, 2**8)
    int16 = ugp.f.integer_parameter(0, 2**16)

    operations_rr = ugp.f.choice_parameter(['add', 'adc', 'sub', 'sbc', 'mul'])
    operations_ri = ugp.f.choice_parameter(['add', 'sub'])
    op_rr = ugp.f.macro('{op} {r1}, {r2}, {r3}', op=operations_rr, r1=register, r2=register, r3=register)
    op_ri = ugp.f.macro('{op} {r1}, {r2}, #{imm:#x}', op=operations_ri, r1=register, r2=register, imm=int8)

    conditions = ugp.f.choice_parameter(
        ['eq', 'ne', 'cs', 'hs', 'cc', 'lo', 'mi', 'pl', 'vs', 'vc', 'hi', 'ls', 'ge', 'lt', 'gt', 'le', 'al'])
    branch = ugp.f.macro('b{cond} {label}', cond=conditions, label=ugp.f.local_reference(backward=False, loop=False))

    prologue = ugp.f.macro('''; prologue
.section	__TEXT,__text,regular,pure_instructions
.globl	_one_max    ; function one_max
.p2align	2
_one_max:
.cfi_startproc''')

    epilogue = ugp.f.macro('''; epilogue
ret
.cfi_endproc''')

    init = ugp.f.macro('''; initialization
mov x0, #{v0:#x}
mov x1, #{v1:#x}
mov x2, #{v2:#x}
mov x3, #{v3:#x}''',
                       v0=int16,
                       v1=int16,
                       v2=int16,
                       v3=int16)

    core = ugp.framework.bunch([op_rr, op_ri, branch], size=(10, 50 + 1))
    program = ugp.framework.sequence([prologue, init, core, epilogue])
    #program = ugp.framework.sequence([prologue, init, core, epilogue])

    population = ugp.classes.Population(top_frame=program, fitness_function=None)
    population.add_random_individual()

    #code = population.dump_individual(0)
    code = population.dump_individual(0, {'$dump_node_info': 1})
    with open('one_max.s', 'w') as src:
        src.write(code)

    pass


if __name__ == '__main__':
    ugp.rrandom.seed(42)
    #ugp.set_logger_level(logging.INFO)
    main()
