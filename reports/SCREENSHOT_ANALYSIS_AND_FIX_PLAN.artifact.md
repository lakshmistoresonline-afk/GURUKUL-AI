# GURUKUL AI — COMPREHENSIVE SCREENSHOT ANALYSIS & FIX PLAN

This document provides a rigorous, screenshot-by-screenshot analysis of the UI rendering issues observed across Class 6 Science and Social Science chapters, identifying root causes and outlining the definitive engineering plan to showcase 100% of the contents cleanly in the dashboard without missing a single word.

---

## 1. Screenshot 1: Class 6 Science Ch 1 (Master Practice / Glossary & Units)
- **Observed Issue**: Glossary and unit cards display raw JSON strings (e.g., `{"term":"Science","definition":"...","u_unit":"N/A","example":"..."}`).
- **Root Cause**: Class 6 Science master practice JSON files store glossary items as structured objects containing `term`, `definition`, `u_unit`, and `example`. The presentation component defaulted to stringifying the raw object when encountering structured fields.
- **Root Cause & Fix Plan**:
  - Enhance `SafeStructuredCard` to explicitly extract and format `term` (bold Indigo header), `definition` (clean body text), and `example` (italicized quotation box).
  - Ensure all subject master components delegate glossary rendering to the safe structured card parser.

---

## 2. Screenshot 2: Class 6 Science Ch 1 (Master Practice / Exam Question Bank)
- **Observed Issue**: Question bank sections render category headings like `TEXTBOOK QUESTIONS`, `OBJECTIVE 1 MARK`, and `SHORT ANSWER 3 MARKS`, but lack consistent typography and interactive answer feedback.
- **Root Cause**: Science question banks use hierarchical category headings that require specialized badge styling and interactive marking scheme toggles.
- **Root Cause & Fix Plan**:
  - Standardize category header badges across all Class 6/7 master practice components.
  - Ensure every question card includes the interactive "Show Answer / Marking Scheme" toggle.

---

## 3. Screenshot 3: Class 6 Social Ch 1 (Notes / Core Map & Conceptual Architecture)
- **Observed Issue**: The Notes overview tab displays a raw JSON block (`{"big_idea_summary":"...","topic_hierarchy":[...]}`) instead of formatted paragraphs and bulleted topic lists.
- **Root Cause**: Class 6 Social Science Notes JSON files structure chapter summaries under `section_1_core_map_and_conceptual_architecture`, containing `big_idea_summary` and a nested `topic_hierarchy` array. The generic notes renderer did not unpack this specific schema block.
- **Root Cause & Fix Plan**:
  - Update `NotesComponent` to check for `section_1_core_map_and_conceptual_architecture` and render `big_idea_summary` as readable lead paragraphs and `topic_hierarchy` as structured hierarchical bullet lists.

---

## 4. Screenshot 4: Class 6 Social Ch 1 (Master Practice / Keywords & Definitions)
- **Observed Issue**: Master practice keyword cards render raw JSON objects inside numbered containers (`0`, `1`, `2`).
- **Root Cause**: Same as Screenshot 1—keyword/vocabulary datasets in Social Science store items as objects (`term`, `definition`) rather than plain strings.
- **Root Cause & Fix Plan**:
  - Apply `SafeStructuredCard` universally to all vocabulary, keyword, and definition arrays across English, Hindi, Maths, Science, and Social Science.

---

## 5. Screenshot 5: Class 6 Social Ch 1 (Flashcards)
- **Observed Issue**: Displays `"No flashcards available."`.
- **Root Cause**: Flashcards JSON files for Class 6 Social Science utilize alternative schema keys (such as `flashcards_dataset`, `cards`, or chapter-level subkeys) that were not captured by the default flashcard loader.
- **Root Cause & Fix Plan**:
  - Expand the universal curriculum normalizer (`generate_processed_content_correctly_v5.py`) to recursively scan all dictionary keys for flashcard arrays (`flashcards`, `cards`, `flashcard_database`, `flashcards_dataset`) and normalize them into standard `flashcards.json`.
