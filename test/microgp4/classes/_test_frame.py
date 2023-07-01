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
from typing import Type
import pytest

import microgp4 as ugp


class FrameConcrete(ugp.classes.FrameABC):
    _name_counter = {}

    def mutate(self, strength: float = 1., **kwargs) -> None:
        pass

    @property
    def successors(self) -> list[Type['ugp.classes.FrameABC'] | Type[ugp.classes.Macro]]:
        return []


def test_frame_instance_creation():
    frame_instance = FrameConcrete(parameters={"test": "test"})
    assert frame_instance._parameters == {"test": "test"}


def test_frame_eq_method():
    frame_instance1 = FrameConcrete()
    frame_instance2 = FrameConcrete()
    assert frame_instance1 == frame_instance2


def test_frame_dump_method():
    frame_instance = FrameConcrete()
    assert frame_instance.dump(ugp.classes.ValueBag()) == ""


def test_frame_is_valid():
    frame_instance = FrameConcrete()
    assert frame_instance.is_valid(None) == True


def test_frame_name():
    assert FrameConcrete.name == "FrameConcrete"


def test_frame_register_name():
    FrameConcrete._registered_names = set()
    assert FrameConcrete.register_name("TestName") == True
    with pytest.raises(AssertionError):
        FrameConcrete.register_name("TestName")
