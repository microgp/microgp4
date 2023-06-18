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

__all__ = [
    'version_info', '__version__', '__author__', '__copyright__', 'FRAMEWORK_DIRECTORY', 'FRAMEWORK', 'LINK',
    'NODE_ZERO', 'UGP4_TAG', 'GENETIC_OPERATOR', 'FITNESS_FUNCTION', 'test_mode', 'notebook_mode', 'debug_mode'
]

import sys
from collections import namedtuple
from abc import ABCMeta

VersionInfo = namedtuple('VersionInfo', ['epoch', 'major', 'minor', 'tag', 'micro', 'codename', 'dev'])
version_info = VersionInfo(4, 2, 0, 'a', 0, 'Meaning of Liff', 1)

__version__ = f'{version_info.epoch}!' + \
              f'{version_info.major}.{version_info.minor}{version_info.tag}{version_info.micro}' + \
              f'.dev{version_info.dev}'
__author__ = 'Giovanni Squillero and Alberto Tonda'
__copyright__ = '''MicroGP v4: Copyright (c) 2022-23 Giovanni Squillero and Alberto Tonda
Licensed under the Apache License, Version 2.0.
MicroGP v3: Copyright (c) 2006-2016 Giovanni Squillero 
Licensed under the GNU General Public License v3.0.
MicroGP v2: Copyright (c) 2002-2006 Giovanni Squillero
Licensed under the GNU General Public License v2.0.
MicroGP v1: Internal (not released)
'''

#####################################################################################################################
# Auto-detected "modes"

test_mode = 'pytest' in sys.modules

notebook_mode = False
try:
    if 'zmqshell' in str(type(get_ipython())):
        notebook_mode = True
except NameError:
    pass

debug_mode = __debug__

#####################################################################################################################
# "Global" constants

FRAMEWORK = 'framework'
LINK = 'link'
NODE_ZERO = 0
UGP4_TAG = 'µGP⁴'
GENETIC_OPERATOR = 'genetic_operator'
FITNESS_FUNCTION = 'fitness_function'

#####################################################################################################################

assert 'FRAMEWORK_DIRECTORY' not in globals(), \
    f"SystemError: FRAMEWORK_DIRECTORY already initialized (paranoia check)"
FRAMEWORK_DIRECTORY: dict[str, 'FrameABC'] = dict()
assert 'FRAMEWORK_DIRECTORY' in globals(), \
    f"SystemError: FRAMEWORK_DIRECTORY not initialized (paranoia check)"
