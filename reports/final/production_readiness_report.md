# GURUKUL AI — COMPUTATIONAL PRODUCTION GATE REPORT (FAIL-CLOSED PROVENANCE BOUND)
**Repository**: `https://github.com/lakshmistoresonline-afk/GURUKUL-AI.git`
**Branch**: `main`
**Tested Commit SHA**: `3a3123f017dc39f3e423a13f695452ddbd50b965`
**Tested Tree SHA**: `6a6173ba81d445ecfb4deb25c670886ada7fd77d`
**Run ID**: `RUN_GATE_20261008_085542`
**Timestamp**: 2026-10-08T08:55:42.048711
**Overall Status**: **BLOCKED**
**Total Gates**: 20 | **Passed**: 6 | **Blocked**: 14 | **Failed**: 0

---

## 20 Mandatory Gurukul-Specific Gates Verification Matrix
| Category ID | Status | Exit Code | Duration (s) | Command | Evidence Path | Failure Reason |
|---|---|---|---|---|---|---|
| source immutability | **PASS** | 0 | 0.472647s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/fail_closed_immutability.py verify-source-integrity` | `D:\GURUKUL\reports\content-integrity\fail_closed_immutability_report.json` | `None` |
| source inventory | **PASS** | 0 | 0.556217s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processing/source_discovery.py` | `D:\GURUKUL\reports\source-inventory\source_inventory.json` | `None` |
| exact curriculum reconciliation | **BLOCKED** | 1 | 3.351105s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/reconciliation_engine.py` | `D:\GURUKUL\reports\reconciliation\curriculum_reconciliation.md` | `Command exited with code 1: Reconciliation completed. Status: FAIL` |
| forensic fidelity | **BLOCKED** | 1 | 6.434534s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/forensic_fidelity_verifier.py` | `D:\GURUKUL\reports\fidelity\source_fidelity_report.json` | `Command exited with code 1: Forensic fidelity verification completed. Status: FA` |
| schema validation | **BLOCKED** | 0 | 1.60759s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_strict_schema_validation.py -v` | `D:\GURUKUL\backend\tests\test_strict_schema_validation.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| processor coverage | **PASS** | 0 | 0.794857s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processors/processor_coverage_audit.py` | `D:\GURUKUL\reports\processors\processor_coverage_report.json` | `None` |
| processor contract tests | **BLOCKED** | 0 | 1.498271s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_processor_contracts.py backend/tests/test_processor_registry_hardened.py -v` | `D:\GURUKUL\backend\tests\test_processor_contracts.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| curriculum registry | **BLOCKED** | 0 | 4.653831s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_authoritative_registry.py backend/tests/test_curriculum_registry_hardened.py -v` | `D:\GURUKUL\backend\tests\test_authoritative_registry.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| API contract tests | **BLOCKED** | 0 | 5.691676s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_authoritative_api_contracts_hardened.py backend/tests/test_api_integration.py -v` | `D:\GURUKUL\backend\tests\test_authoritative_api_contracts_hardened.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| renderer coverage | **BLOCKED** | 0 | 1.592209s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_curriculum_runtime.py -v` | `D:\GURUKUL\backend\tests\test_curriculum_runtime.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| frontend typecheck | **PASS** | 0 | 40.569593s | `npm run build --prefix frontend-nextjs` | `D:\GURUKUL\frontend-nextjs\tsconfig.json` | `None` |
| frontend production build | **BLOCKED** | 0 | 34.379344s | `npm run build --prefix frontend-nextjs` | `D:\GURUKUL\frontend-nextjs\.next` | `Failed to parse evidence provenance: [Errno 13] Permission denied: 'D:\\GURUKUL\` |
| real browser UAT | **PASS** | 0 | 5.786978s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/scripts/run_playwright_uat.py` | `D:\GURUKUL\reports\uat\playwright_uat_report.json` | `None` |
| authentication | **BLOCKED** | 0 | 2.43408s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_real_firebase_auth.py -v` | `D:\GURUKUL\backend\tests\test_real_firebase_auth.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| authorization | **BLOCKED** | 0 | 3.235113s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_auth_security.py -v` | `D:\GURUKUL\backend\tests\test_auth_security.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| WebSocket security | **BLOCKED** | 0 | 7.843596s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_real_websocket_security.py -v` | `D:\GURUKUL\backend\tests\test_real_websocket_security.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| CORS | **BLOCKED** | 0 | 4.847288s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_cors_websocket_security.py -k test_cors -v` | `D:\GURUKUL\backend\tests\test_cors_websocket_security.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| portability | **PASS** | 0 | 100.210367s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/scripts/generate_portability_audit.py` | `D:\GURUKUL\reports\portability\path_portability_report.json` | `None` |
| provenance | **BLOCKED** | 0 | 1.597335s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_rag_provenance.py backend/tests/test_rag_provenance_validation.py -v` | `D:\GURUKUL\backend\tests\test_rag_provenance.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
| cache/RAG isolation | **BLOCKED** | 0 | 1.649187s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_cache_isolation.py backend/tests/test_rag_cache_collision.py -v` | `D:\GURUKUL\backend\tests\test_rag_cache_collision.py` | `Failed to parse evidence provenance: Expecting value: line 1 column 1 (char 0)` |
