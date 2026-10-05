# GURUKUL AI — DASHBOARD NAVIGATION ENHANCEMENT PLAN

This document outlines the engineering plan to introduce seamless, intuitive navigation controls (**Back**, **Next**, **Previous Chapter**, **Next Chapter**, and **Section Progression**) across all relevant dashboard pages.

---

## 1. Scope & Navigation Requirements

To provide a frictionless student learning flow, navigation controls will be introduced at three distinct levels:
1. **Chapter-to-Chapter Progression**: Bottom footer pagination in every chapter view allowing students to instantly jump to the previous chapter or next chapter in sequence.
2. **Curriculum Tab Sequencing**: A "Complete & Continue to [Next Section]" button at the bottom of each content tab (Overview $\rightarrow$ Notes $\rightarrow$ Master Practice $\rightarrow$ Foundational Core $\rightarrow$ Flashcards $\rightarrow$ Mindmaps $\rightarrow$ Quiz $\rightarrow$ Question Papers).
3. **Contextual Breadcrumb Bar**: Enhanced header navigation with explicit "Back to Subject Hub" buttons.

---

## 2. Proposed UI Component Architecture

- **`ChapterPaginationFooter.tsx`**: A reusable bottom bar component rendered in `ChapterClient.tsx` calculating sibling chapter IDs based on current chapter number sequence.
- **Tab Sequence Map**:
  ```ts
  const TAB_SEQUENCE = ['overview', 'notes', 'master', 'foundational', 'flashcards', 'mindmaps', 'quiz', 'question_papers'];
  ```

---

## 3. Implementation Roadmap

1. **Phase 1**: Create `ChapterPaginationFooter` for sequential chapter switching.
2. **Phase 2**: Integrate bottom-of-tab "Next Section" triggers in `ChapterClient.tsx`.
3. **Phase 3**: Verify navigation flows across Class 5, Class 6, and Class 7.
