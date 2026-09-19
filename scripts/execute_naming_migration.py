import json
import pathlib
import sys

def main():
    manifest_path = pathlib.Path('NAMING_MIGRATION_MANIFEST.json')
    if not manifest_path.exists():
        print("Manifest not found!")
        sys.exit(1)

    data = json.loads(manifest_path.read_text(encoding='utf-8'))
    renames = data.get('planned_renames', [])
    if len(renames) != 16:
        print(f"Error: Expected 16 renames, found {len(renames)}")
        sys.exit(1)

    print("Step 1: Pre-rename verification and stats collection...")
    pre_stats = {}
    for r in renames:
        old_path = pathlib.Path(r['OldPath'])
        new_path = pathlib.Path(r['NewPath'])

        if not old_path.exists():
            print(f"PRE-CHECK FAILED: Old path does not exist: {old_path}")
            sys.exit(1)
        if new_path.exists():
            print(f"PRE-CHECK FAILED: Destination path already exists: {new_path}")
            sys.exit(1)

        files = [f for f in old_path.rglob('*') if f.is_file()]
        total_size = sum(f.stat().st_size for f in files)
        pre_stats[r['OldName']] = {'count': len(files), 'size': total_size}

    print("Step 2: Executing 16 atomic physical directory renames...")
    performed = []
    for r in renames:
        old_path = pathlib.Path(r['OldPath'])
        new_path = pathlib.Path(r['NewPath'])

        if not old_path.exists():
            print(f"ABORT: Old path disappeared: {old_path}")
            sys.exit(1)
        if new_path.exists():
            print(f"ABORT: New path already exists: {new_path}")
            sys.exit(1)

        old_path.rename(new_path)

        if not new_path.exists() or old_path.exists():
            print(f"ABORT: Rename verification failed for {old_path} -> {new_path}")
            sys.exit(1)

        performed.append((r['OldName'], r['NewName']))
        print(f"SUCCESS: {r['OldName']} -> {r['NewName']}")

    print("Step 3: Post-rename validation & integrity checks...")
    for r in renames:
        old_path = pathlib.Path(r['OldPath'])
        new_path = pathlib.Path(r['NewPath'])

        if old_path.exists():
            print(f"POST-CHECK FAILED: Old path still exists: {old_path}")
            sys.exit(1)
        if not new_path.exists():
            print(f"POST-CHECK FAILED: New path does not exist: {new_path}")
            sys.exit(1)

        files = [f for f in new_path.rglob('*') if f.is_file()]
        total_size = sum(f.stat().st_size for f in files)
        pre = pre_stats[r['OldName']]

        if pre['count'] != len(files) or pre['size'] != total_size:
            print(f"INTEGRITY FAIL for {r['NewName']}: pre_count={pre['count']}, post_count={len(files)}, pre_size={pre['size']}, post_size={total_size}")
            sys.exit(1)

    print("ALL 16 RECENT RENAME OPERATIONS COMPLETED AND VERIFIED SUCCESSFULLY!")
    sys.exit(0)

if __name__ == '__main__':
    main()
