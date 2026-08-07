# Gurukul AI – Dataset Structure Refactoring Implementation Plan

This plan outlines the restructuring of the data layer for Project Gurukul AI, consolidating all data assets into a new `datasets/` directory while maintaining compatibility with the existing application logic.

## User Review Required

> [!IMPORTANT]
> - Existing hardcoded paths in `FrameworkRepository.dart` and `LessonMediaRepository.dart` will be updated to point to the new `datasets/` structure.
> - The `content_repository` folder will be moved/reorganized into `datasets/`.
> - `datasets/ncert_source/` will be initialized with class and subject subfolders as requested, but will remain empty (containing only `.gitkeep` and `README.md`).

## Proposed Changes

### [Data Layer Refactoring]

#### [NEW] [datasets/](file:///D:/GURUKUL-AI/datasets)
The new root for all data-related assets.

#### [NEW] [datasets/ncert_source/](file:///D:/GURUKUL-AI/datasets/ncert_source)
Placeholder structure for future NCERT resource ingestion. Subfolders for Class 5 and 6 subjects will be created.

#### [NEW] [datasets/processed/](file:///D:/GURUKUL-AI/datasets/processed)
Consolidated location for processed curriculum data, flashcards, quizzes, and AI-generated content.

#### [NEW] [datasets/assets/](file:///D:/GURUKUL-AI/datasets/assets)
Media assets (diagrams, images, illustrations) migrated from `content_repository/multimedia`.

#### [NEW] [datasets/database/](file:///D:/GURUKUL-AI/datasets/database)
Structure for database exports and local database files.

#### [DELETE] [content_repository/](file:///D:/GURUKUL-AI/content_repository)
Obsolete root directory after successful migration.

### [Application Logic Compatibility]

#### [MODIFY] [framework_repository.dart](file:///D:/GURUKUL-AI/lib/features/curriculum/data/framework_repository.dart)
Update `root` path and `chapterDir` to point to `datasets/processed/chapters`.

#### [MODIFY] [lesson_media_repository.dart](file:///D:/GURUKUL-AI/lib/features/curriculum/data/media/lesson_media_repository.dart)
Update `_root` path to point to `datasets/processed/chapters`.

#### [MODIFY] [repository_scanner.dart](file:///D:/GURUKUL-AI/lib/core/content/repository_scanner.dart)
Update scanner logic to handle the new directory structure in `datasets/processed/`.

## Verification Plan

### Automated Tests
- Run `flutter test` to ensure no regression in data-dependent features.
- Execute repository health check via `FrameworkRepository.getRepositoryHealth()`.

### Manual Verification
- Verify the new `datasets/` tree matches the requested architecture.
- Check all `README.md` and `.gitkeep` files are present.
- Ensure the app launches and displays curriculum data (Subjects, Chapters) correctly.
- Verify media assets (images, lottie animations) still load in the UI.

## Reports Generation
1. Repository Structure Report
2. Deleted Files Report
3. New Folder Structure Report
4. Compatibility Report
5. Migration Report
6. Data Architecture Report
