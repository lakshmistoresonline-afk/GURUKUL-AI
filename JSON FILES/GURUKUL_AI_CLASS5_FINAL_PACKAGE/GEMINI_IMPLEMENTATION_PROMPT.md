# GEMINI — IMPLEMENT ONLY, DO NOT GENERATE CONTENT

This package is the complete Class 5 educational-content source.

## Source of truth
- 47 uploaded Class 5 textbook chapters
- SOURCE_TEXT/
- existing generated component JSON
- MULTIMEDIA/MULTIMEDIA_RESOURCE_INDEX.json

## Absolute rule
DO NOT generate, rewrite, paraphrase, supplement, or invent educational content.
All educational content is supplied in this package.

## Implement
1. Inspect the current GURUKUL-AI frontend/backend.
2. Implement the new schema adapter.
3. Map all 47 chapter packages.
4. Expose all 42 components.
5. Connect Teacher Explanation and Story Mode to their supplied JSON.
6. Connect Interactive Lab, activities, assessments, practice, flashcards,
   mastery, remediation and revision.
7. Connect multimedia.
8. Preserve verification status for multimedia:
   - VERIFIED_DIRECT_VIDEO = direct video
   - VERIFIED_OFFICIAL_PORTAL = official NCERT resource portal
   - DISCOVERY_ONLY = search/discovery only
9. Never turn DISCOVERY_ONLY into a verified resource.
10. Never call an AI generation API to fill content.

## Validation
- 47/47 chapters
- 42/42 components per chapter
- JSON/schema validation
- chapter identity validation
- class/subject validation
- duplicate identity validation
- runtime mapping validation
- frontend tests
- backend tests
- clean production build

Produce:
CLASS5_FINAL_IMPLEMENTATION_REPORT.md
CLASS5_FINAL_COMPONENT_COVERAGE.json
CLASS5_FINAL_SCHEMA_VALIDATION.json
CLASS5_FINAL_RUNTIME_MAPPING.json
CLASS5_FINAL_BUILD_REPORT.md

Do not claim complete unless all 47 chapters and all applicable components
are successfully mapped into the running application.
