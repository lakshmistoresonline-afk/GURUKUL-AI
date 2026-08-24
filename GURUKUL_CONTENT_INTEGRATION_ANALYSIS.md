# GURUKUL AI — CONTENT INTEGRATION ANALYSIS

## 1. Project Architecture Overview
The Gurukul AI platform is built as a distributed system:
- **Frontend (Next.js 14):** Modern React-based UI using the App Router. Handles student interaction, dashboard rendering, and learning workflows.
- **Backend (FastAPI):** Python-based orchestrator. Manages curriculum discovery, content serving, AI tutoring, and progress tracking.
- **Content Storage:** Hierarchical JSON-based storage at `backend/GURUKUL_AI_CONTENT`.
- **Database:** Firebase/Firestore for student profiles and progress; SQLite for local caching and job management.

## 2. Final Content Package Analysis (V3)
Authoritative Source: `D:\GURUKUL-AI\Json Files\`

### Inventory Summary
- **Class 5:** 47 Chapters (English, Hindi, Mathematics, EVS)
- **Class 6:** 54 Chapters (English, Hindi, Mathematics, Science, Social Science)
- **Class 7:** 62 Chapters (English, Hindi, Mathematics, Science, Social Science)
- **Total:** 163 Core Chapters.

### Content Structure
Each chapter directory (e.g., `chapter_101_Papa_s_Spectacles`) contains:
- `components/`: 42 JSON files representing specific learning modules (Flashcards, Assessments, Worked Examples, etc.).
- `subject_knowledge/`: Domain-specific facts and concepts.
- `chapter_package.json`: Consolidated manifest for the chapter.
- `SOURCE_INTELLIGENCE.json`: Metadata regarding content derivation.

### Runtime Mapping
The packages include `RUNTIME_MAPPING_MANIFEST.json` and `INTEGRATED_RUNTIME_MAPPING.json`, which define the canonical routes for consuming these components in the application.

## 3. Existing Application Gaps
- **Missing Selection Flow:** The current application assumes a `classId` from the profile but lacks a dedicated Subject and Chapter selection flow upon entry.
- **Context Isolation:** While `PathResolver` exists, the UI needs to be strictly constrained to the `activeLearningContext`.
- **Dashboard Display:** The current dashboard acts more as a "Home" summary; it needs to transition into a "Chapter Dashboard" once a selection is made.
- **Navigation Controls:** "Change Subject" and "Change Chapter" mechanisms need to be explicitly implemented to allow seamless context switching without logout.

## 4. Integration Strategy
- **Master Index Generation:** Automatically generate `master_index.json` for each class to bridge the technical IDs and the human-readable folder names.
- **Learning Context Provider:** Implement a React Context to globally manage `activeClass`, `activeSubject`, and `activeChapter`.
- **Lazy Loading:** Ensure the frontend loads only the 42 components of the *active* chapter, preventing memory bloat from the 163-chapter dataset.

## 5. Risk Assessment
- **Data Loss:** Zero risk to existing Firebase user data; integration will focus on the educational content layer.
- **Content Integrity:** All educational text will be rendered directly from the source JSON, adhering to the "No Invention" rule.
- **Isolation:** Strict validation at the `PathResolver` and Frontend Context levels will prevent class/subject leakage.

---
**Status:** Analysis Complete. Ready for Implementation Planning.
