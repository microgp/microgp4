# -*- coding: utf-8 -*-
# ______________   ______   __
# |____/|____|| \  ||   \\_/
# |R  \_|A   ||N \_||D__/ |Y
#
#    @..@    古池や
#   (----)    蛙飛び込む
#  ( >__< )    水の音
#
# https://github.com/squillero/randy
# Copyright 2023 Giovanni Squillero.
# SPDX-License-Identifier: 0BSD

import math
from functools import lru_cache
from typing import Any
from collections.abc import Sequence, Iterable

import numpy as np
from scipy.stats import truncnorm

from microgp4.user_messages import *
from microgp4.global_symbols import *

__all__ = ['Randy', 'rrandom']


class Randy:
    """Safe, reproducible random numbers for EA applications."""

    SMALL_NUMBER = 1e-9
    LOG_FILENAME = 'randy.log'

    __slots__ = ['_generator', '_calls', '_saved_state']

    def __getstate__(self):
        return self._generator, self._calls

    def __setstate__(self, state):
        _generator, _calls = state

    def __init__(self, seed: Any | None = None) -> None:
        self._generator = np.random.default_rng(seed)
        self._calls = 0
        #with open(Randy.LOG_FILENAME, 'a') as fout:
        #    fout.write(f"Created new Randy: {self}\n")
        self._save_state()

    def __str__(self) -> str:
        description = ', '.join(f"{a}={b!r}" for a, b in self._generator.__getstate__().items())
        return f"Randy @ {hex(id(self))} (calls={self._calls}, {description})"

    #def __repr__(self) -> str:
    #    return f"Randy_{hex(id(self))[2:]}"

    def __bool__(self):
        return self.boolean()

    @lru_cache(maxsize=4096)
    @staticmethod
    def _freeze_truncnorm(a, b, *, loc, scale):
        clip_a, clip_b = (a - loc) / scale, (b - loc) / scale
        return truncnorm(clip_a, clip_b, loc=loc, scale=scale)

    @lru_cache(maxsize=4096)
    @staticmethod
    def _strength_to_sigma(strength: float) -> float | None:
        """Stretches [0,1] on a standard deviation ]0, 20.8[."""
        if strength is None:
            return None
        assert 0 <= strength <= 1, \
            f"ValueError: invalid sigma: {strength} (paranoia check)"
        x = strength / 2 + .5
        x = min(x, 1 - Randy.SMALL_NUMBER)
        val = math.log(x / (1 - x))
        if math.isclose(val, 0):
            val = Randy.SMALL_NUMBER
        return val

    def _save_state(self) -> bool:
        self._saved_state = self._get_current_state()
        #with open(Randy.LOG_FILENAME, 'a') as fout:
        #    fout.write(f"{self!r}: {self._saved_state}\n")
        return True

    def _get_saved_state(self) -> dict:
        return self._saved_state

    def _get_current_state(self) -> dict:
        return self._generator.__getstate__()['state']

    def seed(self, seed: Any | None = None) -> None:
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        assert seed is not None or notebook_mode or messaging.syntax_warning_hint(
            "Random seed is None: results will not be reproducible (generally a bad idea when debugging)")
        self._generator = np.random.default_rng(seed)
        #with open(Randy.LOG_FILENAME, 'a') as fout:
        #    fout.write(f"New seed: {self}\n")
        assert self._save_state()

    def sigma_random(self, a: float, b: float, loc: float | None = None, strength: float | None = None) -> float:
        """Returns a value in [a, b] by perturbing loc with a given strength."""
        self._calls += 1
        assert a <= b, \
            f"ValueError: a > b"
        assert (loc is None and strength is None) or (loc is not None and strength is not None),\
            "ValueError: loc and strength not specified together"
        assert loc is None or a <= loc <= b,\
            "ValueError: loc not in [a, b]"
        assert strength is None or 0 <= strength <= 1,\
            "ValueError: strength not in [0, 1]"
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        if strength is None or strength == 1:
            val = self._generator.random()
            val = val * (b - a) + a
        elif strength == 0:
            val = loc
        else:
            frozen_truncnorm = Randy._freeze_truncnorm(a, b, loc=loc, scale=Randy._strength_to_sigma(strength))
            val = frozen_truncnorm.rvs(random_state=self._generator)
        assert self._save_state()
        return val

    def scale_random(self, a: float, b: float, loc: float | None = None, scale: float | None = None) -> float:
        """Returns a value from a standard normal truncated to [a, b] with mean loc and standard deviation scale."""
        self._calls += 1
        assert a <= b,\
            "ValueError: a must precede b"
        assert (loc is None and scale is None) or (loc is not None and scale is not None),\
            "ValueError: loc and scale not specified together"
        assert loc is None or a <= loc <= b,\
            "ValueError: loc not in [a, b]"
        assert scale is None or scale >= 0,\
            "ValueError: negative scale"
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        if scale is None:
            val = self._generator.random()
            val = val * (b - a) + a
        elif scale == 0:
            val = loc
        else:
            frozen_truncnorm = Randy._freeze_truncnorm(a, b, loc=loc, scale=scale)
            val = frozen_truncnorm.rvs(random_state=self._generator)
        assert self._save_state()
        return val

    def random(self, a: float | None = 0, b: float | None = 1) -> float:
        """Returns a random value in [a, b], default is [0, 1]."""
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        r = self.sigma_random(a=a, b=b, loc=None, strength=None)
        assert self._save_state()
        return r

    def sigma_choice(self, seq: Sequence[Any], loc: int | None = None, strength: float | None = None) -> Any:
        """Returns a random element from seq by perturbing index loc with a given strength."""
        self._calls += 1
        assert strength is None or 0 <= strength <= 1,\
            "ValueError: strength not in [0, 1]"
        assert strength == 1 or (loc is None and strength is None) or (loc is not None and strength is not None),\
            "ValueError: loc and strength not specified together"
        assert loc is None or 0 <= loc < len(seq),\
            "ValueError: invalid loc"
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        if strength == 1 or strength is None:
            r = self._generator.choice(seq)
        elif strength == 0:
            r = seq[loc]
        else:
            i = self.sigma_random(0, len(seq) - Randy.SMALL_NUMBER, loc=loc + .5, strength=strength)
            r = seq[int(i)]
        assert self._save_state()
        return r

    def weighted_choice(self, seq: Sequence[Any], p: Sequence[float]) -> Any:
        """Returns a random element from seq using the probabilities in p."""

        # return self._generetor.choice(seq,p=p)
        assert len(seq) == len(p), \
            "ValueError: different number of elements in seq and weight"
        assert math.isclose(sum(p), 1), \
            "ValueError: weights sum not 1"
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        r = self._generator.random()
        assert self._save_state()
        return next(val for val, cp in ((v, sum(p[0:i + 1])) for i, v in enumerate(seq)) if cp >= r)

    def choice(self, seq: Iterable[Any]) -> Any:
        """Returns a random element from the pool."""
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        r = self._generator.choice(seq)
        assert self._save_state()
        return r

    def boolean(self, p_true: float | None = None, p_false: float | None = None) -> bool:
        """Returns a boolean value with the given probability."""
        self._calls += 1
        assert p_true is None or 0 <= p_true <= 1, \
            "ValueError: p_true not un [0, 1]"
        assert p_false is None or 0 <= p_false <= 1, \
            "ValueError: p_false not in [0, 1]"
        assert p_true is None or p_false is None or math.isclose(p_true + p_false, 1),\
            "ValueError: p_true + p_false not equal to 1"
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        if p_true is None and p_false is None:
            p_true = .5
        elif p_true is None and p_false is not None:
            p_true = 1 - p_false
        r = self._generator.random() < p_true
        assert self._save_state()
        return r

    def randint(self, a, b) -> int:
        """Returns a random integer in [a, b]."""
        assert a <= b, \
            "ValueError: a > b."
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        r = self._generator.random() * (b - a + 1) + a
        assert self._save_state()
        return int(r)

    def sigma_randint(self, a: int, b: int, *, loc: int | None = None, strength: float | None = None) -> int:
        """Returns a random integer in [a, b[ by perturbing loc with a given strength."""
        assert (loc is None and strength is None) or (loc is not None and strength is not None), \
            "ValueError: loc and strength not specified together"
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        if strength == 0:
            r = int(loc)
        if strength is None or strength == 1:
            r = self.randint(a, b - 1)
        else:
            r = int(self.sigma_random(a, b, loc=loc + .5, strength=strength))
        assert self._save_state()
        return r

    def shuffle(self, seq: Sequence) -> None:
        """Shuffle list x in place, and return None."""
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        self._generator.shuffle(seq)
        assert self._save_state()

    def shuffled(self, seq: Sequence) -> list:
        """Returns a shuffled list with the element of seq."""
        assert self._get_current_state() == self._get_saved_state(), \
            "Generator has been modified"
        y = list(seq)
        self.shuffle(y)
        return y

assert 'rrandom' not in globals(), \
    f"SystemError: Randy the Random already initialized (paranoia check)"
rrandom = Randy(42)
assert 'rrandom' in globals(), \
    f"SystemError: Randy the Random not initialized (paranoia check)"
