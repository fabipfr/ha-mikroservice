import os
import sqlite3
from pathlib import Path
from typing import Any


DB_PATH = os.environ.get("SENSOR_DB_PATH", "sensor_data.db")
DB_FILE = Path(DB_PATH).expanduser()


def _get_connection() -> sqlite3.Connection:
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db() -> None:
    with _get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id TEXT NOT NULL,
                value TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


initialize_db()


def store_sensor_data(data: dict[str, Any]) -> int:
    entity_id = str(data["entity_id"])
    value = str(data["value"])
    timestamp = str(data["timestamp"])

    with _get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO sensor_data (entity_id, value, timestamp)
            VALUES (?, ?, ?)
            """,
            (entity_id, value, timestamp),
        )
        row_id = cursor.lastrowid
        if row_id is None:
            raise RuntimeError("Failed to store sensor data")
        return int(row_id)
