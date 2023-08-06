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

import pytest
from typing import Type

import microgp4 as ugp


class MyFrame(ugp.classes.FrameABC):
    def __init__(self, parameters=None):
        super().__init__(parameters=parameters)

    @property
    def successors(self):
        return []

    @property
    def name(self):
        return "MyFrame"

    def dump(self, extra_parameters):
        return f"{self.name}({self.parameters})"

    def is_valid(self, obj):
        return True

    def mutate(self, mutation_rate: float) -> Type["ugp.classes.EvolvableABC"]:
        pass


class MyMacro(ugp.classes.Macro):
    def __init__(self, parameters=None):
        super().__init__(parameters=parameters)

    @property
    def successors(self):
        return []

    @property
    def name(self):
        return "MyMacro"

    def dump(self, extra_parameters):
        return f"{self.name}({self.parameters})"

    def is_valid(self, obj):
        return True

    def mutate(self, mutation_rate: float) -> Type["ugp.classes.EvolvableABC"]:
        pass


def test_cook_sequence():
    expected_output = [ugp.classes.FrameABC, MyFrame, ugp.classes.Macro, MyMacro]
    cooked = ugp.f.utilities.cook_sequence([ugp.classes.FrameABC, MyFrame, ugp.classes.Macro, MyMacro])
    assert cooked == expected_output

    # somelist = [FrameABC, FrameABC]
    # cooked = cook_sequence(somelist)
    # print("smth is cooked")
    # print(cooked)
