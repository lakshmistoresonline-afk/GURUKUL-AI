# Gurukul AI – Repository Overview

## 1. Directory Responsibilities

### Root Directories
- `lib/`: Core Flutter application source.
- `datasets/`: Centralized data store (Input, Processed, Multimedia).
- `assets/`: UI-specific assets (icons, static images).
- `android/`, `web/`: Platform-specific configuration.
- `test/`: Verification suite.

### Feature Modules (`lib/features/`)
- `auth`: Firebase-based user authentication.
- `student`: Primary learning interface and personalized dashboard.
- `admin`: System management console.
- `content_acquisition`: Ingestion pipeline for NCERT resources.
- `curriculum`: Domain logic for frameworks and mastery.
- `ai`: Specialized services for AI Tutor and OCR.
- `questions`/`assessment`: QuML-compatible assessment engine.
- `gamification`: XP and rewards logic.

### Core Infrastructure (`lib/core/`)
- `di`: Service locator (GetIt).
- `telemetry`: Sunbird ED Telemetry v3.0 generator and sync.
- `offline`: Hive-based persistent caching and sync.
- `theme`: Material 3 design system.

## 2. Technology Stack
- **Framework**: Flutter (Latest Stable).
- **State Management**: BLoC (Business Logic Component).
- **Backend**: Firebase (Auth, Firestore, Functions, Cloud Messaging).
- **Local Storage**: Hive (Encrypted) + Secure Storage.
- **AI Engine**: Google Gemini 1.5 Flash.
- **Standards**: Sunbird ED, NCERT Framework.

## 3. Dependency Flow
`UI (Screens/Widgets)` -> `Controllers (BLoCs)` -> `Domain (Models/Services)` -> `Data (Repositories/Providers)` -> `Infrastructure (Core/Datasets)`
