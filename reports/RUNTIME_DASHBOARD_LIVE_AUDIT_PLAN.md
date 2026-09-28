# GURUKUL AI — RUNTIME DASHBOARD LIVE CONTENT AUDIT PLAN

## 1. Objective
To design an automated runtime verification protocol that inspects live dashboard responses and rendered UI DOM elements (via running FastAPI backend and Next.js frontend servers) on a strict **class-by-class, subject-by-subject, and chapter-by-chapter** basis, cross-checking them against authoritative source definitions without reading static disk files.

---

## 2. Execution Methodology & Plan

### Step 1: Live API Route Crawling (Backend Runtime)
- **Execution**: A test script spins up requests against the live FastAPI server (`http://localhost:8080`).
- **Granular Checks**:
  1. **Class Level**: `GET /api/v1/classes` (verifies grade discovery for Class 5, Class 6, and Class 7).
  2. **Subject Level**: `GET /api/v1/classes/{grade}/subjects/{subject}` (verifies subject endpoints for all multi-book subjects like Maths I, Maths II, Social I, Social II).
  3. **Chapter Level**: `GET /api/v1/chapters/{chapterId}/source?grade={grade}&subject={subject}` (verifies that live chapter source payloads return populated `overview`, `notes`, `master`, `flashcards`, `mindmaps`, `quiz`, and `question_papers`).

### Step 2: Headless Browser DOM Crawling & Visual Assertion (Frontend Runtime)
- **Execution**: Playwright / Puppeteer automation script connecting to live Next.js app (`http://localhost:3000`).
- **Granular Checks**:
  - Automatically loops through every Class, Subject, and Chapter URL.
  - Dynamically clicks through all 7 tabs (`Overview`, `Notes`, `Master Practice`, `Flashcards`, `Mindmaps`, `Quiz`, `Question Papers`).
  - Asserts that:
    - Zero `[object Object]` string artifacts appear in the DOM.
    - Zero `TypeError` or React invariant error overlays occur.
    - Sub-section selector tabs and unmerged question paper set/section tabs render active content.

### Step 3: Anomaly & Discrepancy Reporting
- Generates a live runtime audit report categorizing any HTTP 404/500 errors, slow responses, or empty DOM containers per chapter.

---

## 3. Compliance & Safety
- **Plan Only**: This document outlines the runtime auditing methodology. No code changes have been executed.
