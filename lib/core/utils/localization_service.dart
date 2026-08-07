import 'package:flutter/material.dart';

class LocalizationService {
  static const Map<String, Map<String, String>> _localizedValues = {
    'en': {
      'app_title': 'Gurukul AI',
      'home': 'Home',
      'subjects': 'Subjects',
      'practice': 'Practice',
      'ai_tutor': 'AI Tutor',
      'profile': 'Profile',
      'greeting': 'Good Morning',
    },
    'hi': {
      'app_title': 'गुरुकुल AI',
      'home': 'होम',
      'subjects': 'विषय',
      'practice': 'अभ्यास',
      'ai_tutor': 'AI ट्यूटर',
      'profile': 'प्रोफ़ाइल',
      'greeting': 'नमस्ते',
    },
  };

  static String translate(String key, String locale) {
    return _localizedValues[locale]?[key] ?? _localizedValues['en']![key]!;
  }
}
