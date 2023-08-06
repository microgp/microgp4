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

# logging.basicConfig(format="[%(asctime)s] %(levelname)s:%(message)s", datefmt="%H:%M:%S", level=logging.INFO)

import microgp4 as ugp

r = ugp.lib.choice_parameter_instance(["ax", "bx", "cx", "dx"])
v = ugp.lib.integer_parameter_instance(0, 256)
t = "mov {reg}, 0x{val:x} // {val}"

m = ugp.lib.Macro()
m.text = t
m["reg"] = r
m["val"] = v
logging.info("macro: %s", m)

m2 = ugp.lib.Macro("Register:{a} Id1:{_id} Id2:{_id} Unset:{u}", a=r)
logging.info("macro: %s", m2)
