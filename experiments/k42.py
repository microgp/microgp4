# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#############################################################################
#           __________                                                      #
#    __  __/ ____/ __ \__ __   This file is part of MicroGP4 v4!2.0         #
#   / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer  #
#  / /_/ / /_/ / ____/ // /_   https://github.com/microgp/microgp4          #
#  \__  /\____/_/   /__  __/                                                #
#    /_/ --MicroGP4-- /_/      You don't need a big goal, be μ-ambitious!   #
#                                                                           #
#############################################################################
# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0


class MicroGPException(Exception):
    """Base class for exceptions in MicroGP4."""

    def __init__(self):
        self.__foo = 0

    def foo(self):
        print(hasattr(self, "__foo"))
        self.__foo += 1
        print(hasattr(self, "__bar"))
        self.__bar += 1


x = MicroGPException()
x.foo()
