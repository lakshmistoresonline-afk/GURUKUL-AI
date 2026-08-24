# PHASE 8 — FULL CURRICULUM CAPACITY ANALYSIS

## 1. Executive Summary
This analysis evaluates the readiness of the Gurukul AI pipeline for full-curriculum production generation. The architecture is stable, but throughput is currently constrained by external cloud provider quotas.

## 2. Curriculum Inventory
The canonical production dataset has been fully audited:

- **Total Classes:** 3 (Class 05, 06, 07)
- **Total Chapters:** 163
- **Total Existing JSON Files:** ~8,456
- **Existing Content Status:** All 163 chapters have a `chapter_package.json` and approximately 42 individual component files.
- **Completeness Gap:** Existing content lacks `mind_map` and `related_chapters` components, which are now part of the standard 12-stage production pipeline.

## 3. Generation Workload Matrix
To achieve "Cloud-First" standard for the entire curriculum, the following workload is estimated:

| Scope | Total Chapters | Stages/Chapter | Total AI Requests |
| :--- | :--- | :--- | :--- |
| Full Regeneration | 163 | 12 | 1,956 |
| Partial Enrichment | 163 | 2 | 326 |

**Decision:** The analysis assumes a **Full Regeneration** to ensure all 163 chapters meet the new pedagogical and structural standards validated in Phases 6 and 7.

## 4. Token & Request Estimation
Estimates are based on actual measurements from Phase 7.1.

- **Average Input per Stage:** 2,000 tokens (Context + Prompt)
- **Average Output per Stage:** 800 tokens (Structured JSON)
- **Total Tokens per Stage:** 2,800
- **Total Tokens for Curriculum:** **~5,476,800 tokens**
- **Total Primary Requests:** 1,956
- **Expected Fallback/Retry volume (15%):** 293
- **Total Expected Requests:** **~2,250**

## 5. Provider Capacity & Constraints

| Provider | Observed Limit (Daily) | Role | Status |
| :--- | :--- | :--- | :--- |
| **Groq** | ~200,000 tokens | Primary (Speed/Simple) | ✅ Active |
| **OpenRouter** | Credit Based / 2048 Ceiling | Primary (Reasoning/Free) | ✅ Active |
| **NVIDIA** | High Latency / Timeouts | Primary (Complex/GPT-OSS) | ✅ Active |
| **Gemini** | N/A (Authentication Failed) | Specialist | ⚠️ REPLACEMENT REQUIRED |

## 6. Batch Simulation & safe Batch Size
Based on a 200k daily token limit for Groq (the fastest provider):

- **Scenario 100 Chapters:** 1,200 requests | ~336,000 tokens | ~2 Days
- **Scenario 500 Chapters:** 6,000 requests | ~1,680,000 tokens | ~8 Days
- **Full Curriculum (163):** 1,956 requests | ~5,476,800 tokens | **~27 Days**

### **Recommended Safe Batch Size:**
- **Daily Batch:** 10 Chapters
- **Requests per day:** ~120
- **Tokens per day:** ~336,000
- **Strategy:** Distribute load across Groq and OpenRouter (Free models) to maximize daily throughput.

## 7. Cost Analysis
- **Free Models (Nemotron Lightning/Ultra):** $0.00 (High availability, verified)
- **Paid Models (OpenRouter/NVIDIA):** ~$5.00 - $10.00 for the entire curriculum.
- **Project Budget Recommendation:** Maintain a $20.00 balance on OpenRouter for smooth fallback.

## 8. Readiness Assessment
- **Architecture Readiness:** ✅ PASS (Validated E2E)
- **Staging Isolation:** ✅ PASS (Verified READ-ONLY production)
- **Manifest/Progress Tracking:** ✅ PASS (Verified resumable)
- **Provider Readiness:** ⚠️ PARTIAL (Gemini Key Replacement Required)
- **Quota Readiness:** ⚠️ PARTIAL (Throughput limited to ~10 chapters/day)

## 9. Final Decision

**PHASE_8_READY_WITH_REVIEW**

The pipeline is ready for larger scale generation, but the "leaked key" report for Gemini must be resolved, and the daily batch size must be strictly limited to 10 chapters to avoid cascading provider failures due to quota exhaustion.

### **Recommended Next Step**
Replace Gemini API key and proceed with the first **10-Chapter Production Batch**.
