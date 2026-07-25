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
