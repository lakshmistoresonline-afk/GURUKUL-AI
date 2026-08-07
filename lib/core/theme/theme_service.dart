import 'package:flutter/material.dart';
import '../storage/local_storage_service.dart';

class ThemeService {
  final LocalStorageService _storage;
  static const String _themeKey = 'user_theme_mode';

  ThemeService(this._storage);

  ThemeMode get themeMode {
    final mode = _storage.get(_themeKey);
    if (mode == 'light') return ThemeMode.light;
    if (mode == 'dark') return ThemeMode.dark;
    return ThemeMode.system;
  }

  Future<void> setThemeMode(ThemeMode mode) async {
    await _storage.save(_themeKey, mode.name);
  }

  /// Returns a primary color based on the NCERT subject for better context.
  Color getSubjectColor(String subject) {
    switch (subject.toLowerCase()) {
      case 'mathematics':
        return const Color(0xB22563EB); // Modern Blue
      case 'science':
        return const Color(0xFF8B5CF6); // Modern Purple
      case 'evs':
        return const Color(0xFF10B981); // Modern Green
      case 'english':
        return const Color(0xFF6366F1); // Modern Indigo
      case 'hindi':
        return const Color(0xFFF59E0B); // Modern Orange
      case 'social science':
        return const Color(0xFF78350F); // Modern Brown
      default:
        return const Color(0xFF2563EB); // Primary Blue
    }
  }
}
