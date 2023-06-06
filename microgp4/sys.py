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
# v1 / June 2023 / Squillero (GX)

"""Information about the current system.
Mostly useful in interactive environments such as a Jupyter Notebook.
"""

__all__ = ['get_operators']

import inspect
from pprint import pformat
from copy import copy

from microgp4.global_symbols import *


class View:

    def __init__(self, data: dict):
        try:
            self._data = dict(sorted(data.items()))
        except TypeError:
            self._data = dict(sorted(data.items(), key=lambda k: str(k)))

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, item):
        if item not in self._data:
            raise KeyError(item)
        return self._data[item]

    def __repr__(self):
        return "⟦" + pformat(self._data)[1:-1] + "⟧"

    def __str__(self):
        return "⟦" + ', '.join(k for k in self._data.keys()) + "⟧"

    def items(self):
        return tuple(self._data.items())

    def keys(self):
        return tuple(self._data.keys())

    def values(self):
        return tuple(self._data.values())


class SysInfo:

    def __init__(self):
        pass

    @property
    def genetic_operators(self):
        """Shows all genetic operators available in the current namespace"""
        ops = dict()
        snapshot = inspect.currentframe().f_back.f_globals
        for k, v in snapshot.items():
            if hasattr(v, 'microgp') and v.type == GENETIC_OPERATOR:
                ops[k] = v
        return View(ops)

    @property
    def fitness_functions(self):
        """Shows all fitness functions available in the current namespace"""
        ops = dict()
        snapshot = inspect.currentframe().f_back.f_globals
        for k, v in snapshot.items():
            if hasattr(v, 'microgp') and v.type == FITNESS_FUNCTION:
                ops[k] = v
        return View(ops)

    def show(self, object):
        """Gives some information about a MicroGP4 object. The name (string) can be used"""

        if isinstance(object, str):
            if object not in inspect.currentframe().f_back.f_globals:
                raise KeyError(object)
            object = inspect.currentframe().f_back.f_globals[object]

        if hasattr(object, 'microgp') and object.type == GENETIC_OPERATOR:
            print(f"Genetic operator: {object}")
            print(f"  {object.stats}")
        else:
            print(f"Python object: {type(object)}")

def get_operators():
    snapshot = inspect.currentframe().f_back.f_globals
    return [o for o in snapshot.values() if hasattr(o, 'microgp') and o.type == GENETIC_OPERATOR]


assert 'SYSINFO' not in globals(), \
    f"SystemError: SYSINFO already initialized (paranoia check)"
SYSINFO = SysInfo()
assert 'SYSINFO' in globals(), \
    f"SystemError: FRAMEWORK_DIRECTORY not initialized (paranoia check)"
