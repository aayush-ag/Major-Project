import json
import os

import ollama

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


def build_prompt(user_prompt: str, injected_context: str = "") -> str:
    # Load all static context files from context/
    static_context = load_context_files()

    # Combine static and dynamic context
    full_context = f"{static_context}\n\n--- Runtime Context ---\n{injected_context}".strip()

    # Load template
    template_path = os.path.join(CONTEXT_DIR, "llm.txt")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        full_prompt = template.format(
            context=full_context,
            user_prompt=user_prompt
        )
    else:
        full_prompt = f"{full_context}\n\n{user_prompt}"

    return full_prompt

OLLAMA_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

# Tell the Ollama client where the API lives
ollama.base_url = OLLAMA_BASE

def ask_model(user_prompt: str, injected_context: str = "") -> str:
    prompt = build_prompt(user_prompt, injected_context)
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.get("message", {}).get("content", "No response from model.")
