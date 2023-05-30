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
# v1 / May 2023 / Squillero (GX)

__all__ = ['Register', 'GLOBAL_REGISTER']

from typing import Any

from microgp4.user_messages.checks import *


class Register:
    def __init__(self):
        self._register = dict()

    def register(self, item: Any, tag: str, info: dict):
        assert tag not in self._register, \
            f"ValueError: item already registered {item!r} ({tag} / {info})"
        self._register[item] = {'tag': tag} | info

assert 'GLOBAL_REGISTER' not in globals(), \
    f"SystemError: GLOBAL_REGISTER already initialized (paranoia check)"
GLOBAL_REGISTER = Register()
assert 'GLOBAL_REGISTER' in globals(), \
    f"SystemError: GLOBAL_REGISTER not initialized (paranoia check)"
