"""The program converts fractions to their percentage values."""
import sys
from decimal import Decimal, DecimalException, ROUND_HALF_EVEN


def read_fraction_amount() -> int:
    input_msg = 'Input fractions amount: '
    value = input(input_msg)
    while not value.isdigit():
        print_error('Incorrect input. Should be an integer.')
        value = input(input_msg)

    return int(value)


def read_fraction(number: int, amount: int) -> Decimal:
    input_msg = f'Input fraction ({number} of {amount}): '
    value = None
    while value is None:
        try:
            value = Decimal(input(input_msg))
        except DecimalException:
            print_error('Incorrect input. Should be a rational number.')

    return value


def print_error(message: str) -> None:
    sys.stderr.write(f'{message}\n')


def main():
    print(__doc__)
    print('To exit just press Ctrl+C')

    fractions_amount = read_fraction_amount()
    fractions = [
        read_fraction(number, fractions_amount)
        for number in range(1, fractions_amount + 1)
    ]
    fractions_sum = sum(fractions)
    quantize = Decimal('1.000')
    for fraction in fractions:
        print((fraction / fractions_sum).quantize(quantize, rounding=ROUND_HALF_EVEN))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
