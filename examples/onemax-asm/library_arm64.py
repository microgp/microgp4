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

    operations_rrr = ugp.f.choice_parameter(['add', 'sub', 'and', 'eon', 'eor'])
    operations_rri = ugp.f.choice_parameter(['add', 'sub'])
    op_rrr = ugp.f.macro('{op} {r1}, {r2}, {r3}', op=operations_rrr, r1=register, r2=register, r3=register)
    op_rri = ugp.f.macro('{op} {r1}, {r2}, #{imm:#x}', op=operations_rri, r1=register, r2=register, imm=int8)

    conditions = ugp.f.choice_parameter(
        ['eq', 'ne', 'cs', 'hs', 'cc', 'lo', 'mi', 'pl', 'vs', 'vc', 'hi', 'ls', 'ge', 'lt', 'gt', 'le', 'al']
    )
    branch = ugp.f.macro(
        'b{cond} {label}', cond=conditions, label=ugp.f.local_reference(backward=True, loop=False, forward=True)
    )

    prologue_main = ugp.f.macro(
        r"""; [prologue_main]
.section	__TEXT,__text,regular,pure_instructions
.globl	_onemax                         ; -- Begin function onemax
.p2align	2
_onemax:                                ; @onemax
.cfi_startproc
stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
.cfi_def_cfa_offset 16
mov x0, #{init}
mov x1, #{init}
mov x2, #{init}
mov x3, #{init}
; [end-prologue_main]""",
        init=ugp.f.integer_parameter(-15, 16),
    )

    epilogue_main = ugp.f.macro(
        r"""; [epilogue_main]
ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
ret
.cfi_endproc
; [end-epilogue_main]"""
    )

    prologue_sub = ugp.f.macro(
        r"""
; [prologue_sub]
.globl	{_node}             ; -- Begin function {_node}
.p2align	2
{_node}:
.cfi_startproc
sub	sp, sp, #16
; [end-epilogue_sub]""",
        _label='',  # No automatic creation of the label -- it's embedded as "{_node}:"
    )

    epilogue_sub = ugp.f.macro(
        r"""; [epilogue_sub]
str	x8, [sp, #8]
add	sp, sp, #16
ret
.cfi_endproc
; [end-epilogue_sub]"""
    )

    core_sub = ugp.framework.bunch(
        [op_rrr, op_rri, branch],
        size=(1, 5 + 1),
        weights=[operations_rrr.NUM_ALTERNATIVES, operations_rri.NUM_ALTERNATIVES, 1],
    )
    sub = ugp.framework.sequence([prologue_sub, core_sub, epilogue_sub])
    branch_link = ugp.f.macro("bl {label}", label=ugp.f.global_reference(sub, creative_zeal=1, first_macro=True))

    core_main = ugp.framework.bunch(
        [op_rrr, op_rri, branch, branch_link],
        size=(10, 15 + 1),
        weights=[operations_rrr.NUM_ALTERNATIVES, operations_rri.NUM_ALTERNATIVES, 1, 1],
    )
    main = ugp.framework.sequence([prologue_main, core_main, epilogue_main])

    return main
