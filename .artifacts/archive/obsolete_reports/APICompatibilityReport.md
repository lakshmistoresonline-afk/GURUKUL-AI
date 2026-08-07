# API Compatibility Report - Repository Consolidation

## 1. Services
| Old Service | New Service | Compatibility |
| :--- | :--- | :--- |
| `SpacedRepetitionService` | `lib/core/learning/spaced_repetition_service.dart` | Full. Public methods preserved. |
| `PdfTextExtractor` | `PdfTextExtractorService` | Full. |

## 2. Widgets
| Old Widget | New Widget | Compatibility |
| :--- | :--- | :--- |
| `InteractivePlayerWidget` | `InteractivePlayer` | Full. Props mapped to `pathOrUrl`. |
| `InteractiveContentPlayer` | `InteractivePlayer` | Full. |

## 3. Navigation
- `QuestionCentreScreen` route replaced by `QuestionCenterScreen`.
- `ChapterListScreen` route replaced by `SubjectDashboardScreen`.
- All legacy arguments (subject, classLevel) are correctly mapped to new constructors.
