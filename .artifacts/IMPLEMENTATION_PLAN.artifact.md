# Implementation Plan: Repository Consolidation

## 1. Core Consolidation
- **Spaced Repetition**: Create `lib/core/learning/spaced_repetition_service.dart`.
    - *Action*: Merge logic from `planner` and `curriculum` versions.
    - *Justification*: Unify learning algorithms across the app.
- **Text Extraction**: Consolidate `PdfTextExtractor` into `PdfTextExtractorService`.

## 2. Feature Consolidation
- **Questions**: Merge `QuestionCentreScreen` (re) into `QuestionCenterScreen` (er).
    - *Action*: Use (er) as the base, add high-fidelity header from (re).
    - *Justification*: Resolve spelling duplicate and functional fragmentation.
- **Parent/Teacher**: Merge `CoverageReportService` into `ReportService`.

## 3. UI/UX Consolidation (Presentation Layer)
- **Home Dashboard**:
    - *Action*: Delete `QuickActionsGrid` and `StatsHeader`.
    - *Action*: Ensure `DashboardScreen` only uses `CommandCenterGrid` and `GamificationStatsRow`.
- **Subject/Chapter**:
    - *Action*: Fix broken imports in `SubjectDashboardScreen`.
    - *Action*: Deprecate `ChapterListScreen`.

## 4. Code Cleanup
- **Cleanup**: Delete all files identified in `DeadCodeAnalysis.md`.
- **API Modernization**: Run global search/replace for `withOpacity` -> `withValues`.
- **Import Optimization**: Remove unused imports project-wide.

## 5. Verification
- **Audit**: Run `RepositoryConsolidationReport.md` generation.
- **Test**: Run `flutter analyze` and `flutter test`.
