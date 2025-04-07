from fastapi import APIRouter
from pydantic import BaseModel
from db import insert_or_update

router = APIRouter(prefix="/nodes", tags=["nodes"])

class NodesPayload(BaseModel):
    uid: str
    location: str

@router.post("/")
async def ingest_device(data: NodesPayload):
    insert_or_update(data.uid, data.location)
    return {"status": "received"}
