# Content Storage Map - Project Gurukul AI

## Repository Structure

### 1. Educational Content (NCERT)
| Data Type | Location | Description |
|-----------|----------|-------------|
| **Static Framework** | `lib/features/curriculum/data/ncert_framework_v1.dart` | Class-Subject-Chapter hierarchy. |
| **Detailed Content** | `lib/features/curriculum/data/ncert_detailed_content.dart` | Core lessons, objectives, scripts. |
| **Guidelines** | `NCERT_GUIDELINES.md` | Mapping of Learning Outcomes. |

### 2. Multimedia Assets
| Type | Path | Usage |
|------|------|-------|
| **Lottie** | `assets/lottie/*.json` | Concepts & Micro-interactions. |
| **Rive** | `assets/rive/*.riv` | (Pending) Interactive simulations. |
| **Images** | `assets/images/*` | Diagrams and illustrations. |

### 3. Data Persistence
| Layer | Technology | Data Stored |
|-------|------------|-------------|
| **Local Cache** | Hive (`framework_cache`) | Framework structures, recently accessed nodes. |
| **User Data** | Hive / Firestore | Learning progress, Mastery scores, Flashcard status. |
| **Secure Storage** | flutter_secure_storage | Auth tokens, API Keys (GeoGebra/PhET - if any). |
| **Cloud Storage** | Firebase Storage | Heavy multimedia, PDF textbooks (ePathshala sync). |

## Database Collections (Firestore)
- `users`: Profile, class, preferences.
- `progress`: `userId` -> `chapterId` -> `masteryLevel`.
- `questions`: User-generated or scanned questions.
- `telemetry`: Interaction logs (Impression, Click, TimeSpent).
