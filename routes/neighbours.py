from fastapi import APIRouter, HTTPException

from classes.neighbours import NeighboursPayload
from database import insert_neighbours

router = APIRouter(prefix="/neighbours", tags=["nodes"])


@router.post("/insert")
async def neighbours_device(data: NeighboursPayload):
    try:
        insert_neighbours(data)
        return {"status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database insert failed: {str(e)}")
