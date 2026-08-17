import os
import json
import sqlite3
import argparse
import uuid
from datetime import datetime

def normalize_url(url):
    return url.strip().rstrip("/")

def is_youtube(url):
    lower_url = url.lower()
    return "youtube.com" in lower_url or "youtu.be" in lower_url

def process_catalog(catalog_path, db_path, dry_run=False, verbose=False, target_chapter=None):
    if not os.path.exists(catalog_path):
        print(f"Error: Catalog not found at {catalog_path}")
        return

    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    stats = {
        "chapters_found": 0,
        "resources_total": 0,
        "resources_ingested": 0,
        "resources_rejected_youtube": 0,
        "resources_skipped_duplicate": 0
    }

    print(f"Integrating External Multimedia from {os.path.basename(catalog_path)}")
    if dry_run: print("!!! DRY RUN MODE - No database changes !!!")

    for chapter in data.get("chapter_resources", []):
        chapter_id = chapter.get("chapter_id")
        class_name = chapter.get("class")
        subject = chapter.get("subject")

        if target_chapter and target_chapter != chapter_id:
            continue

        stats["chapters_found"] += 1
        if verbose: print(f"\nChapter: {chapter_id} ({subject})")

        for res in chapter.get("external_resources", []):
            stats["resources_total"] += 1
            url = normalize_url(res.get("url", ""))
            provider = res.get("provider")

            if not url:
                continue

            # 1. Filter YouTube
            if is_youtube(url):
                stats["resources_rejected_youtube"] += 1
                if verbose: print(f"  [REJECT] YouTube URL excluded: {url}")
                continue

            # 2. Deduplication Check
            cursor.execute(
                "SELECT id, verification_status FROM external_multimedia_resources WHERE chapter_id = ? AND provider = ? AND url = ?",
                (chapter_id, provider, url)
            )
            existing = cursor.fetchone()

            if existing:
                stats["resources_skipped_duplicate"] += 1
                if verbose: print(f"  [SKIP] Duplicate resource: {provider} - {url}")
                continue

            # 3. Ingest
            stats["resources_ingested"] += 1
            res_id = str(uuid.uuid4())
            title = f"{provider} — {subject.capitalize()}"
            resource_types = json.dumps(res.get("resource_types", []))
            search_url = res.get("search_url")
            search_terms = json.dumps(res.get("search_terms", []))

            # Security Contract: Default to false/pending
            enabled = 0
            verified = 0 # chapter_deep_link_verified
            status = "PENDING"
            source = "CATALOG_V3"
            now = datetime.utcnow().isoformat()

            if not dry_run:
                cursor.execute("""
                    INSERT INTO external_multimedia_resources (
                        id, chapter_id, class_name, subject, provider, title, url,
                        resource_types, search_url, search_terms,
                        chapter_deep_link_verified, enabled, youtube, source,
                        verification_status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?)
                """, (
                    res_id, chapter_id, class_name, subject, provider, title, url,
                    resource_types, search_url, search_terms,
                    verified, enabled, source, status, now, now
                ))

            if verbose: print(f"  [INGEST] {provider} -> {url}")

    if not dry_run:
        conn.commit()
    conn.close()

    return stats

def main():
    parser = argparse.ArgumentParser(description="Deterministic Multimedia Integrator (No-AI)")
    parser.add_argument("--chapter", help="Specific chapter ID to process")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--verbose", action="store_true", help="Show detailed logs")

    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    catalog_path = os.path.join(project_root, "Multimedia", "GURUKUL_EXTERNAL_MULTIMEDIA_101_CHAPTERS_V3.json")
    db_path = os.path.join(project_root, "backend", "gurukul_backend.db")

    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    result = process_catalog(catalog_path, db_path, dry_run=args.dry_run, verbose=args.verbose, target_chapter=args.chapter)

    if result:
        print("\n" + "="*40)
        print("MULTIMEDIA INTEGRATION REPORT")
        print("="*40)
        print(f"Chapters Processed: {result['chapters_found']}")
        print(f"Total Records:      {result['resources_total']}")
        print(f"Ingested (New):     {result['resources_ingested']}")
        print(f"Rejected (YouTube): {result['resources_rejected_youtube']}")
        print(f"Skipped (Duplicate):{result['resources_skipped_duplicate']}")
        print("="*40)

if __name__ == "__main__":
    main()
