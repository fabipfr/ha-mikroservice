import sqlite3
from pathlib import Path
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib
import pandas as pd


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

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.round("1min")

    if df.empty:
        raise ValueError("No numeric values available for training")

    entity_ids = df["entity_id"].unique().tolist()
    training_frame = pd.DataFrame(columns=entity_ids, index=pd.date_range(start=df["timestamp"].min(), end=df["timestamp"].max(), freq="1min"))

    for entity_id in entity_ids:
        entity_values = (
            df.loc[df["entity_id"] == entity_id, ["timestamp", "value"]]
            .groupby("timestamp", as_index=False)
            .last()
            .set_index("timestamp")
        )
        training_frame[entity_id] = entity_values["value"].reindex(training_frame.index)

    # Forward-fill missing values so the last known value stays in place until a new value appears.
    training_frame = training_frame.ffill()

    if len(training_frame) < n_clusters:
        raise ValueError(f"Not enough rows for {n_clusters} clusters")

    for col in training_frame.columns:
        if col != "season" and col != "weather.state":
            training_frame[col] = pd.to_numeric(training_frame[col], errors='coerce')

    # Encode nominal categorical features for KMeans
    training_frame = pd.get_dummies(
        training_frame,
        columns=["weather.state", "season"],
        prefix=["weather_state", "season"],
        dummy_na=False,
    )

    # Ensure everything is numeric
    training_frame = training_frame.apply(pd.to_numeric, errors="coerce")

    # Impute missing values and standardize features

    imputer = SimpleImputer(strategy="median")
    training_frame = pd.DataFrame(
        imputer.fit_transform(training_frame),
        index=training_frame.index,
        columns=training_frame.columns,
    )

    scaler = StandardScaler()
    training_frame = pd.DataFrame(
        scaler.fit_transform(training_frame),
        index=training_frame.index,
        columns=training_frame.columns,
    )

    model = KMeans(n_clusters=n_clusters)
    model.fit(training_frame)

    joblib.dump(model, output_path)
    return model


if __name__ == "__main__":
    train_model()
