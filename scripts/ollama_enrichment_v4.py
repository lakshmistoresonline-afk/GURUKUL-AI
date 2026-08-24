import json
import os
import requests
import time
import re
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_SIMPLE = "qwen3.5:2b-q4_K_M"
MODEL_CONTENT = "gemma4:2b-it-qat"

PROGRESS_FILE = "D:/GURUKUL-AI/OLLAMA_REGENERATION_PROGRESS.json"
LOG_FILE = "D:/GURUKUL-AI/OLLAMA_REGENERATION.log"

def log(message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def ollama_generate(prompt, model=MODEL_CONTENT, system=None):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 16384,
            "temperature": 0.1
        }
    }
    if system:
        payload["system"] = system

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=900)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        log(f"Ollama error: {str(e)}")
        return None

def clean_json_response(text):
    if not text: return "[]"
    # Find the content between [ ] or { }
    text = text.replace('```json', '').replace('```', '').strip()
    match_list = re.search(r'\[.*\]', text, re.DOTALL)
    if match_list: return match_list.group(0)
    match_obj = re.search(r'\{.*\}', text, re.DOTALL)
    if match_obj: return match_obj.group(0)
    return text

def process_unit(unit_entry):
    unit_id = unit_entry['unit_id']
    path = unit_entry['package_path']
    cls = unit_entry['class']
    subj = unit_entry['subject']

    log(f"\n==================================================")
    log(f"GURUKUL AI — OLLAMA CONTENT REGENERATION")
    log(f"Unit: {unit_id} | Class: {cls} | Subject: {subj}")
    log(f"==================================================\n")

    with open(path, 'r', encoding='utf-8') as f:
        package = json.load(f)

    raw_text = package.get("content", {}).get("summary", "") or package.get("content", {}).get("introduction", "")

    # 1. Title Cleaning
    log("STAGE: Metadata Cleaning")
    cleaned_title = ollama_generate(f"Clean this chapter title: {package['metadata']['chapterTitle']}. No indd, no page numbers.", model=MODEL_SIMPLE).strip().strip('"')
    package['metadata']['chapterTitle'] = cleaned_title
    log(f"Cleaned Title: {cleaned_title}")

    # 2. Granular Concept Extraction
    log("STAGE: Concept Extraction")
    if not package['content'].get('concepts'):
        sys_concept = "You are an expert curriculum designer. Extract 5-15 granular learning concepts from the text. Return as JSON array of {id, name, description}."
        concepts_raw = ollama_generate(f"Extract concepts from: {raw_text[:10000]}", system=sys_concept)
        concepts = json.loads(clean_json_response(concepts_raw))
        package['content']['concepts'] = concepts
        log(f"Extracted {len(concepts)} concepts")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2)
    else:
        concepts = package['content']['concepts']
        log(f"Using {len(concepts)} existing concepts")


    # 3. Subject Knowledge & Explanations
    log("STAGE: Pedagogical Enrichment")
    if not package['content'].get('subject_knowledge'):
        sk_prompt = f"Identify all subject-specific knowledge items for the subject '{subj}'. You MUST include: 1. Core Concepts, 2. Case Studies mentioned in text, 3. Key Roles/Responsibilities. Return as JSON array of {{category, content}}. Text: {raw_text[:8000]}"
        sk_raw = ollama_generate(sk_prompt, system="Output ONLY valid JSON array. Categorize as 'CONCEPT', 'CASE_STUDY', or 'ROLE'.")
        package['content']['subject_knowledge'] = json.loads(clean_json_response(sk_raw))
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2)

    for concept in concepts:
        if concept.get('teacher_explanation'):
            log(f"  - Skipping (already explained): {concept['name']}")
            continue
        log(f"  - Explaining: {concept['name']}")
        expl_prompt = f"You are a master teacher. Provide a deep explanation of '{concept['name']}' for a {cls} student. Include: 1. Simple Definition, 2. Detailed Teacher Explanation, 3. Real-world Example. Source: {raw_text[:5000]}"
        concept['teacher_explanation'] = ollama_generate(expl_prompt)
        # Periodic save
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2)

    # 4. Assessment
    log("STAGE: Assessment Generation")
    if not package['content'].get('quiz') or len(package['content']['quiz']) < 5:
        ids = [c['id'] for c in concepts]
        q_prompt = f"""Create 10 high-quality quiz items for this chapter.
Required keys: 'question', 'options' (if MCQ), 'correct_answer' (REAL ANSWER), 'explanation' (Step-by-step reasoning), 'concept_id' (one of {ids}), 'difficulty'.
DO NOT use 'Refer to text'. Provide actual factual answers.
Text: {raw_text[:12000]}"""
        q_raw = ollama_generate(q_prompt, system="Output ONLY valid JSON array.")
        package['content']['quiz'] = json.loads(clean_json_response(q_raw))
        log(f"Generated {len(package['content']['quiz'])} questions")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2)

    # 5. Flashcards & Revision
    log("STAGE: Flashcards & Revision")
    if not package['content'].get('flashcards'):
        fc_raw = ollama_generate(f"Create 10 flashcards (front, back) for: {raw_text[:5000]}", system="Output ONLY valid JSON array.")
        package['content']['flashcards'] = json.loads(clean_json_response(fc_raw))
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2)

    if not package['content'].get('revision'):
        rev_raw = ollama_generate(f"Create Quick, Standard, and Detailed revision notes for: {raw_text[:5000]}", system="Output ONLY JSON object with keys 'quick', 'standard', 'detailed'.")
        package['content']['revision'] = json.loads(clean_json_response(rev_raw))
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2)

    # 6. Mastery Map
    log("STAGE: Mastery Map")

    mastery_map = {"chapterId": unit_id, "concepts": []}
    for concept in concepts:
        c_id = concept['id']
        q_ids = [f"q_{i}" for i, q in enumerate(package['content']['quiz']) if q.get('concept_id') == c_id]
        mastery_map['concepts'].append({
            "conceptId": c_id, "conceptName": concept['name'],
            "assessmentEvidence": {"questionIdsByLevel": {"foundation": q_ids}}
        })

    # Save files
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(package, f, indent=2)

    # Update chapter_metadata.json
    metadata_path = os.path.join(os.path.dirname(path), "chapter_metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        meta['title'] = cleaned_title
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2)

    with open(os.path.join(os.path.dirname(path), "mastery_map.json"), 'w', encoding='utf-8') as f:
        json.dump(mastery_map, f, indent=2)

    log(f"COMPLETE: {unit_id}")
    return True

if __name__ == "__main__":
    import sys

    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        progress = json.load(f)

    if len(sys.argv) > 1:
        target_id = sys.argv[1]
        for entry in progress:
            if entry['unit_id'] == target_id:
                entry['status'] = "PROCESSING"
                entry['started_at'] = datetime.now().isoformat()
                with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(progress, f, indent=2)

                try:
                    if process_unit(entry):
                        entry['status'] = "COMPLETED"
                        entry['completed_at'] = datetime.now().isoformat()
                        entry['validation_status'] = "PASS"
                    else:
                        entry['status'] = "FAILED"
                except Exception as e:
                    log(f"CRITICAL ERROR: {str(e)}")
                    entry['status'] = "FAILED"
                    entry['error'] = str(e)

                with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(progress, f, indent=2)
                break
    else:
        # Default behavior: process first pending unit
        for entry in progress:
            if entry['status'] == "PENDING":
                # ... existing logic ...
                pass



