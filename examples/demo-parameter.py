# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#############################################################################
#           __________                                                      #
#    __  __/ ____/ __ \__ __   This file is part of MicroGP4 v4!2.0         #
#   / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer  #
#  / /_/ / /_/ / ____/ // /_   https://github.com/microgp/microgp4          #
#  \__  /\____/_/   /__  __/                                                #
#    /_/ --MicroGP4-- /_/      You don't need a big goal, be μ-ambitious!   #
#                                                                           #
#############################################################################
# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import microgp4 as ugp

# BASIC PARAMETERS

m_int = ugp.f.macro(
    "{var} = {num1} {op} {num2}",
    var=ugp.f.choice_parameter(["x", "y", "z"]),
    num1=ugp.f.integer_parameter(0, 256),
    op=ugp.f.choice_parameter(list("+-*")),
    num2=ugp.f.integer_parameter(0, 256),
)
m_float = ugp.f.macro(
    "{var} = {var} * {num}", var=ugp.f.choice_parameter(["x", "y", "z"]), num=ugp.f.float_parameter(0, 1)
)
m_array = ugp.f.macro("DNA: {dna}", dna=ugp.f.array_parameter("CGAT", 42))
macros = [m_int, m_float, m_array]

##block = ugp.f.bunch(macros, size=10)
##population = ugp.classes.Population(block)
##population += ugp.operators.random_individual(population.top_frame)
##individual = population[-1]
##print(f"# {individual!r}")
##print(f"{individual}")
##print()
##print(population.dump_individual(0))
##
##exit(0)

# LOCAL REFERENCE

m_jmp = ugp.f.macro("JUMP TO {ref}", ref=ugp.f.local_reference())

# block = ugp.f.bunch(macros, size=10)
# population = ugp.classes.Population(block)
# population += ugp.operators.random_individual(population.top_frame)
# individual = population[-1]
# print(f"{individual} ({individual!r})")
# print()
# print(population.dump_individual(0))

# GLOBAL REFERENCE

zap = ugp.f.macro("zap!")
subs = ugp.f.bunch([zap], size=3, name="whazoo")

# m_outer = ugp.f.macro("OUTER JUMP TO {ref}", ref=ugp.f.global_reference(target_frame=subs, creative_zeal=1))
m_outer = ugp.f.macro("OUTER JUMP TO {ref}", ref=ugp.f.global_reference(target_frame="whazoo", creative_zeal=1))
block2 = ugp.f.sequence([m_int, m_outer])

population = ugp.classes.Population(block2)
population += ugp.operators.random_individual(population.top_frame)
individual = population[-1]
print(f"{individual} ({individual!r})")
print()
print(population.dump_individual(0))

individual.as_lgp(filename="demo_parameter-lgp.png", bbox_inches="tight")
individual.as_forest(filename="demo_parameter-forest.png", bbox_inches="tight")

pass
