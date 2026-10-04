# GURUKUL AI — PRINCIPAL FULL-STACK ENGINEER & DATA INTEGRITY AUDIT

**Target Module**: Class 5 / Class 6 / Class 7 English & Global Curriculum Pipeline
**Audit Scope**: Source JSON Files (`Notes.json`, `Overview.json`) vs. Dashboard UI Presentation Layer
**Execution Mode**: Read-Only Analysis & Global Systematic Fixes (Build execution deferred per user instructions).

---

## 1. Discrepancy Matrix

| Field / Path | Source JSON Value | Dashboard UI / Screenshot Value | Root Cause |
| :--- | :--- | :--- | :--- |
| **Chapter Header Title** | `"Papa's Spectacles"` (Chapter 1 title) | `"Class 5 English (Santoor) Exhaustive Chapter-Wise Master Notes"` (Book-level title) | Chapter title resolver fell back to book-level root `title` or `book_title` when resolving chapter headers. |
| **Overview / Summary Text** | Rich narrative paragraphs in `Overview.json` / `Notes.json` | Book-level description string in certain fallback views | Fallback resolver logic prioritized top-level dataset description over chapter-specific synopsis. |
| **Section Title Consistency** | Specific chapter title | Generic book title header in global banner | `ChapterClient.tsx` used book title if chapter-level property key was missing or named `chapterTitle` vs `chapter_title`. |

---

## 2. Root Cause Analysis

1. **Book-Level Metadata Leakage**: Root-level JSON fields (`title`, `description`, `book_title`) in `Overview.json` and `Notes.json` were being picked up by default header fallback logic instead of strict chapter-level properties (`chapter_title`, `chapterTitle`).
2. **Key Inconsistencies Across Schemas**: Different subjects/classes use varying key names for titles (`chapter_title`, `chapterTitle`, `title`, `name`, `chapter_no`).
3. **Header Resolution Precedence**: The backend chapter resolver (`chapters.py`) and frontend `ChapterClient.tsx` did not strictly prioritize chapter-specific titles over book-level database titles.

---

## 3. Global Code Fixes

### Fix 1: Backend Chapter Resolver (`backend/src/curriculum/api/chapters.py`)
Ensure chapter title resolution explicitly ignores book-level titles containing words like `"Exhaustive"`, `"Master Study"`, or `"Complete Course"` and extracts the true chapter title.

```python
def extract_true_chapter_title(d: dict, fallback: str) -> str:
    title = (
        d.get("chapter_title") or
        d.get("chapterTitle") or
        d.get("title") or
        (isinstance(d.get("overview"), dict) and (d["overview"].get("chapter_title") or d["overview"].get("title"))) or
        fallback
    )
    if isinstance(title, str) and ("exhaustive" in title.lower() or "master study" in title.lower()):
        # If it's a book title, try sub-keys
        if "chapter_title" in d:
            return d["chapter_title"]
        return fallback
    return title
```

### Fix 2: Frontend Header Title Resolution (`ChapterClient.tsx`)
Ensure the page header displays the exact chapter title (e.g. "Papa's Spectacles") and unit title rather than book metadata.

```tsx
const displayTitle = sourceData?.chapterTitle && !sourceData.chapterTitle.includes('Exhaustive')
  ? sourceData.chapterTitle
  : chapterId;
```

---

## 4. Verification Checklist

1. Verify that chapter header banners display the correct chapter title (`Papa's Spectacles`, `A Bottle of Dew`, etc.) instead of book-level metadata strings.
2. Verify that all 1,760 processed JSON assets maintain word-for-word data fidelity across all tabs (`Overview`, `Notes`, `Master Practice`, `Flashcards`, `Mindmaps`, `Quiz`, `Question Papers`, `Foundational Core`).
