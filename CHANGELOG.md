# Changelog - Project Gurukul AI

## [1.0.0] - 2026-08-07
### Added
- Complete UI overhaul with new **Design System** and **Material 3**.
- **Home Dashboard**: Personalized greeting, today's goals, study plan preview, and streak stats.
- **Subject Dashboard**: Subject-specific mini-dashboard with progress tracking and quick actions.
- **Chapter Dashboard**: Overview, objectives, and structured topic list.
- **Curriculum Import Wizard**: Step-by-step tool to convert PDFs into interactive AI lessons.
- **Content Studio**: Professional admin interface for structured lesson editing and AI content generation.
- **Interactive Learning**: New `SortingActivity` and `FillBlanksActivity` widgets.
- **Question Centre**: Multi-tabbed bank for chapter-wise questions, papers, and AI exam generation.
- **Reading Assistant**: Voice narration with real-time highlighting support.
- **Sunbird Telemetry**: Integrated EID lifecycle (START, END, INTERACT, IMPRESSION).
- **Certification Engine**: Automatic PDF certificate generation on course completion.

### Changed
- Replaced legacy navigation and placeholders with content-driven UI.
- Migrated all assets to be chapter-specific to avoid generic reuse.
- Updated `ConceptNode` model to support advanced Studio fields (Scripts, Notes, Outcomes).

### Fixed
- Resolved all major compilation and URI import issues.
- Optimized performance for 60 FPS on low-end devices.
- Improved offline reliability via enhanced Hive/Firestore sync.
