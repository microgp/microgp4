/////////////////////////////////////////////////////////////////////////////
//          __________                                                     //
//   __  __/ ____/ __ \__ __   This file is part of MicroGP v4!2.0         //
//  / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer //
// / /_/ / /_/ / ____/ // /_   https://github.com/microgp/microgp4         //
// \__  /\____/_/   /__  __/                                               //
//   /_/ --MicroGP4-- /_/      You don't need a big goal, be μ-ambitious!  //
//                                                                         //
/////////////////////////////////////////////////////////////////////////////
// Copyright 2022-23 Giovanni Squillero and Alberto Tonda
// SPDX-License-Identifier: Apache-2.0

#include <stdio.h>

unsigned long int one_max(void);

int main(int argc, char *argv[])
{
    int fitness = 0;
    unsigned long int result = one_max();
    for(unsigned long int b=1; b; b <<= 1)
        fitness += !!(result & b);

    printf("%d\n", fitness);
    return 0;
}
