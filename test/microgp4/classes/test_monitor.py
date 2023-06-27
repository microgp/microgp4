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

@ugp.classes.failure_rate
def always_succeeds():
    return True

@ugp.classes.failure_rate
def always_fails():
    return False

def test_failure_rate():
    for _ in range(100):
        assert always_succeeds()

    with pytest.warns(RuntimeWarning):
        for _ in range(100):
            assert not always_fails()

    @ugp.classes.failure_rate
    def raises_exception():
        raise ValueError("This is an exception")

    with pytest.raises(ValueError):
        raises_exception()
