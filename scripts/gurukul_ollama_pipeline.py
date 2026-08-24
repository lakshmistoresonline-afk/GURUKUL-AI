import json
import os
import requests
import time
import re
from datetime import datetime

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_GENERATION = "gemma4:e2b-it-qat"
MODEL_VALIDATION = "qwen3.5:2b-q4_K_M"

PROGRESS_FILE = "D:/GURUKUL-AI/GENERATION_PROGRESS.json"
OUTPUT_BASE_DIR = "D:/GURUKUL-AI/GENERATED_LEARNING_CONTENT"
LOG_FILE = "D:/GURUKUL-AI/scripts/gurukul_pipeline.log"

def log(message):
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {message}"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry + "\n")
    print(log_entry)

def ollama_call(prompt, model, system=None, temperature=0.1):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 16384,
            "temperature": temperature
        }
    }
    if system:
        payload["system"] = system

    log(f"Calling Ollama | Model: {model} | Prompt length: {len(prompt)}")
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=1200)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        log(f"Ollama error ({model}): {str(e)}")
        return None

def extract_json(text):
    if not text: return None
    # Remove markdown code blocks if present
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()

    # Try to find the first [ or {
    start_bracket = text.find('[')
    start_brace = text.find('{')

    if start_bracket != -1 and (start_brace == -1 or start_bracket < start_brace):
        end = text.rfind(']')
        if end != -1:
            return text[start_bracket:end+1]
    elif start_brace != -1:
        end = text.rfind('}')
        if end != -1:
            return text[start_brace:end+1]
    return text

def validate_content(generated_content, source_text):
    system_prompt = f"""You are a Fact-Checker and Validator for educational content.
Your task is to verify the generated content against the source text.
Rules:
1. Ensure every factual claim is grounded in the source text.
2. Check for pedagogical appropriateness for the specified class.
3. Verify that the JSON structure is valid.
4. If an item is hallucinated (not in source), mark it for removal or correction.
5. Provide a 'validation_score' (0-100) and a list of 'corrections'.

Source Text:
{source_text[:8000]}
"""
    prompt = f"Validate the following generated JSON content:\n{generated_content}"

    response = ollama_call(prompt, MODEL_VALIDATION, system=system_prompt)
    return response

def process_chapter(entry):
    cls = entry['class']
    subj = entry['subject']
    chapter_id = entry['chapter_id']
    title = entry['title']
    source_path = entry['source_file']

    if not source_path or not os.path.exists(source_path):
        log(f"Source file not found: {source_path}")
        return False

    log(f"Processing Chapter: {chapter_id} - {title} (Class {cls}, {subj})")

    with open(source_path, 'r', encoding='utf-8') as f:
        source_text = f.read()

    # Stage 1: Generation
    gen_system = f"""You are a Master Curriculum Developer. Create comprehensive learning content based ONLY on the provided source text.
Output MUST be a single JSON object with these keys:
- concepts: array of {{name, definition, explanation, source_quote}}
- examples: array of {{concept_name, example_text, source_quote}}
- quiz: array of {{question, options, correct_answer, explanation, source_quote}}
- flashcards: array of {{front, back, source_quote}}
- revision_notes: {{quick: [], standard: [], detailed: []}}

Class: {cls}
Subject: {subj}
"""
    gen_prompt = f"Source Text:\n{source_text[:12000]}\n\nGenerate the learning content JSON."

    raw_generation = ollama_call(gen_prompt, MODEL_GENERATION, system=gen_system)
    if not raw_generation:
        return False

    json_str = extract_json(raw_generation)
    try:
        content_data = json.loads(json_str)
    except Exception as e:
        log(f"JSON Parse Error in Generation: {str(e)}")
        # Fallback: maybe just save raw if failed
        content_data = {"raw_generation": raw_generation, "error": str(e)}

    # Stage 2: Validation
    validation_report = validate_content(json_str, source_text)

    final_output = {
        "metadata": {
            "class": cls,
            "subject": subj,
            "chapter_id": chapter_id,
            "title": title,
            "generated_at": datetime.now().isoformat(),
            "models": {
                "generation": MODEL_GENERATION,
                "validation": MODEL_VALIDATION
            }
        },
        "content": content_data,
        "validation_report": validation_report
    }

    # Save Output
    output_dir = os.path.join(OUTPUT_BASE_DIR, f"class_{cls:02d}", f"subject_{subj.replace(' ', '_')}")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"chapter_{chapter_id}.json")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)

    entry['output_path'] = output_path
    entry['model_generation'] = MODEL_GENERATION
    entry['model_validation'] = MODEL_VALIDATION
    log(f"Saved content to {output_path}")
    return True

def main():
    if not os.path.exists(PROGRESS_FILE):
        log(f"Progress file {PROGRESS_FILE} not found.")
        return

    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        progress = json.load(f)

    for entry in progress:
        if entry['status'] == "PENDING":
            entry['status'] = "PROCESSING"
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2)

            try:
                success = process_chapter(entry)
                if success:
                    entry['status'] = "COMPLETED"
                else:
                    entry['status'] = "FAILED"
            except Exception as e:
                log(f"Critical error processing {entry['chapter_id']}: {str(e)}")
                entry['status'] = "FAILED"

            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2)

            # For this initialization, we only process the first one as requested
            break

if __name__ == "__main__":
    main()
