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

__all__ = ['canonize_name', 'uncanonize_name']

from collections import Counter
from abc import ABCMeta

from microgp4.user_messages import microgp_logger

_name_counter = Counter()
_used_names = set()


def canonize_name(name: str,
                  tag: str,
                  user: bool | None = None,
                  make_unique: bool = True,
                  user_space: bool = False,
                  warn_duplicates: bool = True) -> str:

    assert any(s not in name for s in '<❬#❭>'), \
        f"ValueError: Illegal character in name: {name} (paranoia check)"

    if user is True:
        user_space = True
    elif make_unique:
        _name_counter[(tag, name)] += 1
        name += f'#{_name_counter[(tag, name)]}'

    if user_space:
        canonic_name = f'{tag}<{name}>'
    else:
        # NOTE[GX]: These "fancy" brackets are difficult to enter ;-)
        canonic_name = f'{tag}❬{name}❭'

    assert not warn_duplicates or canonic_name not in _used_names, \
        f"ValueError: Name {canonic_name} has already been used (paranoia check)"
    _used_names.add(canonic_name)

    return canonic_name


def uncanonize_name(name: str, keep_number: bool = False, user: bool = False) -> str:
    if user is None:
        user = '❬' not in name and '❭' not in name
    if user and '<' in name:
        tag = name[0:name.index('<')]
    elif not user and '❬' in name:
        tag = name[0:name.index('❬')]
    else:
        return ''

    tlen = len(tag)
    assert (name[tlen] == '❬' and name[-1] == '❭') or (name[tlen] == '<' and name[-1] == '>'), \
        f'ValueError: not a canonic name: {name} (paranoia check)'
    stripped = name[tlen + 1:-1]
    if '#' in stripped and not keep_number:
        stripped, num = stripped.split('#')
    return stripped


def _patch_class_info(obj: type, name: str | None, tag: str | None = None) -> None:
    if name:
        obj.__name__ = name
    obj.__qualname__ = obj.__name__
    obj.__module__ = 'microgp4'

    if tag is not None:
        obj.__module__ += f'.{tag}'
