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

JOB_SIZE = 200_000
NUM_JOBS = 10

import logging
import time
import subprocess
import threading
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def prime(num: int) -> bool:
    if num <= 1:
        logging.debug(f"prime: {num} is not prime")
        return False
    elif num == 2:
        logging.debug(f"prime: {num} is prime")
        return True
    for n in range(2, 1 + num // 2):
        if num % n == 0:
            logging.debug(f"prime: {num} is not prime")
            return False
    logging.debug(f"prime: {num} is prime")
    return True


def fibonacci(steps: int) -> int:
    f1, f2 = 1, 1
    for _ in range(1, steps):
        f0, f1 = f1, f2
        f2 = f0 + f1
    logging.info(f"fibonacci: f_{steps}")
    return f2


def shell(*args, **kwargs) -> int:
    return subprocess.run(['sleep', '5'])


def sequential():
    for _ in range(10):
        prime(JOB_SIZE)


def multithread():
    pool = list()
    for _ in range(NUM_JOBS):
        pool.append(threading.Thread(target=shell, args=(JOB_SIZE,)))

    for t in pool:
        t.start()
    for t in pool:
        t.join()


def multiprocess():
    pool = list()
    for _ in range(NUM_JOBS):
        pool.append(multiprocessing.Process(target=shell, args=(JOB_SIZE,)))

    for t in pool:
        t.start()
    for t in pool:
        t.join()


def concurrent1():
    str = ''
    with ThreadPoolExecutor() as pool:
        for result in pool.map(prime, list(range(110050100, 110050250))):
            str += '!' if result else '.'
    print(str)


def concurrent2():
    str = ''
    with ProcessPoolExecutor() as pool:
        for result in pool.map(prime, list(range(110050100, 110050250))):
            str += '!' if result else '.'
    print(str)


from collections import defaultdict

GLOBAL = defaultdict(int)


def add(n: int) -> None:
    global GLOBAL
    if n > 0:
        GLOBAL[n] += 1
    else:
        GLOBAL[-n] -= 1


def timeit(func):
    start_w, start_p = time.time(), time.perf_counter()
    func()
    end_w, end_p = time.time(), time.perf_counter()
    logging.info(f"timeit: {func.__qualname__} wall-clock: {end_w-start_w:.2f}s; time: {end_p-start_p:.2f}s")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    #timeit(sequential)
    #timeit(multithread)
    #timeit(multiprocess)
    #timeit(concurrent1)
    #timeit(concurrent2)

    seq = [1 for _ in range(1_000)] + [-1 for _ in range(1_000)]
    with ThreadPoolExecutor() as pool:
        for result in pool.map(add, seq):
            pass
    print(GLOBAL)