#!/usr/bin/env python3
"""The program converts fractions to their percentage values."""
import logging
import sys
from array import array
from typing import Iterable, Optional

logger = logging.Logger(__name__, level=logging.INFO)
logger.addHandler(logging.StreamHandler())


def read_fraction_amount() -> int:
    """Read fraction amount from standard input.

    :return: Fraction amount.
    """
    while True:
        value: str = sys.stdin.readline().strip()
        if not value.isdigit():
            logger.error('Incorrect input. Should be an integer.')
        else:
            break

    return int(value)


def read_fraction() -> float:
    """Read fraction value from given read stream function.

    :return: Fraction value.
    """
    value: Optional[float] = None
    while True:
        try:
            value = float(sys.stdin.readline().strip())
        except ValueError:
            pass

        if value is None or value <= 0:
            logger.error('Incorrect input. Should be a rational positive number greater than 0.')
        else:
            break

    return round(value, 3)


def calculate_fraction_percents() -> Iterable[float]:
    """Calculate faction percents.

    :return: Iterable with calculated percents.
    """
    fractions_amount: int = read_fraction_amount()
    fractions: array = array('f')
    fractions_sum: float = 0
    for number in range(1, fractions_amount + 1):
        fraction = read_fraction()
        fractions.append(fraction)
        fractions_sum += fraction
    for fraction in fractions:
        yield fraction / fractions_sum


def format_fraction(value: float) -> str:
    """Format fraction to string adding leading zeroes.

    :param value: Float value.
    :return: String of float value with leading zeroes.
    """
    return '{:.3f}'.format(value)


def main() -> None:
    """Execute program flow."""
    for percent in calculate_fraction_percents():
        print(format_fraction(percent))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
