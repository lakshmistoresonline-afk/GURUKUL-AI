# GURUKUL AI — FINAL PRE-STAGING FILE DECISION MANIFEST

## 1. Master Packages (16 Directories under `Contents/`)
- *Path:* `Contents/Class 5/*`, `Contents/Class 6/*`, `Contents/Class 7/*` (`MASTER__...`)
- *Classification:* PROVEN
- *Reason:* Standardized naming convention migration completed with 100% file count and byte preservation.

## 2. Processor Architecture Refactoring
- *Path:* `processors/common/pipeline.py`, `processors/english/processor.py`, `processors/evs/processor.py`, `processors/hindi/processor.py`, `processors/mathematics/processor.py`, `processors/common/registry.py`, `processors/common/source/`, `processors/tests/`
- *Classification:* PROVEN
- *Reason:* Decoupled `ProcessingContext` and `SourceProfile` architecture with 21/21 passing architecture tests.

## 3. Naming & Migration Manifests / Audit Reports
- *Path:* `NAMING_CONVENTION.json`, `NAMING_DEPENDENCY_AUDIT.md`, `NAMING_MIGRATION_MANIFEST.csv`, `NAMING_MIGRATION_MANIFEST.json`, `post_rename_hash_manifest.json`, audit markdown files.
- *Classification:* PROVEN / USER DECISION
- *Reason:* Traceability artifacts documenting migration and validation.

## 4. PWA Build Artifacts
- *Path:* `frontend-nextjs/public/sw.js`, `frontend-nextjs/public/workbox-4754cb34.js`
- *Classification:* USER DECISION
- *Reason:* Generated runtime assets emitted during `next build` which are currently untracked and not ignored.
