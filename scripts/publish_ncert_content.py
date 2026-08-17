import os
import shutil
import argparse
import json
from datetime import datetime

def publish(class_num, staging_dir, production_dir, dry_run=False, update_existing=False):
    class_id = f"class_{class_num}"
    source_root = os.path.join(staging_dir, class_id)

    if not os.path.exists(source_root):
        print(f"Error: Staging directory for {class_id} not found at {source_root}")
        return

    print(f"--- Publishing {class_id} Content to Production ---")
    if dry_run: print("!!! DRY RUN MODE - No files will be moved !!!")

    stats = {"published": 0, "skipped": 0, "errors": 0}

    for subject in os.listdir(source_root):
        subj_path = os.path.join(source_root, subject)
        if not os.path.isdir(subj_path): continue

        for chapter_id in os.listdir(subj_path):
            chapter_path = os.path.join(subj_path, chapter_id)
            if not os.path.isdir(chapter_path): continue

            pkg_file = os.path.join(chapter_path, "package.json")
            if not os.path.exists(pkg_file): continue

            dest_dir = os.path.join(production_dir, class_id, subject, chapter_id)
            dest_pkg = os.path.join(dest_dir, "package.json")

            if os.path.exists(dest_pkg) and not update_existing:
                print(f"  [SKIP] {chapter_id} already in production. Use --update-existing.")
                stats["skipped"] += 1
                continue

            if dry_run:
                print(f"  [DRY-RUN] Would publish {chapter_id} to {dest_dir}")
                stats["published"] += 1
                continue

            try:
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy2(pkg_file, dest_pkg)
                print(f"  [PUBLISHED] {chapter_id}")
                stats["published"] += 1
            except Exception as e:
                print(f"  [ERROR] Failed to publish {chapter_id}: {e}")
                stats["errors"] += 1

    print("\n" + "="*40)
    print("PUBLICATION REPORT")
    print("="*40)
    print(f"Total Published: {stats['published']}")
    print(f"Total Skipped:   {stats['skipped']}")
    print(f"Total Errors:    {stats['errors']}")
    print("="*40)

def main():
    parser = argparse.ArgumentParser(description="Gurukul AI NCERT Publication Tool")
    parser.add_argument("--class", type=int, required=True, dest="class_num", help="Class level")
    parser.add_argument("--input-dir", required=True, help="Path to staging output directory")
    parser.add_argument("--dry-run", action="store_true", help="Report only, no writes")
    parser.add_argument("--update-existing", action="store_true", help="Overwrite existing production packages")

    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    production_dir = os.path.join(project_root, "backend", "storage", "output")
    publish(args.class_num, args.input_dir, production_dir, args.dry_run, args.update_existing)

if __name__ == "__main__":
    main()
