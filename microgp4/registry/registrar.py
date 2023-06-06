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

__all__ = ['Statistics']

from typing import Any
from dataclasses import dataclass
from copy import copy
import shelve
from pickle import HIGHEST_PROTOCOL
from collections import namedtuple

from microgp4.user_messages.checks import *

FAMILYTREE_FILENAME = 'genealogy.db'
FITNESS_LOG_FILENAME = 'fitness.db'


@dataclass
class Statistics:
    """Class for keeping stats of a genetic operator."""
    calls: int = 0
    aborts: int = 0
    total_offsprint: int = 0
    complete_failures: int = 0
    partial_failures: int = 0
    partial_successes: int = 0
    complete_successes: int = 0
    pass
