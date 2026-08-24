import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:2b-q4_K_M"

payload = {
    "model": MODEL,
    "prompt": "Reply with YES only.",
    "stream": False
}

try:
    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
