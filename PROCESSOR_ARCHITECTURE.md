# Gurukul AI — Processor Architecture Specification

## Overview

Gurukul AI utilizes a modular, subject-wise curriculum processing architecture. The fundamental architectural principle is:

- **Class = Execution Configuration** (`ProcessingContext`)
- **Subject = Processing Logic** (`SubjectProcessor` & `SubjectRegistry`)
- **Textbook = Source Profile** (`SourceProfile`)
- **Chapter = Source Data**

---

## Implemented Architecture (Phase 2.1)

### 1. Processing Context (`processors/common/source/context.py`)
Encapsulates runtime job execution parameters (`job_id`, `class_level`, `subject`, `source_package`, `output_dir`). Requires explicit class and subject configuration; rejects defaults or path inference.

### 2. Source Profile (`processors/common/source/profile.py`, `loader.py`)
Describes authoritative source metadata (`class_level`, `subject`, `book`, `source_package`, `source_files`). Validates compatibility against `ProcessingContext`.

### 3. Subject Registry (`processors/common/registry.py`)
Maps supported subject identifiers (`English`, `Hindi`, `Mathematics`, `EVS`) to their reusable subject processors (`EnglishSubjectProcessor`, `HindiSubjectProcessor`, `MathematicsSubjectProcessor`, `EVSSubjectProcessor`). Unsupported subjects fail explicitly.

### 4. Subject Processors & Error Contract
- Stateless or execution-scoped subject processors.
- Strict validation on chapter metadata: missing or invalid `chapter_id` in `CHAPTER_INFO.json` raises a `ValueError` rather than falling back to `"101"`.

---

## Planned for Future Processing Phases (Deferred)
- Semantic cross-pillar duplicate detection engines.
- Domain-specific pedagogical handlers (Prose/Poetry sub-handlers).
- Database migration integration.
- Class 6 and Class 7 curriculum execution runs.
