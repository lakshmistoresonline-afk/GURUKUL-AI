import os
import shutil

def clean_build_caches():
    root_dir = r"D:\GURUKUL"

    print("==========================================================================")
    print("PHASE 0: CLEANING GENERATED BUILD & RUNTIME CACHES")
    print("==========================================================================\n")

    cleared_count = 0

    # 1. Clean Next.js .next folder
    next_dir = os.path.join(root_dir, "frontend-nextjs", ".next")
    if os.path.exists(next_dir):
        try:
            shutil.rmtree(next_dir)
            print(f"Cleared Next.js build cache: {next_dir}")
            cleared_count += 1
        except Exception as e:
            print(f"Warning clearing {next_dir}: {e}")

    # 2. Clean Pytest .pytest_cache folder
    pytest_dir = os.path.join(root_dir, "backend", ".pytest_cache")
    if os.path.exists(pytest_dir):
        try:
            shutil.rmtree(pytest_dir)
            print(f"Cleared Pytest cache: {pytest_dir}")
            cleared_count += 1
        except Exception as e:
            print(f"Warning clearing {pytest_dir}: {e}")

    # 3. Clean all __pycache__ folders
    for root, dirs, files in os.walk(os.path.join(root_dir, "backend")):
        for d in dirs:
            if d == "__pycache__":
                pycache_path = os.path.join(root, d)
                try:
                    shutil.rmtree(pycache_path)
                    print(f"Cleared Python bytecode cache: {pycache_path}")
                    cleared_count += 1
                except Exception as e:
                    print(f"Warning clearing {pycache_path}: {e}")

    print(f"\nTotal Caches & Build Artifacts Cleared: {cleared_count}")

if __name__ == "__main__":
    clean_build_caches()
