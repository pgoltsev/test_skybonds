#!/usr/bin/env python3
"""The program calculates maximum income for given lots within trade period."""
import logging
import sys
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, DecimalException, ROUND_HALF_EVEN
from operator import attrgetter
from typing import Tuple, Optional, List, Dict, TextIO

logger = logging.Logger(__name__, level=logging.INFO)
logger.addHandler(logging.StreamHandler())


@dataclass
class Lot:
    """Trading lot."""
    __slots__ = ['order', 'day', 'price', 'bond_price_percent', 'bond_name', 'bonds_amount', 'bond_overpayment']

    _order_counter = 0
    order: int

    #: Start day when lot is issued to the market.
    day: int
    #: Price of a lot.
    price: Decimal
    bond_price_percent: Decimal
    bond_name: str
    bonds_amount: int
    #: Overpayment considering the price percent.
    bond_overpayment: Decimal

    @classmethod
    def create(cls, day: int, bond_price_percent: Decimal, bond_name: str,
               bonds_amount: int, bond_rating: int) -> 'Lot':
        """Create lot instance.

        This is factory method. It is better to use it instead explicit creation.

        :param day: Start day when lot is issued to the market.
        :param bond_price_percent: Price percent of one bond.
        :param bond_name: Bond name.
        :param bonds_amount: Amount of bonds in the lot.
        :param bond_rating: Bond rating.
        :return: Created lot instance.
        """
        bond_price: Decimal = bond_price_percent / 100 * bond_rating
        lot_price: Decimal = bonds_amount * bond_price
        bond_overpayment: Decimal = bond_price_percent * bond_rating / 100 - bond_rating

        cls._order_counter += 1

        return Lot(order=cls._order_counter, day=day, price=lot_price, bond_price_percent=bond_price_percent,
                   bond_name=bond_name, bonds_amount=bonds_amount, bond_overpayment=bond_overpayment)


class MegaTrader:
    """Trader.

    The class represents a trader that can buy lots on a market.
    """

    def __init__(self, balance: Decimal) -> None:
        """Initialize an instance.

        :param balance: Start balance of a trader.
        """
        super().__init__()
        self.balance: Decimal = balance
        self.lots: List[Lot] = []

    def buy_lots(self, market: 'Market') -> List[Lot]:
        """Buy slots on given market.

        :param market: Market where slots should be bought.
        :return: Slots were bought.
        """
        lots: List[Lot] = sorted(market.lots, key=market.evaluate_income, reverse=True)
        for lot in lots:
            if self.balance >= lot.price:
                self.balance -= lot.price
                self.lots.append(lot)

        self.lots.sort(key=attrgetter('order'))
        return self.lots


class Market:
    """Marker where lots are trading."""

    #: Extra repayment period in days.
    BOND_REPAYMENT_PERIOD: int = 30
    #: Bond rating. All bonds have the same rating.
    BOND_RATING: int = 1000
    #: Daily income of a bond.
    BOND_DAILY_INCOME: int = 1

    class InapplicableSlot(Exception):
        ...

    class DayOutOfRange(InapplicableSlot):
        def __init__(self, first: int, last: int) -> None:
            super().__init__(f'Day out of range. Should be [{first}-{last}]')

    class BondsExceeded(InapplicableSlot):
        def __init__(self, bonds_amount: int) -> None:
            super().__init__(f'Bonds amount per day exceeded. Should be no more than {bonds_amount}')

    def __init__(self, issue_period: int, lots_amount_per_day: int) -> None:
        """Initialize an instance.

        :param issue_period: Period in days when lots can be issued to the market.
        :param lots_amount_per_day: Amount of lots per day that can be issued.
        """
        self._trading_period: int = issue_period
        self._total_trading_period: int = self._trading_period + self.BOND_REPAYMENT_PERIOD
        self._lots_amount_per_day: int = lots_amount_per_day
        self._daily_lots: Dict[int, list] = defaultdict(list)
        self.lots: List[Lot] = []

    def add(self, lot: Lot) -> None:
        """Issue a lot to the market for trading.

        :param lot: Lot for trading.
        """
        if not (1 <= lot.day <= self._trading_period):
            raise self.DayOutOfRange(1, self._trading_period)

        if len(self._daily_lots[lot.day]) >= self._lots_amount_per_day:
            raise self.BondsExceeded(self._lots_amount_per_day)

        self._daily_lots[lot.day].append(lot)
        self.lots.append(lot)

    def evaluate_income(self, lot: Lot) -> Decimal:
        """Evaluate income of given on the end of trading period.

        :param lot: Lot to evaluate.
        :return: Income.
        """
        lot_trading_days: int = self._total_trading_period - lot.day
        bond_income: int = self.BOND_DAILY_INCOME * lot_trading_days
        return (bond_income - lot.bond_overpayment) * lot.bonds_amount


def read_initial_data(stream: TextIO) -> Tuple:
    """Read initial data.

    :param stream: Stream to read data from.
    """
    while True:
        value: str = stream.readline()
        try:
            days, lots_per_day, balance = value.split(' ')
            days: int = int(days)
            lots_per_day: int = int(lots_per_day)
            balance: Decimal = Decimal(balance)
        except (TypeError, ValueError, DecimalException):
            logger.error('Incorrect input. Should be of 3 values, e.g. "2 2 8000"')
        else:
            break

    return days, lots_per_day, balance


def serialize_lot(lot: Lot) -> str:
    """Serialize a lot into string suitable for output.

    :param lot: Lot instance.
    :return: String representation.
    """
    return ' '.join((str(lot.day), lot.bond_name,
                     str(lot.bond_price_percent),
                     str(lot.bonds_amount)))


class SlotDeserializeError(Exception):
    """Error happens if serializable data has incorrect format."""
    ...


def deserialize_lot(data: str) -> Lot:
    """Deserialize input data into a lot instance.

    :param data: String to deserialize.
    :return: Lot instance.
    """
    try:
        day, bond_name, bond_price_percent, bonds_amount = data.split(' ')
        day: int = int(day)
        bond_price_percent: Decimal = Decimal(bond_price_percent)
        bonds_amount: int = int(bonds_amount)
    except (TypeError, ValueError, DecimalException):
        raise SlotDeserializeError('Incorrect input. Should be of 4 values, e.g. "1 alfa-05 100.2 2"')

    return Lot.create(day=day, bond_name=bond_name, bond_price_percent=bond_price_percent, bonds_amount=bonds_amount,
                      bond_rating=Market.BOND_RATING)


def read_lot(stream: TextIO) -> Optional[Lot]:
    """Read lot from given stream.

    The function deserializes input data and creates lot instance. If input data is invalid
    it retries continuously.
    :param stream: Input stream.
    :return: Lot instance or None if the stream is empty.
    """
    while True:
        value: str = stream.readline().strip()
        if not value:
            break

        try:
            return deserialize_lot(value)
        except SlotDeserializeError as exc:
            logger.error(str(exc))

    return None


def main() -> None:
    """Execute main program flow.

    The function consumes standard input, performs calculation and produces
    results into standard output.
    """
    days, lots_per_day, balance = read_initial_data(sys.stdin)
    market: Market = Market(days, lots_per_day)
    trader: MegaTrader = MegaTrader(balance)
    while True:
        lot = read_lot(sys.stdin)
        if lot is None:
            break

        try:
            market.add(lot)
        except Market.InapplicableSlot as exc:
            logger.error(str(exc))

    trader.buy_lots(market)
    income: Decimal = sum(market.evaluate_income(lot) for lot in trader.lots)
    income = income.quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)
    print(income)
    for lot in trader.lots:
        print(serialize_lot(lot))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
