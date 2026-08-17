import os
import sys

BACKEND_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from src.services.chapter_service import ChapterService
from src.orchestrator.ai_orchestrator import AIOrchestrator

service = ChapterService(AIOrchestrator())

single = """
Chapter 1: The Beginning
This is one chapter only.
"""

multi = """
Chapter 1: The Beginning
Some text.

Chapter 2: The Next Chapter
More text.
"""

try:
    service._validate_single_chapter_source(single)
    print("SINGLE-CHAPTER: PASS")
except Exception as e:
    print("SINGLE-CHAPTER: FAIL")
    print("ERROR:", e)

try:
    service._validate_single_chapter_source(multi)
    print("MULTI-CHAPTER REJECTION: FAIL")
except ValueError as e:
    print("MULTI-CHAPTER REJECTION: PASS")
    print("MESSAGE:", e)
except Exception as e:
    print("MULTI-CHAPTER REJECTION: ERROR")
    print("ERROR:", e)
