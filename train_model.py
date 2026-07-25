import sqlite3
from pathlib import Path

import joblib
import pandas as pd
from sklearn.cluster import KMeans


def train_model(
    db_path: str | Path = "sensor_data.db",
    output_path: str | Path = "ml_models/kmeans.joblib",
    n_clusters: int = 4,
) -> KMeans:
    db_path = Path(db_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(
            """
            SELECT entity_id, value, timestamp
            FROM sensor_data
            ORDER BY timestamp
            """,
            conn,
        )

    if df.empty:
        raise ValueError("No rows found in the database")

    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])

    if df.empty:
        raise ValueError("No numeric values available for training")

    pivot = df.pivot_table(index="timestamp", columns="entity_id", values="value").fillna(0)

    if len(pivot) < n_clusters:
        raise ValueError(f"Not enough rows for {n_clusters} clusters")

    feature_columns = list(pivot.columns)
    training_frame = pd.DataFrame(index=pivot.index)
    training_frame["lux"] = pivot[feature_columns[0]] if feature_columns else 0
    training_frame["sun_elevation"] = (
        pivot[feature_columns[1]] if len(feature_columns) > 1 else 0
    )
    training_frame["sun_azimut"] = (
        pivot[feature_columns[2]] if len(feature_columns) > 2 else 0
    )
    training_frame = training_frame.fillna(0)

    model = KMeans(n_clusters=n_clusters, random_state=42)
    model.fit(training_frame)

    joblib.dump(model, output_path)
    return model


if __name__ == "__main__":
    train_model()
