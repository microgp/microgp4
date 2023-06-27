#!/usr/bin/env python3
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
# SPDX-License-Identifier: Apache-2.0

from abc import ABCMeta
from microgp4.classes.node_reference import NodeReference
from microgp4.framework.parameter_structural_global import _global_reference
from microgp4.framework.parameter_structural_global import *
from microgp4.framework.parameter_structural_local import *
from microgp4.user_messages.exception import MicroGPInvalidIndividual
from microgp4.tools.graph import get_siblings
import pytest
from typing import Type, List
from microgp4.framework.parameter_structural_local import _local_reference
