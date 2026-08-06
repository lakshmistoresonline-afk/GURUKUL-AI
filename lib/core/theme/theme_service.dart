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
      case 'mathematics': return Colors.blue;
      case 'science': return Colors.green;
      case 'evs': return Colors.teal;
      case 'english': return Colors.orange;
      case 'hindi': return Colors.red;
      case 'social science': return Colors.brown;
      default: return Colors.deepPurple;
    }
  }
}
