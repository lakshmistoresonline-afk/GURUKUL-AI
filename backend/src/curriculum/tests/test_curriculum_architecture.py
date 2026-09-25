import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.curriculum.class5.english.processor import Class5EnglishProcessor
from src.curriculum.class5.hindi.processor import Class5HindiProcessor
from src.curriculum.class5.maths.processor import Class5MathsProcessor
from src.curriculum.class5.science.processor import Class5ScienceProcessor

client = TestClient(app)

def test_english_c01_processing():
    payload = Class5EnglishProcessor.process_chapter("G5-ENG-U01-C01")
    assert payload["chapterId"] == "G5-ENG-U01-C01"
    assert "sections" in payload
    assert "notes" in payload["sections"]
    assert "flashcards" in payload["sections"]
    assert "quiz" in payload["sections"]
    assert len(payload["sections"]["flashcards"]) > 0

def test_hindi_c01_processing():
    payload = Class5HindiProcessor.process_chapter("G5-HIN-U01-C01")
    assert payload["chapterId"] == "G5-HIN-U01-C01"
    assert "sections" in payload
    assert "notes" in payload["sections"]

def test_maths_c01_processing():
    payload = Class5MathsProcessor.process_chapter("G5-MAT-U01-C01")
    assert payload["chapterId"] == "G5-MAT-U01-C01"
    assert "sections" in payload

def test_science_c01_processing():
    payload = Class5ScienceProcessor.process_chapter("G5-SCI-U01-C01")
    assert payload["chapterId"] == "G5-SCI-U01-C01"
    assert "sections" in payload

def test_api_source_endpoint():
    res = client.get("/api/v1/chapters/G5-ENG-U01-C01/source?grade=5&subject=English")
    assert res.status_code == 200
    data = res.json()
    assert data["chapterId"] == "G5-ENG-U01-C01"
    assert "sections" in data
    assert "overview" in data["sections"]
    assert "question_papers" in data["sections"]
