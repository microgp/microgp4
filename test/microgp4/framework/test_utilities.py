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

# import pytest
# from microgp4.classes.frame import FrameABC
# from microgp4.classes.parameter import ParameterABC
# from microgp4.framework.utilities import cook_sequence
# from microgp4.framework.macro import macro

# class MockFrame(FrameABC):
#     def __init__(self, parameters: dict = None):
#         super().__init__(parameters)

#     @property
#     def successors(self):
#         return None  

# class MockParameter(ParameterABC):
#     def __init__(self):
#         super().__init__()

#     def mutate(self):
#         pass  

    
# def test_cook_sequence():
#     mock_param = MockParameter()
#     mock_macro = macro('test_macro', p=mock_param)
#     mock_frame = MockFrame()

#     raw_sequence = [mock_frame, mock_macro, mock_param, 'test', [mock_frame, 2]]

#     cooked_sequence = cook_sequence(raw_sequence)

#     assert len(cooked_sequence) == 6

#     for e in cooked_sequence:
#         assert isinstance(e, (type(mock_frame), type(mock_macro)))

# def test_cook_sequence_error():
#     raw_sequence = [1, 2, 3]

#     with pytest.raises(AssertionError):
#         cook_sequence(raw_sequence)
