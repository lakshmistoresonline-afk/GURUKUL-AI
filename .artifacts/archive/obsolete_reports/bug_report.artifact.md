# Bug Report: Phase 40 Verification

The following defects and technical debt items were identified during the runtime verification phase.

## 🔴 Critical Issues

### B-001: Build Pipeline Blocked
- **Symptom:** `flutter` command is unrecognized in the terminal.
- **Impact:** Prevents generation of Release APK and execution of unit/widget tests.
- **Proposed Fix:** Install Flutter SDK 3.22.0 or higher and add to system PATH.

### B-002: Gradle Configuration Error
- **Symptom:** `gradlew help` fails with `AndroidLocationsBuildService` creation error.
- **Impact:** Blocks native Android compilation.
- **Proposed Fix:** Verify Android SDK path and ensure build process has permissions to create `~/.android` directories.

## 🟡 Major Issues

### B-003: Non-standard Project Structure
- **Symptom:** Project uses `app/` directory instead of the standard Flutter `android/` directory.
- **Impact:** Confuses build automation and prevents standard Flutter-Gradle integration.
- **Proposed Fix:** Refactor native code into standard `android/` folder using `flutter create .` once CLI is restored.

## 🟢 Minor Issues / Debt

### B-004: Missing TTL for Assessment Sessions
- **Symptom:** Local assessment sessions in Hive do not expire.
- **Impact:** Minor memory bloat over time.
- **Proposed Fix:** Implement a timestamp-based cleanup in `LocalStorageService`.

### B-005: Socratic Prompt Refinement
- **Symptom:** High variability in AI hint quality based on user input.
- **Impact:** Pedagogical inconsistency.
- **Proposed Fix:** Add few-shot examples to the `AiTutorService` system prompt.
