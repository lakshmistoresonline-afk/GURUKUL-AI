# User Actions Required - Project Gurukul AI Content Management

To complete the transition to the Central Content Repository, the Administrator must perform the following actions:

## 1. Multimedia Asset Population

The repository structure is ready, but the actual heavy media files need to be placed in the correct directories.

| Asset Type | Action | Target Directory |
| :--- | :--- | :--- |
| **NCERT Videos** | Download MP4 lessons for Class 5/6 and save them. | `/content_repository/multimedia/videos/` |
| **Lottie Animations** | Move existing JSON animations from `assets/lottie/` to the repository. | `/content_repository/multimedia/animations/` |
| **High-Res Diagrams** | Upload specialized diagrams for Science/Math chapters. | `/content_repository/multimedia/diagrams/` |
| **Audio Narrations** | Record/Upload intro narrations for English/Hindi chapters. | `/content_repository/multimedia/audio/` |

## 2. Configuration & Keys

1.  **Firebase Setup**: Ensure that `google-services.json` is present and that the project has `Cloud Firestore` enabled to support the new `QuestionRepository` and `GamificationRepository`.
2.  **Path Configuration**: In `FrameworkRepository`, ensure the `root` path is updated if the project is moved to a different drive (current: `D:/GURUKUL-AI/content_repository`).

## 3. Repository Cleanup

*   **Deprecated Files**: Once the `LessonMediaRepository` is updated to load from JSON, delete the hardcoded mappings.
*   **Manual Validation**: Spot-check `lesson.json` files in `class_05/evs` to ensure formatting is correct for the UI renderer.

## 4. Next Sync Target
*   Run `test/migration_tool.dart` whenever new content is added to the legacy maps to sync them to the repository (if legacy maps are still being maintained).
