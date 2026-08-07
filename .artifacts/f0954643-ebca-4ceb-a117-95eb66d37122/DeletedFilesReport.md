# Deleted Files Report - Repository Consolidation

The following files have been deleted as part of the phase 55 consolidation to reduce technical debt and remove duplicate implementations.

## 1. Duplicated Screens
- `lib/features/questions/presentation/screens/question_centre_screen.dart` (Merged into `QuestionCenterScreen`)

## 2. Redundant Widgets
- `lib/features/content/presentation/widgets/interactive_player_widget.dart` (Moved to `core/widgets/content/`)
- `lib/features/curriculum/presentation/widgets/interactive_content_player.dart` (Replaced by `InteractivePlayer`)
- `lib/features/student/presentation/widgets/dashboard/quick_actions_grid.dart` (Dead code, replaced by `CommandCenterGrid`)
- `lib/features/student/presentation/widgets/dashboard/stats_header.dart` (Dead code, replaced by `GamificationStatsRow`)

## 3. Duplicated Services
- `lib/features/curriculum/domain/services/spaced_repetition_service.dart` (Unified in `core/learning/`)
- `lib/features/planner/domain/services/spaced_repetition_service.dart` (Unified in `core/learning/`)
- `lib/features/content/data/pdf_text_extractor.dart` (Consolidated into `PdfTextExtractorService`)

## 4. Dead Code
- `lib/features/auth/data/sunbird_auth_service.dart` (Unused)
- `lib/features/parent/domain/services/coverage_report_service.dart` (Unused)
- `lib/features/student/presentation/screens/chapter_list_screen.dart` (Replaced by `SubjectDashboardScreen`)
