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

__all__ = ['default_generator', 'seed', 'random', 'randint', 'choice', 'np_choice']

from typing import Sequence, Any, Optional

from . import main
from . import DEFAULT_SEED

default_generator = main.ReproducibleRandom(seed=DEFAULT_SEED)


def seed(new_seed=DEFAULT_SEED) -> None:
    """Reinitialize the random generator with the given seed

    Args:
        new_seed: The seed used to initialize the `NumPy` `BitGenerator`.
            If None, then unpredictable entropy will be pulled from the OS
    """
    global default_generator
    default_generator = main.ReproducibleRandom(new_seed)


def random(old: Optional[float] = None, strength: float = 1.) -> float:
    """Return a number in [0, 1) by mutating the old value with more or less strength

    Args:
        old: the previous value, if None strength is forced to 1
        strength: how much the old value is perturbed, if  `strength` is 1., then the
            new value is uniformly distributed in [0, 1); if 0, the new value is
            identical to the old one

    Returns:
        a float in [0, 1)
    """
    return default_generator.random(old=old, strength=strength)


def choice(values=Sequence[Any], old: Optional[int] = None, strength: float = 1.) -> Any:
    """Return an item from a sequence by mutating the old choice with more or less strength

    Args:
        values: a sequence of items
        old: the index of the previous item, if None strength is forced to 1
        strength: how much the old item is perturbed, if  `strength` is 1., then the
            new item is chosen with uniform probability; if 0, the new item is
            identical to the old one

    Returns:
        an item in `values`
    """
    return default_generator.choice(values=values, old=old, strength=strength)


def randint(low, high, old: Optional[int] = None, strength: float = 1.) -> int:
    """Return an inter in [low, high) by mutating the old choice with more or less strength

    Args:
        low: lower bound (included)
        high: upper bound (not included)
        old: the previous value, if None strength is forced to 1
        strength: how much the old item is perturbed, if  `strength` is 1., then the
            new item is chosen with uniform probability; if 0, the new item is
            identical to the old one

    Returns:
        an integer in [low, high)
    """
    return default_generator.randint(low=low, high=high, old=old, strength=strength)


def np_choice(*args, **kwargs):
    return default_generator._generator.choice(*args, **kwargs)
