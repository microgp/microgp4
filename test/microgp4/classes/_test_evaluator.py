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

import microgp4 as ugp


def test_evaluator_abstract_methods():
    try:
        evaluator = ugp.classes.evaluator.EvaluatorABC()
    except TypeError:
        pass
    else:
        assert False, "EvaluatorABC should not be instantiable"

    class MyEvaluator(ugp.classes.evaluator.EvaluatorABC):
        def evaluate(self, individuals):
            return [ugp.classes.fitness.FitnessABC() for i in individuals]

    evaluator = MyEvaluator()
    assert callable(evaluator.evaluate)
