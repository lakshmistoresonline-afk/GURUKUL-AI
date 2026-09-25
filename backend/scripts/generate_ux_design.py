import os

reports_dir = r"D:\GURUKUL\reports"
os.makedirs(reports_dir, exist_ok=True)

design_md = """# GURUKUL AI — STUDENT UX DESIGN SPECIFICATION

## 1. The 5-Stage Unified Learning Journey

```
                     ┌────────────────────────┐
                     │   1. OVERVIEW          │
                     │  Chapter Summary &     │
                     │  Central Theme         │
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │   2. LEARN             │
                     │  Lessons, Concepts,    │
                     │  Vocabulary & Principles│
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │   3. PRACTICE          │
                     │  Activities, MCQs &    │
                     │  Word Problems         │
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │   4. REVISION          │
                     │  3D Flashcards &       │
                     │  Concept Mind Maps     │
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │   5. QUIZ (Final)      │
                     │  Step 6 Assessment     │
                     └────────────────────────┘
```

---

## 2. Content Grouping Rules inside the 5 Stages

1. **Overview Stage (`overview`)**:
   - Chapter Summary & Overview (`summary.overview`, `detailed_summary`)
   - Central Theme & Moral Message (`centralTheme`, `theme_and_moral`)
   - Real-World Motivation (`conceptual_foundation.motivation`)
   - Core Key Sections Grid Cards

2. **Learn Stage (`learn`)**:
   - Key Terminology & Word Meanings (`keyTerminology`, `shabdart`, `glossary`)
   - Spelling Correction & Vocabulary (`vocabulary`, `shuddhi_vartani`)
   - Detailed Lesson Breakdown (`detailedBreakdown`)
   - Scientific Principles & Experiments (`scientificPrinciples`, `activities`)
   - Formulas & Scientific Calculations (`numericalsAndFormulas`)
   - Grammar Focus & Language Extraction (`grammar_extraction`)
   - Pedagogy Guidance Accordion Panel (`pedagogyGuides`)

3. **Practice Stage (`practice`)**:
   - Textbook Activities & Writing Tasks (`activities`, `creative_writing`)
   - Multiple Choice Questions (`multipleChoiceQuestions`, `mcqs`)
   - Short & Long Answer Word Problems (`shortAnswerQuestions`, `vsa_questions`, `sa_questions`, `la_questions`)
   - Fill-in-the-Blanks & True/False Drills (`fillInTheBlanks`, `trueFalse`)
   - Real-World Case Studies (`case_study_questions`)
   - Model Examination Papers (`sample_question_papers`, `model_question_paper`)

4. **Revision Stage (`revision`)**:
   - Interactive 3D Flip Flashcards Deck (`flashcards`)
   - Hierarchical Concept Mind Map Visualizer (`mindmap`, `story_mindmap`)
   - Important Takeaways & Core Lessons (`importantTakeaways`)

5. **Quiz Stage (`quiz`)**:
   - Master Assessment Quiz (`quiz`, `interactive_quiz`, `quizzes_mcq`) — **STRICTLY LAST (Step 6)**.

---

## 3. Reading Comfort & Theme System

- **Themes**:
  - **Calm Light Theme**: Warm off-white surface (`#F8FAFC`), deep charcoal text (`#0F172A`), indigo accent (`#4F46E5`).
  - **Warm Reading Theme**: Warm cream surface (`#FFFBEB`), deep charcoal text (`#1C1917`), amber accent (`#D97706`).
  - **Dark Comfortable Theme**: Soft dark slate surface (`#020617` / `#0F172A`), softened light text (`#E2E8F0`), indigo accent (`#818CF8`).
- **Reading Comfort Control (`Aa` Component)**:
  - Text Size: Medium (17px), Large (19px), Extra Large (21px).
  - Line Spacing: Normal (1.5), Comfortable (1.7), Spacious (1.9).
  - Reading Width: Standard (680px), Comfortable (760px).
- **Responsive Layout**:
  - Desktop: Multi-column grid for cards, 680–760px column for prose.
  - Tablet: Adaptive 2-column layout.
  - Mobile: Single column scrollable view with full touch accessibility.
"""

with open(os.path.join(reports_dir, "GURUKUL_STUDENT_UX_DESIGN.md"), "w", encoding="utf-8") as f:
    f.write(design_md)

with open(r"D:\GURUKUL\GURUKUL_STUDENT_UX_DESIGN.md", "w", encoding="utf-8") as f:
    f.write(design_md)

print("DESIGN COMPLETED! GURUKUL_STUDENT_UX_DESIGN.md generated in D:\\GURUKUL\\reports\\ and D:\\GURUKUL\\")
