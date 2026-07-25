from pathlib import Path
from typing import Mapping

import joblib
import numpy as np
import pandas as pd

MODEL_PATH = Path(__file__).with_name("ml_models") / "kmeans.joblib"


def load_model(model_path: str | Path | None = None):
    path = Path(model_path or MODEL_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")
    return joblib.load(path)


def predict_environment(
    features: Mapping[str, float | str],
    model_path: str | Path | None = None,
) -> dict[str, float | str]:
    try:
        model = load_model(model_path)
    except FileNotFoundError:
        return {"prediction": "Unknown", "certainty": 0.0}

    frame = pd.DataFrame(
        [
            {
                "lux": float(features.get("lux", 0.0)),
                "sun_elevation": float(features.get("sun_elevation", 0.0)),
                "sun_azimut": float(features.get("sun_azimut", 0.0)),
            }
        ]
    )

    try:
        cluster = int(model.predict(frame)[0])
        distances = model.transform(frame)[0]
        certainty = float(max(1.0 / (1.0 + distances.min()), 0.0))
        prediction = f"Cluster {cluster}"
        return {"prediction": prediction, "certainty": round(certainty, 3)}
    except Exception:
        return {"prediction": "Unknown", "certainty": 0.0}
