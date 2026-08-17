# NCERT Content Processor Guide

This guide explains how to use the deterministic NCERT pipeline to process textbook PDFs and publish them to the Gurukul AI dashboard.

## Overview

The pipeline consists of two main stages:
1.  **Processing:** Extracts text from PDFs, resolves chapter IDs, and merges existing questions into a staging directory.
2.  **Publishing:** Copies validated staging packages to the production environment.

## Directory Structure

### 1. Source Directory (`--source-dir`)
Organize your PDFs by subject and part:
```text
class7_ncert_source/
├── Mathematics/
│   ├── Part I/
│   │   ├── ch1.pdf
│   │   └── ch2.pdf
│   └── Part II/
├── Science/
└── English/
```

### 2. Output Directory (`--output-dir`)
This is the staging area where `package.json` files are generated.
```text
class7_processed/
├── class_7/
│   ├── mathematics/
│   │   ├── gegp101/
│   │   │   └── package.json
```

## Usage

### Step 1: Dry-Run Processing
Always run a dry-run first to check for unresolved IDs or potential errors.
```bash
python scripts/ncert_content_processor.py `
  --class 7 `
  --source-dir D:\GURUKUL-AI\class7_ncert_source `
  --output-dir D:\GURUKUL-AI\class7_processed `
  --dry-run
```

### Step 2: Actual Processing
Generate the staging packages.
```bash
python scripts/ncert_content_processor.py `
  --class 7 `
  --source-dir D:\GURUKUL-AI\class7_ncert_source `
  --output-dir D:\GURUKUL-AI\class7_processed
```

### Step 3: Validation
Review the `NCERT_PROCESSING_REPORT.md` in your output directory. Check for:
-   **Resolved IDs:** These match your production registry.
-   **Proposed IDs:** These are candidates for new chapters. Add them to `backend/storage/chapter_title_map.json` to make them official.

### Step 4: Publishing
Move the validated content to production.
```bash
python scripts/publish_ncert_content.py `
  --class 7 `
  --input-dir D:\GURUKUL-AI\class7_processed
```

## Feature Integration

### Question Bank
To merge pre-authored questions, use `--question-bank-dir`. The script will look for files named `[chapter_id].json` or `[slug].json` in the subject folder.

### Reproducibility
Every package includes a `source_hash` (SHA256) of the original PDF. This ensures you can track exactly which version of a textbook was used.

## Adding New Classes (e.g. Class 8)

1.  Open `config/ncert_classes.json`.
2.  Add a new entry for `class_8`.
3.  Define the `id_pattern` for each subject.
4.  Run the processor with `--class 8`.

## Safety Features
-   **No Overwrite:** By default, neither script will overwrite existing files. Use `--update-existing` to force an update.
-   **Staging Isolation:** The processor never writes to production.
-   **No AI:** All operations are deterministic (regex, filesystem, JSON merging).
