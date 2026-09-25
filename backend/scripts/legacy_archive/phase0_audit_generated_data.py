import os
import shutil
import hashlib

def run_phase0_audit():
    root_dir = r"D:\GURUKUL"
    archive_dir = r"D:\GURUKUL\_archive\pre_master_cleanup"

    print("==========================================================================")
    print("PHASE 0: GENERATED DATA AUDIT & ISOLATION ARCHIVE CREATION")
    print("==========================================================================\n")

    # Create isolated archive directory if not exists
    os.makedirs(archive_dir, exist_ok=True)

    candidate_locations = [
        {"path": r"D:\GURUKUL\frontend-nextjs\.next", "type": "Frontend Build Cache", "safe_delete": True, "reason": "Next.js static page build cache"},
        {"path": r"D:\GURUKUL\backend\.pytest_cache", "type": "Test Runner Cache", "safe_delete": True, "reason": "Pytest execution cache"},
        {"path": r"D:\GURUKUL\backend\__pycache__", "type": "Python Compiled Bytecode", "safe_delete": True, "reason": "Compiled bytecode cache"},
    ]

    # Audit Python bytecode in subdirectories
    for root, dirs, files in os.walk(os.path.join(root_dir, "backend")):
        if "__pycache__" in dirs:
            cache_path = os.path.join(root, "__pycache__")
            candidate_locations.append({
                "path": cache_path,
                "type": "Python Bytecode Cache",
                "safe_delete": True,
                "reason": "Backend python cache"
            })

    print(f"Discovered Candidate Generated Locations: {len(candidate_locations)}")
    for item in candidate_locations:
        print(f"  [{'SAFE DELETE' if item['safe_delete'] else 'KEEP'}] {item['path']}")
        print(f"    Type: {item['type']} | Reason: {item['reason']}")

    return candidate_locations

if __name__ == "__main__":
    run_phase0_audit()
