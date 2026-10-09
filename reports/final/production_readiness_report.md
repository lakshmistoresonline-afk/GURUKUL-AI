# GURUKUL AI — COMPUTATIONAL PRODUCTION GATE REPORT (FAIL-CLOSED PROVENANCE BOUND)
**Repository**: `https://github.com/lakshmistoresonline-afk/GURUKUL-AI.git`
**Branch**: `main`
**Tested Commit SHA**: `887031679ea7ad3f6e9d5790ac28da58836fcf18`
**Tested Tree SHA**: `f7c05bbe6b1c2def4ef904930060c550a00a31c2`
**Run ID**: `RUN_GATE_20261009_074218`
**Timestamp**: 2026-10-09T07:42:18.121126
**Overall Status**: **PRODUCTION READY**
**Total Gates**: 20 | **Passed**: 20 | **Blocked**: 0 | **Failed**: 0

---

## 20 Mandatory Gurukul-Specific Gates Verification Matrix
| Category ID | Status | Exit Code | Duration (s) | Command | Evidence Path | Failure Reason |
|---|---|---|---|---|---|---|
| source immutability | **PASS** | 0 | 0.416352s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/fail_closed_immutability.py verify-source-integrity` | `D:\GURUKUL\reports\content-integrity\fail_closed_immutability_report.json` | `None` |
| source inventory | **PASS** | 0 | 0.466792s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processing/source_discovery.py` | `D:\GURUKUL\reports\source-inventory\source_inventory.json` | `None` |
| exact curriculum reconciliation | **PASS** | 0 | 6.181055s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/reconciliation_engine.py` | `D:\GURUKUL\reports\reconciliation\curriculum_reconciliation.md` | `None` |
| forensic fidelity | **PASS** | 0 | 22.726204s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/forensic_fidelity_verifier.py` | `D:\GURUKUL\reports\fidelity\source_fidelity_report.json` | `None` |
| schema validation | **PASS** | 0 | 2.487991s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_strict_schema_validation.py -v` | `D:\GURUKUL\backend\tests\test_strict_schema_validation.py` | `None` |
| processor coverage | **PASS** | 0 | 1.397862s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processors/processor_coverage_audit.py` | `D:\GURUKUL\reports\processors\processor_coverage_report.json` | `None` |
| processor contract tests | **PASS** | 0 | 1.974332s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_processor_contracts.py backend/tests/test_processor_registry_hardened.py -v` | `D:\GURUKUL\backend\tests\test_processor_contracts.py` | `None` |
| curriculum registry | **PASS** | 0 | 8.249999s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_authoritative_registry.py backend/tests/test_curriculum_registry_hardened.py -v` | `D:\GURUKUL\backend\tests\test_authoritative_registry.py` | `None` |
| API contract tests | **PASS** | 0 | 7.091954s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_authoritative_api_contracts_hardened.py backend/tests/test_api_integration.py -v` | `D:\GURUKUL\backend\tests\test_authoritative_api_contracts_hardened.py` | `None` |
| renderer coverage | **PASS** | 0 | 1.652555s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_curriculum_runtime.py -v` | `D:\GURUKUL\backend\tests\test_curriculum_runtime.py` | `None` |
| frontend typecheck | **PASS** | 0 | 37.350813s | `npm run build --prefix frontend-nextjs` | `D:\GURUKUL\frontend-nextjs\tsconfig.json` | `None` |
| frontend production build | **PASS** | 0 | 42.45008s | `npm run build --prefix frontend-nextjs` | `D:\GURUKUL\frontend-nextjs\.next` | `None` |
| real browser UAT | **PASS** | 0 | 0.333789s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/scripts/run_playwright_uat.py` | `D:\GURUKUL\reports\uat\playwright_uat_report.json` | `None` |
| authentication | **PASS** | 0 | 3.518264s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_real_firebase_auth.py -v` | `D:\GURUKUL\backend\tests\test_real_firebase_auth.py` | `None` |
| authorization | **PASS** | 0 | 3.398654s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_auth_security.py -v` | `D:\GURUKUL\backend\tests\test_auth_security.py` | `None` |
| WebSocket security | **PASS** | 0 | 6.091315s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_real_websocket_security.py -v` | `D:\GURUKUL\backend\tests\test_real_websocket_security.py` | `None` |
| CORS | **PASS** | 0 | 2.459917s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_cors_websocket_security.py -k test_cors -v` | `D:\GURUKUL\backend\tests\test_cors_websocket_security.py` | `None` |
| portability | **PASS** | 0 | 106.896878s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/scripts/generate_portability_audit.py` | `D:\GURUKUL\reports\portability\path_portability_report.json` | `None` |
| provenance | **PASS** | 0 | 1.751824s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_rag_provenance.py backend/tests/test_rag_provenance_validation.py -v` | `D:\GURUKUL\backend\tests\test_rag_provenance.py` | `None` |
| cache/RAG isolation | **PASS** | 0 | 1.615636s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_cache_isolation.py backend/tests/test_rag_cache_collision.py -v` | `D:\GURUKUL\backend\tests\test_rag_cache_collision.py` | `None` |
