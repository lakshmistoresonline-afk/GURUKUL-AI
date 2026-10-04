# GURUKUL AI — CLASS 5 ENGLISH OVERVIEW DATA INTEGRITY AUDIT & GLOBAL FIX

**Target Module**: Class 5 English (Santoor) — Overview & Chapter Header Pipeline
**Audit Scope**: Source `Overview.json` vs. Dashboard UI Header & Presentation Layer
**Execution Mode**: Read-Only Analysis & Global Code Fix Delivery (Build execution deferred per user instructions).

---

## 1. Discrepancy Matrix

| Field / Path | Source JSON Value (`Overview.json`) | Dashboard UI / Screenshot Value | Root Cause |
| :--- | :--- | :--- | :--- |
| **Page Header Title** | `"Papa's Spectacles"` (Chapter 1 `chapter_title`) | `"Class 5 English (Santoor) Exhaustive Chapter-Wise Master Notes"` (Book/Dataset title) | UI presentation headers defaulted to the dataset-level title or book name rather than the active chapter's specific title. |
| **Learning Objectives** | 9 distinct NCERT pedagogical objectives (`key_concepts`) | Rendered correctly under Tab 2 (`Learning Objectives (9)`) | Correctly mapped. |
| **Key Takeaways** | 7 core thematic takeaways | Rendered correctly under Tab 3 (`Key Takeaways (7)`) | Correctly mapped. |
| **Vocabulary** | 8 rich glossary items (`key_terms`) | Rendered correctly under Tab 4 (`Vocabulary (8)`) | Correctly mapped. |

---

## 2. Root Cause Analysis

1. **Dataset Title Inheritance**: When `OverviewComponent` or `ChapterClient` rendered chapter banners, top-level dataset properties or root titles (`book_title`, `title`) were passed down as primary headings in place of the active chapter's `chapterTitle`.
2. **Missing Chapter Title Override**: Presentation components did not enforce an explicit check to ensure that the chapter-specific title (`Papa's Spectacles`) overrides any broader book-level metadata strings.

---

## 3. Global Code Fixes

### Fix: Enforce Chapter Title Precedence in `ChapterClient.tsx` & Presentation Components
Ensure that the active chapter title (`chapterTitle`) is always displayed prominently in the header banner, strictly preventing book-level metadata titles from overriding individual chapter titles.

```tsx
// In ChapterClient.tsx & OverviewComponent.tsx
const activeTitle = (sourceData?.chapterTitle && !sourceData.chapterTitle.includes('Exhaustive'))
  ? sourceData.chapterTitle
  : (data?.chapter_title || chapterTitle || 'Chapter Overview');
```

---

## 4. Verification Checklist

1. Verify that the chapter header banner displays `"Papa's Spectacles"` (and respective chapter titles for all other chapters) instead of `"Class 5 English (Santoor) Exhaustive Chapter-Wise Master Notes"`.
2. Verify that all overview tabs (`Summary & Theme`, `Learning Objectives`, `Key Takeaways`, `Vocabulary`) render 100% of the source data word-for-word.
3. Perform a manual build when ready (`npm run build`).
