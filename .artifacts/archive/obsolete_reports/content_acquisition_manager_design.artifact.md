# Content Acquisition Manager Design

## Overview
The Content Acquisition Manager (CAM) is a specialized module designed to automate the ingestion, processing, and enrichment of educational resources (NCERT PDFs, etc.) into the Gurukul AI platform.

## Architecture
The module follows a layered architecture (Feature-driven):
- **Models**: `AcquisitionFile`, `ImportQueueItem`, `ExtractionResult`, `ValidationReport`.
- **Services**:
  - `RepositoryScannerService`: Automatically detects new files in `ncert_source`.
  - `PDFProcessorService`: Extracts text, images, and tables from documents.
  - `AssetProcessorService`: Organizes and renames extracted media.
  - `ChapterBuilderService`: Structures raw text into logical `ConceptNode` entities.
  - `AIPipelineService`: Enriches chapters with summaries, quizzes, and embeddings.
  - `ValidationEngine`: Ensures repository integrity and data quality.
- **Repository**: `ContentAcquisitionRepository` (Persistence via Hive).
- **Controller**: `AcquisitionBloc` (Business logic and state management).
- **UI**: `AcquisitionDashboardScreen` (Progress monitoring and manual controls).

## Data Flow
1. **Discovery**: `RepositoryScanner` identifies files in `datasets/ncert_source/`.
2. **Queuing**: Files are added to the persistent `ImportQueue`.
3. **Extraction**: `PDFProcessor` performs OCR/Extraction and saves raw output to `ai_json/raw_extractions/`.
4. **Structuring**: `ChapterBuilder` creates `lesson.json` and `metadata.json` for each chapter.
5. **Enrichment**: `AIPipeline` generates auxiliary assets (flashcards, quizzes).
6. **Validation**: `ValidationEngine` confirms the processed output matches standards.

## Progress Dashboard
Accessible via **Admin Console > Content Acquisition**. It provides real-time visibility into the import pipeline, storage usage, and system health.
