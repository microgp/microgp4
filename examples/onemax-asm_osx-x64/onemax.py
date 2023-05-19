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

from itertools import chain
from copy import deepcopy
from subprocess import Popen, PIPE

import microgp4 as ugp


def prepare_frames():
    register = ugp.f.choice_parameter(['%rax', '%rbx', '%rcx', '%rdx'])
    int8 = ugp.f.integer_parameter(0, 2**8)
    int16 = ugp.f.integer_parameter(0, 2**16)
    int32 = ugp.f.integer_parameter(0, 2**32)
    int64 = ugp.f.integer_parameter(0, 2**64)

    opcode = ugp.f.choice_parameter(['addq', 'subq', 'andq', 'orq', 'xorq'])
    inst_rr = ugp.f.macro('{op} {r1}, {r2}', op=opcode, r1=register, r2=register)
    inst_ri = ugp.f.macro('{op} ${i:#x}, {r}', op=opcode, i=int16, r=register)

    cond = ugp.f.choice_parameter(['z', 'nz'])
    ref = ugp.f.local_reference(backward=False, loop=False, forward=True)
    branch = ugp.f.macro('j{c} {t}', c=cond, t=ref)

    prologue = ugp.f.macro(r'''
.globl _one_max ## -- Begin function one_max
_one_max:
push %rbx
push %rcx
push %rdx
pushq %rbp
movq %rsp, %rbp
movq ${init:#x}, %rax
movq ${init:#x}, %rbx
movq ${init:#x}, %rcx
movq ${init:#x}, %rdx
addq $0, %rax
''',
                           init=int64)

    epilogue = ugp.f.macro('''
popq %rbp
pop %rdx
pop %rcx
pop %rbx
retq
''')

    main_body = ugp.f.bunch([inst_rr, inst_ri, branch], size=(10, 101))
    program = ugp.f.sequence([prologue, main_body, epilogue])

    return program


def evaluate(txt):
    with open('onemax.s', 'w') as fout:
        fout.write(txt)

    process = Popen(['make', '-s'], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    #ugp.microgp_logger.debug(f"eval: out=%s / err=%s / exit_code=%s", output, err, exit_code)
    return int(output)


def main():

    top_frame = prepare_frames()

    population = ugp.classes.Population(top_frame, None, extra_parameters={'_comment': '#'})
    population.add_random_individual()
    txt = population.dump_individual(-1)
    old_value = evaluate(txt)
    print(f"Initial fitness: {old_value}")

    for n in range(1000):
        I = deepcopy(population.individuals[-1])
        params = list(
            chain.from_iterable(I.G.nodes[n]['_macro'].parameters.values() for n in I.G if '_macro' in I.G.nodes[n]))
        p = ugp.rrandom.choice(params)
        p.mutate(1)
        population.individuals.append(I)
        txt = population.dump_individual(-1)
        new_value = evaluate(txt)
        print(f"New fitness {n} => {new_value}")
        if new_value > old_value:
            old_value = new_value
        elif new_value < old_value:
            print("Popping")
            population.individuals.pop()
        if new_value == 64:
            break

    with open('solution.s', 'w') as fout:
        fout.write(population.dump_individual(-1))
    population.individuals[-1].as_lgp(figsize=(20, 50), filename='soluzion.png', bbox_inches='tight')


if __name__ == '__main__':
    ugp.rrandom.seed(42)
    #ugp.set_logger_level(logging.INFO)
    main()
