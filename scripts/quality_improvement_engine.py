import json
import os
import shutil
import requests
import re
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_CONTENT = "gemma4:2b-it-qat"

PROGRESS_FILE = "D:/GURUKUL-AI/OLLAMA_QUALITY_IMPROVEMENT_PROGRESS.json"
LOG_FILE = "D:/GURUKUL-AI/OLLAMA_QUALITY_IMPROVEMENT.log"
BACKUP_ROOT = "D:/GURUKUL-AI/backend/GURUKUL_AI_CONTENT_BACKUP"

def log(message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def ollama_generate(prompt, system=None):
    payload = {
        "model": MODEL_CONTENT,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": 32768, "temperature": 0.1}
    }
    if system: payload["system"] = system
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=600)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        log(f"Ollama error: {str(e)}")
        return None

def clean_json_response(text):
    if not text: return "[]"
    text = text.replace('```json', '').replace('```', '').strip()
    match_list = re.search(r'\[.*\]', text, re.DOTALL)
    if match_list: return match_list.group(0)
    match_obj = re.search(r'\{.*\}', text, re.DOTALL)
    if match_obj: return match_obj.group(0)
    return text

def update_mastery_map(package_path, concepts, quiz):
    mastery_path = package_path.replace("package.json", "mastery_map.json")
    if not os.path.exists(mastery_path):
        # Create new if missing
        mastery_data = {"chapterId": os.path.basename(os.path.dirname(package_path)), "concepts": []}
    else:
        with open(mastery_path, 'r', encoding='utf-8') as f:
            mastery_data = json.load(f)

    # Rebuild concepts list to ensure alignment
    new_mastery_concepts = []
    for c in concepts:
        c_id = c['id']
        # Find questions mapped to this concept
        mapped_qs = [q['id'] for q in quiz if q.get('concept_id') == c_id or q.get('conceptId') == c_id]

        new_mastery_concepts.append({
            "conceptId": c_id,
            "conceptName": c['name'],
            "assessmentEvidence": {
                "questionIdsByLevel": {
                    "foundation": mapped_qs[:int(len(mapped_qs)*0.6)] if mapped_qs else [],
                    "application": mapped_qs[int(len(mapped_qs)*0.6):int(len(mapped_qs)*0.9)] if mapped_qs else [],
                    "mastery": mapped_qs[int(len(mapped_qs)*0.9):] if mapped_qs else []
                }
            }
        })

    mastery_data['concepts'] = new_mastery_concepts
    with open(mastery_path, 'w', encoding='utf-8') as f:
        json.dump(mastery_data, f, indent=2)
    return True

def process_unit(unit_entry):
    unit_id = unit_entry['unit_id']
    path = unit_entry['package_path']
    cls = unit_entry['class']
    subj = unit_entry['subject']

    log(f"\n==================================================")
    log(f"GURUKUL AI QUALITY IMPROVEMENT - PROCESSING {unit_id}")
    log(f"==================================================")

    # 1. Backup
    rel_path = os.path.relpath(path, "D:/GURUKUL-AI/backend/GURUKUL_AI_CONTENT")
    dst_path = os.path.normpath(os.path.join(BACKUP_ROOT, rel_path))
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    if not os.path.exists(dst_path):
        shutil.copy2(path, dst_path)
        src_mastery = path.replace("package.json", "mastery_map.json")
        if os.path.exists(src_mastery):
            dst_mastery = dst_path.replace("package.json", "mastery_map.json")
            shutil.copy2(src_mastery, dst_mastery)
        log(f"Backup created: {dst_path}")
    unit_entry['backup_created'] = True

    with open(path, 'r', encoding='utf-8') as f:
        package = json.load(f)

    raw_text = package.get("content", {}).get("summary", "") or package.get("content", {}).get("introduction", "")
    concepts = package.get('content', {}).get('concepts', [])
    quiz = package.get('content', {}).get('quiz', [])

    # 2. Add Granular Concepts if count is low (< 4)
    if len(concepts) < 4:
        log("STAGE: EXTRACTING GRANULAR CONCEPTS")
        concept_prompt = f"Extract 5-10 granular learning concepts from the text. Return as JSON array of {{id, name, description}}. Text: {raw_text[:12000]}"
        new_concepts_raw = ollama_generate(concept_prompt, system="Expert curriculum designer. Output ONLY valid JSON array.")
        try:
            new_concepts = json.loads(clean_json_response(new_concepts_raw))
            if isinstance(new_concepts, list) and len(new_concepts) > 0:
                package['content']['concepts'] = new_concepts
                concepts = new_concepts
                log(f"  Updated to {len(concepts)} granular concepts.")
        except: log("  Failed to extract concepts")

    # 3. Enrich Teacher Explanations
    log("STAGE: ENRICHING TEACHER EXPLANATIONS")
    for concept in concepts:
        current_expl = concept.get('teacher_explanation', "")
        if len(current_expl) < 250 or "What:" not in current_expl:
            log(f"  Enriching explanation for: {concept['name']}")
            prompt = f"""Expand this explanation for {cls} student.
Include labels: WHAT it is, WHY it matters, HOW it works, an EXAMPLE, and a COMMON MISTAKE.
Existing: {current_expl}
Text: {raw_text[:6000]}"""
            enriched = ollama_generate(prompt)
            if enriched: concept['teacher_explanation'] = enriched

    # 4. Fix placeholders in quiz
    log("STAGE: REPAIRING QUIZ PLACEHOLDERS")
    for q in quiz:
        ans = str(q.get('answer', q.get('correct_answer', "")))
        if any(p in ans for p in ["Refer to the source", "Refer to text", "Answers may vary"]):
            log(f"  Fixing answer for: {q['question'][:50]}...")
            fix_prompt = f"Provide a factual answer and reasoning for this question based on the text. Return JSON with 'answer' and 'explanation'.\nQuestion: {q['question']}\nText: {raw_text[:5000]}"
            fixed_raw = ollama_generate(fix_prompt, model=MODEL_SIMPLE)
            try:
                fixed = json.loads(clean_json_response(fixed_raw))
                if 'answer' in q: q['answer'] = fixed['answer']
                if 'correct_answer' in q: q['correct_answer'] = fixed['answer']
                q['explanation'] = fixed.get('explanation', "Grounded in chapter text.")
            except: pass

    # 5. Add more questions if < 10
    if len(quiz) < 10:
        log("STAGE: ADDING MORE QUESTIONS")
        ids = [c['id'] for c in concepts]
        prompt = f"Generate 5-10 high-quality questions. JSON array of {{id, question, options, correct_answer, explanation, concept_id, difficulty}}. Concept IDs must be from: {ids}. Text: {raw_text[:12000]}"
        more_q_raw = ollama_generate(prompt, system="Expert examiner. Output ONLY valid JSON array.")
        try:
            more_q = json.loads(clean_json_response(more_q_raw))
            package['content']['quiz'] = quiz + more_q
            quiz = package['content']['quiz']
        except: pass

    # 6. Save and Sync Mastery
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(package, f, indent=2)

    update_mastery_map(path, concepts, quiz)

    log(f"COMPLETE: {unit_id}")
    return True

if __name__ == "__main__":
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        progress = json.load(f)

    for entry in progress:
        if entry['status'] == "PENDING":
            entry['status'] = "PROCESSING"
            if process_unit(entry):
                entry['status'] = "COMPLETED"
            else:
                entry['status'] = "FAILED"

            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2)
            break
