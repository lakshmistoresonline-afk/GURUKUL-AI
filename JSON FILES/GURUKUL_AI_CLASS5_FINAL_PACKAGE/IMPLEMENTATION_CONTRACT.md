# Gurukul AI — Fresh Class 5 Content Contract

This package is the CONTENT SOURCE. No content generation is delegated to Gemini.

Source:
- User-provided Class 5 NCERT PDF package.
- 47 chapter PDFs: English 10, Hindi 12, Mathematics 15, EVS 10.

Every chapter contains 42 component files plus chapter_package.json and
SOURCE_INTELLIGENCE.json.

## Non-negotiable rules

1. Treat the supplied chapter content as the canonical source.
2. Do not regenerate, paraphrase, replace, or invent textbook facts.
3. Do not remove generated components because the old repository lacks them.
4. Preserve component IDs and chapter IDs.
5. Adapt the existing application to consume this fresh schema.
6. Validate every JSON file before runtime integration.
7. Do not create generic repeated chapter content where the component is expected
   to be chapter-specific.
8. Teacher Explanation and Story Mode are fully supplied here.
9. Quiz, flashcards, practice, HOTS, labs and assessments are fully supplied here.
10. Multimedia entries explicitly distinguish LOCAL_SOURCE from runtime-rendered
    visuals; no fabricated external URLs are claimed.
11. The application must map each chapter to its new package rather than mixing
    old MASTER_CONTENT with the fresh package unless an explicit compatibility
    adapter is required.

## Required implementation sequence

A. Inventory current frontend/backend content loaders.
B. Create a single content adapter for the new schema.
C. Map chapter_id -> new chapter_package.json.
D. Map each component to its UI feature.
E. Add graceful handling for subject-dependent UI.
F. Validate all 47 chapter packages.
G. Run unit/integration/UI tests.
H. Run a clean production build.
I. Produce a content coverage matrix showing 47/47 chapters and every component.

Gemini is an IMPLEMENTATION ENGINE only for this package. It must not generate
new educational content.
