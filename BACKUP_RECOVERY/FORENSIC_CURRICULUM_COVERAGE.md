# Forensic Curriculum Coverage Report

## Ground Truth vs Canonical Content

| Class | Actual Textbook Chapters | Canonical Entries Found | Classification |
| :--- | :--- | :--- | :--- |
| **Class 5** | 47 | 89 | 47 Valid, 37 Redundant, 5 Placeholder 00 |
| **Class 6** | 54 | 60 | 54 Valid, 6 Placeholder 00 |
| **Class 7** | 62 | 68 | 62 Valid (Thin), 6 Placeholder 00 |
| **Total** | **163** | **217** | **163 Textbook Chapters + 54 Extras** |

## Audit Details

### 1. Actual Chapter Verification
The original NCERT source repository contains exactly **163 chapters** across Class 5, 6, and 7. Every single one of these has a corresponding entry in `CANONICAL_CONTENT`.

### 2. Forensic Findings on Extras (54 units)
- **Placeholders (17)**: Every subject has a `chapter_00` with "Untitled" metadata. These are artifacts of the merge process and not real textbook content.
- **Redundant Class 5 Numbering (37)**: Class 5 EVS, Hindi, and Mathematics were mapped with a 1-10 range in addition to their correct canonical range (11-20, 21-32, 33-47). These redundant units are mostly thin and lack the full integration data found in the valid units.

### 3. "None" Subject Investigation
Three "none" subject entries were identified:
- `class_05/none/chapters/chapter_00`
- `class_06/none/chapters/chapter_00`
- `class_07/none/chapters/chapter_00`
These are empty directories created from files where neither subject nor class could be determined from the filename or JSON content.

### 4. Component Completeness Audit
- **Class 5 & 6**: Generally complete with `lesson`, `quiz`, and `flashcards`.
- **Class 7**: **CRITICAL ISSUE**. Most Class 7 canonical chapters are "thin", containing only a `lesson.json` with metadata. The full content (Question Banks, Summaries, HOTS) was not correctly merged and exists in the `ARCHIVE_DUPLICATES` folder.

### 5. Multimedia Audit (653 Resources)
- Resources are mapped across **101 chapters** (Class 5 and 6).
- **Class 7 is missing all multimedia mapping.**
- Most resources are **Discovery/Search Links** (DIKSHA Search, YouTube Search) rather than verified direct video IDs.

## Conclusion
The report of 217 canonical chapters is mathematically correct (163 valid + 54 extras), but pedagogically misleading as it includes placeholders and redundant numbering. Furthermore, the Class 7 curriculum is structurally present but content-deficient due to merge failures.
