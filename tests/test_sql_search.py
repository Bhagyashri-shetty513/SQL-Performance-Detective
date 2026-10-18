
import unittest

from sample_sql_data import find_sql


class TestSQLSearch(unittest.TestCase):

    def test_existing_sql_id_with_two_plans(self):
        result = find_sql("4abc123xyz789")

        self.assertIsNotNone(result)
        self.assertEqual(result["sql_id"], "4abc123xyz789")
        self.assertEqual(len(result["plans"]), 2)

    def test_existing_sql_id_with_one_plan(self):
        result = find_sql("7def456uvw123")

        self.assertIsNotNone(result)
        self.assertEqual(len(result["plans"]), 1)

    def test_sql_id_is_case_insensitive(self):
        result = find_sql("4ABC123XYZ789")

        self.assertIsNotNone(result)

    def test_unknown_sql_id(self):
        result = find_sql("unknown123")

        self.assertIsNone(result)

    def test_sql_id_with_extra_spaces(self):
        result = find_sql(" 4abc123xyz789 ")

        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
