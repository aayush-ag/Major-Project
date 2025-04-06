from fastapi import APIRouter
from models import ChatRequest
from ollama_infer import ask_model

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
async def chat_with_context(data: ChatRequest):
    context = f"Nearest device: {data.nearest.id} ({data.nearest.rssi})\n"
    context += "Neighbors:\n" + "\n".join([f"- {d.id} ({d.rssi})" for d in data.neighbour])
    full_prompt = context + f"\n\nUser: {data.prompt}"
    response = ask_model(full_prompt)
    return {"response": response}
