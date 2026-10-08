# E2E UAT REPORT (GEN-2 STRICT)
**Timestamp**: 2026-10-08T07:33:03.226243
**Status**: **PASS**
**Environment**: FastAPI TestClient Authoritative E2E Engine
**Working Directory**: `D:\GURUKUL`
**Test Count**: 16 | **Passed**: 16 | **Failed**: 0 | **Skipped**: 0
**Exit Code**: 0

---

## Command Executed
`C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_authoritative_api_contracts_hardened.py backend/tests/test_api_integration.py backend/tests/test_isolation.py -v`

## Artifact Paths
- `reports/uat/playwright_uat_report.json`
- `reports/uat/playwright_uat_report.md`

## Output / Evidence
```text

backend\tests\test_authoritative_api_contracts_hardened.py::test_api_hierarchy_endpoint PASSED [  7%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_api_resolve_valid_class7_maths_i PASSED [ 14%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_api_resolve_valid_class7_maths_ii PASSED [ 21%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_class7_maths_ii_never_returns_maths_i PASSED [ 28%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_class7_social_ii_never_returns_social_i PASSED [ 35%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_api_resolve_missing_identity_params PASSED [ 42%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_api_resolve_unsupported_content_type PASSED [ 50%]
backend\tests\test_api_integration.py::test_api_classes_endpoint PASSED  [ 57%]
backend\tests\test_api_integration.py::test_api_grade_subjects_endpoint PASSED [ 64%]
backend\tests\test_api_integration.py::test_api_chapter_source_endpoint PASSED [ 71%]
backend\tests\test_api_integration.py::test_api_chapter_source_not_found PASSED [ 78%]
backend\tests\test_isolation.py::test_chapter_isolation_success PASSED   [ 85%]
backend\tests\test_isolation.py::test_negative_isolation_wrong_class PASSED [ 92%]
backend\tests\test_isolation.py::test_negative_isolation_nonexistent_chapter PASSED [100%]

============================== warnings summary ===============================
C:\Users\srina\AppData\Local\Programs\Python\Python313\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\srina\AppData\Local\Programs\Python\Python313\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 14 passed, 1 warning in 4.39s ========================
```
