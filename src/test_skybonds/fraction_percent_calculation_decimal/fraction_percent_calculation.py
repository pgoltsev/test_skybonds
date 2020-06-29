#!/usr/bin/env python3
"""The program converts fractions to their percentage values."""
import logging
import sys
from decimal import Decimal, ROUND_HALF_EVEN, DecimalException
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


def read_fraction() -> Decimal:
    """Read fraction value from given read stream function.

    :return: Fraction value.
    """
    value: Optional[Decimal] = None
    while True:
        try:
            value = Decimal(sys.stdin.readline().strip())
        except DecimalException:
            pass

        if value is None or value <= 0:
            logger.error('Incorrect input. Should be a rational positive number greater than 0.')
        else:
            break

    return value


def calculate_fraction_percents() -> Iterable[Decimal]:
    """Calculate faction percents.

    :return: Iterable with calculated percents.
    """
    fractions_amount: int = read_fraction_amount()
    fractions: list = []
    fractions_sum: Decimal = Decimal()
    for number in range(1, fractions_amount + 1):
        fraction = read_fraction()
        fractions.append(fraction)
        fractions_sum += fraction
    quantize: Decimal = Decimal('1.000')
    for fraction in fractions:
        yield (fraction / fractions_sum).quantize(quantize, rounding=ROUND_HALF_EVEN)


def main():
    """Execute program flow."""
    for percent in calculate_fraction_percents():
        print(percent)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
