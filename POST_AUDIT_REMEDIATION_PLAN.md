# GURUKUL AI — POST-AUDIT REMEDIATION PLAN

## Phase 1 — SHA-256 Status
- **Status:** `SHA-256 PRE/POST EQUALITY = NOT PROVABLE`
- **Root Cause:** No verified pre-rename hash manifest was generated prior to executing the master package directory renames.
- **Action:** Retain `NOT PROVABLE`. Do not fabricate historical hashes.

---

## Phase 2 — Root Test Discovery Investigation
- **Root Cause:** Python `unittest` default discovery (`python -m unittest discover -v`) looks for `test*.py` at the project root level. Gurukul AI organizes tests in package-specific directories (`processors/tests/` and `backend/src/tests/`).
- **Classification:** Expected repository structure issue.
- **Recommended Test Commands:**
  - Processor architecture tests: `python -m unittest discover -s processors/tests -v` (21 tests, PASS).

---

## Phase 3 — Backend Test Suite Investigation
- **Findings:** `backend/src/tests/` currently contains no active Python unit test modules (`.py`), and backend test execution discovers 0 items.
- **Action:** Document that backend unit testing is `NOT AVAILABLE` pending future test authoring.

---

## Phase 4 — Frontend Runtime Verification
- **Trace:** Frontend dashboard, subject listing, and chapter page (`frontend-nextjs/src/app/chapter/[chapterId]/page.tsx`) consume data via `studentApi` client using canonical identifiers (`chapterId`, `subjectId`).
- **Conclusion:** `STATIC FRONTEND TRACE = PROVEN` (Top-level master package directory names are not referenced by frontend runtime code).

---

## Phase 5 — RAG Pipeline Verification
- **Trace:** Backend resource and indexing scripts consume `runtime-data/catalog.json` and canonical chapter/subject JSON records.
- **Conclusion:** `RAG STATIC TRACE = PROVEN` (RAG and resource loading operate independently of top-level master package directory names).

---

## Phase 6 — PWA Generated Files Investigation
- **Files:** `frontend-nextjs/public/sw.js`, `frontend-nextjs/public/workbox-4754cb34.js`
- **Investigation:** `git check-ignore` returned exit code 1 (not currently ignored by `.gitignore`).
- **Recommendation:** Add `frontend-nextjs/public/sw.js` and `frontend-nextjs/public/workbox-*.js` to `.gitignore` as they are `GENERATED_BUILD_ARTIFACT` outputs from Next.js PWA compilation.
- **Requires User Approval:** Yes.

---

## Phase 7 — Git Reconciliation Classification
- **A (Master Package Rename):** Deletion of old `Contents/...` paths and addition of new `MASTER__...` directories.
- **B (Intentional Application Code):** Refactoring of processor pipeline and subject processors (`processors/common/pipeline.py`, `processors/english/processor.py`, `processors/evs/processor.py`, `processors/hindi/processor.py`, `processors/mathematics/processor.py`, `processors/common/registry.py`, `processors/common/source/`, `processors/tests/`).
- **C (Audit / Documentation):** `NAMING_CONVENTION.json`, `NAMING_DEPENDENCY_AUDIT.md`, `NAMING_MIGRATION_MANIFEST.json`, `NAMING_MIGRATION_MANIFEST.csv`, `POST_RENAME_HARDENING_REPORT.md`, `PROCESSOR_ARCHITECTURE.md`, `FINAL_PRE_STAGING_RECONCILIATION_REPORT.md`, `POST_AUDIT_REMEDIATION_PLAN.md`.
- **D (Generated Artifacts):** `frontend-nextjs/public/sw.js`, `frontend-nextjs/public/workbox-4754cb34.js`, `post_rename_hash_manifest.json`.

---

## Phase 8 — Remediation Plan Table

| Issue | Root Cause | Evidence | Recommended Action | Risk | Files Affected | Code Change Required? | User Approval Required? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. SHA-256 Not Provable** | No pre-rename hash manifest | Missing baseline JSON | Document limitation in hardening report | Low | `POST_RENAME_HARDENING_REPORT.md` | No | No |
| **2. Root Unittest Discovery** | Tests stored in subpackages (`processors/tests/`) | `unittest discover` returns 0 at root | Use explicit suite command (`-s processors/tests`) | Low | N/A | No | No |
| **3. Backend Test Suite** | Test directory structure empty | 0 tests discovered in `backend/src/tests/` | Author backend unit tests in future phase | Medium | `backend/src/tests/` | Yes | Yes |
| **4. PWA Generated Files** | Next.js PWA output in `public/` untracked | Present in `git status` | Add service worker entries to `.gitignore` | Low | `.gitignore` | Yes (Config only) | Yes |
| **5. Unstaged Git State** | Master package renames and architecture updates uncommitted | `git status --short` shows D / ?? | Stage and commit changes after user review | Low | Entire repo | No (Git operation) | Yes |

---
**FINAL STATUS:** POST-MIGRATION HARDENING INCOMPLETE — HUMAN ACTION REQUIRED
