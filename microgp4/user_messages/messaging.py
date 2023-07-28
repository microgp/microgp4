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
    'microgp_logger', 'performance', 'deprecation', 'runtime_warning', 'user_warning', 'syntax_warning',
    'deprecation_warning', 'syntax_warning_hint'
]

import logging
import sys
import warnings

from microgp4.global_symbols import notebook_mode

BASE_STACKLEVEL = 3


def _indent_msg(message):
    return '\n  ' + message.replace('\n', '\n  ')


def deprecation(message: str, stacklevel_offset: int = 0) -> bool:
    warnings.warn(f"{_indent_msg(message)}", DeprecationWarning, stacklevel=BASE_STACKLEVEL + stacklevel_offset)
    return True


def performance(message: str, stacklevel_offset: int = 0) -> bool:
    warnings.warn(f"{_indent_msg(message)}", RuntimeWarning, stacklevel=BASE_STACKLEVEL + stacklevel_offset)
    return True


def runtime_warning(message: str, stacklevel_offset: int = 0) -> bool:
    warnings.warn(f"{_indent_msg(message)}", RuntimeWarning, stacklevel=BASE_STACKLEVEL + stacklevel_offset)
    return True


def user_warning(message: str, stacklevel_offset: int = 0) -> bool:
    warnings.warn(f"{_indent_msg(message)}", UserWarning, stacklevel=BASE_STACKLEVEL + stacklevel_offset)
    return True


def syntax_warning(message: str, stacklevel_offset: int = 0) -> bool:
    warnings.warn(f"{_indent_msg(message)}", SyntaxWarning, stacklevel=BASE_STACKLEVEL + stacklevel_offset)
    return True


def deprecation_warning(message: str, stacklevel_offset: int = 0) -> bool:
    warnings.warn(f"{_indent_msg(message)}", DeprecationWarning, stacklevel=BASE_STACKLEVEL + stacklevel_offset)
    return True


def syntax_warning_hint(message: str, stacklevel_offset: int = 0) -> bool:
    if microgp_logger.level < logging.INFO:
        warnings.warn(f"Friendly suggestion:{_indent_msg(message)}",
                      SyntaxWarning,
                      stacklevel=BASE_STACKLEVEL + stacklevel_offset)
        DEBUG_FRIENDLY_SUGGESTIONS = "Friendly suggestion:\n  Friendly suggestions are only shown if code is not optimized and logging level is DEBUG"
        if not notebook_mode:
            warnings.warn(DEBUG_FRIENDLY_SUGGESTIONS, SyntaxWarning)
    return True


#############################################################################
# CUSTOMIZATIONS

assert 'microgp_logger' not in globals(), \
    f"SystemError: MicroGP logger already initialized (paranoia check)"
logging.basicConfig()  # Initialize logging
microgp_logger = logging.getLogger('MicroGP')
microgp_logger.propagate = False
assert 'microgp_logger' in globals(), \
    f"SystemError: MicroGP logger not initialized (paranoia check)"

if notebook_mode:
    microgp_logger.setLevel(logging.DEBUG)
elif __debug__:
    microgp_logger.setLevel(logging.DEBUG)
else:
    microgp_logger.setLevel(logging.INFO)

# Alternative symbols: ⍄ ┊
console_formatter = logging.Formatter('%(asctime)s ▷ %(levelname)s ▷ %(name)s::%(message)s', datefmt="%H:%M:%S")
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
microgp_logger.addHandler(console_handler)

# file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s::%(message)s', datefmt="%Y-%m-%d %H:%M:%S,uuu")
# file_handler = logging.FileHandler('debug.log')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# Avoid excessive warnings...
if not sys.warnoptions:
    warnings.filterwarnings('once')
