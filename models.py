from pydantic import BaseModel

class SensorData(BaseModel):
    entity_id: str
    value: float | str
    timestamp: str