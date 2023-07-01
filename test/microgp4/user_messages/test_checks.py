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

from typing import Sequence
import microgp4 as ugp
import pytest

PARANOIA_TYPE_ERROR = "TypeError (paranoia check)"
PARANOIA_VALUE_ERROR = "ValueError (paranoia check)"


def test_check_valid_type():

    assert ugp.user_messages.check_valid_type(404, int) == True
    my_sequence: Sequence[int] = [1, 2, 3, 4, 5]
    assert ugp.user_messages.check_valid_type(my_sequence, Sequence) == True
    try:
        ugp.user_messages.check_valid_type("303", int)
    except ugp.user_messages.exception.MicroGPError as e:
        assert str(e) == PARANOIA_TYPE_ERROR

    class someClass:
        pass

    class someSubClass(someClass):
        pass

    assert ugp.user_messages.check_valid_type(someClass, object, False) == True


def test_check_valid_types():
    assert ugp.user_messages.check_valid_types(42, int) == True
    assert ugp.user_messages.check_valid_types("hello", str) == True
    assert ugp.user_messages.check_valid_types([1, 2, 3], list) == True
    assert ugp.user_messages.check_valid_types((1, 2, 3), tuple) == True
    assert ugp.user_messages.check_valid_types({"a": 1, "b": 2}, dict) == True
    assert ugp.user_messages.check_valid_types({1, 2, 3}, set) == True
    assert ugp.user_messages.check_valid_types(3.14, (int, float)) == True
    assert ugp.user_messages.check_valid_types("world", (str, list)) == True

    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_types(42, str)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_types("hello", int)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_types([1, 2, 3], tuple)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_types((1, 2, 3), list)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_types({"a": 1, "b": 2}, set)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_types({1, 2, 3}, dict)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_types(3.14, int)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_types("world", int)


def test_check_value_range():
    assert ugp.user_messages.check_value_range(42, 0, 100) == True
    assert ugp.user_messages.check_value_range(3.14, 0, 3.1416) == True
    assert ugp.user_messages.check_value_range(-10, -100, 0) == True
    assert ugp.user_messages.check_value_range(0, None, 10) == True
    assert ugp.user_messages.check_value_range(10, 10, None) == True

    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_value_range(-10, 0, 100)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_value_range(3.14, 0, 3.0)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_value_range(100, -100, 0)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_value_range(10, None, 5)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_value_range(-10, -5, 0)


def test_check_valid_length():
    assert ugp.user_messages.check_valid_length([1, 2, 3], 1, 4) == True
    assert ugp.user_messages.check_valid_length("hello", 1, 6) == True
    assert ugp.user_messages.check_valid_length([], None, 10) == True
    assert ugp.user_messages.check_valid_length([1, 2, 3], 3, None) == True

    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_length([1, 2, 3], 4, None)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_length("hello", None, 3)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_length([], 1, 10)
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_valid_length([1, 2, 3], None, 2)


def test_check_no_duplicates():
    assert ugp.user_messages.check_no_duplicates([1, 2, 3]) == True
    assert ugp.user_messages.check_no_duplicates("helo") == True
    assert ugp.user_messages.check_no_duplicates([[1, 2], [1, 4]]) == True
    assert ugp.user_messages.check_no_duplicates([]) == True

    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_no_duplicates([1, 2, 3, 2])
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_no_duplicates("hello world")
    with pytest.raises(ugp.user_messages.exception.MicroGPError):
        ugp.user_messages.check_no_duplicates([1, 2, 3, 3, 4])
