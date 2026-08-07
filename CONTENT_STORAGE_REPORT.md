# Content Storage Report - Project Gurukul AI

## 1. Repository Structure (`/content_repository/`)

| Folder | Purpose |
| :--- | :--- |
| `/curriculum/` | Core NCERT syllabus structure (Class -> Subject -> Chapter). |
| `/multimedia/` | Centralized store for images, videos, audios, and animations. |
| `/questions/` | Question bank assets and generated paper templates. |
| `/metadata/` | System-wide educational metadata and taxonomy definitions. |
| `/worksheets/` | Printable and interactive PDF worksheets. |
| `/assessments/` | Structured assessment frameworks and rubrics. |
| `/ai_generated/` | Cache for AI-driven lesson enrichments and hints. |
| `/logs/` | Content ingestion and sync logs. |
| `/backups/` | Automated snapshots of the repository. |
| `/imports/` / `/exports/` | Staging areas for bulk data operations. |

## 2. Educational Asset Mapping

| Asset Type | Primary Location | Linked By |
| :--- | :--- | :--- |
| **Lesson JSON** | `/curriculum/class_XX/{subject}/chapters/chapter_XX/lesson.json` | `FrameworkRepository` |
| **Videos (MP4)** | `/multimedia/videos/` | `media.json` in chapter folder |
| **Animations (Lottie)** | `/multimedia/animations/` | `lesson.json` -> `animatedLessonAsset` |
| **Images/Diagrams** | `/multimedia/images/` & `/multimedia/diagrams/` | `media.json` |
| **Audio (Narration)** | `/multimedia/audio/` | `media.json` |
| **SVG Icons** | `/multimedia/svg/` | Shared across UI |

## 3. Database & Cache Mapping

*   **Firestore Collections**:
    *   `users`: User profiles and preferences.
    *   `progress`: Granular learning progress per concept.
    *   `question_papers`: Metadata for generated and official papers.
    *   `gamification`: XP, Streaks, and Achievement status.
*   **Hive Boxes**:
    *   `framework_cache`: Local cache of the scanned repository structure.
    *   `dynamic_content`: Overrides and user-imported content.
    *   `app_settings`: UI preferences and offline status.
*   **Firebase Storage**:
    *   Mirror of `/content_repository/multimedia/` for remote delivery.

## 4. Migration Status

| Category | Status | Notes |
| :--- | :--- | :--- |
| **NCERT Curriculum** | **COMPLETED** | 141 lessons migrated from hardcoded maps to JSON. |
| **Media Mapping** | **IN PROGRESS** | Mappings defined in `LessonMediaRepository`; files need physical move. |
| **Question Bank** | **IN PROGRESS** | Moving from local JSON to Firestore `question_papers`. |
| **Gamification** | **PENDING** | Achievement definitions still hardcoded in `GamificationRepository`. |
