from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import EnvironmentFeatures, SensorData
from database import store_sensor_data

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root():
    readme_path = Path(__file__).with_name("README.html")
    if readme_path.exists():
        return readme_path.read_text(encoding="utf-8")
    return "<h1>No README found</h1>"

@app.post("/environment/sensors")
def write_sensor_data(sensor_data: SensorData):
    row_id = store_sensor_data(sensor_data.model_dump())
    return {"message": "Sensor data received", "data": sensor_data, "stored_id": row_id}

@app.post("/environment")
def predict_environment(environment_features: EnvironmentFeatures):
    # Here we will let the model predict the environment based on the submitted features.
    return {"prediction": "Day", "certainty": 0.95}