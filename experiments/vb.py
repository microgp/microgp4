# !/usr/bin/env python3
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
# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

try:
    import microgp4 as ugp
except ModuleNotFoundError as e:
    import sys, os
    sys.path.append(os.curdir)
    sys.path.append(os.pardir)
    import microgp4 as ugp


def test_print(**p):
    print("--content--")
    for k, v in p.items():
        print(f"{k}: {v!r}")


vb = ugp.classes.ValueBag({'a': 1, 'b': 2, 'c': 3})
test_print(**vb)

vb = ugp.classes.ValueBag(a=1, b=2, c=3)
test_print(**vb)

vb._foo = 'bar'
test_print(**vb)

del vb['b']
test_print(**vb)

vb['$internal'] = 'ZAPPA!'
print(vb['$internal'])
test_print(**vb)

print(list(vb.items()), list(vb._items()))

print(vb.z23)
print(vb['z24'])
print(vb['$z24'])
