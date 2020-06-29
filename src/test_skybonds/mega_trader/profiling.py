import random
import shlex
import subprocess
import sys
from pathlib import Path
from time import sleep
from timeit import timeit


def generate_lot_data() -> str:
    percent = random.randint(900, 990) / 10
    amount = random.randint(1, 5)
    return f'1 name {percent} {amount}'


cpu_results = []
for data_amount in [1000, 10000, 70000]:
    initial_data = f'{data_amount} {data_amount} 999999999'
    data = '\\n'.join(generate_lot_data() for _ in range(data_amount))
    cpu_results.append(
        timeit(
            setup='from test_skybonds.mega_trader.mega_trader import main\n'
                  f'from io import StringIO\n'
                  f'from unittest.mock import patch\n',
            stmt=f'with patch(\'sys.stdin\', StringIO(\'{initial_data}\\n{data}\\n\')): main()', number=3)
    )
print('cpu_results: %s' % cpu_results)
sleep(5)

try:
    import memory_profiler
except ImportError:
    print('To profile memory please install "memory_profiler"')
    sleep(5)
else:
    filename = Path(__file__).absolute().parent / 'mega_trader.py'
    exec_line = shlex.split(f'{sys.executable} -m memory_profiler {filename}')
    for data_amount in [1000, 10000, 70000]:
        initial_data = f'{data_amount} {data_amount} 999999999'
        data = '\n'.join(generate_lot_data() for _ in range(data_amount))
        subprocess.run(exec_line, text=True, input=f'{initial_data}\n{data}\n')
        sleep(10)

# Extra profiling.
filename = Path(__file__).absolute().parent / 'mega_trader.py'
data_amount = 2000
initial_data = f'{data_amount} {data_amount} 999999999'
data = '\n'.join(generate_lot_data() for _ in range(data_amount))
exec_line = shlex.split(f'{sys.executable} -m cProfile {filename}')
subprocess.run(exec_line, text=True, input=f'{initial_data}\n{data}\n')
