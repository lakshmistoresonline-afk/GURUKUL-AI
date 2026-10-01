import json
import os

path = r"D:/GURUKUL/ProcessedContent/Class5/English/G5-ENG-U01-C01/question_papers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Chapter title:", data.get("chapter_title"))
print("Number of question_papers:", len(data.get("question_papers", [])))
for i, qp in enumerate(data.get("question_papers", [])):
    print(f"  Paper {i+1}: id={qp.get('paper_id')}, title={qp.get('paper_title')}")
    sections = qp.get("sections", [])
    print(f"    Sections: {len(sections)}")
    total_q = sum(len(sec.get("questions", [])) for sec in sections)
    print(f"    Total questions in paper: {total_q}")
