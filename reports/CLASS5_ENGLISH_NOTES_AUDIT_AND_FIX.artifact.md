# GURUKUL AI — CLASS 5 ENGLISH NOTES DATA INTEGRITY AUDIT & GLOBAL FIX

**Target Module**: Class 5 English (Santoor) — Notes Pipeline & Data Materialization
**Audit Scope**: Source `Notes.json` vs. Processed `notes.json` & Dashboard UI Rendering
**Execution Mode**: Read-Only Analysis & Global Code Fix Delivery (Build execution deferred per user instructions).

---

## 1. Discrepancy Matrix

| Field / Path | Source JSON Value (`Notes.json`) | Dashboard UI / Screenshot Value | Root Cause |
| :--- | :--- | :--- | :--- |
| **Chapter Summary (`overview`)** | `"A humorous and affectionate poem..."` | Blank / Unrendered | Key mismatch: Source uses camelCase `"chapterNumber"`, whereas materialization scripts looked exclusively for snake_case `"chapter_number"`. |
| **Central Theme (`centralTheme`)** | `"Family humor, daily misplaced items..."` | Blank / Unrendered | Chapter lookup failed, falling back to an empty notes stub (`{"detailedBreakdown": []}`). |
| **Detailed Breakdown (`detailedBreakdown`)** | Array of 3 stanza breakdown objects | Missing from view | Same as above (missing chapter match during content generation). |
| **Poetic Devices / Characters** | Rich objects (`poeticDevices`, `characterAnalysis`) | Missing from view | Same as above. |

---

## 2. Root Cause Analysis

1. **CamelCase vs. SnakeCase Key Mismatch**: Source files like `Class 5/English/Notes.json` define chapter keys as `"chapterNumber"` and `"chapterTitle"`, whereas ingestion and generation scripts checked `ch.get("chapter_number")` and `ch.get("chapter_title")`.
2. **Silent Fallback Stubs**: When chapter matching failed due to key naming differences, generators fell back to writing empty fallback stubs (`{ "chapter_title": ..., "detailedBreakdown": [] }`), leaving UI components with no data to display.

---

## 3. Global Code Fixes

### Fix: Universal Chapter Number & Title Extractor (`generate_processed_content_correctly_v10.py` / Data Pipeline)
Update ingestion and generation scripts across all classes and subjects to support both snake_case and camelCase keys seamlessly.

```python
def extract_chapter_number(ch: dict, default_idx: int) -> int:
    return int(
        ch.get("chapter_number") or
        ch.get("chapterNumber") or
        ch.get("chapter_no") or
        ch.get("unit_number") or
        (ch.get("metadata", {}) and ch.get("metadata", {}).get("chapter_no")) or
        default_idx
    )

def extract_chapter_title(ch: dict, default_title: str) -> str:
    return (
        ch.get("chapter_title") or
        ch.get("chapterTitle") or
        ch.get("title") or
        (ch.get("metadata", {}) and ch.get("metadata", {}).get("title")) or
        default_title
    )
```

---

## 4. Verification Checklist

1. Verify that Class 5 English Notes populate fully under the `Notes` tab (Summary & Theme, Breakdown, Poetic Devices, Characters).
2. Verify that all 172 chapters across all subjects correctly resolve chapter numbers (`chapterNumber` vs `chapter_number`).
3. Perform a manual build when ready (`npm run build`).
