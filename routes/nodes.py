from fastapi import APIRouter, HTTPException
from classes.nodes import NodesPayload
from database import insert_or_update

router = APIRouter(prefix="/nodes", tags=["nodes"])

@router.post("/")
async def ingest_device(data: NodesPayload):
    try:
        insert_or_update(data)
        return {"status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database insert failed: {str(e)}")