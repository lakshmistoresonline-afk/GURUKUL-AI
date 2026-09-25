# GURUKUL AI — OLD PIPELINE ELIMINATION PLAN

## 1. Executive Summary
This forensic dependency audit evaluates the coexistence of the legacy runtime content pipeline (`ContentLoaderService`, `AdapterResolver`, `BaseAdapter`, `ContentBlock`, `RendererRegistry`, old `/manifest`, `/content`) versus the new offline build-time curriculum processing architecture (`ProcessedContent/`, `Class+Subject Processors`, `/api/v1/chapters/{chapterId}/source`).

## 2. Legacy Component Classification Inventory

| File / Component | Imported By | Called By | Runtime Reachable | Classification | Action |
|------------------|-------------|-----------|-------------------|----------------|--------|
| `backend/src/services/content_loader.py` | `universal_routes.py`, `process_cli.py`, tests | `process_cli.py` (CLI only), legacy tests | Yes (via tests & CLI) | KEEP BUT ISOLATE | Keep for offline CLI source extraction; remove from runtime API. |
| `backend/src/adapters/adapter_resolver.py` | Universal tests | None in new runtime | No (dead in runtime) | LEGACY | DELETE / ARCHIVE |
| `backend/src/adapters/base_adapter.py` | Adapters | None in new runtime | No (dead in runtime) | LEGACY | DELETE / ARCHIVE |
| `backend/src/adapters/english/` | AdapterResolver | None in new runtime | No (dead in runtime) | LEGACY | DELETE / ARCHIVE |
| `backend/src/adapters/hindi/` | AdapterResolver | None in new runtime | No (dead in runtime) | LEGACY | DELETE / ARCHIVE |
| `backend/src/adapters/maths/` | AdapterResolver | None in new runtime | No (dead in runtime) | LEGACY | DELETE / ARCHIVE |
| `backend/src/adapters/science/` | AdapterResolver | None in new runtime | No (dead in runtime) | LEGACY | DELETE / ARCHIVE |
| `backend/src/processors/` | Adapters | None in new runtime | No (dead in runtime) | LEGACY | DELETE / ARCHIVE |
| `frontend-nextjs/src/renderers/` | ChapterClient (old) | None in new dashboard | No (dead in frontend) | LEGACY | DELETE / ARCHIVE |
| `frontend-nextjs/src/navigation/NavigationBuilder.ts` | Old ChapterClient | None in new dashboard | No (dead in frontend) | LEGACY | DELETE / ARCHIVE |
| `backend/src/routes/universal_routes.py` | `main.py` | Legacy routes | Potentially if mounted | LEGACY | ISOLATE / DEPRECATE |

## 3. Runtime Call Graph Verification
- **Dashboard Request**: `GET /api/v1/chapters/{chapterId}/source`
- **Execution Path**:
  1. `backend/src/curriculum/api/chapters.py` (Curriculum router)
  2. Reads directly from `D:\GURUKUL\ProcessedContent\Class5\{Subject}\{ChapterId}\`
  3. Returns exact 7 fixed sections (`overview`, `notes`, `master`, `flashcards`, `mindmaps`, `quiz`, `question_papers`)
- **Conclusion**: The runtime API does **NOT** invoke `ContentLoaderService`, `AdapterResolver`, adapters, or `ContentBlock` generation during dashboard requests.

## 4. Replacement Components
- **Old `ContentLoaderService` / Adapters** ➔ Replaced by `Class5EnglishLoader`, `Class5HindiLoader`, `Class5MathsLoader`, `Class5ScienceLoader`, and offline CLI `process_cli.py`.
- **Old `RendererRegistry` / `SectionRenderer`** ➔ Replaced by direct section JSON consumption and presentation components (`OverviewComponent`, `NotesComponent`, etc.).
