# GURUKUL AI — DASHBOARD ARCHITECTURE SPECIFICATION

**Version**: 2.0 Dynamic Student & Admin Dashboard
**Frontend**: Next.js 14 App Router (`frontend-nextjs/src/app`)
**Backend**: FastAPI Python 3.13 (`backend/src`)

## 1. Dynamic API Endpoints
* `GET /api/v1/student/catalog`: Discovers all active subjects and chapters
* `GET /api/v1/student/classes`: Returns class levels list
* `GET /api/v1/student/subjects/{subject_id}`: Returns subject chapter stream
* `GET /api/v1/student/chapters/{chapter_uid}/full`: Returns full 5-pillar chapter package

## 2. Dynamic UI Component Pipeline
* **Chapter Header**: Subject badge, level, title, navigation, and "What You Will Learn" summary.
* **"View Textbook Source" Drawer**: Exposes raw NCERT source text and page numbers without cluttering student view.
* **Subject Pedagogy Badges**:
  * English: Literature, poetry, dialogue, Santoor vocabulary, grammar cards.
  * Hindi: 100% Devanagari Unicode preserved without broken glyphs or transliteration.
  * EVS: Observation, survey, experiment, and field task badges.
  * Mathematics: Step-by-step worked solutions, mathematical operators, and numerical QA.
