"""The program converts fractions to their percentage values."""
import sys
from array import array
from typing import Callable, Iterable, Optional


def read_fraction_amount(read_input: Callable[[str], str]) -> int:
    """Read fraction amount from given read stream function.

    :param read_input: Function for reading input stream.
    :return: Fraction amount.
    """
    input_msg: str = 'Input fractions amount: '
    value: str = read_input(input_msg)
    while not value.isdigit():
        print_error('Incorrect input. Should be an integer.')
        value = read_input(input_msg)

    return int(value)


def read_fraction(number: int, amount: int, read_input: Callable[[str], str]) -> float:
    """Read fraction value from given read stream function.

    :param number: Number of input.
    :param amount: Amount of fractions should be consumed.
    :param read_input: Function for reading input stream.
    :return: Fraction value.
    """
    input_msg: str = f'Input fraction ({number} of {amount}): '
    value: Optional[float] = None
    while value is None:
        try:
            value = float(read_input(input_msg))
        except ValueError:
            print_error('Incorrect input. Should be a rational number.')

    return value


def print_error(message: str) -> None:
    """Output the error message to standard error stream.

    :param message: Message.
    """
    sys.stderr.write(f'{message}\n')


def calculate_fraction_percents(read_input: Callable[[str], str]) -> Iterable[float]:
    """Calculate faction percents.

    :param read_input: Function that accepts a message which will be printed to a user, then reads input from the user
    and returns it.
    :return: Iterable with calculated percents.
    """
    print(__doc__)
    print('To exit just press Ctrl+C.')

    fractions_amount: int = read_fraction_amount(read_input)
    fractions: array = array('f')
    fractions_sum: float = 0
    for number in range(1, fractions_amount + 1):
        fraction = read_fraction(number, fractions_amount, read_input)
        fractions.append(fraction)
        fractions_sum += fraction
    for fraction in fractions:
        yield round((fraction / fractions_sum), 3)


def format_fraction(value: float) -> str:
    """Format fraction to string adding leading zeroes.

    :param value: Float value.
    :return: String of float value with leading zeroes.
    """
    return '{:.3f}'.format(value)


if __name__ == '__main__':
    try:
        for percent in calculate_fraction_percents(input):
            print(format_fraction(percent))
    except KeyboardInterrupt:
        exit(0)
