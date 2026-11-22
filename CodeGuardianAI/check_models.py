import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY est absente du fichier .env")

client = genai.Client(api_key=api_key)

print("Modèles disponibles pour generateContent :\n")

for model in client.models.list():
    if "generateContent" in (model.supported_actions or []):
        print(model.name)