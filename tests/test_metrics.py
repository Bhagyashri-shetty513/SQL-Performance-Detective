
import unittest
from utils import calculate_change


class TestCalculateChange(unittest.TestCase):

    def test_performance_improvement(self):
        self.assertEqual(calculate_change(100, 75), 25.0)

    def test_performance_degradation(self):
        self.assertEqual(calculate_change(100, 125), -25.0)

    def test_no_change(self):
        self.assertEqual(calculate_change(100, 100), 0.0)

    def test_zero_before_value(self):
        self.assertIsNone(calculate_change(0, 50))


if __name__ == "__main__":
    unittest.main()
