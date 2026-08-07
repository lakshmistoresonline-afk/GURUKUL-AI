# Gurukul AI – Phased Roadmap

## Phase A: Stability & Polish (Immediate)
- Fix all `flutter analyze` errors and warnings.
- Resolve duplicate method in `ContentPlayerScreen`.
- Standardize all package imports (no relative imports).

## Phase B: Production Data Ingestion (Month 1)
- Populating `ncert_source` with actual PDFs for Class 5 and 6.
- Replace simulation in `PDFProcessorService` with ML Kit Text Recognition.
- Implement Gemini-powered extraction for `MetadataGenerator`.

## Phase C: AI Enrichment fine-tuning (Month 2)
- Transition `AIPipelineService` to live Gemini 1.5 calls.
- Optimize prompt templates for Summary and Quiz generation.
- Implement Vector DB (Chroma/Pinecone) or local search index.

## Phase D: Quality Assurance (Month 3)
- Target 60% test coverage for `core` and `features/curriculum`.
- Conduct security audit on Firebase Rules and Hive encryption.
- Performance benchmarking for large dataset loading.
