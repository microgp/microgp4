#!/usr/bin/env bash
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

cd microgp4 || exit

find . -name "*.cpython-3*.opt-2.pyc" -print0 | while read -d $'\0' pyo; do
  dir="$(dirname "$pyo")"
  pyc="$(basename "$pyo" .opt-2.pyc).pyc"
  echo "Linking \"$pyo\" -> \"$dir/$pyc\""
  cp -f "$pyo" "$dir/$pyc"
done
