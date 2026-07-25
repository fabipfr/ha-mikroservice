import sqlite3
import tempfile
import unittest
from pathlib import Path

import joblib

import train_model


class TrainModelTests(unittest.TestCase):
    def test_train_model_writes_joblib_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "sensor_data.db"
            output_path = Path(temp_dir) / "model.joblib"

            with sqlite3.connect(db_path) as conn:
                conn.execute(
                    """
                    CREATE TABLE sensor_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        entity_id TEXT NOT NULL,
                        value TEXT NOT NULL,
                        timestamp TEXT NOT NULL
                    )
                    """
                )
                conn.executemany(
                    "INSERT INTO sensor_data (entity_id, value, timestamp) VALUES (?, ?, ?)",
                    [
                        ("sensor_a", "10.0", "2026-07-25T10:00:00Z"),
                        ("sensor_b", "20.0", "2026-07-25T10:00:00Z"),
                        ("sensor_c", "30.0", "2026-07-25T10:00:00Z"),
                        ("sensor_d", "40.0", "2026-07-25T10:00:00Z"),
                        ("sensor_a", "11.0", "2026-07-25T10:01:00Z"),
                        ("sensor_b", "21.0", "2026-07-25T10:01:00Z"),
                        ("sensor_c", "31.0", "2026-07-25T10:01:00Z"),
                        ("sensor_d", "41.0", "2026-07-25T10:01:00Z"),
                    ],
                )

            model = train_model.train_model(db_path=db_path, output_path=output_path, n_clusters=2)

            self.assertTrue(output_path.exists())
            loaded_model = joblib.load(output_path)
            self.assertEqual(loaded_model.__class__.__name__, model.__class__.__name__)
            self.assertEqual(list(model.feature_names_in_), ["lux", "sun_elevation", "sun_azimuth"])


if __name__ == "__main__":
    unittest.main()
