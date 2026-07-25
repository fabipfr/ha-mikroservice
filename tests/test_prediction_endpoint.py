import importlib
import unittest

import main


class PredictionEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.main = importlib.reload(main)

    def test_predict_environment_returns_default_prediction(self) -> None:
        payload = {
            "lux": 300.0,
            "sun_elevation": 45.0,
            "sun_azimut": 120.0,
            "season": "summer",
        }

        response = self.main.predict_environment(
            self.main.EnvironmentFeatures(**payload)
        )

        self.assertEqual(response["prediction"], "Day")
        self.assertEqual(response["certainty"], 0.95)


if __name__ == "__main__":
    unittest.main()
