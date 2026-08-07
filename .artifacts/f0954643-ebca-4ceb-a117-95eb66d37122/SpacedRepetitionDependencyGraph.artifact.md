# Dependency Analysis: SpacedRepetitionService

## 1. Implementations
- `lib/features/curriculum/domain/services/spaced_repetition_service.dart`
- `lib/features/planner/domain/services/spaced_repetition_service.dart`

## 2. Consumers
### Dependency Injection
- `lib/core/di/injection.dart`: Registered as a LazySingleton.

### UI / Features
- `lib/features/curriculum/domain/services/mastery_service.dart` (likely usage)
- `lib/features/planner/presentation/screens/study_planner_screen.dart` (likely usage)

## 3. Reference Prove
- `lib/core/di/injection.dart` line 79: `sl.registerLazySingleton(() => SpacedRepetitionService());`

## 4. Consolidation Goal
- Move to `lib/core/learning/spaced_repetition_service.dart`.
- Update all imports.
