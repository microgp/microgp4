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

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# =[ HISTORY ]===============================================================
# v1 / April 2023 / Squillero (GX)

# v1 / April 2023 / Squillero (GX)

"""Decorators and functions for monitoring the evolution"""

__all__ = ['failure_rate']

from collections import Counter
from functools import wraps

from microgp4.user_messages import performance

_STAT = Counter()


def failure_rate(func):
    """Generate sporadic RuntimeWarning messages if the failure rate is above 90%

    The function *fails* if it raises an exception, or if the returned value is evaluated as boolean `False` (eg.
    `False`, `0`, `None`, empty collection).
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        exception = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = False
            exception = e

        _STAT[(func, bool(result))] += 1

        if not result:
            # Failures are `None`, `False`, and `0` (plz note that root is node 0)
            failures = _STAT[(func, False)]
            successes = _STAT[(func, True)]
            total = failures + successes
            if failures / total > .9 and any(total == 10**n for n in range(2, 10)):
                performance(f"The failure rate of '{func.__qualname__}' is {100 * failures / total:g}% " +
                            f"({successes:,} success{'es' if successes != 1 else ''} out of {total:,} calls)")
        if exception:
            raise exception
        else:
            return result

    return wrapper
