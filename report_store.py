"""Local SQLite storage for generated tuning reports."""

import json
import os
import sqlite3
from pathlib import Path


def _database_path():
    configured_path = os.environ.get("SQL_DETECTIVE_DB_PATH")
    if configured_path:
        path = Path(configured_path).expanduser()
    else:
        path = Path(__file__).resolve().parent / "data" / "tuning_reports.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _connect():
    connection = sqlite3.connect(_database_path(), timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def save_report(rows):
    """Store the rows from one generated report and return its ID."""
    with _connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tuning_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                report_json TEXT NOT NULL
            )
        """)
        cursor = connection.execute(
            "INSERT INTO tuning_reports (report_json) VALUES (?)",
            (json.dumps(rows, ensure_ascii=False),),
        )
        return cursor.lastrowid


def load_reports():
    """Return all saved report rows, newest report first."""
    with _connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tuning_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                report_json TEXT NOT NULL
            )
        """)
        reports = connection.execute(
            "SELECT id, generated_at, report_json FROM tuning_reports "
            "ORDER BY id DESC"
        ).fetchall()

    saved_rows = []
    for report in reports:
        for row in json.loads(report["report_json"]):
            saved_rows.append({
                "Report #": report["id"],
                "Saved At": report["generated_at"],
                **row,
            })
    return saved_rows
