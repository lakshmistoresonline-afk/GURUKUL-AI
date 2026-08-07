# Duplicate Detection Report - Project Gurukul AI

The following components have been identified as duplicates or near-duplicates and are scheduled for consolidation.

## 1. Presentation Layer (Screens)
| Component A | Component B | Status | Recommendation |
| :--- | :--- | :--- | :--- |
| `QuestionCenterScreen` | `QuestionCentreScreen` | **DUPLICATE** | Merge into `QuestionCenterScreen` (ER-spelling). |
| `ChapterListScreen` | `SubjectDashboardScreen` | **OVERLAP** | Use `SubjectDashboardScreen`; deprecate `ChapterListScreen`. |
| `DashboardScreen` (old) | `DashboardScreen` (new) | **REPLACED** | Ensure only the premium Material 3 version exists. |

## 2. Presentation Layer (Widgets)
| Component A | Component B | Status | Recommendation |
| :--- | :--- | :--- | :--- |
| `QuickActionsGrid` | `CommandCenterGrid` | **DUPLICATE** | Merge logic into `CommandCenterGrid`. |
| `StatsHeader` | `GamificationStatsRow` | **DUPLICATE** | Use `GamificationStatsRow`. |

## 3. Business Logic & Services
| Component A | Component B | Status | Recommendation |
| :--- | :--- | :--- | :--- |
| `SpacedRepetitionService` (Planner) | `SpacedRepetitionService` (Curriculum) | **DUPLICATE** | Move to `lib/core/learning/`. |
| `PdfTextExtractor` | `PdfTextExtractorService` | **DUPLICATE** | Consolidate into `PdfTextExtractorService`. |
| `ReportService` | `CoverageReportService` | **OVERLAP** | Merge into `ReportService`. |

## 4. Storage & Models
| Item | Duplicate Paths / Collections |
| :--- | :--- |
| **Firestore** | None detected. |
| **Hive Boxes** | `framework_cache` vs `dynamic_content` (Both used for different purposes, valid). |
| **Assets** | Old `assets/lottie` files moved to `datasets`; internal copies should be removed. |
