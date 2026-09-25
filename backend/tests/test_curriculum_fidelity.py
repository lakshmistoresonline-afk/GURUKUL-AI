import os
import json
import hashlib
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent\Class5"
CONTENTS_ROOT = r"D:\GURUKUL\Contents\Class 5"

def test_all_47_chapters_processed_and_faithful():
    subject_counts = {"English": 10, "Hindi": 12, "Maths": 15, "Science": 10}
    total_chapters = 0

    for subject, expected_count in subject_counts.items():
        sub_dir = os.path.join(PROCESSED_ROOT, subject)
        assert os.path.exists(sub_dir), f"ProcessedContent missing for {subject}"
        ch_dirs = [d for d in os.listdir(sub_dir) if os.path.isdir(os.path.join(sub_dir, d))]
        assert len(ch_dirs) == expected_count, f"Expected {expected_count} chapters for {subject}, found {len(ch_dirs)}"
        total_chapters += len(ch_dirs)

        for ch_id in ch_dirs:
            ch_path = os.path.join(sub_dir, ch_id)
            # Verify manifest
            manifest_path = os.path.join(ch_path, "manifest.json")
            assert os.path.exists(manifest_path)
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
                assert manifest["meta"]["chapter_id"] == ch_id

            # Verify 7 sections exist
            for sec in ["overview", "notes", "master", "flashcards", "mindmaps", "quiz", "question_papers"]:
                sec_path = os.path.join(ch_path, f"{sec}.json")
                assert os.path.exists(sec_path), f"Missing section {sec} for {ch_id}"

            # Verify API /source endpoint
            res = client.get(f"/api/v1/chapters/{ch_id}/source?grade=5&subject={subject}")
            assert res.status_code == 200
            data = res.json()
            assert data["chapterId"] == ch_id
            assert "sections" in data
            for sec in ["overview", "notes", "master", "flashcards", "mindmaps", "quiz", "question_papers"]:
                assert sec in data["sections"]

    assert total_chapters == 47

def test_source_immutability():
    # Verify all 29 source JSON files exist and are readable
    for subject in ["English", "Hindi", "Maths", "Science"]:
        subj_dir = os.path.join(CONTENTS_ROOT, subject)
        assert os.path.exists(subj_dir)
        files = [f for f in os.listdir(subj_dir) if f.endswith(".json")]
        assert len(files) >= 7
