from fastapi import FastAPI
from pydantic import BaseModel
from models.emotion_model import EmotionModel
from models.musicgen_model import MusicGenerator
from utils.mapping import emotion_to_prompt
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os


if not os.path.exists("generated"):
    os.makedirs("generated")

app = FastAPI()

app.mount("/static", StaticFiles(directory="generated"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

emotion_model = EmotionModel()
music_model = MusicGenerator()

class TextInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


@app.post("/generate_music/")
async def generate_music(input_data: TextInput):
    # Emotion classification
    emotion = emotion_model.predict_emotion(input_data.text)
    prompt = emotion_to_prompt.get(emotion, "calm instrumental music")

    # Generate 3 DIFFERENT music tracks
    paths = music_model.generate_variants(prompt, num_variants=3)

    # Convert to public URLs
    urls = [
        f"http://localhost:8000/static/{os.path.basename(p)}"
        for p in paths
    ]

    return {
        "emotion": emotion,
        "prompt": prompt,
        "tracks": urls
    }
