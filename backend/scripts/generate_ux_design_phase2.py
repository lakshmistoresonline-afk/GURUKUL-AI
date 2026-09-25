import os

reports_dir = r"D:\GURUKUL\reports"
os.makedirs(reports_dir, exist_ok=True)

design_md = """# GURUKUL AI — STUDENT UX DESIGN SPECIFICATION

## 1. Option C + B Primary Design Language

- **Page Background**: Cloud White / Soft Blue-Gray (`#F8FAFC` / `bg-slate-50`)
- **Reading Surfaces**: Pure White (`#FFFFFF`) with subtle border (`border-slate-200`)
- **Main Text**: Deep Charcoal / Very Dark Blue-Gray (`#0F172A` / `text-slate-900`)
- **Primary Accent / Action**: Calm Indigo (`#4F46E5` / `bg-indigo-600`)
- **Secondary Accent**: Soft Sage / Muted Teal (`#0D9488` / `text-teal-600` / `bg-teal-500/10`)
- **Success State**: Soft Green (`#10B981`)
- **Warning State**: Muted Amber (`#F59E0B`)
- **Error State**: Clear Accessible Red (`#EF4444`)

---

## 2. Dashboard Redesign Hierarchy

```
GURUKUL AI

Good morning, Learner 👋

CONTINUE LEARNING
┌─────────────────────────────────────────────┐
│ Papa's Spectacles                           │
│ English • Unit 1 • Chapter 1                │
│ Continue where you stopped        Continue →│
└─────────────────────────────────────────────┘

YOUR SUBJECTS
[ English ]   [ Hindi ]   [ Maths ]   [ Science ]

YOUR CHAPTERS
Unit 1 — Let's Have Fun
  Papa's Spectacles                       Open Chapter →
  Gone with the Scooter                   Open Chapter →

Unit 2 — My Colourful World
  The Rainbow                             Open Chapter →
  The Wise Parrot                         Open Chapter →
```

---

## 3. The 5-Stage Unified Chapter Navigation

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

## 4. Reading Comfort & Typography
- **Aa Reading Comfort Control**:
  - Text Size: Medium (17px), Large (19px), Extra Large (21px).
  - Line Spacing: Normal (1.5), Comfortable (1.7), Spacious (1.9).
  - Themes: Calm Light, Warm Reading, Dark Comfortable.
  - Prose Column Width: $680\text{--}760\text{ px}$ with left alignment.
- **Devanagari Line Padding**: Enforces `lineHeight = 28.sp` / `leading-relaxed` / `leading-loose` to prevent vertical matra clipping (e.g. `किरन`, `न्याय की कुर्सी`).
"""

with open(os.path.join(reports_dir, "GURUKUL_STUDENT_UX_DESIGN.md"), "w", encoding="utf-8") as f:
    f.write(design_md)

with open(r"D:\GURUKUL\GURUKUL_STUDENT_UX_DESIGN.md", "w", encoding="utf-8") as f:
    f.write(design_md)

print("DESIGN COMPLETED! GURUKUL_STUDENT_UX_DESIGN.md generated in D:\\GURUKUL\\reports\\ and D:\\GURUKUL\\")
