
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



from utils import compare_execution_plans


class TestExecutionPlanComparison(unittest.TestCase):

    def test_compares_two_plans(self):
        plans = [
            {"plan_hash_value": 101, "elapsed_seconds": 2.0},
            {"plan_hash_value": 202, "elapsed_seconds": 1.0},
        ]

        result = compare_execution_plans(plans)

        self.assertEqual(result["best_plan_hash"], 202)
        self.assertEqual(result["worst_plan_hash"], 101)
        self.assertEqual(result["fastest_time"], 1.0)
        self.assertEqual(result["slowest_time"], 2.0)
        self.assertAlmostEqual(result["improvement_percent"], 50.0)

    def test_empty_plans(self):
        self.assertIsNone(compare_execution_plans([]))

    def test_equal_plan_times(self):
        plans = [
            {"plan_hash_value": 101, "elapsed_seconds": 1.0},
            {"plan_hash_value": 202, "elapsed_seconds": 1.0},
        ]

        result = compare_execution_plans(plans)

        self.assertAlmostEqual(result["improvement_percent"], 0.0)

    
    def test_zero_elapsed_time(self):
        plans = [
            {"plan_hash_value": 101, "elapsed_seconds": 0.0},
            {"plan_hash_value": 202, "elapsed_seconds": 0.0},
        ]

        result = compare_execution_plans(plans)

        self.assertEqual(result["fastest_time"], 0.0)
        self.assertEqual(result["slowest_time"], 0.0)
        self.assertEqual(result["improvement_percent"], 0.0)
