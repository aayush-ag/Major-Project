from pydantic import BaseModel

class Neighbour(BaseModel):
    id: str
    rsid: int

class NeighboursPayload(BaseModel):
    node_id: str
    neighbours: list[Neighbour]