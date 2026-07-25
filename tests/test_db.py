import importlib
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path


class DatabasePersistenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_sensor_data.db"
        os.environ["SENSOR_DB_PATH"] = str(self.db_path)
        import database

        self.database = importlib.reload(database)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_store_sensor_data_persists_row(self) -> None:
        payload = {
            "entity_id": "sensor-1",
            "value": 24.5,
            "timestamp": "2026-07-25T10:00:00Z",
        }

        row_id = self.database.store_sensor_data(payload)

        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT entity_id, value, timestamp FROM sensor_data WHERE id = ?",
                (row_id,),
            ).fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], "sensor-1")
        self.assertEqual(row[1], "24.5")
        self.assertEqual(row[2], "2026-07-25T10:00:00Z")


if __name__ == "__main__":
    unittest.main()
