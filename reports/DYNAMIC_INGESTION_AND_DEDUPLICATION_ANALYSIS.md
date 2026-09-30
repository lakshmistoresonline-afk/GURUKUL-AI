# GURUKUL AI — DYNAMIC INGESTION & DEDUPLICATION ARCHITECTURE ANALYSIS

## 1. Executive Summary
This document analyzes how Gurukul AI handles **any** incoming source JSON file (whether `Overview`, `Notes`, `Master`, `Flashcards`, `Mindmaps`, `Quiz`, `Question Papers`, or future custom source files) placed inside any class or subject source folder under `Contents/`.

---

## 2. Universal Ingestion & Processing Logic

### A. Universal Directory Scanning
- The backend processing CLI scripts (`process_cli.py`, `class6_process_cli.py`, `class7_process_cli.py`) do not hardcode specific filenames. Instead, they dynamically scan **all `.json` files** present in any subject directory at runtime.
- If a brand-new source file is introduced, the ingestion script automatically loads it into memory alongside existing files.

### B. Flexible Schema Resolution & Key Matching
- The curriculum resolvers (`chapter_resolver.py` across classes) employ fallback key resolution (checking `chapters`, `flashcards`, `flashcards_dataset`, `mind_map`, `quizzes`, `questions`, `question_papers`, etc.).
- If a new source file provides additional data points or sections, the resolver maps them to the chapter bundle safely without breaking existing structures.

### C. Deterministic Overwrite & Zero Duplication
- Processed output files are written to strict, deterministic file paths per chapter (`overview.json`, `notes.json`, `master.json`, `flashcards.json`, `mindmaps.json`, `quiz.json`, `question_papers.json`).
- Re-running the ingestion pipeline cleanly updates these files in-place, guaranteeing **zero file duplication or redundant records**.

### D. Immediate Dashboard Showcase
- The FastAPI backend (`chapters.py`) and Next.js frontend (`ChapterClient.tsx`) read directly from these persistent processed files at runtime, ensuring any new source content is immediately showcased in its respective dashboard tab.
