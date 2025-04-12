import whisper

model = whisper.load_model("base")  # or "medium", "large"
result = model.transcribe("Test-01.mp3")  # or .wav, .m4a, etc.

print(result["text"])
