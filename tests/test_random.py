# -*- coding: utf-8 -*-
#          __________                                                       #
#   __  __/ ____/ __ \__ __   This file is part of MicroGP4 v1.0a1 "Kiwi"   #
#  / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer   #
# / /_/ / /_/ / ____/ // /_   https://github.com/squillero/microgp4         #
# \__  /\____/_/   /__  __/                                                 #
#   /_/ --MicroGP4-- /_/      "You don't need a big goal, be μ-ambitious!"  #
#                                                                           #

# Copyright 2022 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import microgp4 as ugp

NUM_TESTS = 100_000


def test_seed():
    with pytest.warns(RuntimeWarning):
        ugp.rr.seed(None)


def test_random():
    import random as builtin_random
    import numpy.random as numpy_random

    ugp.rr.seed()
    seq1 = [ugp.rr.random() for _ in range(NUM_TESTS)]
    seq2 = [ugp.rr.random() for _ in range(NUM_TESTS)]
    assert seq1 != seq2, "Sanity check"
    ugp.rr.seed()
    seq1b = [ugp.rr.random() for _ in range(NUM_TESTS)]
    seqt1 = [numpy_random.random() for _ in range(NUM_TESTS)]
    seqt2 = [builtin_random.random() for _ in range(NUM_TESTS)]
    assert seqt1 != seqt2, "Sanity check"
    seq2b = [ugp.rr.random() for _ in range(NUM_TESTS)]
    assert seq1 == seq1b, "Reproducibility check"
    assert seq2 == seq2b, "Reproducibility check"

    ugp.rr.seed()
    seq1a = [ugp.rr.random() for _ in range(NUM_TESTS)]
    seqt1a = [numpy_random.random() for _ in range(NUM_TESTS)]
    seqt2a = [builtin_random.random() for _ in range(NUM_TESTS)]
    ugp.rr.seed()
    seq1b = [ugp.rr.random() for _ in range(NUM_TESTS)]
    seqt1b = [numpy_random.random() for _ in range(NUM_TESTS)]
    seqt2b = [builtin_random.random() for _ in range(NUM_TESTS)]
    assert seq1a == seq1b, "Reproducibility check"
    assert seqt1a != seqt1b, "Non interference"
    assert seqt2a != seqt2b, "Non interference"

    ugp.rr.seed(42)
    numpy_random.seed(42)
    seq1a = [ugp.rr.random() for _ in range(NUM_TESTS)]
    numpy_random.seed(42)
    seq1b = [ugp.rr.random() for _ in range(NUM_TESTS)]
    assert seq1a != seq1b, "Non interference"

    with pytest.raises(AssertionError):
        ugp.rr.random(old=None, strength=0)
    with pytest.raises(AssertionError):
        ugp.rr.random(old=-0.1)
    with pytest.raises(AssertionError):
        ugp.rr.random(old=1.1)
    with pytest.raises(AssertionError):
        ugp.rr.random(strength=-0.1)
    with pytest.raises(AssertionError):
        ugp.rr.random(strength=1.1)
