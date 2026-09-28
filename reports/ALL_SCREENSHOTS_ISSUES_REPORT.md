# GURUKUL AI — CONSOLIDATED SCREENSHOTS & ISSUES REPORT

## 1. Executive Summary
This document provides a consolidated catalog of every UI presentation issue, schema mismatch, and rendering gap identified across all user-provided screenshots during our development and audit cycle.

---

## 2. Catalog of Identified Issues & Resolutions

### Issue 1: Hindi Comprehensive Grammar Raw JSON Blocks
- **Observed in**: Hindi Chapter Notes & Master views (e.g., *न्याय की कुर्सी*).
- **Issue**: Complex nested grammar objects (`gender_and_number`, `idioms_and_phrases` with example sentences) rendered as raw JSON stringified dictionaries inside `<pre>` blocks.
- **Status**: Identified. Requires a dedicated Hindi grammar card renderer to format gender, number, and idioms into polished tables.

### Issue 2: Class 6 English Notes Missing for Chapters 1–4
- **Observed in**: Class 6 English Chapter 1–4 Notes tabs (`A Bottle of Dew`, etc.).
- **Issue**: Displayed *"No notes available."* because source `Notes.json` started at Chapter 5.
- **Status**: **Fixed** via fallback synthesis from `Overview.json`.

### Issue 3: Class 6 English Master & Mindmaps Raw JSON
- **Observed in**: Class 6 English Master and Mindmaps tabs.
- **Issue**: Displayed `{}` or raw JSON because Class 6 English uses unique schema keys (`m1_overview`, `central_node`, `plot_summary_nodes`).
- **Status**: **Fixed** via purpose-built Class 6 presentation components (`Class6MasterComponent`, `Class6MindmapComponent`).

### Issue 4: Flashcards Blank Content (Front/Back Missing)
- **Observed in**: Class 6 English and Maths Flashcards tabs.
- **Issue**: Flashcard cards rendered empty because source data uses `front_prompt`, `back_answer`, and `front_question`.
- **Status**: **Fixed** in `FlashcardsComponent`.

### Issue 5: Quiz Non-MCQ Questions Missing Input Fields
- **Observed in**: Science and Social Quiz tabs for Fill-in-the-Blanks / Reasoning questions.
- **Issue**: Questions with empty option arrays (`[]`) displayed nothing below the question statement.
- **Status**: **Fixed** by adding interactive text input boxes for open-ended response verification.

### Issue 6: Question Papers Long Merged Scrolling
- **Observed in**: Question Papers tabs across all subjects.
- **Issue**: All sets and sections were merged into a single long vertical scroll.
- **Status**: **Fixed** via dual-tier Set Selector Tabs (Set 1–5) and Section Selector Tabs (Section A–D).
