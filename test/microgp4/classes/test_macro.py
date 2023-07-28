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

from typing import Any
import microgp4 as ugp
import pytest


class MockParameter(ugp.classes.ParameterABC):
    def __init__(self):
        super().__init__()
        self._value = "test"

    def is_valid(self, obj: Any) -> bool:
        return super().is_valid(obj) and isinstance(obj, str)


def test_macro():
    text = "Hello, {name}"
    parameters = {"name": MockParameter}

    MacroClass = ugp.framework.macro(text, **parameters)

    macro_instance = MacroClass()

    assert isinstance(macro_instance, MacroClass)

    assert macro_instance.text == text

    assert macro_instance.PARAMETERS == parameters
