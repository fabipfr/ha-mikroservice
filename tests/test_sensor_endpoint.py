import importlib
import os
import tempfile
import unittest
from pathlib import Path

import main


class SensorEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_sensor_data.db"
        os.environ["SENSOR_DB_PATH"] = str(self.db_path)
        import database

        self.database = importlib.reload(database)
        self.main = importlib.reload(main)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_write_sensor_data_returns_stored_id(self) -> None:
        payload = {
            "entity_id": "sensor-3",
            "value": 42.0,
            "timestamp": "2026-07-25T13:00:00Z",
        }

        response = self.main.write_sensor_data(
            self.main.SensorData(**payload)
        )

        self.assertEqual(response["message"], "Sensor data received")
        self.assertEqual(response["data"].entity_id, "sensor-3")
        self.assertTrue(isinstance(response["stored_id"], int))


if __name__ == "__main__":
    unittest.main()
