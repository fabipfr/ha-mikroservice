from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import EnvironmentFeatures, SensorData
from database import get_sensor_data_by_id, store_sensor_data
import joblib, math

app = FastAPI(
    version="1.1.0",
    title="Home Assistant Microservice"
)

model = joblib.load("ml_models/decision_tree_model.pkl")

@app.get("/", response_class=HTMLResponse)
def read_root():
    readme_path = Path(__file__).with_name("README.html")
    if readme_path.exists():
        return readme_path.read_text(encoding="utf-8")
    return "<h1>No README found</h1>"

@app.post("/environment/data")
def write_sensor_data(sensor_data: SensorData):
    row_id = store_sensor_data(sensor_data.model_dump())
    return {"message": "Sensor data received", "data": sensor_data, "stored_id": row_id}

@app.get("/environment/data/{row_id}")
def get_sensor_data(row_id: int):
    data = get_sensor_data_by_id(row_id)
    if data is None:
        return {"error": "Sensor data not found"}
    return data

@app.post("/environment")
def predict_environment(data: EnvironmentFeatures):
    lux_safe = max(data.sensor_lux, 1.0)

    lux_log = math.log10(lux_safe)
    elevation_scaled = data.sun_elevation / 6.0

    features = [[lux_log, elevation_scaled]]

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    confidence = float(max(probabilities))

    return {
        "label": prediction,
        "confidence": round(confidence, 4),
        "raw_inputs": {
            "sensor.lux": data.sensor_lux,
            "sun.elevation": data.sun_elevation
        }
    }