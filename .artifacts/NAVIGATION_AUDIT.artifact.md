# Navigation Audit - Project Gurukul AI

## 1. Route Verification
Every major navigation path has been verified for structural integrity and logical flow.

| Start Screen | Destination | Trigger | Verification |
| :--- | :--- | :--- | :--- |
| **Home (Dashboard)** | Subject Hub | `_SubjectCard` Tap | **VERIFIED** |
| **Subject Hub** | Chapter Dashboard | `_ChapterCard` Tap | **VERIFIED** |
| **Subject Hub** | Learning Journey | "View Map" Button | **VERIFIED** |
| **Subject Hub** | Flashcards | Command Centre Action | **VERIFIED** |
| **Chapter Dashboard**| AI Tutor Chat | "Start Chat" Action | **VERIFIED** |
| **Global Nav** | Progress Analytics | Bottom Navigation Tab | **VERIFIED** |
| **Global Nav** | AI Tutor | Bottom Navigation Tab | **VERIFIED** |

## 2. Component Clickability Matrix
- [x] **Bottom Navigation:** All 5 tabs (`Home`, `Learning`, `Tutor`, `Progress`, `Profile`) correctly update the `IndexedStack`.
- [x] **Subject Cards:** Dynamic routing based on `subject` and `classLevel` params.
- [x] **Command Centre:** All icons in `subject_dashboard_screen.dart` have defined `onTap` handlers or are verified stubs.
- [x] **Back Navigation:** All secondary screens use standard `Scaffold` or `SliverAppBar` back behavior.

## 3. Deep Link & Telemetry Integration
- **Telemetry:** Navigation events are logged via `sl<TelemetryService>().logImpression()` on tab changes.
- **State Preservation:** `IndexedStack` ensures that scroll position and state are maintained when switching between main tabs.

---
**Status: ZERO BROKEN ROUTES**
The navigation graph is fully connected and adheres to the "Three-Tap Rule" (Access any learning content within 3 taps).
