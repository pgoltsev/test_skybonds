from unittest import TestCase

from .fraction_percent_calculation import calculate_fraction_percents, format_fraction


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
            def read_input(_: str) -> str:
                return input_values.pop(0)

            percents = list(calculate_fraction_percents(read_input))
            self.assertNotEqual(len(percents), 0, input_values)
            for actual, expected in zip(percents, expected_output):
                self.assertEqual(format_fraction(actual), expected)
