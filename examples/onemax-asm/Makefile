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

SHELL=/bin/sh
CFLAGS = -O3

# GNU timeout is /opt/homebrew/bin/gtimeout on my system
TIMEOUT_CMD=gtimeout
ALLOWED_TIME=2

.PHONY: run

run: onemax
	${TIMEOUT_CMD} ${ALLOWED_TIME} ./onemax || echo -1

onemax: main.o onemax.s
	gcc -o $@ $^

clean:
	-rm -f onemax
	-rm -f *.o *.out
	-rm -f *ind[a-f0-9]*.s
	-rm -f *.svg *.png
