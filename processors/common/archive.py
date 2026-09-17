import zipfile
from pathlib import Path

def extract_zip_archive(zip_path: Path, target_dir: Path) -> list[Path]:
    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP archive not found: {zip_path}")

    extracted_files = []
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(target_dir)
        for name in zf.namelist():
            extracted_files.append(target_dir / name)
    return extracted_files
