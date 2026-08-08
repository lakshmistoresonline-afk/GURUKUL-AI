import 'package:flutter/services.dart';
import 'package:flutter/foundation.dart';

/// Service responsible for loading AI prompts from external Markdown files.
/// This allows updating prompts without changing the application code.
class PromptManager {
  static const String _basePath = 'lib/features/ai_enrichment/prompts/';

  /// Loads a prompt by name (e.g. 'quiz_prompt').
  /// Supports optional template variable replacement.
  Future<String> getPrompt(String name, {Map<String, String>? variables}) async {
    try {
      // In production/release, we might use rootBundle if these are assets.
      // For development/enrichment CLI, we use direct file access.
      // We'll use a simple abstraction here.
      String content = await _loadContent(name);

      if (variables != null) {
        variables.forEach((key, value) {
          content = content.replaceAll('{{$key}}', value);
        });
      }

      return content;
    } catch (e) {
      debugPrint('PromptManager: Error loading prompt $name - $e');
      return '';
    }
  }

  Future<String> _loadContent(String name) async {
    // Attempt to load as a file string.
    // Note: If using rootBundle, prompts must be listed in pubspec assets.
    final path = '$_basePath$name.md';
    return await rootBundle.loadString(path);
  }
}
