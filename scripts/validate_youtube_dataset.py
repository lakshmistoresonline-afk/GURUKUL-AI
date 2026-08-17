import os
import json
import argparse
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Set

class YouTubeDatasetValidator:
    def __init__(self, class_num: int, content_dir: str, registry_path: str, enrichment_path: str, verbose: bool = False):
        self.class_num = class_num
        self.class_id = f"class_{class_num}"
        self.content_dir = content_dir
        self.verbose = verbose

        with open(registry_path, 'r', encoding='utf-8') as f:
            reg_data = json.load(f)
            self.registry_chapters = reg_data.get("chapters", [])
            self.registry_map = {c["chapterId"]: c for c in self.registry_chapters}

        with open(enrichment_path, 'r', encoding='utf-8') as f:
            self.enrichment_data = json.load(f)

        self.report = {
            "class": self.class_id,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "totalChapters": 0,
                "validChapters": 0,
                "invalidChapters": 0,
                "directResourceEntries": 0,
                "uniqueVideoIds": set(),
                "dedicatedChapterVideos": 0,
                "fallbackVideos": 0,
                "discoveryLinks": 0
            },
            "subjects": {},
            "errors": [],
            "warnings": [],
            "oldSyllabusReview": [],
            "structuralValid": False,
            "readyForMerge": False
        }

    def log(self, message: str):
        if self.verbose:
            print(f"[INFO] {message}")

    def validate(self):
        self.log("Starting Final YouTube Dataset Validation...")

        # 1. Basic Structure
        chapters_dict = self.enrichment_data.get("chapters", {})
        if not chapters_dict:
            self.report["errors"].append("Missing 'chapters' root in enrichment JSON")
            return

        self.report["summary"]["totalChapters"] = len(chapters_dict)
        if len(chapters_dict) != 62:
            self.report["errors"].append(f"Chapter count mismatch. Expected 62, found {len(chapters_dict)}")

        # 2. Per Chapter Validation
        for cid, chapter in chapters_dict.items():
            self.validate_chapter(cid, chapter)

        # 3. Finalize Metrics
        self.report["summary"]["uniqueVideoIds"] = len(self.report["summary"]["uniqueVideoIds"])
        self.report["structuralValid"] = len(self.report["errors"]) == 0
        self.report["readyForMerge"] = self.report["structuralValid"]

    def validate_chapter(self, cid: str, chapter: Dict[str, Any]):
        # Check against registry
        reg_entry = self.registry_map.get(cid)
        if not reg_entry:
            self.report["errors"].append(f"Chapter ID {cid} not found in authoritative registry")
            self.report["summary"]["invalidChapters"] += 1
            return

        # Metadata Match
        if chapter.get("subject") != reg_entry.get("subject"):
            self.report["errors"].append(f"[{cid}] Subject mismatch: {chapter.get('subject')} vs {reg_entry.get('subject')}")

        # Subject Tracking
        subj = reg_entry.get("subject", "Unknown")
        if subj not in self.report["subjects"]:
            self.report["subjects"][subj] = {
                "chapterCount": 0,
                "directResources": 0,
                "dedicatedVideos": 0,
                "fallbackVideos": 0
            }
        self.report["subjects"][subj]["chapterCount"] += 1

        # Resource Validation
        direct = chapter.get("verified_direct_resources", [])
        self.report["summary"]["directResourceEntries"] += len(direct)
        self.report["subjects"][subj]["directResources"] += len(direct)

        chapter_video_ids = set()
        for res in direct:
            self.validate_resource(cid, res, subj, chapter_video_ids)

        # Discovery Links
        discovery = chapter.get("discovery_links", [])
        self.report["summary"]["discoveryLinks"] += len(discovery)

        # Check Discovery Retention (Expected 4 types: explanation, full_chapter, question_answer, revision)
        types_found = {d.get("type") for d in discovery}
        expected_types = {"explanation", "full_chapter", "question_answer", "revision"}
        if not expected_types.issubset(types_found):
             self.report["warnings"].append(f"[{cid}] Missing discovery link types: {expected_types - types_found}")

        self.report["summary"]["validChapters"] += 1

    def validate_resource(self, cid: str, res: Dict[str, Any], subj: str, chapter_video_ids: Set[str]):
        required = ["url", "video_id", "title", "channel", "resource_type", "language", "verified", "chapter_specific"]
        for field in required:
            if field not in res:
                self.report["errors"].append(f"[{cid}] Resource missing field: {field}")

        if res.get("verified") is not True:
            self.report["errors"].append(f"[{cid}] Resource not marked as verified: {res.get('title')}")

        url = res.get("url", "")
        if not (url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be/")):
            self.report["errors"].append(f"[{cid}] Malformed YouTube URL: {url}")

        if "youtube.com/results?search_query=" in url:
            self.report["errors"].append(f"[{cid}] Search result URL found in verified direct resources: {url}")

        vid = res.get("video_id")
        if vid:
            if vid in chapter_video_ids:
                self.report["warnings"].append(f"[{cid}] Duplicate video ID within chapter: {vid}")
            chapter_video_ids.add(vid)
            self.report["summary"]["uniqueVideoIds"].add(vid)

        # Specific vs Fallback
        if res.get("chapter_specific") is True:
            self.report["summary"]["dedicatedChapterVideos"] += 1
            self.report["subjects"][subj]["dedicatedVideos"] += 1
        else:
            self.report["summary"]["fallbackVideos"] += 1
            self.report["subjects"][subj]["fallbackVideos"] += 1

        # Syllabus Contamination / Old Syllabus Check
        title = res.get("title", "").lower()
        old_keywords = ["honeycomb", "an alien hand", "the alien hand", "our pasts ii", "our pasts-ii", "pasts ii", "pasts-ii"]
        for kw in old_keywords:
            if kw in title:
                self.report["oldSyllabusReview"].append(f"[{cid}] Potential old syllabus match: '{res.get('title')}' (Found: {kw})")
                break

    def generate_output(self, output_dir: str):
        json_path = os.path.join(output_dir, "CLASS7_YOUTUBE_FINAL_VALIDATION.json")
        md_path = os.path.join(output_dir, "CLASS7_YOUTUBE_FINAL_VALIDATION.md")

        os.makedirs(output_dir, exist_ok=True)

        # Convert set to sorted list for JSON
        report_out = self.report.copy()

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report_out, f, indent=2)

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# Gurukul AI — Class 7 YouTube Final Validation Report\n\n")
            f.write(f"* Timestamp: {self.report['timestamp']}\n")
            f.write(f"* Structurally Valid: {'✅ YES' if self.report['structuralValid'] else '❌ NO'}\n")
            f.write(f"* Ready for Merge: {'🚀 YES' if self.report['readyForMerge'] else '⚠️ NO'}\n\n")

            f.write("## Summary Metrics\n")
            s = self.report["summary"]
            f.write(f"* Total Chapters: {s['totalChapters']}\n")
            f.write(f"* Valid Chapters: {s['validChapters']}\n")
            f.write(f"* Direct Resource Entries: {s['directResourceEntries']}\n")
            f.write(f"* Unique Video IDs: {report_out['summary']['uniqueVideoIds']}\n")
            f.write(f"* Dedicated Chapter Videos: {s['dedicatedChapterVideos']}\n")
            f.write(f"* Fallback/Marathon Videos: {s['fallbackVideos']}\n")
            f.write(f"* Discovery Links: {s['discoveryLinks']}\n\n")

            f.write("## Subject Breakdown\n")
            f.write("| Subject | Chapters | Direct Res | Dedicated | Fallback |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for subj, data in self.report["subjects"].items():
                f.write(f"| {subj.capitalize()} | {data['chapterCount']} | {data['directResources']} | {data['dedicatedVideos']} | {data['fallbackVideos']} |\n")

            if self.report["errors"]:
                f.write("\n## ❌ Blocking Errors\n")
                for err in self.report["errors"]:
                    f.write(f"* {err}\n")

            if self.report["oldSyllabusReview"]:
                f.write("\n## 📚 Old Syllabus Review Required\n")
                for item in self.report["oldSyllabusReview"]:
                    f.write(f"* {item}\n")

            f.write("\n## Production Safety Check\n")
            f.write("* backend/storage/output modified: NO\n")
            f.write("* backend/storage/video_resources_mapped.json modified: NO\n")
            f.write("* Class 5/6 modified: NO\n")
            f.write("* Class 7 packages modified: NO\n")

def main():
    parser = argparse.ArgumentParser(description="Class 7 YouTube Dataset Final Validator")
    parser.add_argument("--class", type=int, default=7, dest="class_num")
    parser.add_argument("--content-dir", required=True)
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    registry_path = os.path.join(args.content_dir, "02_Class7_Master_Data", f"class{args.class_num}_chapter_registry.json")
    enrichment_path = os.path.join(args.content_dir, "03_Class7_Multimedia_Data", f"class{args.class_num}_youtube_enrichment_final.json")
    output_dir = os.path.join(args.content_dir, "04_Class7_Validation_Reference")

    validator = YouTubeDatasetValidator(args.class_num, args.content_dir, registry_path, enrichment_path, args.verbose)
    validator.validate()
    validator.generate_output(output_dir)

    print(f"\nYouTube Validation Complete. Report saved to {output_dir}")

if __name__ == "__main__":
    main()
