from pydantic import BaseModel

class SensorData(BaseModel):
    entity_id: str
    value: float | str
    timestamp: str

class EnvironmentFeatures(BaseModel):
    lux: float
    sun_elevation: float
    sun_azimuth: float
    season: str