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

from collections import abc
import pytest
from unittest.mock import patch, MagicMock
from typing import Type
from microgp4.classes.frame import FrameABC
from microgp4.classes.macro import Macro
from microgp4.classes.parameter import ParameterABC
from microgp4.framework.utilities import cook_sequence
from microgp4.classes.evolvable import EvolvableABC
from microgp4.user_messages.checks import check_valid_type, check_valid_types


class MyFrame(FrameABC):

    def __init__(self, parameters=None):
        super().__init__(parameters=parameters)

    @property
    def successors(self):
        return []

    @property
    def name(self):
        return 'MyFrame'

    def dump(self, extra_parameters):
        return f'{self.name}({self.parameters})'

    def is_valid(self, obj):
        return True

    def mutate(self, mutation_rate: float) -> Type['EvolvableABC']:
        pass


class MyMacro(Macro):

    def __init__(self, parameters=None):
        super().__init__(parameters=parameters)

    @property
    def successors(self):
        return []

    @property
    def name(self):
        return 'MyMacro'

    def dump(self, extra_parameters):
        return f'{self.name}({self.parameters})'

    def is_valid(self, obj):
        return True

    def mutate(self, mutation_rate: float) -> Type['EvolvableABC']:
        pass


def test_cook_sequence():

    expected_output = [FrameABC, MyFrame, Macro, MyMacro]

    cooked = cook_sequence([FrameABC, MyFrame, Macro, MyMacro])
    assert cooked == expected_output

    # somelist = [FrameABC, FrameABC]
    # cooked = cook_sequence(somelist)
    # print("smth is cooked")
    # print(cooked)
