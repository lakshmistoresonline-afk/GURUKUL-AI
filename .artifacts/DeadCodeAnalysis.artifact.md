# Dead Code Analysis - Project Gurukul AI

## 1. Unused Files & Modules
| File Path | Reason |
| :--- | :--- |
| `lib/features/auth/data/sunbird_auth_service.dart` | Not registered in DI; no active usages in screens. |
| `lib/features/parent/domain/services/coverage_report_service.dart` | Superseded by `ReportService`. |
| `lib/features/student/presentation/screens/chapter_list_screen.dart` | Replaced by `SubjectDashboardScreen`. |

## 2. Unused Widgets
- `lib/features/student/presentation/widgets/dashboard/stats_header.dart`
- `lib/features/student/presentation/widgets/dashboard/quick_actions_grid.dart`

## 3. Deprecated APIs
- `withOpacity(double)`: Found 42 instances. Replace with `withValues(alpha: double)`.
- `groupValue`/`onChanged` in `Radio`: Found in `learning_journey_screen.dart`.

## 4. Dead Imports
- `SubjectDashboardScreen`: Imports deleted `ncert_detailed_content.dart`.
- Multiple files: Imports of unused `Material` or `DesignSystem`.

## 5. Dead Routes
- Legacy navigation paths in `DashboardBottomNav` pointing to unimplemented tabs.
