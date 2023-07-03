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

import random
import microgp4 as ugp

BATCH_SIZE = 4096


def test_reproducibility():
    seed = random.randint(0, 1_000_000)
    ugp.rrandom.seed(seed)
    v1 = [ugp.rrandom.random() for _ in range(BATCH_SIZE)]
    v2 = [ugp.rrandom.random() for _ in range(BATCH_SIZE)]
    ugp.rrandom.seed(seed)
    v3 = [ugp.rrandom.random() for _ in range(BATCH_SIZE)]
    assert v1 == v3
    assert v2 != v3

    ugp.rrandom.seed()
    v4 = [ugp.rrandom.random() for _ in range(BATCH_SIZE)]
    assert v1 != v4


def test_independence():
    seed = random.randint(0, 1_000_000)
    ugp.rrandom.seed(seed)
    v1 = [ugp.rrandom.random() for _ in range(BATCH_SIZE)]
    ugp.rrandom.seed(seed)
    v2_1 = [ugp.rrandom.random() for _ in range(BATCH_SIZE // 2)]
    z = [random.random() for _ in range(BATCH_SIZE)]
    v2_2 = [ugp.rrandom.random() for _ in range(BATCH_SIZE // 2)]
    assert v1 == v2_1 + v2_2


def test_randy_init():
    randy = ugp.randy.Randy(42)
    assert randy._calls == 0


def test_randy_random():
    randy = ugp.randy.Randy(42)
    rand_val = randy.random()
    assert 0 <= rand_val <= 1


def test_randy_boolean():
    randy = ugp.randy.Randy(42)
    boolean_val = randy.boolean(p_true=0.6)
    assert isinstance(boolean_val, bool)


def test_randy_randint():
    randy = ugp.randy.Randy(42)
    rand_int = randy.randint(1, 10)
    assert 1 <= rand_int <= 10


def test_randy_sigma_random():
    randy = ugp.randy.Randy(42)
    sigma_rand_val = randy.sigma_random(1, 10, 5, 0.5)
    assert 1 <= sigma_rand_val <= 10


def test_randy_sigma_randint():
    a = 0
    b = 10
    loc = 5
    strength = 0.5
    randy = ugp.randy.Randy(42)
    res = randy.sigma_randint(a, b, loc=loc, strength=strength)
    assert a <= res < b
    assert type(res) == int


def test_randy_choice():
    randy = ugp.randy.Randy(42)
    seq = ['apple', 'banana', 'cherry']
    choice_val = randy.choice(seq)
    assert choice_val in seq


def test_randy_weighted_choice():
    randy = ugp.randy.Randy(42)
    seq = ['apple', 'banana', 'cherry']
    weights = [0.1, 0.3, 0.6]
    weighted_choice_val = randy.weighted_choice(seq, weights)
    assert weighted_choice_val in seq


def test_randy_sigma_choice():
    randy = ugp.randy.Randy(42)
    seq = ['apple', 'banana', 'cherry']
    sigma_choice_val = randy.sigma_choice(seq, 1, 0.5)
    assert sigma_choice_val in seq


def test_randy_shuffle():
    randy = ugp.randy.Randy(42)
    seq = ['apple', 'banana', 'cherry']
    shuffled_seq = randy.shuffled(seq)
    assert set(shuffled_seq) == set(seq)


def test_randy_str():
    randy = ugp.randy.Randy(42)
    str_val = str(randy)
    assert str_val.startswith("Randy @")


def test_randy_bool():
    randy = ugp.randy.Randy(42)
    bool_val = bool(randy)
    assert isinstance(bool_val, bool)


def test_randy_sigma_random():
    randy = ugp.randy.Randy(42)
    sigma_val = randy.sigma_random(0, 1, loc=0.5, strength=0.1)
    assert 0 <= sigma_val <= 1


def test_randy_scale_random():
    randy = ugp.randy.Randy(42)
    scale_val = randy.scale_random(0, 1, loc=0.5, scale=0.1)
    assert 0 <= scale_val <= 1


def test_randy_sigma_choice():
    randy = ugp.randy.Randy(42)
    seq = [0, 1, 2, 3, 4, 5]
    choice_val = randy.sigma_choice(seq, loc=2, strength=0.1)
    assert choice_val in seq


def test_randy_weighted_choice():
    randy = ugp.randy.Randy(42)
    seq = [0, 1, 2, 3, 4, 5]
    p = [0.1, 0.1, 0.1, 0.1, 0.3, 0.3]
    choice_val = randy.weighted_choice(seq, p)
    assert choice_val in seq


def test_randy_choice():
    randy = ugp.randy.Randy(42)
    seq = [0, 1, 2, 3, 4, 5]
    choice_val = randy.choice(seq)
    assert choice_val in seq


def test_randy_boolean():
    randy = ugp.randy.Randy(42)
    bool_val = randy.boolean(p_true=0.3)
    assert isinstance(bool_val, bool)


def test_randy_randint():
    randy = ugp.randy.Randy(42)
    int_val = randy.randint(0, 5)
    assert 0 <= int_val <= 5


def test_randy_sigma_randint():
    randy = ugp.randy.Randy(42)
    int_val = randy.sigma_randint(0, 5, loc=2, strength=0.1)
    assert 0 <= int_val < 5


def test_randy_shuffle():
    randy = ugp.randy.Randy(42)
    seq = [0, 1, 2, 3, 4, 5]
    shuffled_seq = seq.copy()
    randy.shuffle(shuffled_seq)
    assert len(seq) == len(shuffled_seq)


def test_randy_shuffled():
    randy = ugp.randy.Randy(42)
    seq = [0, 1, 2, 3, 4, 5]
    shuffled_seq = randy.shuffled(seq)
    assert len(seq) == len(shuffled_seq)
