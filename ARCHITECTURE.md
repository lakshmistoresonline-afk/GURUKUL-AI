# Project Gurukul AI - Full Architecture Documentation

## 1. System Overview
Project Gurukul AI is a distributed educational platform designed to provide an AI-tutor companion for NCERT students. It adheres to the **Sunbird ED** design principles and utilizes a modern Flutter/Firebase tech stack.

## 2. Core Layers

### Presentation Layer (Flutter)
- **UI:** Material 3 design, responsive layouts.
- **Navigation:** Multi-tab student dashboard (Home, Progress, Ranks).
- **State Management:** BLoC (Business Logic Component) for predictable state transitions.
- **Widgets:** Specialized components for gamification (XP bars), interactive chat, and high-quality loaders (Lottie).

### Domain Layer
- **Models:** Entities representing Concepts, Mastery, Assignments, Assessment Sessions, and Gamification stats.
- **Services:** Pure business logic including:
    - **Recommendation Engine:** Personalized study paths.
    - **Spaced Repetition:** Scientifically scheduled revision.
    - **Mastery Engine:** Performance-based progress tracking.
    - **Milestone Service:** Achievement detection.

### Data Layer
- **Repositories:** Single source of truth coordinating between Remote (Firebase) and Local (Hive) sources.
- **Services:** Specialized wrappers for external APIs:
    - **AiTutorService:** Gemini 1.5 Flash (Socratic logic).
    - **OcrService:** Google ML Kit Text Recognition.
    - **VoiceService:** Speech-to-Text & Text-to-Speech.
    - **NotificationService:** Firebase Cloud Messaging.

## 3. Modular Breakdown
- `core/`: Cross-cutting concerns (DI, Telemetry, Storage, Sync, Notifications).
- `features/auth/`: Identity management and Sunbird Lern contract bridging.
- `features/curriculum/`: Framework management and Knowledge Graph mastering.
- `features/ai/`: Multi-modal tutoring (Chat, Voice, OCR).
- `features/student/`: Primary learning experience and visual progress tracking.
- `features/parent/`: Empathetic insight generation for oversight.
- `features/teacher/`: Analytical class management.
- `features/gamification/`: Engagement drivers (XP, Streaks, Leaderboards).

## 4. Data Standards
- **Telemetry:** Ver 3.0 compliant with Sunbird standards (IMPRESSION, INTERACT, ASSESS events).
- **Content:** Metadata-driven discovery following NCERT/CBSE taxonomies.
- **Assessment:** QuML 3.0 aligned structures with session recovery and AI-powered hints.

## 5. Security & Performance
- **Firestore Rules:** Role-based access control (RBAC) ensuring data isolation.
- **Caching:** Multi-tier caching (Firestore persistence + Hive metadata + Framework cache).
- **Lazy Loading:** Paginated UI and batched telemetry syncing.
