from fastapi import APIRouter
from classes.chat import ChatRequest
from ollama_infer import ask_model
from datetime import datetime
import pytz

router = APIRouter(prefix="/chat", tags=["chat"])

def get_time_info_ist():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    return {
        "time": now.strftime("%I:%M %p"),
        "day": now.strftime("%A"),
        "date": now.strftime("%Y-%m-%d")
    }
@router.post("/")
async def chat_with_context(data: ChatRequest):
    context = f"Nearest device: {data.nearest} . "
    time_info = get_time_info_ist()
    context += "Current Time:Date: {date} Day: {day} Time: {time} in IST."
    context += "Neighbors:\n" + "\n".join([f"- {d.id} ({d.rssi})" for d in data.neighbour])
    full_prompt = context + f"\n\nUser: {data.prompt}"
    response = ask_model(full_prompt)
    return {"response": response}
