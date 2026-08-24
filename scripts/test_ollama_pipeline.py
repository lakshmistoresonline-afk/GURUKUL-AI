import json
import os
import requests
import re
from datetime import datetime

# CONFIGURATION
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_GEN = "gemma4:2b-it-qat"
MODEL_VAL = "qwen3.5:2b-q4_K_M"

# SOURCE DATA
SOURCE_FILE = "D:/GURUKUL-AI/JSON FILES/GURUKUL_AI_CLASS5_COMPLETE_FINAL_PACKAGE_V3/SOURCE_TEXT/class_05_EVS_eeev101.txt"
OUTPUT_DIR = "D:/GURUKUL-AI/GENERATED_LEARNING_CONTENT/TEST"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def log(message):
    print(f"[{datetime.now().isoformat()}] {message}")

def ollama_generate(prompt, model, system=None, num_ctx=16384):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": num_ctx,
            "temperature": 0.1
        }
    }
    if system:
        payload["system"] = system

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=900)
        response.raise_for_status()
        res_json = response.json()
        return res_json.get("response", "")
    except Exception as e:
        log(f"Ollama error ({model}): {str(e)}")
        return None

def clean_json_response(text):
    if not text: return None
    text = text.replace('```json', '').replace('```', '').strip()

    first_brace = text.find('{')
    first_bracket = text.find('[')
    last_brace = text.rfind('}')
    last_bracket = text.rfind(']')

    start, end = -1, -1
    if first_brace != -1 and (first_bracket == -1 or first_brace < first_bracket):
        start, end = first_brace, last_brace
    elif first_bracket != -1:
        start, end = first_bracket, last_bracket

    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    return text

def run_test():
    log("Starting Model Verification Test")
    log(f"GEN: {MODEL_GEN}")
    log(f"VAL: {MODEL_VAL}")

    if not os.path.exists(SOURCE_FILE):
        log(f"Error: Source file not found at {SOURCE_FILE}")
        return

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        source_text = f.read()

    # 1. GENERATION
    log(f"STEP 1: Generating content using {MODEL_GEN}")
    gen_prompt = f"Generate a JSON object for Class 5 EVS. Keys: 'explanation' (Importance of water), 'quiz_item'. TEXT: {source_text[:500]}"
    generated_raw = ollama_generate(gen_prompt, MODEL_GEN, system="Output ONLY valid JSON.")
    generated_json_str = clean_json_response(generated_raw)

    if not generated_json_str:
        log("Error: Generation failed")
        return

    generated_data = json.loads(generated_json_str)
    log("Content generated successfully.")

    # 2. VALIDATION
    log(f"STEP 2: Validating content using {MODEL_VAL}")
    val_prompt = f"Is this content factually correct according to the text? CONTENT: {json.dumps(generated_data)} TEXT: {source_text[:500]} Answer as JSON: {{\"is_valid\": true/false}}"
    validation_raw = ollama_generate(val_prompt, MODEL_VAL, system="Output ONLY JSON.")
    validation_json_str = clean_json_response(validation_raw)

    if not validation_json_str:
        log("Error: Validation failed")
        return

    validation_data = json.loads(validation_json_str)
    log(f"Validation result: {validation_data.get('is_valid')}")

    log("Model Verification Test Complete.")

if __name__ == "__main__":
    run_test()
