# GURUKUL AI — AUTONOMOUS INTELLIGENT CURRICULUM PIPELINE RESEARCH & ARCHITECTURE BLUEPRINT

This research document analyzes the current curriculum data pipeline and outlines the missing implementations required to achieve a fully autonomous, fault-free, self-describing system that ingests raw source files from `Contents/` and renders them flawlessly in the dashboard.

---

## 1. Current State vs. Autonomous Target

- **Current State**: Static Python ingestion scripts (`generate_processed_content_strict_1to1.py`) mapping predefined filenames (`Overview.json`, `Notes.json`, `Master.json`, etc.) to strict 1-to-1 processed assets.
- **Autonomous Target**: A dynamic, schema-agnostic ingestion engine that automatically discovers *any* JSON structure, infers dataset types, resolves chapter boundaries, validates data fidelity, and materializes dashboard-ready assets with zero manual mapping.

---

## 2. Missing Implementations for a Fault-Free Pipeline

### A. Universal File Type & Schema Inference Engine
- **Gap**: Fixed filename matching (`Overview.json`, `Notes.json`) fails if source files use alternative naming conventions or schema layouts.
- **Proposed Implementation**: An AST-based schema analyzer that inspects the root keys of *any* JSON file (`resource_type`, `chapters`, `units`, `content`, `glossary`, `questions`) and automatically classifies it into the correct dashboard presentation domain.

### B. Autonomous Chapter Boundary & Sequence Resolver
- **Gap**: Discrepancies between snake_case (`chapter_number`) and camelCase (`chapterNumber`) or unit-wrapped arrays (`units` $\rightarrow$ `stories`) required custom patching.
- **Proposed Implementation**: A recursive chapter-boundary indexer that scans any incoming JSON structure, extracts numerical or alpha-numeric chapter identifiers, sorts them chronologically, and constructs a unified chapter manifest.

### C. Real-Time Self-Healing Metadata Validator
- **Gap**: Missing or incomplete fields resulted in empty UI states requiring fallback injection.
- **Proposed Implementation**: A pre-flight validator that checks data payloads against strict TypeScript/Pydantic schemas and auto-generates pedagogical placeholders or AI pedagogical guidance when source data is sparse.

### D. Bi-Directional Delta Sync & Watcher Mechanism
- **Gap**: Processing required explicit CLI script executions when source files were updated.
- **Proposed Implementation**: A file-system watcher (`watchdog`) or Next.js build-hook that triggers incremental, chapter-level reprocessing whenever an authoritative source file in `Contents/` is modified.

---

## 3. Implementation Roadmap & Verification

1. **Phase 1: Autonomous Schema Inference Service** (`backend/services/schema_inference_service.py`)
2. **Phase 2: Universal Chapter Indexer** (`backend/services/chapter_boundary_service.py`)
3. **Phase 3: Self-Healing Dashboard Loader** (`backend/src/curriculum/api/chapters.py`)
4. **Phase 4: Continuous UAT Verification Suite** (`backend/scripts/uat_word_by_word_verification.py`)
