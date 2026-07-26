from pydantic import BaseModel

class SensorData(BaseModel):
    entity_id: str
    value: float | str
    timestamp: str

class EnvironmentFeatures(BaseModel):
    sensor_lux: float
    sun_elevation: float