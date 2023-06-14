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

import unittest

from microgp4.classes.checkable import Checkable

class test_checkable(unittest.TestCase):
    def test_add_check(self):
        def check_function():
            return True

        Checkable.add_check(check_function)
        self.assertIn(check_function, Checkable._CLASS_CHECKS)

    def test_add_instance_check(self):
        def check_function():
            return True

        checkable = Checkable()
        checkable.add_instance_check(check_function)
        self.assertIn(check_function, checkable._Checkable__instance_checks)
        
    def test_run_checks(self):
        def class_check_function():
            return True

        def instance_check_function():
            return True

        Checkable.add_check(class_check_function)

        checkable = Checkable()
        checkable.add_instance_check(instance_check_function)

        assert checkable.run_checks() == True