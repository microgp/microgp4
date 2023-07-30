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

import logging
import platform
import platform

import microgp4 as ugp

if platform.machine() == "arm64":
    import library_arm64 as library
else:
    raise NotImplementedError(f"Unknown machine type: {platform.machine()}")


SCRIPT_NAME = {"Linux": "./evaluate-all.sh", "Darwin": "./evaluate-all.sh", "Windows": "evaluate-all.cmd"}


def main():
    top_frame = library.define_frame()

    ugp.microgp_logger.setLevel(logging.INFO)
    evaluator = ugp.evaluator.ScriptEvaluator(SCRIPT_NAME[platform.system()], file_name="ind{i}.s")
    ugp.ea.vanilla_ea(top_frame, evaluator, population_extra_parameters={"_comment": "#"})


if __name__ == "__main__":
    ugp.rrandom.seed(42)
    # ugp.set_logger_level(logging.INFO)
    main()
