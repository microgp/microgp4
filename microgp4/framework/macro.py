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

__all__ = ['macro']

from functools import cache
from typing import Any

from microgp4.global_symbols import FRAMEWORK, FRAMEWORK_DIRECTORY
from microgp4.user_messages import *
from microgp4.tools.names import canonize_name, _patch_class_info
from microgp4.classes.macro import Macro
from microgp4.classes.parameter import ParameterABC


@cache
def _macro(text: str, macro_parameters: tuple[tuple[str, type[ParameterABC]]],
           macro_extra_parameters: tuple[tuple[str, Any]]) -> type[Macro]:

    class M(Macro):
        TEXT = text
        PARAMETERS = dict(macro_parameters)
        EXTRA_PARAMETERS = dict(macro_extra_parameters)

        __slots__ = []  # Preventing the automatic creation of __dict__

    if not macro_parameters:
        _patch_class_info(M, canonize_name('UserText', 'Macro'), tag=FRAMEWORK)
    else:
        _patch_class_info(M, canonize_name('User', 'Macro'), tag=FRAMEWORK)

    FRAMEWORK_DIRECTORY[M.__name__] = M
    return M


def macro(text: str, **parameters: type[ParameterABC] | str) -> type[Macro]:
    """Class factory: Returns the class for a specific macro.

    A macro is a fragment of text with variable elements, the `parameters`, appearing
    in curly brackets, eg. ``"My name is {surname}, {name} {surname}"``.

    Parameters are specified as keyword arguments.

    Note: The text and the parameters are eventually parsed by the ``str.format()``, thus
    the `Format Specification Mini-Language` `[1]`_ may be used.

    Parameters
    ----------
    text :
        the text of the macro in f-string format.
    parameters :
        parameters used in the macro.

    Returns
    -------
    A macro.

    Examples
    --------
    Macro that displays the same 8-bit integer in decimal and hexadecimal formats

    >>> M = macro('Decimal {v} is {v:#x} in hexadecimal', v=integer_parameter(0, 256))
    >>> m = M()

    References
    ----------
    .. [1] https://docs.python.org/3/library/string.html#formatspec
    """
    assert check_valid_type(text, str)
    macro_parameters = list()
    macro_extra_parameters = list()
    for n, p in parameters.items():
        if n[0] != '_':
            assert Macro.is_name_valid(n), \
                f"ValueError: invalid parameter name: {n!r}"
            assert check_valid_type(p, ParameterABC, subclass=True)
            macro_parameters.append((n, p))
        else:
            macro_extra_parameters.append((n, p))

    return _macro(text, tuple(sorted(macro_parameters)), tuple(sorted(macro_extra_parameters)))
