# Fix MasteryRepository Registration Error

The error `Bad state: GetIt: Object/factory with type MasteryRepository is not registered inside GetIt` occurs because `MasteryRepository` is not being registered in the Service Locator (`sl`) before it is used. This is happening in two scenarios:

1. **Runtime (likely Web):** `di.init()` fails when initializing `FrameworkRepository` due to a hardcoded absolute Windows path (`D:/GURUKUL-AI/...`) that doesn't exist in the runtime environment (especially on Web). Since `MasteryRepository` is registered *after* this failing call, its registration is skipped.
2. **Tests:** `dashboard_widget_test.dart` pumps `DashboardScreen`, which contains `ProgressDashboardScreen` in an `IndexedStack`. `IndexedStack` initializes all children's states, calling `sl<MasteryRepository>()` in `ProgressDashboardScreen.initState`. However, the test's `setUp` does not register `MasteryRepository`.

## Proposed Changes

### 1. [DI Registration Logic](file:///D:/GURUKUL-AI/lib/core/di/injection.dart)
- Move `MasteryRepository` and other independent registrations *before* `frameworkRepo.init()`.
- Wrap `frameworkRepo.init()` in a `try-catch` block to ensure that a failure in loading local datasets doesn't break the entire dependency tree.

### 2. [Test Setup](file:///D:/GURUKUL-AI/test/dashboard_widget_test.dart)
- Add a mock or real registration for `MasteryRepository` in the `setUp` method of the dashboard widget test.

### 3. [Framework Repository Robustness](file:///D:/GURUKUL-AI/lib/features/curriculum/data/framework_repository.dart)
- Add a check for `kIsWeb` and ensure it doesn't try to use absolute local paths on Web.

## Verification Plan

### Automated Tests
- Run `flutter test test/dashboard_widget_test.dart` to verify that the smoke test passes.

### Manual Verification
- Re-run the app (especially if targeting Web) and verify that the "Progress" tab (and the app initialization) no longer crashes with DI errors.
