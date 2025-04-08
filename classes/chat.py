from pydantic import BaseModel

class ChatRequest(BaseModel):
    nearest: str
    neighbour: list
    name: str
    prompt: str