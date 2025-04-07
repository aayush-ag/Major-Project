from pydantic import BaseModel

class ChatRequest(BaseModel):
    nearest: str
    neighbour: list
    prompt: str