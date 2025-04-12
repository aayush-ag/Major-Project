from fastapi import APIRouter, UploadFile, File, Form
from datetime import datetime
import pytz
import whisper
import tempfile

from database import get_active_devices_with_info, get_neighbour_count_all_nodes
from ollama_infer import ask_model

router = APIRouter(prefix="/voicechat", tags=["chat"])

model = whisper.load_model("base")  # Or "small", "medium", "large" depending on accuracy vs speed

def get_time_info_ist():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    return {
        "time": now.strftime("%I:%M %p"),
        "day": now.strftime("%A"),
        "date": now.strftime("%Y-%m-%d")
    }

@router.post("/")
async def chat_with_audio(
    nearest: str = Form(...),
    name: str = Form(...),
    audio: UploadFile = File(...)
):
    # Save audio file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        contents = await audio.read()
        tmp.write(contents)
        tmp_path = tmp.name

    # Transcribe audio using Whisper
    transcript = model.transcribe(tmp_path)["text"]

    # Compose context
    time_info = get_time_info_ist()
    active_nodes = get_active_devices_with_info()
    neighbour_counts = get_neighbour_count_all_nodes()

    context = f"Nearest Node: {nearest}\n"
    context += f"Name of the student: {name}\n"
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

    # Final inference using Whisper transcription
    response = ask_model(transcript, context, name)
    return {"transcription": transcript, "response": response}
