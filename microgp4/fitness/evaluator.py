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

import os
import subprocess
from datetime import datetime
from typing import Callable, Type, Union, Tuple, Any
from .fitnesstuple import FitnessTuple
from .simple import Numeric
from ..utils import logging


def _run_script(script: Union[str, callable],
                individual: 'Individual',
                num_elements: int = None,
                auto_delete: bool = True) -> Tuple[Tuple[Any], str]:
    """Run an external scripts and parse the result

    Args:
        script (str or callable): script to run.
        individual (Individual): individual on which to execute the script.
        num_elements (int): Number of elements used for the fitness value, the
         other values passed will be considered as comment.

    Returns:

    """
    assert script, "script can't be None"
    assert isinstance(script, str) or hasattr(script, '__call__'), "script must be a string (name of the" \
                                                                   "script or a callable (script itself)"
    assert individual, "individual can't be None"
    filename = individual.constraints.file_name.format(id=individual.id)
    # filename = individual.constraints.file_name.format(node_id=individual.id)

    with open(filename, 'w') as file:
        file.write(str(individual))
    completed = subprocess.run([script, filename], check=True, capture_output=True, universal_newlines=True)
    if completed.stderr:
        logging.info("STDERR %s %s -> %s", script, filename, completed.stderr.strip())
    # logging.debug(completed)
    raw_array = completed.stdout.split()
    if not num_elements:
        values = [eval(b) for b in raw_array]
        comment = "%s %s @ %s -> %s" % (script, filename, datetime.now(), ' '.join(raw_array))
    else:
        values = [eval(b) for b in raw_array[:num_elements]]
        comment = ' '.join(raw_array[num_elements:])
    logging.debug(comment)
    if auto_delete:
        os.remove(filename)
    return tuple(values), comment


def make_evaluator(evaluator: Union[str, callable],
                   fitness_type: Type[FitnessTuple] = Numeric,
                   num_elements: int = None) -> Callable:
    """Build a fitness evaluator that calls a script.

    Args:
        evaluator (str or callable): name of the script. The result is taken from stdout.
        fitness_type: kind of fitness, ie. type of comparison.
        num_elements (int): number of relevant element in the script output,
            the remaining are considered "comment". If None, the all output
            is part of the fitness.
    Returns:
        A function that can be stored into Constraints.evaluator.
    """

    if isinstance(evaluator, str):
        assert os.path.isfile(evaluator), f"Can't use the script \"{evaluator}\" as evaluator"

        def r(i):
            f, c = _run_script(evaluator, i, num_elements, auto_delete=True)
            return fitness_type(f), c
    elif callable(evaluator):

        def r(i):
            f = evaluator(str(i))
            c = "%s -> %s" % (evaluator.__name__, f)
            return fitness_type(f), c
    else:
        assert isinstance(evaluator, str) or callable(evaluator), \
            "evaluator must be either a string (the name of a script), or a callable object (eg. a function)"

    return r
