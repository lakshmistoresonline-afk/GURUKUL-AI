import requests
import json
import time

def test_model(model):
    print(f"Testing model: {model}...")
    start = time.time()
    try:
        response = requests.post("http://localhost:11434/api/generate",
                                json={"model": model, "prompt": "Hi", "stream": False},
                                timeout=120)
        print(f"Status: {response.status_code}")
        print(f"Time: {time.time() - start:.2f}s")
        print(f"Response: {response.json().get('response')}")
    except Exception as e:
        print(f"Error: {e}")

test_model("qwen3.5:2b-q4_K_M")
