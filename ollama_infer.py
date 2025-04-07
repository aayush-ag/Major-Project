import os
import json
import ollama
from datetime import datetime
import pytz

CONTEXT_DIR = "context"  # Your folder with .txt, .json etc.

def load_context_files():
    combined_context = ""
    for filename in os.listdir(CONTEXT_DIR):
        if filename == "llm.txt":
            continue  # Skip llm.txt (used as template only)

        path = os.path.join(CONTEXT_DIR, filename)
        if filename.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                combined_context += f"\n\n--- {filename} ---\n"
                combined_context += f.read()
        elif filename.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                combined_context += f"\n\n--- {filename} ---\n"
                combined_context += json.dumps(data, indent=2)
    return combined_context

def get_time_info_ist():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    return {
        "time": now.strftime("%I:%M %p"),
        "day": now.strftime("%A"),
        "date": now.strftime("%Y-%m-%d")
    }

def build_prompt(user_prompt: str) -> str:
    context = load_context_files()
    time_info = get_time_info_ist()

    template_path = os.path.join(CONTEXT_DIR, "llm.txt")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        full_prompt = template.format(
            context=context,
            user_prompt=user_prompt,
            time=time_info["time"],
            day=time_info["day"],
            date=time_info["date"]
        )
    else:
        full_prompt = user_prompt
    return full_prompt

def ask_model(user_prompt: str) -> str:
    prompt = build_prompt(user_prompt)
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response
