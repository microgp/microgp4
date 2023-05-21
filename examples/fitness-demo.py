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

from math import sqrt
from itertools import combinations

import microgp4 as ugp

FITNESS_TYPES = [
    ugp.fit.Scalar,
    ugp.fit.Integer,
    ugp.fit.Float,
]

MAGIC_NUMBERS = [('42.1 vs. 42.2', 42.1, 42.2),
                 ('2 vs. sqrt(2)**2', 2, sqrt(2)**2),
                 ('3 vs. .1+.1+.1', .3, .1+.1+.1)]

def test(type_, n1, n2):
    f1 = type_(n1)
    f2 = type_(n2)
    print(f"* {type_.__name__:<18s} :: {f1} == {f2}: {f1 == f2}")
    print(f"* {type_.__name__:<18s} :: {f1} < {f2}: {f1 < f2}")
    print(f"* {type_.__name__:<18s} :: {f1} > {f2}: {f1 > f2}")
    print(f"* {type_.__name__:<18s} :: {f1} << {f2}: {f1 << f2}")
    print(f"* {type_.__name__:<18s} :: {f1} >> {f2}: {f1 >> f2}")


def main():
    for d, n1, n2 in MAGIC_NUMBERS:
        print(f"\n# {d}")
        for type_ in FITNESS_TYPES:
            test(type_, n1, n2)
        for type_ in FITNESS_TYPES:
            test(ugp.fit.reverse_fitness(type_), n1, n2)


if __name__ == '__main__':
    main()