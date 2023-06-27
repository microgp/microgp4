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
from collections import abc
from typing import Type
from microgp4.classes.frame import FrameABC
from microgp4.classes.macro import Macro
from microgp4.framework.macro import macro
from microgp4.framework.framework import alternative


class TestAlternative:

    class MockFrame(FrameABC):
        pass

    class MockMacro(Macro):
        pass

    @pytest.fixture
    def mock_frame(self):
        return self.MockFrame

    @pytest.fixture
    def mock_macro(self):
        return self.MockMacro

    def test_alternative_with_valid_input(self, mock_frame, mock_macro):
        result = alternative([mock_frame, mock_macro], name='test')
        assert isinstance(result, Type)
        assert issubclass(result, FrameABC)
        assert result.ALTERNATIVES == (mock_frame, mock_macro)

    def some_test(self):
        print(alternative(['smth here should be a class']))

    # def test_alternative_with_invalid_input(self):
    #     with pytest.raises(AssertionError):
    #         alternative(['not a class'])

    # def test_alternative_with_no_input(self):
    #     with pytest.raises(AssertionError):
    #         alternative([])

    def test_alternative_with_only_frame(self, mock_frame):
        result = alternative([mock_frame])
        assert isinstance(result, Type)
        assert issubclass(result, FrameABC)
        assert result.ALTERNATIVES == (mock_frame,)

    def test_alternative_with_only_macro(self, mock_macro):
        result = alternative([mock_macro])
        assert isinstance(result, Type)
        assert issubclass(result, FrameABC)
        assert result.ALTERNATIVES == (mock_macro,)
