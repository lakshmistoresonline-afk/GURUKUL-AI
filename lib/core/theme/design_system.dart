import 'package:flutter/material.dart';

class DesignSystem {
  // Brand Colors
  static const Color primary = Color(0xFF4F46E5);
  static const Color primaryLight = Color(0xFFEEF2FF);
  static const Color secondary = Color(0xFF8B5CF6);
  static const Color accent = Color(0xFF10B981);
  static const Color orange = Color(0xFFF97316);
  static const Color pink = Color(0xFFEC4899);

  static const Color background = Color(0xFFF1F5F9);
  static const Color surface = Colors.white;
  static const Color border = Color(0xFFE2E8F0);

  static const Color textPrimary = Color(0xFF0F172A);
  static const Color textSecondary = Color(0xFF475569);
  static const Color textTertiary = Color(0xFF94A3B8);

  // Gradients
  static const LinearGradient primaryGradient = LinearGradient(
    colors: [Color(0xFF4F46E5), Color(0xFF7C3AED)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // Spacing
  static const double spacingXs = 4.0;
  static const double spacingSm = 8.0;
  static const double spacingMd = 16.0;
  static const double spacingLg = 24.0;
  static const double spacingXl = 32.0;

  // Corner Radius
  static const double radiusSm = 8.0;
  static const double radiusMd = 12.0;
  static const double radiusLg = 24.0;
  static const double radiusXl = 32.0;

  // Typography
  static const TextStyle headlineLarge = TextStyle(fontSize: 32, fontWeight: FontWeight.w800, color: textPrimary, letterSpacing: -1);
  static const TextStyle headlineMedium = TextStyle(fontSize: 24, fontWeight: FontWeight.w700, color: textPrimary, letterSpacing: -0.5);
  static const TextStyle titleLarge = TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: textPrimary);
  static const TextStyle titleMedium = TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: textPrimary);
  static const TextStyle titleSmall = TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: textPrimary);
  static const TextStyle bodyLarge = TextStyle(fontSize: 16, color: textSecondary, height: 1.5);
  static const TextStyle bodyMedium = TextStyle(fontSize: 14, color: textSecondary, height: 1.4);
  static const TextStyle bodySmall = TextStyle(fontSize: 12, color: textSecondary);
  static const TextStyle labelSmall = TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: textTertiary, letterSpacing: 1);

  // Aliases for analyzer compliance
  static const TextStyle h1 = headlineLarge;
  static const TextStyle h2 = headlineMedium;
  static const TextStyle title = titleLarge;
  static const TextStyle label = labelSmall;

  // Shadows
  static List<BoxShadow> shadowSm = [
    BoxShadow(color: Colors.black.withValues(alpha: 0.04), blurRadius: 4, offset: const Offset(0, 2)),
  ];

  static List<BoxShadow> shadowMd = [
    BoxShadow(color: Colors.black.withValues(alpha: 0.06), blurRadius: 12, offset: const Offset(0, 4)),
  ];

  static List<BoxShadow> shadowLg = [
    BoxShadow(color: Colors.black.withValues(alpha: 0.1), blurRadius: 24, offset: const Offset(0, 8)),
  ];

  static BoxDecoration cardDecoration = BoxDecoration(
    color: surface,
    borderRadius: BorderRadius.circular(radiusLg),
    border: Border.all(color: border),
    boxShadow: shadowSm,
  );
}
