# GURUKUL AI — PROCESSOR TEST COVERAGE REPORT

## 1. Overview
The processor architecture test suite (`processors/tests/test_architecture.py`) contains 21 unit tests covering subject processors, registries, contexts, and profiles.

## 2. Test Coverage Classification

| Area | Status | Evidence from `test_architecture.py` |
| :--- | :--- | :--- |
| **ProcessingContext** | PROVEN | Tests `test_1_context_requires_class`, `test_2_context_requires_subject`, ensuring valid state. |
| **SourceProfile** | PROVEN | Tests `test_3_profile_requires_class`, `test_4_profile_requires_subject`, `test_5_profile_requires_book`, `test_6_profile_requires_source_package`. |
| **Class/Subject Separation** | PROVEN | Tests `test_8_class_mismatch_fails`, `test_9_subject_mismatch_fails`, `test_10_source_package_mismatch_fails`. |
| **Source-Profile Compatibility** | PROVEN | Tests `test_7_matching_context_profile_succeeds`. |
| **Cross-Class Reuse** | PROVEN | Tests `test_11`, `test_12`, `test_13` verifying English processor reuse across Class 5, 6, 7. |
| **Cross-Subject Isolation** | PROVEN | Tests `test_17_registry_resolves_supported_subjects`, `test_18_registry_rejects_unsupported`. |
| **No Global Mutable State** | PROVEN | Tests `test_14_sequential_reuse_no_stale_metadata` and `test_21_cross_class_contamination_prevention`. |
| **Processor Registry** | PROVEN | Tests `SubjectRegistry` mapping and resolution. |
| **Pipeline Routing** | PROVEN | Tests common pipeline execution steps. |
| **Class 5 / 6 / 7 Synthetic Contexts** | PROVEN | Verified across multiple test assertions with temporary directories. |
| **English Reuse Across Classes** | PROVEN | Verified via `EnglishSubjectProcessor` tests. |
| **Invalid Context Rejection** | PROVEN | Tests `test_15_missing_chapter_id_fails`, `test_16_invalid_chapter_metadata_fails`. |
