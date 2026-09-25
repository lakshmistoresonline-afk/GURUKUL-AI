# GURUKUL AI — LEGACY PIPELINE CURRENT STATE AUDIT

## A. Legacy Files Actually Present
1. `backend/src/services/content_loader.py` — Old dynamic content loader.
2. `backend/src/adapters/` — `adapter_resolver.py`, `base_adapter.py`, `generic_adapter.py`, `english/`, `hindi/`, `maths/`, `science/`.
3. `backend/src/processors/` — `generic_fallback.py`, `standard_processors.py`, etc.
4. `frontend-nextjs/src/renderers/` — `RendererRegistry.ts`, `SectionRenderer.tsx`, etc.
5. `frontend-nextjs/src/navigation/NavigationBuilder.ts` — Old manifest-driven navigation builder.
6. `backend/src/routes/universal_routes.py` — Old `/chapter`, `/manifest`, `/content` API routes.

## B. Exact Imports & Callers
- `content_loader.py` was imported by old tests and universal routes.
- `AdapterResolver` was imported by old tests and universal routes.
- `RendererRegistry` was imported by old `ChapterClient.tsx`.

## C. Runtime & CLI Reachability
- **Runtime API**: Now uses `backend/src/curriculum/api/chapters.py` reading strictly from `ProcessedContent/`.
- **CLI (`process_cli.py`)**: Migrated to use `Class5EnglishLoader`, `Class5HindiLoader`, `Class5MathsLoader`, and `Class5ScienceLoader`.

## D. Proposed Deletion Plan
- Delete `backend/src/services/content_loader.py`.
- Delete `backend/src/adapters/`.
- Delete `backend/src/processors/`.
- Delete `frontend-nextjs/src/renderers/` and `NavigationBuilder.ts` (if unused).
- Deprecate/remove legacy universal routes in `universal_routes.py`.
