import importlib
import os
import tempfile
import unittest
from pathlib import Path

import main


class EnvironmentDataEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_sensor_data.db"
        os.environ["SENSOR_DB_PATH"] = str(self.db_path)
        import database

        self.database = importlib.reload(database)
        self.main = importlib.reload(main)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_get_sensor_data_returns_existing_row(self) -> None:
        row_id = self.database.store_sensor_data(
            {
                "entity_id": "sensor-2",
                "value": 12.3,
                "timestamp": "2026-07-25T12:00:00Z",
            }
        )

        response = self.main.get_sensor_data(row_id)

        self.assertEqual(response["entity_id"], "sensor-2")
        self.assertEqual(response["value"], "12.3")
        self.assertEqual(response["timestamp"], "2026-07-25T12:00:00Z")

    def test_get_sensor_data_returns_error_for_missing_row(self) -> None:
        response = self.main.get_sensor_data(999999)

        self.assertEqual(response, {"error": "Sensor data not found"})


if __name__ == "__main__":
    unittest.main()
