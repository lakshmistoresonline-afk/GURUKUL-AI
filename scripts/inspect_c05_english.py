import pathlib
import json

pkg = pathlib.Path(r'D:\GURUKUL-AI\Contents\Class 5\MASTER__C05__ENGLISH__SANTOOR__P00__V02\Class5_English_Santoor_Revised_Master_Package_v2')

chapters_inventory = []
total_chapters = 0

total_files_all = 0

for chap_folder in sorted(pkg.glob("*")):
    if chap_folder.is_dir() and not chap_folder.name.startswith("."):
        total_chapters += 1
        info_file = chap_folder / "00_CHAPTER_INFO" / "CHAPTER_INFO.json"
        title = chap_folder.name
        chap_id = "unknown"
        if info_file.exists():
            info = json.loads(info_file.read_text(encoding='utf-8'))
            title = info.get("title", title)
            chap_id = str(info.get("chapter_id", chap_id))

        files = [str(f.relative_to(chap_folder)) for f in chap_folder.rglob("*") if f.is_file()]
        total_files_all += len(files)
        file_types = list(set(f.split('.')[-1] for f in files))

        sections = [d.name for d in chap_folder.iterdir() if d.is_dir()]
        all_possible_sections = ["00_CHAPTER_INFO", "01_LEARN", "02_PRACTICE", "03_ASSESS", "04_REVISE", "05_MULTIMEDIA", "06_MASTERY", "99_INTERNAL_TRACEABILITY"]
        sections_missing = [s for s in all_possible_sections if not (chap_folder / s).exists()]

        source_derived = [f for f in files if "SOURCE_DERIVED" in f or "SOURCE_PAGES" in f]
        assessment_files = [f for f in files if "ASSESS" in f]
        practice_files = [f for f in files if "PRACTICE" in f]
        revision_files = [f for f in files if "REVISE" in f]
        resource_files = [f for f in files if "RESOURCES" in f or "MULTIMEDIA" in f]
        traceability_files = [f for f in files if "TRACEABILITY" in f]

        chapters_inventory.append({
            "chapter_id": chap_id,
            "chapter_folder": chap_folder.name,
            "chapter_title": title,
            "files": files,
            "file_types": file_types,
            "sections_present": sections,
            "sections_missing": sections_missing,
            "source_pages_available": (chap_folder / "01_LEARN" / "04_SOURCE_DERIVED" / "SOURCE_PAGES.json").exists(),
            "source_derived_files": source_derived,
            "assessment_files": assessment_files,
            "practice_files": practice_files,
            "revision_files": revision_files,
            "resource_files": resource_files,
            "traceability_files": traceability_files
        })

inventory_data = {
    "subject": "English",
    "book": "Santoor",
    "class_level": "5",
    "total_chapters": total_chapters,
    "total_files": total_files_all,
    "chapters": chapters_inventory
}

struct_path = pathlib.Path(r'D:\GURUKUL-AI\SOURCE_STRUCTURE__C05_ENGLISH_SANTOOR.json')
struct_path.write_text(json.dumps(inventory_data, indent=2, ensure_ascii=False), encoding='utf-8')
print(f"Created {struct_path} with {total_chapters} chapters and {total_files_all} files.")
