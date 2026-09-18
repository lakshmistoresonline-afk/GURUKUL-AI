# GURUKUL AI — CLEAN SLATE AUDIT REPORT (PHASE A)
**Audit Timestamp**: 2026-09-18T01:40:29.436421+00:00
**Project Root**: `D:\GURUKUL-AI`
**Authoritative Source Root**: `D:\GURUKUL-AI\Contents`

## Purge & Reset Targets (PATH + ACTION + REASON)
| Path | Action | Reason |
|---|---|---|
| `backend\scripts\legacy_backups` | **DELETE** | Obsolete historical backup scripts folder |
| `runtime-data\.temp_class5_extract` | **DELETE** | Temporary ZIP extraction working directory |
| `Processed` | **DELETE** | Old processed staging directory |
| `runtime-data\backups` | **DELETE** | Obsolete runtime backups directory |
| `runtime-data\search` | **RESET** | Stale RAG search index directory |