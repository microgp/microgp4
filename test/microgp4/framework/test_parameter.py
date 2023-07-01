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
import microgp4 as ugp


def test_integer_parameter():
    param = ugp.framework.integer_parameter(1, 10)

    assert issubclass(param, ugp.classes.ParameterABC)
    assert param.MIN == 1
    assert param.MAX == 10

    instance = param()
    instance.mutate(0.5)
    assert 1 <= instance.value < 10

    assert not instance.is_valid(10)
    assert not instance.is_valid("2")


def test_float_parameter():
    param = ugp.framework.float_parameter(0.0, 1.0)

    assert issubclass(param, ugp.classes.ParameterABC)
    assert param.MIN == 0.0
    assert param.MAX == 1.0

    instance = param()
    instance.mutate(0.5)
    assert 0.0 <= instance.value < 1.0

    assert not instance.is_valid(1.5)
    assert not instance.is_valid("0.5")


def test_choice_parameter():
    param = ugp.framework.choice_parameter(["A", "B", "C"])

    assert issubclass(param, ugp.classes.ParameterABC)
    assert param.ALTERNATIVES == ("A", "B", "C")

    instance = param()
    instance.mutate(0.5)
    assert instance.value in {"A", "B", "C"}

    assert not instance.is_valid("D")


def test_array_parameter():
    param = ugp.framework.array_parameter(["0", "1"], 4)

    assert issubclass(param, ugp.classes.ParameterABC)
    assert param.DIGITS == ("0", "1")
    assert param.LENGTH == 4

    instance = param()
    initial_value = instance.value
    instance.mutate(1.0)

    assert instance.value != initial_value


def test_integer_parameter():
    param = ugp.framework.integer_parameter(1, 10)
    assert isinstance(param, type)
    assert issubclass(param, ugp.classes.ParameterABC)
    assert param.MIN == 1
    assert param.MAX == 10
    instance = param()
    assert instance.run_paranoia_checks()
    assert instance.is_valid(5)
    assert not instance.is_valid(11)
    assert instance.mutate(0.5) is None


def test_float_parameter():
    param = ugp.framework.float_parameter(1.0, 10.0)
    assert isinstance(param, type)
    assert issubclass(param, ugp.classes.ParameterABC)
    assert param.MIN == 1.0
    assert param.MAX == 10.0
    instance = param()
    assert instance.run_paranoia_checks()
    assert instance.is_valid(5.0)
    assert not instance.is_valid(11.0)
    assert instance.mutate(0.5) is None


def test_choice_parameter():
    param = ugp.framework.choice_parameter(['A', 'B', 'C'])
    assert isinstance(param, type)
    assert issubclass(param, ugp.classes.ParameterABC)
    assert param.ALTERNATIVES == ('A', 'B', 'C')
    instance = param()
    assert instance.run_paranoia_checks()
    assert instance.is_valid('A')
    assert not instance.is_valid('D')
    assert instance.mutate(0.5) is None


def test_array_parameter():
    param = ugp.framework.array_parameter(['0', '1'], 3)
    assert isinstance(param, type)
    assert issubclass(param, ugp.classes.ParameterABC)
    assert param.DIGITS == ('0', '1')
    assert param.LENGTH == 3
    instance = param()
    assert instance.run_paranoia_checks()
    assert instance.is_valid('010')
    assert not instance.is_valid('012')
    assert not instance.is_valid('01')
    assert instance.mutate(1.0) is None
    with pytest.raises(NotImplementedError):
        instance.mutate(0.5)


def test_integer_parameter_range():
    with pytest.raises(ugp.user_messages.MicroGPError):
        ugp.framework.integer_parameter(1, 2)


def test_float_parameter_check_valid_type():
    with pytest.raises(ugp.user_messages.MicroGPError):
        ugp.framework.float_parameter("invalid", 10.0)


def test_integer_parameter_range():
    with pytest.warns(SyntaxWarning):
        ugp.framework.integer_parameter(1, 2)


def test_choice_parameter_check_size():
    with pytest.warns(SyntaxWarning):
        ugp.f.parameter.choice_parameter(list(range(1000)))
