import json
import os
import requests
import re
import time
from datetime import datetime

# CONFIGURATION
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_GEN = "gemma4:2b-it-qat"
MODEL_VAL = "qwen3.5:2b-q4_K_M"

PROGRESS_FILE = "D:/GURUKUL-AI/GENERATION_PROGRESS.json"
OUTPUT_ROOT = "D:/GURUKUL-AI/GENERATED_LEARNING_CONTENT"
LOG_FILE = "D:/GURUKUL-AI/GENERATION_PIPELINE.log"

def log(message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

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

    for attempt in range(3):
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=900)
            response.raise_for_status()
            res_json = response.json()
            return res_json.get("response", "")
        except Exception as e:
            log(f"Attempt {attempt+1} failed for {model}: {e}")
            time.sleep(10)
    return None

def clean_json_response(text):
    if not text: return None
    # Remove thought process blocks
    text = re.sub(r'<thought>.*?</thought>', '', text, flags=re.DOTALL)
    text = re.sub(r'Thinking Process:.*?\n\n', '', text, flags=re.DOTALL)

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

def validate_content(content, source_text):
    val_prompt = f"""Task: Audit if the following content is grounded in the text.
Return JSON: {{"is_valid": boolean, "hallucinations": ["list"], "notes": "..."}}

TEXT:
{source_text[:3000]}

CONTENT:
{json.dumps(content)[:2000]}
"""
    raw_val = ollama_generate(val_prompt, MODEL_VAL, system="Expert auditor. Output JSON only.", num_ctx=4096)
    json_val = clean_json_response(raw_val)
    if not json_val: return {"is_valid": False, "error": "No response from validator"}
    try:
        return json.loads(json_val)
    except Exception as e:
        log(f"Validation JSON decoding error: {e}")
        return {"is_valid": False, "raw_response": raw_val}

def process_chapter(entry):
    ch_id = entry['chapter_id']
    cls = entry['class']
    subject = entry['subject']
    source_path = entry['source_file']

    log(f"STARTING CHAPTER: {ch_id}")

    if not source_path or not os.path.exists(source_path):
        log(f"Error: Source file missing for {ch_id}")
        return False

    with open(source_path, 'r', encoding='utf-8') as f:
        source_text = f.read()

    rel_dir = f"class_{str(cls).zfill(2)}/{subject.lower().replace(' ', '_')}"
    out_dir = os.path.join(OUTPUT_ROOT, rel_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"{ch_id}.json")

    # 1. GENERATION
    log("STAGE 1: Generation (Gemma)")
    gen_prompt = f"""Generate educational JSON for {subject} Class {cls}.
Text: {source_text[:10000]}
Keys: concepts (id, name, desc), teacher_explanations (id -> {{WHAT, WHY, HOW, Example}}), quiz (question, options, correct_answer, explanation), flashcards, revision.
"""
    raw_gen = ollama_generate(gen_prompt, MODEL_GEN, system="Expert teacher. Output JSON only.")
    json_gen = clean_json_response(raw_gen)

    if not json_gen:
        log("Error: Generation failed to produce JSON")
        return False

    try:
        content = json.loads(json_gen)
    except Exception as e:
        log(f"Error: Failed to decode generation JSON: {e}")
        return False

    # 2. VALIDATION
    log("STAGE 2: Validation (Qwen)")
    validation = validate_content(content, source_text)

    # Check if validation passed
    if not validation.get('is_valid', False):
        log(f"Validation FAILED for {ch_id}. Notes: {validation.get('notes') or validation.get('error')}")
        # Save failed attempt for manual review/debugging
        final_package = {
            "metadata": {
                "chapter_id": ch_id, "status": "VALIDATION_FAILED",
                "generation": {"provider": "ollama", "model_gen": MODEL_GEN, "model_val": MODEL_VAL, "timestamp": datetime.now().isoformat()}
            },
            "learning_content": content,
            "validation_report": validation
        }
        with open(out_file + ".failed", 'w', encoding='utf-8') as f:
            json.dump(final_package, f, indent=2)
        return False # This will trigger another attempt in the main loop or mark as FAILED

    # 3. ASSEMBLY
    log("STAGE 3: Saving")
    final_package = {
        "metadata": {
            "chapter_id": ch_id, "class": cls, "subject": subject, "title": entry['title'],
            "source_provenance": {"source_file": source_path, "authority": "NCERT"},
            "generation": {"provider": "ollama", "model_gen": MODEL_GEN, "model_val": MODEL_VAL, "timestamp": datetime.now().isoformat()}
        },
        "learning_content": content,
        "validation_report": validation
    }

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(final_package, f, indent=2)

    entry['output_path'] = out_file
    entry['model_generation'] = MODEL_GEN
    entry['model_validation'] = MODEL_VAL
    entry['last_updated'] = datetime.now().isoformat()
    entry['validation_status'] = "PASS"

    log(f"COMPLETED CHAPTER: {ch_id}. Validation: PASS")
    return True

def main():
    if not os.path.exists(PROGRESS_FILE):
        log("Error: Progress file not found.")
        return

    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        progress = json.load(f)

    processed_count = 0
    for entry in progress:
        # Retry logic: Process if PENDING, PROCESSING (interrupted), or FAILED
        if entry['status'] in ["PENDING", "PROCESSING", "FAILED"]:
            entry['status'] = "PROCESSING"
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2)

            try:
                success = process_chapter(entry)
                entry['status'] = "COMPLETED" if success else "FAILED"
            except Exception as e:
                log(f"Critical error processing {entry['chapter_id']}: {e}")
                entry['status'] = "FAILED"
                entry['error'] = str(e)

            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2)

            if entry['status'] == "COMPLETED":
                processed_count += 1

            # Stop after 2 successful chapters in this run
            if processed_count >= 2:
                break

    log(f"Batch run complete. Successfully processed {processed_count} chapters.")

if __name__ == "__main__":
    main()
