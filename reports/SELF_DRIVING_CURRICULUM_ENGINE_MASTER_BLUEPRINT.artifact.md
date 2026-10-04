# GURUKUL AI — THE SELF-DRIVING CURRICULUM ENGINE: MASTER ARCHITECTURE & RESEARCH REPORT

This master research report defines the architectural blueprint for a truly self-driving, fault-free educational platform that ingests raw source files and intelligently processes and renders them up to the student dashboard.

---

## 1. The Autonomous Data Lifecycle

1. **Intelligent Ingestion (`WatcherDaemon` + `SchemaInferenceService`)**: Continuously watches `Contents/`, auto-discovers files, and infers semantic domains.
2. **Graph Normalization (`JsonLdNormalizer`)**: Standardizes any incoming JSON structure into a canonical graph representation.
3. **Strict 1-to-1 Materialization (`generate_processed_content_strict_1to1.py`)**: Materializes chapter-scoped assets without data loss or duplication.
4. **AI Enrichment (`AiEnrichmentService`)**: Automatically synthesizes step-by-step solutions and grading rubrics for unpopulated questions.
5. **Fault-Tolerant Rendering (`ErrorBoundary` + `SafeStructuredCard`)**: Guarantees zero blank screens or runtime exceptions in the React dashboard.

---

## 2. Final Architectural Recommendations

To maintain a 100% fault-free state permanently:
- Keep authoritative source files (`Contents/`) read-only.
- Run continuous UAT word-by-word verification (`uat_word_by_word_verification.py`).
- Use the Playwright test suite (`visual.spec.ts`) for headless UI regression testing.
