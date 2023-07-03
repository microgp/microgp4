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

# =[ HISTORY ]===============================================================
# v1 / April 2023 / Squillero (GX)

__all__ = ['ValueBag', 'USER_PARAMETER']

import re

from microgp4.user_messages import *

USER_PARAMETER = re.compile(r'[a-z][a-z_0-9]*', re.IGNORECASE)


class ValueBag(dict):
    """A wrapper around a standard dictionary for reading parameters and options.

    A "safe key" is a key that can be safely used as Python identifier (regex: /[a-z_][a-z_0-9]*/).
    A "reserved key" is a key that starts with '$' and then follows the same rules as safe keys (regex: /$[a-z_0-9]*/).
    A ValueBag may be accessed almost as a standard dict with string keys, but:

    * The object is read-only and hashable
    * All key/values are available using _keys(), _values(), and _items().
    * Only safe keys are shown in standard dict() methods such as keys(), values(), and items()
    * Only safe keys appear when using standard iterator (`for k in value_bag`) or parameter expansion (`**value_bag`).
    * Safe keys can be accessed as attributes (`value_bag.foo`).
    * The default value for missing keys is None
    """

    FLAG_KEY = re.compile(r'\$[a-z_0-9]*', re.IGNORECASE)
    SAFE_KEY = re.compile(r'[a-z_][a-z_0-9]*', re.IGNORECASE)
    VALID_KEY = re.compile(r'[a-z_$][a-z_0-9]*', re.IGNORECASE)

    def __init__(self, init=None, **items):
        if init and isinstance(init, ValueBag):
            super().__init__(init._items(), **items)
        elif init:
            super().__init__(init, **items)
        else:
            super().__init__(**items)

    def __str__(self):
        return '{{' + ', '.join(f'{k!r}: {self[k]!r}' for k in sorted(super().keys())) + '}}'

    def __repr__(self):
        return f"<{self.__class__.__module__}.{self.__class__.__name__} @ {hex(id(self))}>"

    def __setitem__(self, key, value):
        # super().__setitem__(key, value)
        raise NotImplementedError(f"{self!r} is read-only: can't set {key!r} to {value!r}")

    def __delitem__(self, key):
        raise NotImplementedError(f"{self!r} is read-only: can't delete {key!r}")

    def __setattr__(self, key: str, value):
        # super().__setitem__(key, value)
        raise NotImplementedError(f"{self!r} is read-only: can't set {key!r} to {value!r}")

    def __delattr__(self, key: str):
        # assert check_valid_types(key, str)
        # assert ValueBag.SAFE_KEY.fullmatch(key), \
        #     f"KeyError: invalid key: {key!r} (paranoia check)"
        # del self[key]
        raise NotImplementedError(f"ValueBag is read-only: can't delete {key!r}")

    def __missing__(self, key):
        if ValueBag.FLAG_KEY.fullmatch(key):
            return False
        else:
            return None

    #def __getitem__(self, key: str):
    #    assert check_valid_types(key, str)
    #    assert ValueBag.VALID_KEY.fullmatch(key), \
    #        f"ValueError: Invalid key: {key!r} (paranoia check)"
    #    try:
    #        return super().__getitem__(key)
    #    except KeyError:
    #        return None

    def __getattr__(self, key: str):
        assert check_valid_type(key, str)
        assert ValueBag.SAFE_KEY.fullmatch(key), \
            f"KeyError: invalid key (paranoia check): {key!r}"
        return self[key]

    def __iter__(self):
        return super().__iter__()

    def __or__(self, other) -> 'ValueBag':
        new = ValueBag(self._items())
        if isinstance(other, ValueBag):
            new.update(other._items())
        else:
            new.update(other.items())
        return new

    def __ior__(self, other) -> 'ValueBag':
        if isinstance(other, ValueBag):
            super().update(other._items())
        else:
            super().update(other.items())
        return self

    def keys(self):
        """Same as dict.keys(), but for safe keys only."""
        return [k for k in super().keys() if ValueBag.SAFE_KEY.fullmatch(k)]

    def values(self):
        """Same as dict.values(), but for safe keys only."""
        return [v for k, v in super().items() if ValueBag.SAFE_KEY.fullmatch(k)]

    def items(self):
        """Same as dict.items(), but for safe keys only."""
        return [(k, v) for k, v in super().items() if ValueBag.SAFE_KEY.fullmatch(k)]

    def _keys(self):
        """Same as dict.keys()."""
        return super().keys()

    def _values(self):
        """Same as dict.values()."""
        return super().values()

    def _items(self):
        """Same as dict.items()."""
        return super().items()
