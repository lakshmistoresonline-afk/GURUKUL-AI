import os

reports_dir = r"D:\GURUKUL\reports"
os.makedirs(reports_dir, exist_ok=True)

audit_md = """# GURUKUL AI — STUDENT UX AUDIT REPORT

## 1. Current Application Structure & Navigation
- **Routing**: Next.js App Router (`src/app/page.tsx` for Dashboard, `src/app/[grade]/[subject]/[chapterId]/page.tsx` for Chapter Page).
- **Backend API**: FastAPI running on port 8080 (`backend/src/main.py` + `backend/src/routes/universal_routes.py`).
- **Current Chapter Navigation**: Server-driven 6-stage navigation (`Overview`, `Learn`, `Practice`, `Flashcards`, `Mind Map`, `Quiz`).
- **Target Presentation Alignment**: Consolidate into **5 Unified Primary Learning Stages**:
  1. **Overview**: Chapter Summary, Central Theme, Real-World Motivation.
  2. **Learn**: Lessons, Core Concepts, Vocabulary, Grammar Focus, Scientific Principles, Glossary, Formulas, Takeaways, and Pedagogy Guidance.
  3. **Practice**: Activities, MCQs, Short & Long Answer Problems, Fill-in-the-Blanks, True/False, Case Studies, Model Papers.
  4. **Revision**: Interactive 3D Flip Flashcards, Hierarchical Concept Mind Map, Key Takeaways.
  5. **Quiz**: Step 6 Final Assessment (Always Last).

---

## 2. Reusable Component Inventory
- **[`OverviewRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/OverviewRenderer.tsx)**: Handles Chapter Summary, Themes, and Key Sections.
- **[`TerminologyRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/TerminologyRenderer.tsx)**: Handles Key Terms, Glossaries, and Usage Sentences.
- **[`VocabularyRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/VocabularyRenderer.tsx)**: Handles Spelling Correction (`shuddhi_vartani`).
- **[`SectionRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/SectionRenderer.tsx)**: Handles Detailed Breakdown, Scientific Principles, Experiments, and Formulas.
- **[`StudyQuestionsRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/StudyQuestionsRenderer.tsx)**: Handles Practice Questions, MCQs, VSAs, SAs, LAs, Case Studies, and Model Papers.
- **[`FlashcardDeck.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/FlashcardDeck.tsx)**: Handles 3D Flip Flashcard Deck with Leitner Box controls.
- **[`MindMapRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/MindMapRenderer.tsx)**: Handles Hierarchical Node Graphs, Narrative Progression, and Grammar Focus.
- **[`QuizRenderer.tsx`](file:///D:/GURUKUL/frontend-nextjs/src/renderers/QuizRenderer.tsx)**: Handles Step 6 Final Assessment Quiz.

---

## 3. UI/UX & Reading Comfort Improvements Plan
1. **Calm Default Theme**: Soft warm background (`bg-slate-950` / `bg-slate-900` or warm off-white in light mode), deep readable text, restrained accents.
2. **Reading Comfort Control (`Aa` Control)**:
   - Text Size: Medium (17px), Large (19px), Extra Large (21px).
   - Line Spacing: Normal (1.5), Comfortable (1.7), Spacious (1.9).
   - Theme Selector: Calm Light, Warm Reading, Dark Comfortable.
   - Max Reading Width: $680\text{--}760\text{ px}$ reading column for long-form prose with left alignment.
3. **5-Stage Navigation Alignment**:
   - Merge `Flashcards` and `Mind Map` into the **Revision Stage**.
   - Keep `Quiz` as the 5th and final stage.
4. **Accessibility (TalkBack & Screen Readers)**:
   - Explicit `aria-label`, visible focus rings (`focus-visible:ring-2`), high contrast text ratios, and keyboard navigation.

---

## 4. Audit Acceptance
- **Content Preservation**: **100% (0 source files modified, 0 text rewritten)**
- **API Compatibility**: **100% Compatible with existing FastAPI endpoints**
- **Status**: **AUDIT COMPLETED — READY FOR PHASE 2 DESIGN & PHASE 3 IMPLEMENTATION**
"""

with open(os.path.join(reports_dir, "GURUKUL_STUDENT_UX_AUDIT.md"), "w", encoding="utf-8") as f:
    f.write(audit_md)

with open(r"D:\GURUKUL\GURUKUL_STUDENT_UX_AUDIT.md", "w", encoding="utf-8") as f:
    f.write(audit_md)

print("AUDIT COMPLETED! GURUKUL_STUDENT_UX_AUDIT.md generated in D:\\GURUKUL\\reports\\ and D:\\GURUKUL\\")
