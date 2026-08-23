import os
import json
import logging

BASE_DIR = "D:/GURUKUL-AI/backend/GURUKUL_AI_CONTENT"

def get_stats(path):
    stats = {
        "concepts": 0,
        "questions": 0,
        "sprints": 0,
        "flashcards": 0,
        "intro_len": 0,
        "has_roadmap": False,
        "has_expl": False
    }

    # Check super files
    for sf in ["super_system.json", "super_assessment.json", "super_foundation.json", "super_pedagogy.json", "super_experiential.json"]:
        p = os.path.join(path, sf)
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    if sf == "super_system.json":
                        stats["concepts"] = len(d.get("concepts", []))
                        stats["flashcards"] = len(d.get("flashcards", []))
                    elif sf == "super_assessment.json":
                        stats["questions"] = len(d.get("assessment_pool", []))
                    elif sf == "super_foundation.json":
                        stats["intro_len"] = len(str(d.get("chapter_content", {}).get("overview", "")))
                    elif sf == "super_pedagogy.json":
                        stats["has_expl"] = bool(d.get("teacher_explanation"))
                    elif sf == "super_experiential.json":
                        sprints = d.get("learning_sprints", [])
                        stats["sprints"] = len(sprints)
                        stats["has_roadmap"] = len(sprints) > 0
            except: pass
    return stats

def run_audit():
    full_report = {}

    for class_name in sorted(os.listdir(BASE_DIR)):
        if not class_name.startswith("class_"): continue
        class_path = os.path.join(BASE_DIR, class_name)
        full_report[class_name] = {}

        for subject in sorted(os.listdir(class_path)):
            subject_path = os.path.join(class_path, subject)
            if not os.path.isdir(subject_path) or subject == "master_index.json": continue

            chapters_path = os.path.join(subject_path, "chapters")
            if not os.path.exists(chapters_path): continue

            full_report[class_name][subject] = []

            for chapter_id in sorted(os.listdir(chapters_path)):
                chapter_path = os.path.join(chapters_path, chapter_id)
                if not os.path.isdir(chapter_path) or "supplemental" in chapter_id: continue

                stats = get_stats(chapter_path)

                # Get Title
                title = chapter_id
                pkg_p = os.path.join(chapter_path, "package.json")
                if os.path.exists(pkg_p):
                    try:
                        with open(pkg_p, 'r', encoding='utf-8') as f:
                            pk = json.load(f)
                            title = pk.get("chapter", {}).get("chapter_title") or pk.get("chapter", {}).get("title") or chapter_id
                    except: pass

                full_report[class_name][subject].append({
                    "id": chapter_id,
                    "title": title,
                    "stats": stats
                })

    return full_report

def generate_markdown(report):
    md = ["# COMPREHENSIVE CURRICULUM IMPLEMENTATION LOG\n"]
    md.append("This log provides a per-chapter breakdown of all implemented pedagogical data nodes.\n")

    for class_name, subjects in report.items():
        md.append(f"## {class_name.replace('_', ' ').upper()}")
        for subject, chapters in subjects.items():
            md.append(f"### SUBJECT: {subject.replace('_', ' ').upper()}")
            md.append("| Chapter ID | Title | Concepts | Questions | Sprints | Flashcards | Intro | Status |")
            md.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |")
            for c in chapters:
                s = c["stats"]
                status = "✅ READY" if s["has_roadmap"] and s["concepts"] > 0 else "⚠️ INCOMPLETE"
                md.append(f"| {c['id']} | {c['title']} | {s['concepts']} | {s['questions']} | {s['sprints']} | {s['flashcards']} | {s['intro_len']} | {status} |")
            md.append("\n")

    return "\n".join(md)

if __name__ == "__main__":
    report_data = run_audit()
    md_content = generate_markdown(report_data)
    with open("D:/GURUKUL-AI/FULL_CURRICULUM_LOG.artifact.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Comprehensive Log generated at D:/GURUKUL-AI/FULL_CURRICULUM_LOG.artifact.md")
