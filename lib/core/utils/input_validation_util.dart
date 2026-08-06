class InputValidationUtil {
  /// Sanitizes text input by removing potentially harmful characters
  /// and trimming whitespace.
  static String sanitizeText(String input) {
    if (input.isEmpty) return "";

    // Basic trimming
    String sanitized = input.trim();

    // Remove potential script tags or HTML-like structures (basic)
    sanitized = sanitized.replaceAll(RegExp(r'<[^>]*>'), '');

    // Limit length to prevent buffer/memory attacks in processing
    if (sanitized.length > 2000) {
      sanitized = sanitized.substring(0, 2000);
    }

    return sanitized;
  }

  /// Validates email format
  static bool isValidEmail(String email) {
    return RegExp(r"^[a-zA-Z0-9.a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9]+\.[a-zA-Z]+")
        .hasMatch(email);
  }

  /// Validates that a string is alphanumeric (useful for IDs/Names)
  static bool isAlphanumeric(String input) {
    return RegExp(r'^[a-zA-Z0-9 ]+$').hasMatch(input);
  }
}
