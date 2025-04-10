from datetime import datetime

import pytz
from fastapi import APIRouter

from classes.chat import ChatRequest
from database import get_active_devices_with_info, get_neighbour_count_all_nodes
from ollama_infer import ask_model

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
    # Core context parts
    time_info = get_time_info_ist()
    active_nodes = get_active_devices_with_info()
    neighbour_counts = get_neighbour_count_all_nodes()

    # Compose context string
    context = f"Nearest Node: {data.nearest}\n"
    context += f"Name of the student: {data.name}\n"
    context += f"Current Date: {time_info['date']}, Day: {time_info['day']}, Time: {time_info['time']} IST\n"

    context += "\nActive Nodes:\n"
    if active_nodes:
        context += "\n".join([f"- ID: {d['id']}, Location: {d['location']}" for d in active_nodes])

    context += "\n\nEstimated People Count per Node:\n"
    if neighbour_counts:
        context += "\n".join([
            f"- {n['location']}: Estimated {n['count']} people present"
            for n in neighbour_counts
        ])
    else:
        context += "No data available for people counts in rooms."

    response = ask_model(data.prompt, context, data.name)
    return {"response": response}
