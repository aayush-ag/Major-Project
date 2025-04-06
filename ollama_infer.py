import subprocess

def ask_model(prompt: str) -> str:
    result = subprocess.run([
        "ollama", "run", "mistral"  # or your model name
    ], input=prompt.encode(), capture_output=True)
    return result.stdout.decode(errors="ignore")
