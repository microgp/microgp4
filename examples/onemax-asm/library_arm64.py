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

COMMENT = ';'

# Hacked as a blind monkey using <https://godbolt.org/>


def define_frame():
    register = ugp.f.choice_parameter([f"x{n}" for n in range(4)])
    int8 = ugp.f.integer_parameter(0, 2**8)
    int16 = ugp.f.integer_parameter(0, 2**16)

    operations_rr = ugp.f.choice_parameter(["add", "adc", "sub", "sbc", "mul"])
    operations_ri = ugp.f.choice_parameter(["add", "sub"])
    op_rr = ugp.f.macro("{op} {r1}, {r2}, {r3}", op=operations_rr, r1=register, r2=register, r3=register)
    op_ri = ugp.f.macro("{op} {r1}, {r2}, #{imm:#x}", op=operations_ri, r1=register, r2=register, imm=int8)

    conditions = ugp.f.choice_parameter(
        ["eq", "ne", "cs", "hs", "cc", "lo", "mi", "pl", "vs", "vc", "hi", "ls", "ge", "lt", "gt", "le", "al"]
    )
    branch = ugp.f.macro("b{cond} {label}", cond=conditions, label=ugp.f.local_reference(backward=False, loop=False))

    prologue = ugp.f.macro(
        r"""; [prologue]
.globl _one_max ; -- Begin function one_max
.p2align 2
_one_max:       ; @one_max
sub sp, sp, #16
str x0, [sp, #8]
mov x1, #{init}
mov x2, #{init}
mov x3, #{init}
; [end prologue]""",
        init=ugp.f.integer_parameter(-7, 8),
    )

    epilogue = ugp.f.macro(
        r"""; [epilogue]
ldr x8, [sp, #8]
add sp, sp, #16
ret"""
    )

    core = ugp.framework.bunch([op_rr, op_ri, branch], size=(10, 50 + 1))
    program = ugp.framework.sequence([prologue, core, epilogue])
    return program
