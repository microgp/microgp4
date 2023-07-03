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


class TestIdentifiable:

    def test_identity(self):

        class MyIdentifiable(ugp.classes.IdentifiableABC):

            def __init__(self, id):
                self.id = id

            @property
            def _identity(self):
                return self.id

        obj1 = MyIdentifiable(1)
        obj2 = MyIdentifiable(2)
        obj3 = MyIdentifiable(1)

        assert obj1._identity == 1
        assert obj2._identity == 2
        assert obj3._identity == 1

    def test_hash(self):

        class MyIdentifiable(ugp.classes.IdentifiableABC):

            def __init__(self, id):
                self.id = id

            @property
            def _identity(self):
                return self.id

        obj1 = MyIdentifiable(1)
        obj2 = MyIdentifiable(2)
        obj3 = MyIdentifiable(1)

        assert hash(obj1) != hash(obj2)
        assert hash(obj1) == hash(obj3)

    def test_eq(self):

        class MyIdentifiable(ugp.classes.IdentifiableABC):

            def __init__(self, id):
                self.id = id

            @property
            def _identity(self):
                return self.id

        obj1 = MyIdentifiable(1)
        obj2 = MyIdentifiable(2)
        obj3 = MyIdentifiable(1)
        obj4 = None
        obj5 = "not an IdentifiableABC object"

        assert obj1 == obj3
        assert obj1 != obj2
        assert obj1 != obj4
        assert obj1 != obj5
