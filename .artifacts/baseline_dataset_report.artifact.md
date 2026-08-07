# Dataset Architecture Report

## 1. Directory Structure
The repository uses a centralized `datasets/` root, separated from application assets.

- **`ncert_source/`**: Entry point for raw resources. Organized by `class_XX/subject/`.
- **`processed/`**: Production data area.
  - `chapters/`: Contains 141 verified curriculum nodes.
  - `quizzes/`, `flashcards/`, `mindmaps/`: Auxiliary learning assets linked to nodes.
  - `embeddings/`: Pre-calculated vectors for semantic search.
- **`assets/`**: Multimedia store (diagrams, images, tables).

## 2. Lesson Schema
The `lesson.json` (ConceptNode) is the core entity.
- **Strengths**: Highly granular; includes Bloom's taxonomy mapping, estimated study time, and prerequisites.
- **Weaknesses**: Large file size (~200KB per chapter) may impact initial load if not cached efficiently.

## 3. Versioning & Manifests
- **Current Status**: Manual versioning via folder names.
- **Risk**: Lack of automated schema versioning for JSON files. If the `ConceptNode` model changes, existing files may break.

## 4. Search & Indexing
Search indexes are currently file-system based (traversed by `RepositoryScanner`).
- **Recommendation**: Transition to the `processed/search_index` JSON for O(1) lookups in UI.
