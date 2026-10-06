import os
from .core.config import GurukulConfig

CONTENT_ROOT = GurukulConfig.get_content_root()

def main():
    print(f"Class 6 Process CLI using Content Root: {CONTENT_ROOT}")

if __name__ == "__main__":
    main()
