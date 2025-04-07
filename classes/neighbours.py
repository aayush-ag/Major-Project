from pydantic import BaseModel

class NeighboursPayload(BaseModel):
    node_id: str
    neighbours: int