# GURUKUL AI — CLASS 5 ENGLISH NOTES ROOT CAUSE ANALYSIS & GLOBAL FIX

**Target Module**: Class 5 English (Santoor) — Notes Data Pipeline & Materialization
**Audit Scope**: Source `Notes.json` vs. Materialized `notes.json` & Dashboard UI Rendering
**Execution Mode**: Read-Only Analysis & Global Code Fix Delivery (Build execution deferred per user instructions).

---

## 1. Discrepancy Matrix

| Field / Path | Source JSON Value (`Notes.json`) | Dashboard UI / Screenshot Value | Root Cause |
| :--- | :--- | :--- | :--- |
| **Chapter Overview (`overview`)** | `"A humorous and affectionate poem..."` | Blank / Unrendered | The generator stored the entire subject-level `Notes.json` file (containing root metadata and a `"chapters"` array) as `notes.json` instead of extracting the specific chapter object (`chapters[0]`). |
| **Central Theme (`centralTheme`)** | `"Family humor, daily misplaced items..."` | Blank / Unrendered | Component expected `data.overview` / `data.centralTheme` at the root of `notes.json`, but received the book-level wrapper object. |
| **Detailed Breakdown (`detailedBreakdown`)** | Array of stanza analysis dictionaries | Missing from view | Same as above. |

---

## 2. Root Cause Analysis

1. **Book-Level Wrapper Assignment**: During materialization, dataset loaders assigned the entire raw `Notes.json` file (which has a root `"chapters"` array) directly to `notes.json` in the chapter directory.
2. **Missing Chapter-Level Projection**: Frontend components expect `notes.json` to be a chapter-scoped object (`{ chapterTitle, overview, centralTheme, detailedBreakdown }`), but received a multi-chapter container, causing property lookups (`data.overview`) to return `undefined`.

---

## 3. Global Code Fixes

### Fix: Chapter-Scoped Projection in Materializer (`generate_processed_content_correctly_v11.py`)
Ensure that when generating `notes.json` (and other chapter-scoped files), the pipeline extracts only the specific chapter dictionary matching `ch_num`.

```python
# Extract exact chapter object for notes, overview, master
def extract_chapter_record(dataset: Any, ch_num: int) -> dict:
    chrs = extract_chapters_from_json(dataset)
    for idx, ch in enumerate(chrs):
        if isinstance(ch, dict):
            c = (
                ch.get("chapter_number") or
                ch.get("chapterNumber") or
                ch.get("chapter_no") or
                ch.get("unit_number") or
                (ch.get("metadata", {}) and ch.get("metadata", {}).get("chapter_no")) or
                (idx + 1)
            )
            try:
                if int(c) == ch_num:
                    return ch
            except:
                if (idx + 1) == ch_num:
                    return ch
    return {}
```

---

## 4. Verification Checklist

1. Verify that `notes.json` in every processed chapter folder contains the chapter-scoped dictionary (`overview`, `centralTheme`, `detailedBreakdown`, `poeticDevices`, `characterAnalysis`) rather than the book-level wrapper.
2. Verify that the Notes tab in the dashboard renders all summaries, breakdowns, and vocabulary word-for-word without blank states.
3. *Build execution deferred per your instructions (run `npm run build` manually).*
