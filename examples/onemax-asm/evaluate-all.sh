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

# Compiles and runs a genome, kills it if it does not terminate swiftly
# (GNU timeout is /opt/homebrew/bin/gtimeout on my system)
TIMEOUT_CMD=gtimeout
ALLOWED_TIME=3

for file in "$@"; do
    gcc -o onemax.out main.o "$file"
    $TIMEOUT_CMD $ALLOWED_TIME ./onemax.out || ( cp "$file" "problem-$file"; echo 0 )
    grep -q 'nNone' "$file" && cp "$file" "nNone-$file"
done

exit 0
