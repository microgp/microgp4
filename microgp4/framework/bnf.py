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

__all__ = ["bnf"]

from microgp4.global_symbols import FRAMEWORK, FRAMEWORK_DIRECTORY
from microgp4.tools.names import _patch_class_info
from microgp4.classes.frame import FrameABC
from microgp4.classes.macro import Macro
from microgp4.classes.readymade_frames import SELF
from microgp4.tools.names import canonize_name, uncanonize_name
from microgp4.framework.macro import macro

from .framework import *


def bnf(production: list[list[FrameABC | Macro | str]],
        name: str | None = None,
        extra_parameters: dict = None) -> FrameABC:
    r"""Creates the class for a frame specifying a BNF derivation rule.

    The ``bnf`` specifies a single derivation rule in a Backus normal form [1]_, where
    the derivation consists of one or more alternative sequences.

    The `production` is, a list of lists: the outer list contains the alternative
    sequences, and each sequence is itself a list of ``FrameABC`` or ``Macro``. The
    special frame ``SELF`` can be used to denote the symbol being defined and allows
    recursive definitions.

    The `name` identifies the frame, allowing to refer to it in other portions of the code.

    The `parameters` is a dictionary of parameters that are made available to the frame and
    to all its successors in the structure tree.

    Note
    ----
        The ``bnf`` is the only frame factory allowing a recursive definition.

    Parameters
    ----------
    production : list of lists
        the derivation rule.
    name : str, optional
        the name of the frame.
    extra_parameters : dict, optional
        dictionary of parameters.

    Returns
    -------
    FrameABC
        A class frame.

    Examples
    --------
    The definition of an expression in prefix notation::

        <expr> ::= <term> | <op> <expr> <expr>
        <op>   ::= '+' | '-' | '*' | '/'
        <term> ::= <num> | <var>
        <num>  ::= 0-999
        <var>  ::= 'x' | 'y' | 'z'

    In MicroGP4, `num` and `var` are macros; `term`, a frame; and `expr`, the bnf frame.

    >>> var = macro('{v}', v=choice_parameter('xyz'))
    >>> num = macro('{n}', n=integer_parameter(0, 1000))
    >>> term = alternative([var, num])
    >>> op = macro('{o}', o=choice_parameter('+-*/'))
    >>> expr = bnf([[term], [op, SELF, SELF]])

    To avoid the newline after each macro when dumping the frame, one may specify the
    parameter ``_text_after_macro``

    >>> expr = bnf([[term], [op, SELF, SELF]],
                   parameters={'_text_after_macro': ''})


    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form
    """
    derivations = list()
    for expression in production:
        frame = sequence(expression)
        _patch_class_info(frame, canonize_name('BNF:' + uncanonize_name(frame.__name__), 'Frame'), tag=FRAMEWORK)
        derivations.append(frame)

    root = alternative(derivations, extra_parameters=extra_parameters)
    if name:
        _patch_class_info(root, canonize_name(name, 'Frame', user=True), tag=FRAMEWORK)
    else:
        _patch_class_info(root, canonize_name('BNF', 'Frame'), tag=FRAMEWORK)

    # patch derivations to include a self reference
    for derivation in root.ALTERNATIVES:
        if SELF in derivation.SEQUENCE:
            derivation.SEQUENCE = tuple(f if f != SELF else root for f in derivation.SEQUENCE)

    FRAMEWORK_DIRECTORY[root.__name__] = root
    return root
