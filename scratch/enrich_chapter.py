import json
import subprocess
import os
import sys

def enrich(unit_id, model="qwen3.5:2b-q4_K_M"):
    base_path = f"D:/GURUKUL-AI/backend/GURUKUL_AI_CONTENT/class_05/english/chapters/{unit_id}/"
    pkg_path = os.path.join(base_path, "package.json")

    if not os.path.exists(pkg_path):
        print(f"Error: {pkg_path} not found")
        return

    with open(pkg_path, "r", encoding="utf-8") as f:
        pkg_data = json.load(f)

    prompt = f"""You are an expert curriculum designer. Improve the following Class 5 English chapter content (Unit {unit_id}).

Current Content:
{json.dumps(pkg_data, indent=2)}

Requirements:
1. Concepts: Identify at least 8 granular concepts. Currently there are {len(pkg_data['content']['concepts'])}. Add more or split existing ones.
2. Teacher Explanation: For EVERY concept in the final list, provide a structured explanation in the 'teacher_explanation' string using exactly these 5 components:
   - What: Definition or description.
   - Why: Importance or relevance.
   - How: Process or mechanism.
   - Example: A concrete example from the text or real life.
   - Mistake: A common misconception or error students make.
   Use Markdown headers for each concept in the 'teacher_explanation' string.
3. Questions: Increase total questions in 'quiz' to at least 20. Ensure they map to the new concepts. No 'Refer to source' answers.
4. Content Consistency: Update 'flashcards', 'revision', and 'concepts' to reflect the enriched content.
5. Return only the final improved JSON object. No conversational text.
"""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 4096,
            "temperature": 0.1
        }
    }

    payload_path = f"D:/GURUKUL-AI/scratch/payload_{unit_id}.json"
    with open(payload_path, "w", encoding="utf-8") as f:
        json.dump(payload, f)

    response_path = f"D:/GURUKUL-AI/scratch/response_{unit_id}.json"
    subprocess.run(["curl", "-s", "-X", "POST", "http://localhost:11434/api/generate", "-d", f"@{payload_path}", "-o", response_path])

    if os.path.exists(response_path):
        with open(response_path, "r", encoding="utf-8") as f:
            try:
                resp = json.load(f)
            except Exception as e:
                print(f"Error loading response JSON: {e}")
                return

            text = resp.get('response', "")
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            try:
                improved_pkg = json.loads(text.strip())
                output_path = f"D:/GURUKUL-AI/scratch/{unit_id}_improved.json"
                with open(output_path, "w", encoding="utf-8") as out_f:
                    json.dump(improved_pkg, out_f, indent=2)
                print(f"Success: Improved package saved to {output_path}")
            except Exception as e:
                print(f"Error parsing JSON from response: {e}")
                with open(f"D:/GURUKUL-AI/scratch/{unit_id}_raw_response.txt", "w", encoding="utf-8") as raw_f:
                    raw_f.write(text)
    else:
        print("Error: No response from Ollama")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        enrich(sys.argv[1])
    else:
        print("Usage: python enrich_chapter.py <unit_id>")
