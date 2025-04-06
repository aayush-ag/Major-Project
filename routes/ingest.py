from fastapi import APIRouter
from pydantic import BaseModel
from db import insert_or_update

router = APIRouter(prefix="/ingest", tags=["ingest"])

class IngestPayload(BaseModel):
    uid: str
    rssi: int

@router.post("/")
async def ingest_device(data: IngestPayload):
    insert_or_update(data.uid, data.rssi)
    return {"status": "received"}
