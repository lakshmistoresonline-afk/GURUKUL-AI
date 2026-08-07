# Phase 42 — UI/UX Redesign & Student Experience Enhancement

This phase focuses on transforming the Project Gurukul AI interface into a premium, child-friendly learning environment for Class 5 and 6 students, while maintaining the underlying architecture.

## Proposed Changes

### [Component: Core Theme & Styles]
Update the global theme to use the specified modern educational palette and child-friendly typography.

#### [MODIFY] [theme_service.dart](file:///D:/GURUKUL-AI/lib/core/theme/theme_service.dart)
- Update `getSubjectColor` with the new color mapping:
    - Mathematics → Blue (#2563EB)
    - EVS → Green (#10B981)
    - Science → Purple (#8B5CF6)
    - English → Indigo (#6366F1)
    - Hindi → Orange (#F59E0B)
    - Social Science → Brown (#78350F)

#### [MODIFY] [app.dart](file:///D:/GURUKUL-AI/lib/app.dart)
- Configure `ThemeData` with rounded corners, soft shadows, and the new primary color (#2563EB).
- Set background color to #F8FAFC.

---

### [Component: Main Navigation]
Implement an animated bottom navigation bar with the new destinations: Home, Subjects, Practice, AI Tutor, and Profile.

---

### [Component: Home Dashboard]
Replace the current subject grid with a personalized, multi-section dashboard.

#### [MODIFY] [dashboard_screen.dart](file:///D:/GURUKUL-AI/lib/features/student/presentation/screens/dashboard_screen.dart)
- **Top Section**: Personalized greeting ("Good Morning, [Name]"), Avatar, Class info.
- **Stats Row**: Learning Streak, XP, Level, and Coins.
- **Continue Learning**: A prominent card to resume the last lesson/topic.
- **Today's Plan**: Daily goal and AI recommendations.
- **Horizontal Subject List**: A row or grid of redesigned subject cards.

---

### [Component: AI Tutor Experience]
Transform the AI Tutor from a simple floating button into an interactive, animated assistant.

#### [MODIFY] [ai_tutor_chat_screen.dart](file:///D:/GURUKUL-AI/lib/features/ai/presentation/screens/ai_tutor_chat_screen.dart)
- Enhance chat UI with modern bubbles, suggested questions, and quick actions.
- Add voice input support UI.

---

### [Component: Content & Progress]
Enhance the visual representation of progress and curriculum content.

#### [MODIFY] [progress_dashboard_screen.dart](file:///D:/GURUKUL-AI/lib/features/student/presentation/screens/progress_dashboard_screen.dart)
- Redesign with charts, "Weak Areas", "Strong Areas", and achievement timelines.

#### [MODIFY] [chapter_list_screen.dart](file:///D:/GURUKUL-AI/lib/features/student/presentation/screens/chapter_list_screen.dart)
- Add beautiful headers, difficulty badges, and "Continue" buttons.

## Verification Plan

### Automated Tests
- Run `flutter analyze` to ensure no UI breakages.
- (Optional) Run existing widget tests to ensure functionality remains intact.

### Manual Verification
- Verify layout responsiveness on Web (Edge) and Android Emulator.
- Check Dark Mode implementation.
- Verify all navigation paths.
- Ensure "Continue Learning" correctly fetches and displays the last active concept.
