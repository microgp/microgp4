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

__all__ = ['sequence', 'alternative', 'bunch']

from collections import abc

from microgp4.global_symbols import FRAMEWORK, FRAMEWORK_DIRECTORY
from microgp4.user_messages import *
from microgp4.tools.names import canonize_name, _patch_class_info
from microgp4.classes.frame import FrameABC
from microgp4.classes.macro import Macro
from microgp4.framework.macro import macro
from microgp4.framework.utilities import cook_sequence
from microgp4.randy import rrandom


def alternative(alternatives: abc.Collection[type[FrameABC] | type[Macro]],
                *,
                name: str | None = None,
                extra_parameters: dict = None) -> type[FrameABC]:
    r"""Creates the class for a frame that can have alternative forms.

    An ``alternative`` is a frame that can take different forms,

    The `alternatives` is the collection of different forms, either ``FrameABC` or
    `Macro`. The different forms are atomic and equally probable.

    The `name` identifies the frame, allowing to refer to it in other portions of the code.

    The `parameters` is a dictionary of parameters that are made available to the frame and
    to all its successors in the structure tree.

    Parameters
    ----------
    alternatives : collection
        the possible alternatives.
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

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form
    """
    assert check_valid_type(alternatives, abc.Collection)
    assert all(check_valid_types(a, FrameABC, Macro, subclass=True) for a in alternatives)
    assert check_valid_length(alternatives, 1)

    class T(FrameABC):
        ALTERNATIVES = tuple(alternatives)

        def __init__(self):
            super().__init__(extra_parameters)

        @property
        def successors(self):
            return [rrandom.choice(T.ALTERNATIVES)]

    if name:
        _patch_class_info(T, canonize_name(name, 'Frame', user=True), tag=FRAMEWORK)
    else:
        _patch_class_info(T, canonize_name('FrameAlternative', 'Frame'), tag=FRAMEWORK)

    FRAMEWORK_DIRECTORY[T.__name__] = T
    return T


def sequence(seq: abc.Sequence[type[FrameABC] | type[Macro] | str],
             *,
             name: str | None = None,
             extra_parameters: dict = None) -> type[FrameABC]:

    cooked_seq = cook_sequence(seq)

    class T(FrameABC):
        SEQUENCE = tuple(cooked_seq)

        def __init__(self):
            super().__init__(extra_parameters)

        @property
        def successors(self):
            return T.SEQUENCE

    if name:
        _patch_class_info(T, canonize_name(name, 'Frame', user=True), tag=FRAMEWORK)
    else:
        _patch_class_info(T, canonize_name('FrameSequence', 'Frame'), tag=FRAMEWORK)

    FRAMEWORK_DIRECTORY[T.__name__] = T
    return T


def bunch(pool: Macro | abc.Collection[type[Macro]],
          size: tuple[int, int] | int = 1,
          *,
          name: str | None = None,
          extra_parameters: dict = None) -> type[FrameABC]:

    def _debug_hints(size):
        if not isinstance(size, int) and size[0] + 1 == size[1]:
            syntax_warning_hint(
                f"Ranges are half open: the size of this macro bunch is always {size[0]} — did you mean 'size=({size[0]}, {size[1]+1})'?",
                stacklevel_offset=1)
        return True

    assert check_valid_types(size, int, abc.Collection)
    assert (not isinstance(pool, abc.Collection) and check_valid_type(pool, Macro, subclass=True)) or \
           isinstance(pool, abc.Collection) and (not pool or any(check_valid_type(t, Macro, subclass=True) for t in pool))

    assert _debug_hints(size)

    if isinstance(pool, type) and issubclass(pool, Macro):
        pool = [pool]
    #assert check_no_duplicates(pool)
    assert check_valid_length(pool, 1)

    if isinstance(size, int):
        size = (size, size + 1)
    else:
        size = tuple(size)
        assert len(size) == 2, \
            f"ValueError: Not a half open range [min, max) (paranoia check)"
    assert 0 < size[0] <= size[1] - 1, \
        f"ValueError: min size is {size[0]} and max size is {size[1]-1} (paranoia check)"

    class T(FrameABC):
        SIZE = size
        POOL = tuple(pool)

        __slots__ = []  # Preventing the automatic creation of __dict__

        def __init__(self):
            super().__init__(extra_parameters)

        @property
        def successors(self):
            n_macros = rrandom.randint(T.SIZE[0], T.SIZE[1] - 1)
            return [rrandom.choice(T.POOL) for _ in range(n_macros)]

    # White parentheses: ⦅ ⦆  (U+2985, U+2986)
    if name:
        canonic_name = canonize_name(name, 'Frame', user=True)
    elif size == (1, 2):
        canonic_name = canonize_name('SingleMacro', 'Frame')
    elif size[1] - size[0] == 1:
        canonic_name = canonize_name('MacroArray', 'Frame')
    else:
        canonic_name = canonize_name('MacroBunch', 'Frame')
    _patch_class_info(T, canonic_name, tag=FRAMEWORK)

    FRAMEWORK_DIRECTORY[T.__name__] = T
    return T
