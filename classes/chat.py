from pydantic import BaseModel

class ChatRequest(BaseModel):
    nearest: str
    name: str
    prompt: str