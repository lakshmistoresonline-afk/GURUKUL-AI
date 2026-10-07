# GURUKUL AI — FAIL-CLOSED PRODUCTION READINESS REPORT
**Run ID**: RUN_READINESS_20261007_104831
**Timestamp**: 2026-10-07T10:50:43.457558
**Overall Status**: **PRODUCTION READY**
**Total Gates**: 20 | **Passed**: 20 | **Blocked**: 0

---

## 20 Mandatory Executable Gates Verification Matrix
| Gate Name | Status | Exit Code | Duration (s) | Command | Evidence Artifact | Failure Reason |
|---|---|---|---|---|---|---|
| Contents cryptographic integrity | **PASS** | 0 | 0.510767s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/fail_closed_immutability.py verify-source-integrity` | `reports/content-integrity/fail_closed_immutability_report.json` | `None` |
| Source inventory | **PASS** | 0 | 0.606875s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processing/source_discovery.py` | `reports/source-inventory/source_inventory.json` | `None` |
| Exact curriculum reconciliation | **PASS** | 0 | 1.558822s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/reconciliation_engine.py` | `reports/reconciliation/curriculum_reconciliation.md` | `None` |
| Forensic fidelity | **PASS** | 0 | 10.565045s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_curriculum_fidelity.py -v` | `reports/fidelity/source_fidelity_report.json` | `None` |
| Processor coverage | **PASS** | 0 | 1.254161s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processors/processor_coverage_audit.py` | `reports/processors/processor_coverage_report.json` | `None` |
| Processor contract tests | **PASS** | 0 | 2.871456s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_processor_contracts.py backend/tests/test_processor_registry_hardened.py -v` | `backend/tests/test_processor_contracts.py` | `None` |
| Content schema validation | **PASS** | 0 | 2.972694s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_strict_schema_validation.py -v` | `backend/tests/test_strict_schema_validation.py` | `None` |
| Registry exact-resolution tests | **PASS** | 0 | 2.951285s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_curriculum_registry_hardened.py backend/tests/test_authoritative_registry.py -v` | `backend/tests/test_curriculum_registry_hardened.py` | `None` |
| API identity tests | **PASS** | 0 | 4.071493s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_authoritative_api_contracts_hardened.py backend/tests/test_api_integration.py -v` | `backend/tests/test_authoritative_api_contracts_hardened.py` | `None` |
| Renderer registry tests | **PASS** | 0 | 2.121055s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_forensic_fidelity.py -v` | `frontend-nextjs/src/components/presentation/RendererRegistry.tsx` | `None` |
| Frontend build | **PASS** | 0 | 48.851219s | `npm run build --prefix frontend-nextjs` | `frontend-nextjs/.next` | `None` |
| TypeScript validation | **PASS** | 0 | 33.918378s | `npm run build --prefix frontend-nextjs` | `frontend-nextjs/tsconfig.json` | `None` |
| Playwright UAT | **PASS** | 0 | 3.115635s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/scripts/run_playwright_uat.py` | `reports/uat/playwright_uat_report.json` | `None` |
| Security tests | **PASS** | 0 | 2.446427s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_auth_security.py -v` | `backend/tests/test_auth_security.py` | `None` |
| WebSocket tests | **PASS** | 0 | 5.403343s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_real_websocket_security.py -v` | `backend/tests/test_real_websocket_security.py` | `None` |
| Authentication tests | **PASS** | 0 | 2.363779s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_real_firebase_auth.py -v` | `backend/tests/test_real_firebase_auth.py` | `None` |
| CORS tests | **PASS** | 0 | 2.375842s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_cors_websocket_security.py -k test_cors -v` | `backend/tests/test_cors_websocket_security.py` | `None` |
| Path portability tests | **PASS** | 0 | 1.458712s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_portability_audit.py -v` | `backend/tests/test_portability_audit.py` | `None` |
| RAG provenance tests | **PASS** | 0 | 1.411897s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_rag_provenance_validation.py backend/tests/test_rag_provenance.py -v` | `backend/tests/test_rag_provenance.py` | `None` |
| Cache isolation tests | **PASS** | 0 | 1.424981s | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_cache_isolation.py backend/tests/test_rag_cache_collision.py -v` | `backend/tests/test_rag_cache_collision.py` | `None` |
