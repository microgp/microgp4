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

"""MicroGP 4!1.0α "Kiwi" <https://squillero.github.io/microgp4/>

A versatile evolutionary optimizer and fuzzer.
Copyright 2022 Giovanni Squillero and Alberto Tonda.
Distributed under Apache-2.0.
"""

from collections import namedtuple
import logging

from .utils import *
from . import reproducible_random as rr
from . import fitness

logger = logging.getLogger(__name__)

VersionInfo = namedtuple('VersionInfo', ['epoch', 'major', 'minor', 'tag', 'micro', 'codename', 'dev'])
version_info = VersionInfo(4, 1, 0, 'a', 0, 'Kokand', 26)

# hard code
__name__ = "microgp"
__version__ = f"{version_info.epoch}!{version_info.major}.{version_info.minor}{version_info.tag}{version_info.micro}.dev{version_info.dev}"
__author__ = "Giovanni Squillero and Alberto Tonda"
__copyright__ = """MicroGP v4: Copyright (c) 2022 Giovanni Squillero and Alberto Tonda
Licensed under the Apache License, Version 2.0.
MicroGP v3: Copyright (c) 2006-2016 Giovanni Squillero 
Licensed under the GNU General Public License v3.0.
MicroGP v2: Copyright (c) 2002-2006 Giovanni Squillero
Licensed under the GNU General Public License v2.0.
MicroGP v1: Internal (not released)
"""

logger = logging.getLogger('MicroGP')
logger.debug(f"This is MicroGP v{__version__} \"{version_info.codename}\"")
logger.debug(f"(c) 2022 G. Squillero & A. Tonda — Licensed under Apache-2.0")
