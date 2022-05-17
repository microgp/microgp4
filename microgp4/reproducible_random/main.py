# -*- coding: utf-8 -*-
#############################################################################
#          __________                                                       #
#   __  __/ ____/ __ \__ __   This file is part of MicroGP4 v1.0a1 "Kiwi"   #
#  / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer   #
# / /_/ / /_/ / ____/ // /_   https://github.com/squillero/microgp4         #
# \__  /\____/_/   /__  __/                                                 #
#   /_/ --MicroGP4-- /_/      "You don't need a big goal, be μ-ambitious!"  #
#                                                                           #
#############################################################################

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

from collections import abc
import logging
import warnings
import numpy as np
from scipy.stats import truncnorm

logger = logging.getLogger(__name__)


class ReproducibleRandom:
    """Default random module for MicroGP

    All functions are coherent with the idea of perturbing with variable intensity (strength)
    a previous value (old). When old is None or strength == 1, the new value is uniformly
    distributed; if strength == 0, the new value is identical to the old one, and a warning
    is raised.

    Results are assumed to be fully reproducible and independent of user's calls to other
    random/numpy.random functions.

    Don't use this object directly, see individual docstrings in facade.py
    """

    def __init__(self, seed) -> None:
        logger.debug(f"Initializing RRandom with seed {seed}")
        if seed is None:
            warnings.warn("Using None as random seed: Results will not be reproducible",
                          category=RuntimeWarning,
                          stacklevel=3)
        self._generator = np.random.default_rng(seed)
        self._state = np.random.get_state()

    def _save_status(self) -> bool:
        self._status = np.random.get_state(False)
        return True

    def _check_status(self) -> bool:
        return self._status == np.random.get_state()

    @staticmethod
    def _strength2stddev(x):
        # Almost-black-magic function that is assumed to smoothly convert a "strength"
        # into a standard deviation that can be used inside the truncated normal distribution
        return .8 / 1.4**((1 - x) * 12 - 3)

    def _tnorm(self, loc=None, scale=None, size=None):
        # Please note that SciPy's tnorm rvs has been reported to be agonizingly slow in version 1.5.0rc2
        a, b = 0, 1
        if loc is None:
            loc = (a + b) / 2
        return truncnorm.rvs((a - loc) / scale, (b - loc) / scale,
                             loc=loc,
                             scale=scale,
                             random_state=self._generator,
                             size=size)

    def random(self, old=None, strength=1.):
        assert old is None or 0 <= old < 1, f"Old value must be None or in [0, 1) (found {old})"
        assert 0 <= strength <= 1, f"Mutation strength must be in [0, 1] (found {strength})"
        assert old is not None or strength > 0, f"Strength cannot be zero if there is no previous value"
        if old is None or strength == 1:
            return self._generator.random()
        elif strength == 0:
            warnings.warn("Strength is zero: New results are identical to old ones",
                          category=RuntimeWarning,
                          stacklevel=2)
            return old
        else:
            return self._tnorm(loc=old, scale=ReproducibleRandom._strength2stddev(strength))

    def choice(self, values, old=None, strength=1.):
        assert isinstance(values, abc.Sequence), f"Values must be a sequence (found {type(values)}"
        step = 1 / len(values)
        old_r = old * step + step / 2
        selected = int(self.random(old=old_r, strength=strength) / step)
        return values[selected]

    def randint(self, low, high, old=None, strength=1.0):
        if old is not None:
            old = (old - low) / (high - low)
        r = self.random(old=old, strength=strength)
        return int(r * (high - low) + low)
