# Dependency Analysis: QuestionCentreScreen

## 1. Implementation
- `lib/features/questions/presentation/screens/question_centre_screen.dart`

## 2. Consumers
- `lib/features/student/presentation/screens/subject_dashboard_screen.dart`: Navigates to `QuestionCentreScreen(subject: subject)`.

## 3. Consolidation Goal
- Merge design elements into `QuestionCenterScreen`.
- Redirect `SubjectDashboardScreen` to `QuestionCenterScreen`.
- Delete `QuestionCentreScreen`.
