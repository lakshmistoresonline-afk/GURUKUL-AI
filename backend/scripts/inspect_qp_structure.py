import json

path = r"D:/GURUKUL/ProcessedContent/Class5/English/G5-ENG-U01-C01/question_papers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for idx, p in enumerate(data.get("question_papers", [])):
    print(f"Paper {idx+1}: id={p.get('paper_id')}, title={p.get('paper_title')}")
    for s_idx, sec in enumerate(p.get("sections", [])):
        print(f"  Section {s_idx+1}: {sec.get('section_name')} (questions: {len(sec.get('questions', []))})")
        for q in sec.get("questions", []):
            # print sample question text snippet
            pass
