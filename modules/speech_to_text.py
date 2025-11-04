import whisper

def convert_audio_to_text(audio_path: str) -> str:
    model = whisper.load_model("medium")  # change to "small" or "medium" for better accuracy
    result = model.transcribe(audio_path, fp16=False, language="en")
    return result["text"]
