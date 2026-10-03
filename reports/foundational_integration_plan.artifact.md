# GURUKUL AI — FOUNDATIONAL.JSON DASHBOARD INTEGRATION PLAN

This document outlines the architectural and engineering plan to process and showcase the newly added `Foundational.json` files for every class and subject across the Gurukul AI platform, ensuring 100% data fidelity without missing a single word.

---

## 1. Schema & Content Analysis of `Foundational.json`

Each `Foundational.json` file across Class 5, Class 6, and Class 7 contains structured pedagogical metadata:
- **Textbook & Curriculum Metadata**: Textbook title, publisher, grade level, curriculum framework (NEP 2020 / NCF-SE 2023), and total chapters.
- **Chapter Indexing & Units**: Mapping of chapter numbers to titles and units.
- **Foundational Core Content (`content` object)**: Subject-specific foundational modules (e.g., Grammar rules, linguistic structures, math foundational principles, scientific method fundamentals, or social science core concepts) with detailed explanations, concrete examples, and cross-references to specific chapters.

---

## 2. Backend Processing & Materialization Strategy

To integrate `Foundational.json` without duplicating data or disrupting existing chapter structures:
1. **Dedicated Ingestion Parser**: Extend curriculum processing scripts (e.g., V6 normalizer) to detect and parse `Foundational.json` during the `Contents` scan.
2. **Materialization Layer**: Create a dedicated `foundational.json` asset inside each chapter's processed folder (`ProcessedContent/Class{grade}/{Subject}/G{grade}-{SUBJ}-UXX-CXX/foundational.json`) or a subject-level foundational index (`ProcessedContent/Class{grade}/{Subject}/foundational_master.json`) so chapters can reference subject-wide foundational concepts.
3. **Deduplication**: Use canonical SHA-256 object fingerprinting on each foundational concept/rule to prevent redundant records.

---

## 3. Frontend Dashboard UI Presentation Architecture

To showcase the full foundational contents seamlessly in the student dashboard:
1. **New Navigation Tab**: Add a dedicated **"Foundational Core"** (or **"Foundational Modules"**) tab alongside *Overview*, *Notes*, *Master Practice*, *Flashcards*, *Mindmaps*, *Quiz*, and *Question Papers*.
2. **Interactive Component (`FoundationalComponent.tsx`)**:
   - **Textbook Metadata Header**: Displays curriculum framework, publisher, and textbook name.
   - **Search & Filter Bar**: Allows students to search foundational concepts/grammar rules instantly across chapters.
   - **Structured Concept Cards**: Renders concept definitions, detailed explanations, bulleted examples, and source context badges (e.g., *"Derived from Chapter 1 & Chapter 6"*).
3. **Safe Text Rendering**: Integrate `renderSafeText` and `SafeStructuredCard` to ensure zero runtime errors and flawless typographic presentation.

---

## 4. Verification & Testing Protocol

1. **Automated Inventory Audit**: Run a verification script to confirm 100% of chapters and foundational modules are mapped.
2. **Build Compilation**: Run `npm run build` in `frontend-nextjs` to verify static generation across all routes.
3. **Zero Source Modification**: Authoritative source files under `Contents/` remain byte-for-byte untouched during planning and staging.
