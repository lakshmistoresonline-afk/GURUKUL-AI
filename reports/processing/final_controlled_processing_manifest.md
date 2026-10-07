# GURUKUL AI — FINAL CONTROLLED PROCESSING MANIFEST (EVIDENCE-BASED)
**Run ID**: RUN_FINAL_20261007_170835
**Timestamp**: 2026-10-07T17:10:50.699549
**Overall Status**: **PRODUCTION READY**
**Source Coverage**: 100.0%

---

## Gate Verification Results
| Gate Name | Command | Result | Exit Code | Duration (s) | Evidence Artifact |
|---|---|---|---|---|---|
| Source integrity | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/fail_closed_immutability.py verify-source-integrity` | **PASS** | 0 | 0.675386s | `reports/content-integrity/fail_closed_immutability_report.json` |
| Source inventory | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processing/source_discovery.py` | **PASS** | 0 | 0.518982s | `reports/source-inventory/source_inventory.json` |
| Curriculum reconciliation | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/verification/reconciliation_engine.py` | **PASS** | 0 | 1.691474s | `reports/reconciliation/curriculum_reconciliation.md` |
| Fidelity verification | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_curriculum_fidelity.py -v` | **PASS** | 0 | 29.881796s | `reports/fidelity/source_fidelity_report.json` |
| Schema validation | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_strict_schema_validation.py -v` | **PASS** | 0 | 2.187765s | `backend/tests/test_strict_schema_validation.py` |
| Processor coverage | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/src/curriculum/processors/processor_coverage_audit.py` | **PASS** | 0 | 1.035102s | `reports/processors/processor_coverage_report.json` |
| Renderer coverage | `npm run build --prefix frontend-nextjs` | **PASS** | 0 | 46.932772s | `frontend-nextjs/src/components/presentation/RendererRegistry.tsx` |
| API tests | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_api_integration.py -v` | **PASS** | 0 | 3.95286s | `backend/tests/test_api_integration.py` |
| Frontend build | `npm run build --prefix frontend-nextjs` | **PASS** | 0 | 37.101608s | `frontend-nextjs/.next` |
| Playwright UAT | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe backend/scripts/run_playwright_uat.py` | **PASS** | 0 | 3.262667s | `reports/uat/playwright_uat_report.json` |
| Security tests | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_real_websocket_security.py backend/tests/test_real_firebase_auth.py -v` | **PASS** | 0 | 5.61041s | `backend/tests/test_real_websocket_security.py` |
| Portability tests | `C:\Users\srina\AppData\Local\Programs\Python\Python313\python.exe -m pytest backend/tests/test_portability_audit.py -v` | **PASS** | 0 | 1.445134s | `backend/tests/test_portability_audit.py` |
