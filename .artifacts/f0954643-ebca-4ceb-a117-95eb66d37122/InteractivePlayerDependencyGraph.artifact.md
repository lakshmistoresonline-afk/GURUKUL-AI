# Dependency Analysis: Interactive Player Widgets

## 1. Implementations
- `lib/features/content/presentation/widgets/interactive_player_widget.dart` (Advanced, with Telemetry)
- `lib/features/curriculum/presentation/widgets/interactive_content_player.dart` (Basic)

## 2. Consumers
- `lib/features/content/presentation/screens/content_player_screen.dart`: Uses `InteractivePlayerWidget`.
- `lib/features/curriculum/presentation/screens/content_viewer_screen.dart`: Uses `InteractiveContentPlayer`.

## 3. Consolidation Goal
- Move `InteractivePlayerWidget` to `lib/core/widgets/content/interactive_player.dart`.
- Merge URL support and Title support.
- Update consumers.
- Delete redundant files.
