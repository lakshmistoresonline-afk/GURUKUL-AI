# PROJECT CLEANUP AND CONSOLIDATION PLAN

## 1. Overview
This plan defines the safe removal of experimental artifacts, temporary diagnostics, and obsolete code from the Gurukul AI project.

## 2. Classification Legend
- **KEEP**: Production code, required evidence, or architectural documentation.
- **REMOVE**: Conclusively obsolete, redundant, or temporary artifacts.
- **REVIEW**: Ambiguous items requiring further investigation.

## 3. Inventory & Actions

### A. Obsolete Provider Artifacts
| Path | Action | Reason |
| :--- | :--- | :--- |
| `backend/src/providers/ollama_cloud.py.before_structured_fix` | **REMOVE** | Backup file created during a manual fix. Obsolete. |

### B. Experimental/Temporary Scripts (backend/scratch/)
| Path | Action | Reason |
| :--- | :--- | :--- |
| `backend/scratch/execute_ramp_batch.py` | **KEEP** | Active test utility for Phase 9.2 ramp validation. |
| `backend/scratch/test_nvidia_e2e.py` | **REMOVE** | Temporary diagnostic from Phase 6. |
| `backend/scratch/test_specialist.py` | **REMOVE** | Temporary diagnostic from Phase 6. |

### C. Temporary Generation Output (backend/storage/output/)
| Path | Action | Reason |
| :--- | :--- | :--- |
| `backend/storage/output/Class_99/` | **REMOVE** | Leftover from synthetic tests. |
| `backend/storage/output/test_5348f22b/` | **REMOVE** | Leftover from synthetic tests. |

### D. Generation Staging Runs (backend/storage/generation_staging/)
| Run ID | Action | Reason |
| :--- | :--- | :--- |
| `RUN_20260824_140242` | **REMOVE** | Failed/Empty run. |
| `RUN_20260824_140651` | **REMOVE** | Failed/Empty run. |
| `RUN_20260824_140752` | **REMOVE** | Failed/Empty run. |
| `RUN_20260824_140847` | **KEEP** | **REQUIRED FOR AUDIT**: Phase 6 validation success. |
| `RUN_20260824_141437` | **REMOVE** | Failed/Empty run. |
| `RUN_20260824_141604` | **REMOVE** | Failed/Empty run. |
| `RUN_20260824_142717` | **KEEP** | **REQUIRED FOR AUDIT**: Phase 7/7.1 stabilization results. |
| `RUN_20260824_170226` to `..._173828` | **REMOVE** | Interrupted/Empty runs during testing. |
| `RUN_20260824_180723` | **KEEP** | **REQUIRED FOR AUDIT**: Phase 9/9.1 Batch 1 generation. |
| `RUN_20260824_220925` | **KEEP** | **ACTIVE**: Phase 9.2 ramp start. |
| `RUN_20260824_221032` to `..._221802` | **REMOVE** | Empty/Init only. |

### E. Discovery Tests (backend/tests/)
| Path | Action | Reason |
| :--- | :--- | :--- |
| `backend/tests/*_discovery.py` | **REVIEW** | One-off discovery scripts. Keep for now to avoid losing config debug logic. |
| `backend/tests/test_p0*` | **KEEP** | Regression tests for core logic. |

### F. Reports & Audit Metadata
| Path | Action | Reason |
| :--- | :--- | :--- |
| `PHASE7_1_STABILIZATION_REPORT.md` | **KEEP** | Critical provenance. |
| `PHASE8_CAPACITY_ANALYSIS.md` | **KEEP** | Strategic roadmap. |
| `PHASE9_1_PROVIDER_CAPACITY_REPORT.md` | **KEEP** | Architectural record. |
| `GURUKUL_FINAL_CONTENT_INVENTORY.json` | **KEEP** | Production baseline. |

## 4. Data Safety Verification
- **Production Content**: `backend/GURUKUL_AI_CONTENT/` is strictly **READ-ONLY** and excluded from cleanup.
- **Environment**: `backend/.env` is excluded.
- **Staging**: Valid generation artifacts are preserved.

## 5. Branch Cleanup Recommendation
- `cloud-ai-router`: **SAFE TO DELETE** (Merged to main)
- `free-model-expansion`: **SAFE TO DELETE** (Merged to main)
- `fix/runtime-content-integration`: **SAFE TO DELETE** (Merged to main)

---
**PLAN_CREATED_FOR_REVIEW**
