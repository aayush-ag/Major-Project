from fastapi import APIRouter
from pydantic import BaseModel
from db import insert_neighbours

router = APIRouter(prefix="/neighbours", tags=["nodes"])

class Neighbour(BaseModel):
    id: str
    rsid: int

class NeighboursPayload(BaseModel):
    node_id: str
    neighbours: list[Neighbour]

@router.post("/")
async def neighbours_device(data: NeighboursPayload):
    insert_neighbours(data.node_id, data.neighbours)
    return {"status": "received"}
