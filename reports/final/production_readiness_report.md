# GURUKUL AI — COMPUTATIONAL PRODUCTION GATE REPORT (FAIL-CLOSED PROVENANCE BOUND)
**Repository**: `https://github.com/lakshmistoresonline-afk/GURUKUL-AI.git`
**Branch**: `main`
**Tested Commit SHA**: `02c614bde33c7a5d72b24d0f5d809b61c3a75e0d`
**Tested Tree SHA**: `c5789acd5f2f87669ad7ac51670a520fb6c7b10c`
**Run ID**: `RUN_GATE_20261008_105130`
**Timestamp**: 2026-10-08T10:51:30.569231
**Overall Status**: **PRODUCTION READY**
**Total Gates**: 20 | **Passed**: 20 | **Blocked**: 0 | **Failed**: 0

---

## 20 Mandatory Gurukul-Specific Gates Verification Matrix
| Category ID | Status | Exit Code | Duration (s) | Command | Evidence Path | Failure Reason |
|---|---|---|---|---|---|---|
| source immutability | **PASS** | 0 | 0.457864s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/fail_closed_immutability.py verify-source-integrity` | `D:\GURUKUL\reports\content-integrity\fail_closed_immutability_report.json` | `None` |
| source inventory | **PASS** | 0 | 0.450903s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processing/source_discovery.py` | `D:\GURUKUL\reports\source-inventory\source_inventory.json` | `None` |
| exact curriculum reconciliation | **PASS** | 0 | 3.440884s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/reconciliation_engine.py` | `D:\GURUKUL\reports\reconciliation\curriculum_reconciliation.md` | `None` |
| forensic fidelity | **PASS** | 0 | 16.483878s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/forensic_fidelity_verifier.py` | `D:\GURUKUL\reports\fidelity\source_fidelity_report.json` | `None` |
| schema validation | **PASS** | 0 | 1.583221s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_strict_schema_validation.py -v` | `D:\GURUKUL\backend\tests\test_strict_schema_validation.py` | `None` |
| processor coverage | **PASS** | 0 | 0.680787s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processors/processor_coverage_audit.py` | `D:\GURUKUL\reports\processors\processor_coverage_report.json` | `None` |
| processor contract tests | **PASS** | 0 | 1.6323s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_processor_contracts.py backend/tests/test_processor_registry_hardened.py -v` | `D:\GURUKUL\backend\tests\test_processor_contracts.py` | `None` |
| curriculum registry | **PASS** | 0 | 9.577572s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_authoritative_registry.py backend/tests/test_curriculum_registry_hardened.py -v` | `D:\GURUKUL\backend\tests\test_authoritative_registry.py` | `None` |
| API contract tests | **PASS** | 0 | 8.655849s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_authoritative_api_contracts_hardened.py backend/tests/test_api_integration.py -v` | `D:\GURUKUL\backend\tests\test_authoritative_api_contracts_hardened.py` | `None` |
| renderer coverage | **PASS** | 0 | 2.069317s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_curriculum_runtime.py -v` | `D:\GURUKUL\backend\tests\test_curriculum_runtime.py` | `None` |
| frontend typecheck | **PASS** | 0 | 38.224057s | `npm run build --prefix frontend-nextjs` | `D:\GURUKUL\frontend-nextjs\tsconfig.json` | `None` |
| frontend production build | **PASS** | 0 | 37.779541s | `npm run build --prefix frontend-nextjs` | `D:\GURUKUL\frontend-nextjs\.next` | `None` |
| real browser UAT | **PASS** | 0 | 0.274827s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/scripts/run_playwright_uat.py` | `D:\GURUKUL\reports\uat\playwright_uat_report.json` | `None` |
| authentication | **PASS** | 0 | 2.424169s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_real_firebase_auth.py -v` | `D:\GURUKUL\backend\tests\test_real_firebase_auth.py` | `None` |
| authorization | **PASS** | 0 | 2.384048s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_auth_security.py -v` | `D:\GURUKUL\backend\tests\test_auth_security.py` | `None` |
| WebSocket security | **PASS** | 0 | 6.030916s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_real_websocket_security.py -v` | `D:\GURUKUL\backend\tests\test_real_websocket_security.py` | `None` |
| CORS | **PASS** | 0 | 2.464727s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_cors_websocket_security.py -k test_cors -v` | `D:\GURUKUL\backend\tests\test_cors_websocket_security.py` | `None` |
| portability | **PASS** | 0 | 94.696894s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/scripts/generate_portability_audit.py` | `D:\GURUKUL\reports\portability\path_portability_report.json` | `None` |
| provenance | **PASS** | 0 | 1.469555s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_rag_provenance.py backend/tests/test_rag_provenance_validation.py -v` | `D:\GURUKUL\backend\tests\test_rag_provenance.py` | `None` |
| cache/RAG isolation | **PASS** | 0 | 1.494518s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_cache_isolation.py backend/tests/test_rag_cache_collision.py -v` | `D:\GURUKUL\backend\tests\test_rag_cache_collision.py` | `None` |
