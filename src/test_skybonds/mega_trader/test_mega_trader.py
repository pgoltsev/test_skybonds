from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from test_skybonds.mega_trader.mega_trader import main


class MegaTraderTestCase(TestCase):
    def test_buying_profitable_slots(self):
        """Test buying the most profitable slots and total trader's income."""
        input_values = [
            '2 2 8000',
            '1 alfa-05 100.2 2',
            '2 gazprom-17 100.0 2',
            '2 alfa-05 101.5 5',
            '2 gazprom-17 102.0 1',  # Must be skipped due to bonds per day exceeded.
            '3 gazprom-17 103.0 1',  # Must be skipped due to day out of range.
            '1 gazprom-17 96.0 100',  # Must be skipped because trader can not afford it.
        ]
        expected_income = '135'
        expected_lots = [
            '2 gazprom-17 100.0 2',
            '2 alfa-05 101.5 5',
        ]
        out = StringIO()

        with patch('sys.stdin', StringIO('\n'.join(input_values))), patch('sys.stdout', out):
            main()

        out.seek(0)
        income = out.readline().strip()
        actual_lots = [line.strip() for line in out]
        self.assertEqual(income, expected_income)
        self.assertListEqual(actual_lots, expected_lots)
