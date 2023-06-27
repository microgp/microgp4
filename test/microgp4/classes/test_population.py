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
from unittest.mock import MagicMock
import microgp4 as ugp

@pytest.fixture
def mock_frame():
    return MagicMock(spec=ugp.classes.frame.FrameABC)

@pytest.fixture
def mock_evaluator():
    return MagicMock(spec=ugp.classes.evaluator.EvaluatorABC)

@pytest.fixture
def mock_individual():
    return MagicMock(spec=ugp.classes.individual.Individual)

@pytest.fixture
def population(mock_frame, mock_evaluator):
    return ugp.classes.Population(top_frame=mock_frame, evaluator=mock_evaluator)

def test_mu_setter(population):
    population.mu = 10
    assert population.mu == 10

def test_lambda_setter(population):
    population.lambda_ = 10
    assert population.lambda_ == 10

def test_individuals_property(population):
    assert isinstance(population.individuals, list)

def test_parameters_property(population):
    assert isinstance(population.parameters, dict)

def test_evaluate(population, mock_individual):
    population._individuals = [mock_individual]
    population.evaluate()
    assert mock_individual.fitness is not None
