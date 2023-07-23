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
import subprocess

# NOTE:
# https://www.scivision.dev/windows-symbolic-link-permission-enable/

import microgp4 as ugp


def instruction_library():
    prologue = ugp.f.macro('''
    .text
    .globl	one_max
one_max:
    pushq	%rbp
    movq	%rsp, %rbp
        ''')

    epilogue = ugp.f.macro('''
	popq	%rbp
	ret
        ''')

    op = ugp.f.macro("	movl	${val:#x}, %eax", val=ugp.f.integer_parameter(0, 2**32))

    core = ugp.framework.bunch(op, size=(10, 50 + 1))
    return ugp.framework.sequence([prologue, core, epilogue])


def main():
    ugp.microgp_logger.setLevel(logging.INFO)
    evaluator = ugp.evaluator.ScriptEvaluator('evaluate.cmd')
    top_frame = instruction_library()
    ugp.ea.vanilla_ea(top_frame, evaluator, population_extra_parameters={'_comment': '#'})


if __name__ == '__main__':
    main()
