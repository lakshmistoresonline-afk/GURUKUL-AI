# Project Gurukul AI - Architecture

## 1. Overview
Gurukul AI is a comprehensive, AI-powered learning platform designed specifically for NCERT/CBSE students (Class 5-12). It uses a clean, modular architecture to ensure scalability, offline-first reliability, and a premium educational experience.

## 2. Core Modules
- **`core/`**: Infrastructure, Dependency Injection, Theme/Design System, Telemetry, and Utilities.
- **`features/auth/`**: Firebase Authentication for students, teachers, and parents.
- **`features/curriculum/`**: NCERT framework mapping, lesson repository, and the "Learning Journey" engine.
- **`features/ai/`**: Gemini-powered tutors, OCR answer evaluation, and generative content factory.
- **`features/gamification/`**: Reward systems, streaks, achievements, and certification engine.
- **`features/content/`**: Content Provider Framework (Local + External), Content Studio for admin management, and multi-format player.
- **`features/questions/`**: A vast question bank and AI-driven personalized exam generator.
- **`features/planner/`**: Smart study scheduling and spaced repetition revision engine.

## 3. Technology Stack
- **Frontend**: Flutter (Material 3)
- **Backend**: Firebase (Auth, Firestore, Functions, Storage)
- **AI**: Google Generative AI (Gemini), ML Kit (Text Recognition, Barcode)
- **Database**: Hive (Local caching/Offline), Firestore (Cloud Sync)
- **Animation**: Lottie, Rive, Flutter Custom Painter
- **Telemetry**: Sunbird-compatible Telemetry V3 standard

## 4. Content Ecosystem
Gurukul AI follows a "Local Primary" content policy. External providers (DIKSHA, ePathshala) enrich the experience, but the core learning journey is always available offline using AI-generated or pre-packaged local content.

## 5. Design Principles
- **Zero Whitespace**: Every screen is content-dense and provides immediate educational value.
- **Child-Friendly**: UI/UX optimized for Class 5-6 students (vibrant colors, large touch targets, story-based flows).
- **Responsive**: Adapts to Mobile, Tablet, and Web (Edge).
