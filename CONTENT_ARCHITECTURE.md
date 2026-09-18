# GURUKUL AI — CONTENT ARCHITECTURE SPECIFICATION

**Version**: 2.0 Fresh Clean-Slate Ingestion
**Authoritative Content Source**: `D:\GURUKUL-AI\Contents`
**Runtime Output Root**: `D:\GURUKUL-AI\runtime-data\chapters`

## 1. Single Source of Truth Pipeline
```
Contents/Class 5/*.zip
       │
       ▼ (Processors Package)
processors/english/ -> EnglishProcessor
processors/hindi/   -> HindiProcessor (Devanagari Unicode Safe)
processors/evs/     -> EVSProcessor (Task Badges Preserved)
processors/maths/   -> MathematicsProcessor (Notation & Numerical QA)
       │
       ▼ (Atomic Materialization)
runtime-data/chapters/class_5/{subject_id}/{chapter_id}.json
       │
       ├── CONTENT_INDEX.json (Unified Catalog Index)
       └── search/index.json  (Fresh RAG Search Vector/Keyword Index)
```

## 2. Dynamic Chapter Schema Contract
Every ingested chapter JSON contains:
* `id`: Globally unique identifier (`{class_id}_{subject_id}_{chapter_id}`)
* `classId`: Level identifier (`class_5`)
* `subjectId`: Curriculum subject stream (`01_english_complete`, `02_hindi_complete`, `03_evs_complete`, `03_maths_complete`)
* `chapter_id`: Number identifier (`101`, `102`, etc.)
* `title`: Canonical chapter title
* `learn`: Array of structured lesson, concept, and example blocks
* `practice`: Array of activity, question, and worked practice blocks
* `assess`: Array of MCQ, short answer, and assessment blocks
* `revise`: Array of key concept, rule, recall, and activity blocks
* `resources`: Array of verified official portals (NCERT/DIKSHA) and discovery search query descriptors
