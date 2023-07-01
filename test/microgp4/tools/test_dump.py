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
import microgp4.tools.dump as ugp


class TestObject:

    def __init__(self, key_to_raise=None):
        self.key_to_raise = key_to_raise

    def dump(self, **kwargs):
        if self.key_to_raise and self.key_to_raise not in kwargs:
            raise KeyError(self.key_to_raise)
        else:
            return f"success: {kwargs.get(self.key_to_raise, '')}"


def test_safe_dump():
    obj = TestObject()
    assert ugp.safe_dump(obj) == "success: "

    obj = TestObject("key")
    assert ugp.safe_dump(obj) == "success: {key}"

    obj = TestObject("key")
    assert ugp.safe_dump(obj, key="value") == "success: value"


class TestObjectException(Exception):
    pass


class TestObjectWithException:

    def __init__(self, exception):
        self.exception = exception

    def dump(self, **kwargs):
        raise self.exception


def test_safe_dump_with_general_exception():
    obj = TestObjectWithException(TestObjectException())
    with pytest.raises(TestObjectException):
        ugp.safe_dump(obj)


def test_safe_dump_with_key_error_exception():
    obj = TestObjectWithException(KeyError('key'))
    with pytest.raises(KeyError):
        ugp.safe_dump(obj)
