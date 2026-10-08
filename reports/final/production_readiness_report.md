# GURUKUL AI — COMPUTATIONAL PRODUCTION GATE REPORT (FAIL-CLOSED PROVENANCE BOUND)
**Repository**: `https://github.com/lakshmistoresonline-afk/GURUKUL-AI.git`
**Branch**: `main`
**Tested Commit SHA**: `1d624c732bdbb9ce25c7185c503c70546860f6d9`
**Tested Tree SHA**: `05e360cc8adc9c469d86f740ddbfa97bc1323d0f`
**Run ID**: `RUN_GATE_20261008_082950`
**Timestamp**: 2026-10-08T08:29:50.191464
**Overall Status**: **BLOCKED**
**Total Gates**: 20 | **Passed**: 7 | **Blocked**: 13 | **Failed**: 0

---

## 20 Mandatory Gurukul-Specific Gates Verification Matrix
| Category ID | Status | Exit Code | Duration (s) | Command | Evidence Path | Failure Reason |
|---|---|---|---|---|---|---|
| source immutability | **PASS** | 0 | 0.47842s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/fail_closed_immutability.py verify-source-integrity` | `D:\GURUKUL\reports\content-integrity\fail_closed_immutability_report.json` | `None` |
| source inventory | **PASS** | 0 | 0.362404s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processing/source_discovery.py` | `D:\GURUKUL\reports\source-inventory\source_inventory.json` | `None` |
| exact curriculum reconciliation | **BLOCKED** | 0 | 1.121224s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/reconciliation_engine.py` | `D:\GURUKUL\reports\reconciliation\curriculum_reconciliation.md` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| forensic fidelity | **PASS** | 0 | 6.739224s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/forensic_fidelity_verifier.py` | `D:\GURUKUL\reports\fidelity\source_fidelity_report.json` | `None` |
| schema validation | **BLOCKED** | 0 | 1.693636s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_strict_schema_validation.py -v` | `D:\GURUKUL\backend\tests\test_strict_schema_validation.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| processor coverage | **PASS** | 0 | 0.685049s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processors/processor_coverage_audit.py` | `D:\GURUKUL\reports\processors\processor_coverage_report.json` | `None` |
| processor contract tests | **BLOCKED** | 0 | 1.83763s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_processor_contracts.py backend/tests/test_processor_registry_hardened.py -v` | `D:\GURUKUL\backend\tests\test_processor_contracts.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| curriculum registry | **BLOCKED** | 0 | 5.838663s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_authoritative_registry.py backend/tests/test_curriculum_registry_hardened.py -v` | `D:\GURUKUL\backend\tests\test_authoritative_registry.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| API contract tests | **BLOCKED** | 0 | 6.983404s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_authoritative_api_contracts_hardened.py backend/tests/test_api_integration.py -v` | `D:\GURUKUL\backend\tests\test_authoritative_api_contracts_hardened.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| renderer coverage | **BLOCKED** | 0 | 2.209136s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_curriculum_runtime.py -v` | `D:\GURUKUL\backend\tests\test_curriculum_runtime.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| frontend typecheck | **PASS** | 0 | 35.856447s | `npm run build --prefix frontend-nextjs` | `D:\GURUKUL\frontend-nextjs\tsconfig.json` | `None` |
| frontend production build | **BLOCKED** | 0 | 35.677427s | `npm run build --prefix frontend-nextjs` | `D:\GURUKUL\frontend-nextjs\.next` | `Failed to parse evidence provenance: [Errno 13] Permission denied: 'D:\\GURUKUL\` |
| real browser UAT | **PASS** | 0 | 5.762842s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/scripts/run_playwright_uat.py` | `D:\GURUKUL\reports\uat\playwright_uat_report.json` | `None` |
| authentication | **BLOCKED** | 0 | 2.44401s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_real_firebase_auth.py -v` | `D:\GURUKUL\backend\tests\test_real_firebase_auth.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| authorization | **BLOCKED** | 0 | 2.373355s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_auth_security.py -v` | `D:\GURUKUL\backend\tests\test_auth_security.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| WebSocket security | **BLOCKED** | 0 | 5.764846s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_real_websocket_security.py -v` | `D:\GURUKUL\backend\tests\test_real_websocket_security.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| CORS | **BLOCKED** | 0 | 2.840547s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_cors_websocket_security.py -k test_cors -v` | `D:\GURUKUL\backend\tests\test_cors_websocket_security.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| portability | **PASS** | 0 | 88.519672s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/scripts/generate_portability_audit.py` | `D:\GURUKUL\reports\portability\path_portability_report.json` | `None` |
| provenance | **BLOCKED** | 0 | 1.472583s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_rag_provenance.py backend/tests/test_rag_provenance_validation.py -v` | `D:\GURUKUL\backend\tests\test_rag_provenance.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| cache/RAG isolation | **BLOCKED** | 0 | 1.490093s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_cache_isolation.py backend/tests/test_rag_cache_collision.py -v` | `D:\GURUKUL\backend\tests\test_rag_cache_collision.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
