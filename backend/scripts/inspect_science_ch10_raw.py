import json

s_notes = json.load(open(r"D:\GURUKUL\Contents\Class 5\Science\Notes.json", encoding="utf-8"))
chs = s_notes.get("chapters", [])
ch10 = next((c for c in chs if c.get("chapterNumber") == 10 or c.get("chapter_no") == 10), {})
print("Science Notes.json Ch 10 keys:", list(ch10.keys()))
print("Science Notes.json Ch 10 overview:", ch10.get("overview"))
print("Science Notes.json Ch 10 summary:", ch10.get("summary"))

s_master = json.load(open(r"D:\GURUKUL\Contents\Class 5\Science\Master.json", encoding="utf-8"))
m_chs = s_master.get("chapters", [])
m_ch10 = next((c for c in m_chs if c.get("chapterNumber") == 10 or c.get("chapter_no") == 10), {})
print("\nScience Master.json Ch 10 keys:", list(m_ch10.keys()))
print("Science Master.json Ch 10 concepts:", m_ch10.get("concepts"))
print("Science Master.json Ch 10 question_bank keys:", list(m_ch10.get("question_bank", {}).keys()) if isinstance(m_ch10.get("question_bank"), dict) else type(m_ch10.get("question_bank")))

s_quiz = json.load(open(r"D:\GURUKUL\Contents\Class 5\Science\Quiz.json", encoding="utf-8"))
q_chs = s_quiz.get("chapters", [])
q_ch10 = next((c for c in q_chs if c.get("chapterNumber") == 10 or c.get("chapter_no") == 10), {})
print("\nScience Quiz.json Ch 10 questions count:", len(q_ch10.get("questions", [])))
if q_ch10.get("questions"):
    print("Sample Q0 keys:", list(q_ch10.get("questions")[0].keys()))
    print("Sample Q0 content:", q_ch10.get("questions")[0])
    print("Sample Q10 content:", q_ch10.get("questions")[10])
