from pydantic import BaseModel
from chat import BLEDevice

class NeighboursPayload(BaseModel):
    node_id: str
    neighbours: list[BLEDevice]