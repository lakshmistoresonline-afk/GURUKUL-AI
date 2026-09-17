# GURUKUL AI — CLASS 5 CLEANUP PROPOSAL & ARCHITECTURE PLAN
**Proposal Date**: 2026-09-17T07:26:37.403028+00:00
**Target Workspace**: `D:\GURUKUL-AI`

## Proposed Category Actions

### Category 1: KEEP (Core Authoritative Code & Active Data)
| Path | Current Purpose | Proposed Action | Risk |
|---|---|---|---|
| `Contents/Class 5/` | Raw Class 5 ZIP packages | **KEEP & PROTECT** | HIGH if modified |
| `runtime-data/` | Active canonical runtime chapter JSONs | **KEEP** | HIGH if deleted |
| `backend/src/` | FastAPI routes, DB models, Auth logic | **KEEP** | HIGH if deleted |
| `frontend-nextjs/src/` | Next.js App router, page views, components | **KEEP** | HIGH if deleted |
| `processors/` | Modular subject processor package | **KEEP & REFACTOR** | LOW |

### Category 2: ARCHIVE (Temporary Processing Artifacts & Old Backups)
| Path | Current Purpose | Proposed Action | Risk |
|---|---|---|---|
| `runtime-data/.temp_class5_extract/` | Extracted ZIP working directory | **ARCHIVE / RE-EXTRACT** | NONE |
| `backend/scripts/*.backup*` | Historical backup adapter scripts | **ARCHIVE to `backend/scripts/legacy_backups/`** | LOW |

### Category 3: DELETE (Obsolete Scratch Scripts & Stale Builds)
| Path | Current Purpose | Proposed Action | Risk |
|---|---|---|---|
| `*.tmp` / scratch temp files | One-off debugging scripts | **DELETE** | NONE |
| `frontend-nextjs/.next/` | Stale Next.js build cache | **CLEAN** | NONE |

## Approval Sign-off
Please review this proposal and provide approval before Stage B cleanup and processing execution begins.