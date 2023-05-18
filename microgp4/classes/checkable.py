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

from typing import Callable

from microgp4.user_messages import microgp_logger


class Checkable:
    """Checkable classes allow to `add_check` and `run_checks`."""

    @classmethod
    def add_check(cls, function: Callable) -> None:
        try:
            cls._CLASS_CHECKS.append(function)
        except AttributeError:
            cls._CLASS_CHECKS = list()
            cls._CLASS_CHECKS.append(function)

    def add_instance_check(self, function: Callable) -> None:
        try:
            self.__instance_checks.append(function)
        except AttributeError:
            self.__instance_checks = list()
            self.__instance_checks.append(function)

    def run_checks(self, *args, **kwargs) -> bool:
        if '_CLASS_CHECKS' in self.__class__.__dict__ and not all(
                f(*args, **kwargs) for f in self.__class__._CLASS_CHECKS):
            microgp_logger.debug(f"CheckFail: CLASS: {self.__class__._CLASS_CHECKS}")
            return False
        if '_Checkable__instance_checks' in self.__dict__ and not all(
                f(*args, **kwargs) for f in self.__instance_checks):
            microgp_logger.debug(f"CheckFail: INSTANCE: {self.__class__.__instance_checks}")
            return False
        return True
