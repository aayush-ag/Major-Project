from pydantic import BaseModel

class BLEDevice(BaseModel):
    id: str
    rssi: int

class NeighboursPayload(BaseModel):
    node_id: str
    neighbours: list[BLEDevice]