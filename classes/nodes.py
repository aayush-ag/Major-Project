from pydantic import BaseModel

class NodesPayload(BaseModel):
    uid: str
    location: str