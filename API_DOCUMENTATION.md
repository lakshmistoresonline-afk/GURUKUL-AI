# API & Service Documentation - Project Gurukul AI

## 1. Sunbird API Integration
Gurukul AI interfaces with Sunbird backend services through standardized contracts.

### Lern Service (User & Org)
- `ISunbirdAuthService`: Bridge for authentication and profile management.
- Maps Firebase UID to Sunbird User IDs for interoperability.

### Knowlg Service (Content & Framework)
- `FrameworkRepository`: Caches and navigates CBSE/NCERT framework structures (Subjects -> Chapters -> Topics).
- Supports local Hive caching for offline curriculum browsing.

### Inquiry Service (Assessment)
- `QuMLParser`: Translates Sunbird Question Markup Language into Flutter interactive widgets.
- `AssessmentEngine`: Manages test lifecycle and session recovery.

### Telemetry Service
- `TelemetryService`: Buffers and queues Ver 3.0 events locally in Hive.
- `SyncService`: Performs background batch synchronization to the cloud.

## 2. AI & Multimodal Services

### Gemini 1.5 Flash (Generative AI)
- `AiTutorService`: Specialized in Socratic tutoring and assessment hints.
- `AiInsightService`: Specialized in summarizing student performance for Parents and Teachers.

### Google ML Kit (OCR)
- `OcrService`: Extracts question text from textbook images using on-device text recognition.

### Voice Services (STT/TTS)
- `VoiceService`: Enables natural language interaction via speech input and spoken AI feedback.

## 3. Firebase & Database

### Firestore Collections
- `users`: Core profile data.
- `mastery`: Per-student, per-concept performance tracking.
- `gamification`: Real-time XP, streaks, and achievements.
- `assignments`: Teacher-managed tasks.
- `telemetry_sync`: Audit log for synchronized events.

### Cloud Functions
- `LearningCoordinator`: Local coordinator that chains learning activities.
- `onAssessmentSubmit`: (Planned) Cloud trigger for deeper analytics.
