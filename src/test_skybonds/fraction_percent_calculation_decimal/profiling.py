import shlex
import subprocess
import sys
from functools import wraps
from random import random
from time import time
from typing import Callable, Iterator

from test_skybonds.fraction_percent_calculation_decimal.fraction_percent_calculation import calculate_fraction_percents


def timeit(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = fn(*args, **kwargs)
        exec_time = time() - start_time
        print(f'Exec time {args[0]}: {exec_time:.10f}s')
        return result

    return wrapper


@timeit
def test_as_process(length: str, data: str):
    subprocess.run(shlex.split(f'{sys.executable} ./fraction_percent_calculation.py'), text=True,
                   stdout=subprocess.PIPE,
                   input=f'{length}\n{data}')


@timeit
def test_as_function(length: str, data: Iterator[str]):
    def read_input(_: str) -> str:
        if hasattr(read_input, 'length_sent'):
            return next(data)
        read_input.length_sent = True
        return length

    for _ in calculate_fraction_percents(read_input):
        ...


print('test_as_process:')
for data_amount in [1000, 1000000]:
    test_as_process(str(data_amount), '\n'.join(str(random()) for _ in range(data_amount)))

print('test_as_function:')
for data_amount in [1000, 1000000, 2000000]:
    test_as_function(str(data_amount), (str(random()) for _ in range(data_amount)))
