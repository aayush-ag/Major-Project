from pydantic import BaseModel


class NodesPayload(BaseModel):
    id: str
    location: str
