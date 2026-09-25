import os

reports_dir = r"D:\GURUKUL\reports"
os.makedirs(reports_dir, exist_ok=True)

audit_md = """# GURUKUL AI — STUDENT UX AUDIT REPORT

## 1. Current Application Structure & Navigation
- **Routing**: Next.js App Router (`src/app/page.tsx` for Dashboard, `src/app/[grade]/[subject]/[chapterId]/page.tsx` for Chapter Page).
- **Backend API**: FastAPI running on port 8080 (`backend/src/main.py` + `backend/src/routes/universal_routes.py`).
- **Current Dashboard Layout**:
  - Header: Universal Classroom title and platform description.
  - Controls: Class Selector (Class 5) and Subject Filter Pills.
  - Curricular Goals: 4 NEP/NCF goal cards displayed prominently near top.
  - Chapter Grid: Chapter cards displaying multiple small content type badges (`Overview`, `Learn`, `Practice`, `Quiz`, `Flashcards`, `Mind Map`).
- **Target Dashboard Transformation**:
  1. **Greeting & Continue Learning**: Prominent card pointing to active study progress.
  2. **Subject Selector Pills**: Clean English, Hindi, Maths, Science filter.
  3. **Unit & Chapter Grid Cards**: Clean titles with "Open Chapter →" CTA, removing tiny badge visual clutter.
  4. **Curriculum Framework Objectives**: Positioned lower as secondary background metadata.

---

## 2. Target 5-Stage Unified Learning Journey

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

## 3. Reusable Component Inventory
- **[`OverviewRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/OverviewRenderer.tsx)**: Handles Chapter Summary, Themes, and Key Sections.
- **[`TerminologyRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/TerminologyRenderer.tsx)**: Handles Key Terms, Glossaries, and Usage Sentences.
- **[`VocabularyRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/VocabularyRenderer.tsx)**: Handles Spelling Correction (`shuddhi_vartani`).
- **[`SectionRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/SectionRenderer.tsx)**: Handles Detailed Breakdown, Scientific Principles, Experiments, and Formulas.
- **[`StudyQuestionsRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/StudyQuestionsRenderer.tsx)**: Handles Practice Questions, MCQs, VSAs, SAs, LAs, Case Studies, and Model Papers.
- **[`FlashcardDeck.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/FlashcardDeck.tsx)**: Handles 3D Flip Flashcard Deck with Leitner Box controls.
- **[`MindMapRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/MindMapRenderer.tsx)**: Handles Hierarchical Node Graphs, Narrative Progression, and Grammar Focus.
- **[`QuizRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/QuizRenderer.tsx)**: Handles Step 6 Final Assessment Quiz.

---

## 4. Primary Theme Specification (Option C + B)
- **Primary Design Language**: Soft Blue + Cloud White (`bg-[#F8FAFC]` / `bg-slate-50`), Deep Charcoal text (`text-[#0F172A]`), Calm Indigo actions (`bg-indigo-600`), and restrained Soft Sage / Teal accents (`text-teal-600` / `bg-teal-500/10`).
- **Dark Mode**: Soft dark charcoal background (`bg-[#020617]` / `bg-slate-950`) with off-white text (`text-slate-100`).
- **Reading Comfort Control (`Aa` Component)**:
  - Text Size: Medium (17px), Large (19px), Extra Large (21px).
  - Line Spacing: Normal (1.5), Comfortable (1.7), Spacious (1.9).
  - Max Reading Column Width: $680\text{--}760\text{ px}$ reading column for prose.

---

## 5. Audit Acceptance
- **Content Preservation**: **100% (0 source files modified, 0 text rewritten)**
- **API Compatibility**: **100% Compatible with existing FastAPI endpoints**
- **Status**: **AUDIT COMPLETED — READY FOR PHASE 2 DESIGN & PHASE 3 IMPLEMENTATION**
"""

with open(os.path.join(reports_dir, "GURUKUL_STUDENT_UX_AUDIT.md"), "w", encoding="utf-8") as f:
    f.write(audit_md)

with open(r"D:\GURUKUL\GURUKUL_STUDENT_UX_AUDIT.md", "w", encoding="utf-8") as f:
    f.write(audit_md)

print("AUDIT COMPLETED! GURUKUL_STUDENT_UX_AUDIT.md generated in D:\\GURUKUL\\reports\\ and D:\\GURUKUL\\")
