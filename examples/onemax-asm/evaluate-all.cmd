@echo off
rem           __________
rem    __  __/ ____/ __ \__ __   This file is part of MicroGP v4!2.0
rem   / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer
rem  / /_/ / /_/ / ____/ // /_   https://github.com/microgp/microgp4
rem  \__  /\____/_/   /__  __/
rem    /_/ --MicroGP4-- /_/      You don't need a big goal, be μ-ambitious!
rem
rem Copyright 2022-23 Giovanni Squillero and Alberto Tonda
rem SPDX-License-Identifier: Apache-2.0

for %%x in (%*) do (
    copy "%%~x" onemax.s >NUL:
    make -s
)
