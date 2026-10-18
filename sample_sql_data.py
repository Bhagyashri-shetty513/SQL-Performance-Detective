
# Simulated Oracle SQL data for offline development.
# These are examples, not results from a live database.

SAMPLE_SQL = {
    "4abc123xyz789": {
        "sql_id": "4abc123xyz789",
        "sql_text": (
            "SELECT employee_id, last_name "
            "FROM employees WHERE department_id = :dept_id"
        ),
        "plans": [
            {
                "plan_hash_value": 101001,
                "operation": "INDEX RANGE SCAN",
                "elapsed_seconds": 0.18,
                "cpu_seconds": 0.07,
                "buffer_gets": 420,
                "disk_reads": 12,
                "executions": 100,
            },
            {
                "plan_hash_value": 202002,
                "operation": "TABLE ACCESS FULL",
                "elapsed_seconds": 0.95,
                "cpu_seconds": 0.31,
                "buffer_gets": 3800,
                "disk_reads": 240,
                "executions": 100,
            },
        ],
    },
    "7def456uvw123": {
        "sql_id": "7def456uvw123",
        "sql_text": (
            "SELECT department_id, COUNT(*) "
            "FROM employees GROUP BY department_id"
        ),
        "plans": [
            {
                "plan_hash_value": 303003,
                "operation": "HASH GROUP BY",
                "elapsed_seconds": 0.42,
                "cpu_seconds": 0.28,
                "buffer_gets": 1600,
                "disk_reads": 80,
                "executions": 25,
            },
        ],
    },
}


def find_sql(sql_id):
    """Return simulated SQL details for a SQL ID, if available."""
    return SAMPLE_SQL.get(sql_id.strip().lower())
