# GURUKUL AI — RUNTIME DASHBOARD CONTENT VERIFICATION & E2E TESTING PLAN

## 1. Objective
To establish a rigorous, automated verification protocol that inspects **live runtime dashboard content** (via running FastAPI backend APIs and Next.js frontend pages) rather than static files on disk, ensuring 100% data integrity, zero React rendering errors, and absolute UI fidelity.

---

## 2. Verification Methodology & Plan

### Phase 1: Live API Contract & Payload Inspection (Runtime Backend)
- **Tooling**: Automated Python test suite leveraging `httpx` or `FastAPI TestClient` against live runtime server instances.
- **Procedure**:
  1. Ping live endpoints (`/api/v1/classes`, `/api/v1/classes/{grade}/subjects/{subject}`, `/api/v1/chapters/{chapterId}/source`).
  2. Validate response status codes, payload schemas, and ensure required section keys (`overview`, `notes`, `master`, `flashcards`, `mindmaps`, `quiz`, `question_papers`) are non-null and correctly populated.

### Phase 2: Headless Browser E2E Crawling & DOM Assertion (Runtime Frontend)
- **Tooling**: Playwright / Puppeteer automated test runner.
- **Procedure**:
  1. Spin up the Next.js frontend (`http://localhost:3000`) and FastAPI backend (`http://localhost:8080`).
  2. Programmatically navigate to every grade (`Class 5`, `Class 6`, `Class 7`), every subject, and every chapter.
  3. Sequentially click through all 7 tabs (`Overview`, `Notes`, `Master Practice`, `Flashcards`, `Mindmaps`, `Quiz`, `Question Papers`).
  4. Intercept browser console logs to detect any unhandled runtime errors (`Error: Objects are not valid as a React child`).
  5. Assert that DOM content nodes are successfully rendered and visible (checking for absence of "No content available" or blank containers).

### Phase 3: Automated Anomaly Reporting
- Generate a runtime execution report flagging any slow endpoints, HTTP 404/500 responses, or DOM rendering exceptions in real-time.

---

## 3. Compliance & Safety
- **Plan Only**: This document outlines the verification strategy. No code changes have been executed.
