from fastapi import FastAPI
from models import SensorData
from database import store_sensor_data

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/environment/sensors")
def write_sensor_data(sensor_data: SensorData):
    row_id = store_sensor_data(sensor_data.model_dump())
    return {"message": "Sensor data received", "data": sensor_data, "stored_id": row_id}


@app.get("/environment")
def predict_environment(lux: float, sun_elevation: float, sun_azimut: float, season: str):
    # Here we will let the model predict the environment based on the submitted features.
    return {"prediction": "Day", "certainty": 0.95}