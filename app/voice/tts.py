from gtts import gTTS
import tempfile

def speak(text: str):
    if not text:
        return None

    tts = gTTS(text=text, lang="en")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        return f.name
