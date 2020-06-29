import random
import shlex
import subprocess
import sys
from pathlib import Path
from time import sleep
from timeit import timeit

cpu_results = []
for data_amount in [1000, 10000, 100000]:
    data = '\\n'.join(str(random.randint(1, 100)) for _ in range(data_amount))
    cpu_results.append(
        timeit(
            setup='from test_skybonds.fraction_percent_calculation_decimal.fraction_percent_calculation import main\n'
                  f'from io import StringIO\n'
                  f'from unittest.mock import patch\n',
            stmt=f'with patch(\'sys.stdin\', StringIO(\'{data_amount}\\n{data}\')): main()', number=3)
    )
print('cpu_results: %s' % cpu_results)
sleep(10)

filename = Path(__file__).absolute().parent / 'fraction_percent_calculation.py'
exec_line = shlex.split(f'{sys.executable} -m memory_profiler {filename}')
for data_amount in [1000, 10000, 100000]:
    data = '\n'.join(str(random.randint(1, 100)) for _ in range(data_amount))
    subprocess.run(exec_line, text=True, input=f'{data_amount}\n{data}')
    sleep(5)
