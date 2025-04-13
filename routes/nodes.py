from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from classes.nodes import NodesPayload
from database import insert_or_update, get_active_devices

router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.post("/insert")
async def insert_node(data: NodesPayload):
    try:
        insert_or_update(data)
        return {"status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database insert failed: {str(e)}")

@router.get("/")
async def get_active_nodes():
    try:
        devices = get_active_devices()
        response = [{"id": row[0], "location": row[1]} for row in devices]
        return JSONResponse(content={"devices": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch active devices: {str(e)}")
