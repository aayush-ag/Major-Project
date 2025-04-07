from pydantic import BaseModel


class BLEDevice(BaseModel):
    id: str
    rssi: int


class ChatRequest(BaseModel):
    nearest: str
    neighbour: list[BLEDevice]
    prompt: str
