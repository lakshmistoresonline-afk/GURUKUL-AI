# Refactored Modules Report - Repository Consolidation

## 1. Unified Spaced Repetition Service
- **New Location**: `lib/core/learning/spaced_repetition_service.dart`
- **Changes**: Merged basic threshold-based interval logic with SM-2 algorithm principles.
- **Benefit**: Centralized learning algorithm ensures consistent revision scheduling across Planner and Curriculum modules.

## 2. Question Center Overhaul
- **Location**: `lib/features/questions/presentation/screens/question_center_screen.dart`
- **Changes**: 
    - Merged design from `QuestionCentreScreen` (RE).
    - Added high-fidelity gradient header.
    - Expanded tabs to include a "Hub" with active question banks (PYQ, HOTS, etc.).
    - Unified navigation entry points.

## 3. Core Interactive Player
- **New Location**: `lib/core/widgets/content/interactive_player.dart`
- **Changes**: 
    - Created a shared component supporting both local file paths and remote URLs.
    - Integrated `GurukulBridge` for JavaScript-to-Flutter telemetry reporting.
- **Benefit**: Simplified content playback logic and guaranteed telemetry capture for all interactive modules.

## 4. Subject Dashboard
- **Changes**: 
    - Refactored `_CommandCenter` to be stateless and configurable.
    - Refactored `_LearningJourneyMap` to use `FrameworkRepository` for dynamic concept lookup, removing hardcoded dependency on deleted content files.
