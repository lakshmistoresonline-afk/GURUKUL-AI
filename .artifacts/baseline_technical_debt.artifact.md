# Gurukul AI – Technical Debt Assessment

| Area | Debt Description | Severity | Recommendation |
| :--- | :--- | :--- | :--- |
| **Code** | 85+ lint/analyzer warnings (mostly unused imports and deprecated `withOpacity`). | Medium | Perform a bulk lint cleanup. |
| **Architecture** | Simulations in CAM (Extraction and AI logic). | High | Integrate real OCR (ML Kit) and Gemini API calls. |
| **Testing** | Low unit test coverage for complex logic like `SpacedRepetitionService`. | Medium | Add targeted unit tests for `core/learning`. |
| **Dataset** | Hardcoded chapter folder suffixes in `FrameworkRepository` mapping logic. | Low | Use the standard `id` from metadata for directory resolution. |
| **UI** | Duplicate `dispose()` method in `ContentPlayerScreen`. | Low | Remove redundant method definition. |
| **Platform** | Non-standard `app/` folder in root (legacy artifact). | Low | Confirm it can be safely removed or renamed. |

## Debt Summary
Most technical debt is "Planned Debt" (Simulations in CAM). The infrastructure is healthy, but the "glue" code (linting, imports) needs maintenance.
