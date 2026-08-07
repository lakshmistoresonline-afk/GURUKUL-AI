# Folder Structure Report - Project Gurukul AI

## Root Data Directory: `datasets/`

### 1. `ncert_source/` (Input Area)
- `class_5/`: english, mathematics, evs, hindi, other_languages.
- `class_6/`: english, mathematics, science, social_science, hindi, sanskrit, other_languages.

### 2. `processed/` (Platform Data)
- `metadata/`: Registry files (media, achievements).
- `chapters/`: Processed curriculum JSON (class_XX/subject/chapters/chapter_XX).
- `quizzes/`: AI-generated practice questions.
- `flashcards/`: Study aids.
- `mindmaps/`: Interactive relationship graphs.
- `summaries/`: Chapter introductions and takeaways.
- `revision_notes/`: Structured notes for quick learning.
- `embeddings/`: Vector representations for semantic search.
- `vector_db/`: Local vector database storage.
- `search_index/`: Full-text search indexes.
- `ai_json/`: Raw model outputs and extraction artifacts.

### 3. `assets/` (Multimedia)
- `diagrams/`: Curated educational diagrams.
- `images/`: Photographs and illustrations.
- `illustrations/`: Concept art.
- `tables/`: Structured data as JSON.
- `videos/`: MP4 lessons.
- `audio/`: Narrations and pronunciations.
- `animations/`: Lottie and Rive assets.

### 4. `database/`, `logs/`, `manifests/`, `scripts/`
Standard management and utility directories.

## Application Module: `lib/features/content_acquisition/`
- Standard Flutter feature structure for Content Acquisition Manager.
