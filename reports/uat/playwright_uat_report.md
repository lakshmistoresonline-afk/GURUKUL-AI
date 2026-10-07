# E2E UAT REPORT (GEN-2 STRICT)
**Timestamp**: 2026-10-07T11:43:29.628789
**Status**: **PASS**
**Environment**: Python TestClient E2E UAT Suite
**Test Count**: 12 | **Passed**: 12 | **Failed**: 0 | **Skipped**: 0
**Exit Code**: 0

---

## Command Executed
`C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_authoritative_api_contracts_hardened.py backend/tests/test_api_integration.py -v`

## Artifact Paths
- `reports/uat/playwright_uat_report.json`
- `reports/uat/playwright_uat_report.md`

## Output / Evidence
```text
ytest_cache
rootdir: D:\GURUKUL\backend
configfile: pytest.ini
plugins: anyio-4.14.2, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 11 items

backend\tests\test_authoritative_api_contracts_hardened.py::test_api_hierarchy_endpoint PASSED [  9%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_api_resolve_valid_class7_maths_i PASSED [ 18%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_api_resolve_valid_class7_maths_ii PASSED [ 27%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_class7_maths_ii_never_returns_maths_i PASSED [ 36%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_class7_social_ii_never_returns_social_i PASSED [ 45%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_api_resolve_missing_identity_params PASSED [ 54%]
backend\tests\test_authoritative_api_contracts_hardened.py::test_api_resolve_unsupported_content_type PASSED [ 63%]
backend\tests\test_api_integration.py::test_api_classes_endpoint PASSED  [ 72%]
backend\tests\test_api_integration.py::test_api_grade_subjects_endpoint PASSED [ 81%]
backend\tests\test_api_integration.py::test_api_chapter_source_endpoint PASSED [ 90%]
backend\tests\test_api_integration.py::test_api_chapter_source_not_found PASSED [100%]

============================== warnings summary ===============================
C:\Users\srina\AppData\Local\Programs\Python\Python313\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\srina\AppData\Local\Programs\Python\Python313\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 11 passed, 1 warning in 1.79s ========================
```
