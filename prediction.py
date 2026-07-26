from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).with_name("ml_models") / "kmeans.joblib"


def load_model(model_path: str | Path | None = None):
    path = Path(model_path or MODEL_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")
    loaded = joblib.load(path)
    if isinstance(loaded, dict):
        return loaded
    return {"model": loaded, "imputer": None, "scaler": None, "feature_columns": None}


def _build_feature_frame(features: dict[str, float | str]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "sensor.lux": float(features.get("sensor.lux", 0.0)),
                "sun.elevation": float(features.get("sun.elevation", 0.0)),
                "sun.azimuth": float(features.get("sun.azimuth", 0.0)),
                "season": features.get("season", ""),
            }
        ]
    )


def _transform_features_for_prediction(
    frame: pd.DataFrame,
    feature_columns: list[str] | None,
    imputer,
    scaler,
) -> pd.DataFrame:
    prepared_frame = frame.copy()

    for col in ["sensor.lux", "sun.elevation", "sun.azimuth"]:
        prepared_frame[col] = pd.to_numeric(prepared_frame[col], errors="coerce")

    prepared_frame = pd.get_dummies(
        prepared_frame,
        columns=["season"],
        prefix=["season"],
        dummy_na=False,
    )
    prepared_frame = prepared_frame.apply(pd.to_numeric, errors="coerce")

    if feature_columns is not None:
        prepared_frame = prepared_frame.reindex(columns=feature_columns, fill_value=0)

    if imputer is not None:
        prepared_frame = pd.DataFrame(
            imputer.transform(prepared_frame),
            index=prepared_frame.index,
            columns=prepared_frame.columns,
        )

    if scaler is not None:
        prepared_frame = pd.DataFrame(
            scaler.transform(prepared_frame),
            index=prepared_frame.index,
            columns=prepared_frame.columns,
        )

    return prepared_frame


def predict_environment(
    features: dict[str, float | str],
    model_path: str | Path | None = None,
) -> dict:
    try:
        bundle = load_model(model_path)
    except FileNotFoundError:
        return {"cluster": None, "error": "Model file not found"}

    frame = _build_feature_frame(features)
    model = bundle.get("model")

    if model is None:
        return {"cluster": None, "error": "Model data could not be loaded"}

    try:
        prepared_frame = _transform_features_for_prediction(
            frame,
            bundle.get("feature_columns"),
            bundle.get("imputer"),
            bundle.get("scaler"),
        )
        cluster = int(model.predict(prepared_frame)[0])
        return {"cluster": cluster}
    except Exception:
        return {"cluster": None, "error": "Prediction failed due to invalid input features"}
