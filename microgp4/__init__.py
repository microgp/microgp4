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

import logging

from microgp4.global_symbols import *
from microgp4 import user_messages
from microgp4.user_messages.modes import *

from microgp4 import classes
from microgp4 import classes as C

from microgp4 import framework
from microgp4 import framework as f

from microgp4 import fitness_ as fitness
from microgp4 import fitness_ as fit

from microgp4 import evaluator_ as evaluator
from microgp4 import evaluator_ as eval

# Globals

from microgp4.randy.randy import rrandom
from microgp4.user_messages.messaging import microgp_logger
from microgp4.decorators import fitness_function

#############################################################################
# Patch names to ease debugging and visualization

from microgp4.tools.names import _patch_class_info
for name in sorted(dir()):
    item = globals()[name]
    if isinstance(item, type) and item.__name__.endswith('ABC'):
        _patch_class_info(item, item.__name__, tag='abc')
    elif isinstance(item, type):
        _patch_class_info(item, item.__name__, tag=None)
del _patch_class_info

#############################################################################
# Warning

if notebook_mode and logging.getLogger().level <= logging.WARNING:
    user_messages.performance(
        "Paranoia checks are always enabled in notebooks: performances can be significantly impaired")
elif not notebook_mode:
    assert test_mode or user_messages.performance(
        "Paranoia checks are enabled: performances can be significantly impaired — consider using '-O'")

#############################################################################
# Welcome!

__welcome__ = f"This is MicroGP v{__version__} \"{version_info.codename}\"\n" + \
    f"(c) 2022-23 G. Squillero & A. Tonda — Licensed under Apache-2.0"


def welcome(level=logging.DEBUG):
    from sys import stderr
    stderr.flush()
    for m in __welcome__.split('\n'):
        user_messages.microgp_logger.log(level, f"*: {m}")
    return True


if not notebook_mode:
    assert welcome(logging.INFO)