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

# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
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

__all__ = ['safe_dump']

from collections import Counter
from microgp4.user_messages import microgp_logger

_name_counter = Counter()
_used_names = set()


def safe_dump(obj, **extra_parameters):
    extra = dict(extra_parameters)
    dumped = None
    while not dumped:
        try:
            dumped = obj.dump(**extra)
        except KeyError as k:
            if k.args[0] in extra:
                microgp_logger.error(f"dump: Can't safely dump {obj!r}")
                raise k
            extra[k.args[0]] = '{' + k.args[0] + '}'
        except Exception as e:
            microgp_logger.error(f"dump: Can't safely dump {obj!r}")
            raise e
    return dumped
