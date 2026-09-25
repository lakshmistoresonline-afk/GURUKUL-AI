import json

fpath = r"D:\GURUKUL\Contents\Class 5\Hindi\Hindi Master.json"
data = json.load(open(fpath, encoding="utf-8"))

print("==========================================================================")
print("FORENSIC HINDI MASTER.JSON ITEM-BY-ITEM AUDIT (ALL 12 CHAPTERS)")
print("==========================================================================\n")

chapters = data.get("chapters_master_data", [])
print(f"TOTAL HINDI CHAPTERS: {len(chapters)}\n")

for i, ch in enumerate(chapters, 1):
    c_num = ch.get("chapter_number")
    c_title = ch.get("chapter_title")
    info = ch.get("chapter_info", {})
    title_hindi = info.get("title_hindi") or c_title

    meta = ch.get("metadata", {})
    summary = ch.get("detailed_summary")
    theme = ch.get("theme_and_moral")
    chars = ch.get("character_analysis", [])
    shabdart = ch.get("shabdart", [])
    vartani = ch.get("shuddhi_vartani", [])
    grammar = ch.get("grammar_extraction", {})
    mindmap = ch.get("story_mindmap", {})
    flashcards = ch.get("flashcards", [])
    qb = ch.get("question_bank", {})
    quiz = ch.get("interactive_quiz", [])
    act = ch.get("activities_and_checklist", {})
    model_p = ch.get("model_question_paper", {})

    print(f"Chapter {c_num}: {title_hindi} (Genre: {meta.get('genre')}, Author: {meta.get('author')})")
    print(f"  1. detailed_summary: {len(summary) if summary else 0} chars")
    print(f"  2. theme_and_moral: {len(theme) if theme else 0} chars")
    print(f"  3. character_analysis: {len(chars)} characters ({[c.get('character_name') for c in chars]})")
    print(f"  4. shabdart: {len(shabdart)} words ({[w.get('word') for w in shabdart]})")
    print(f"  5. shuddhi_vartani: {len(vartani)} words ({[v.get('ashuddh') + ' -> ' + v.get('shuddh') for v in vartani]})")
    print(f"  6. grammar_extraction: sangya({len(grammar.get('sangya', []))}), sarvanam({len(grammar.get('sarvanam', []))}), visheshand({len(grammar.get('visheshand', []))}), kriya({len(grammar.get('kriya', []))}), vilom({len(grammar.get('vilom', []))}), paryayvachi({len(grammar.get('paryayvachi', []))})")
    print(f"  7. story_mindmap: start({bool(mindmap.get('start'))}), events({len(mindmap.get('events', []))}), conclusion({bool(mindmap.get('conclusion'))})")
    print(f"  8. flashcards: {len(flashcards)} cards")
    print(f"  9. question_bank: extracts({len(qb.get('seen_extracts', [])) if isinstance(qb.get('seen_extracts'), list) else bool(qb.get('seen_extracts'))}), dialogues({len(qb.get('context_dialogues', [])) if isinstance(qb.get('context_dialogues'), list) else bool(qb.get('context_dialogues'))}), mcqs({len(qb.get('mcqs', []))}), short({len(qb.get('short_answers', []))}), long({len(qb.get('long_answers', []))}), writing({bool(qb.get('creative_writing'))})")
    print(f"  10. interactive_quiz: {len(quiz)} questions")
    print(f"  11. activities_and_checklist: activity({bool(act.get('activity'))}), checklist({len(act.get('checklist', []))})")
    print(f"  12. model_question_paper: max_marks({model_p.get('max_marks')}), sections({len(model_p.get('sections', []))})")
    print("-" * 74)
