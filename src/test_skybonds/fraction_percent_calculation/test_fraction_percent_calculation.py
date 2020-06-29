from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from .fraction_percent_calculation import main


class TestFractionPercentCalculationTestCase(TestCase):
    def test_fraction_percent_calculation(self):
        data = [
            (['2',
              '1.5', '1.5'], ['0.500', '0.500']),
            (['2',
              '0.5', '1.5'], ['0.250', '0.750']),
            (['2',
              '0.111', '0.222'], ['0.333', '0.667']),
            (['2',
              '0.111',
              '-0.222',  # Invalid value, new value should be prompted.
              '0',  # Invalid value, new value should be prompted.
              '0.111'], ['0.500', '0.500']),
        ]

        for input_values, expected_output in data:
            out = StringIO()

            with patch('sys.stdin', StringIO('\n'.join(input_values))), patch('sys.stdout', out):
                main()

            out.seek(0)
            percents = [line.strip() for line in out]
            self.assertNotEqual(len(percents), 0, input_values)
            for actual, expected in zip(percents, expected_output):
                self.assertEqual(actual, expected)
