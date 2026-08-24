import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.utils.path_resolver import PathResolver
from src.config.app_config import settings

def test():
    class_name = "class_5"
    subject = "english"
    chapter_id = "eesa101"

    print(f"Testing retrieval for {class_name} {subject} {chapter_id}")
    master_path = PathResolver.get_chapter_path(class_name, chapter_id, subject=subject)
    print(f"Master path: {master_path}")

    if master_path:
        for fname in ["chapter_package.json", "package.json"]:
            package_path = os.path.join(master_path, fname)
            exists = os.path.exists(package_path)
            print(f"File {fname} exists: {exists} at {package_path}")

if __name__ == "__main__":
    test()
