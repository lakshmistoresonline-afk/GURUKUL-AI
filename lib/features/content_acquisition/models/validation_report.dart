class ValidationReport {
  final DateTime timestamp;
  final List<ValidationIssue> issues;
  final Map<String, int> statistics;

  ValidationReport({
    required this.timestamp,
    required this.issues,
    required this.statistics,
  });

  Map<String, dynamic> toJson() {
    return {
      'timestamp': timestamp.toIso8601String(),
      'issues': issues.map((e) => e.toJson()).toList(),
      'statistics': statistics,
    };
  }
}

enum ValidationSeverity { error, warning, info }

enum ValidationCategory {
  missingChapter,
  duplicateFile,
  corruptedFile,
  emptyFile,
  unsupportedFormat,
  duplicateMetadata,
  pathMismatch
}

class ValidationIssue {
  final String message;
  final String path;
  final ValidationSeverity severity;
  final ValidationCategory category;

  ValidationIssue({
    required this.message,
    required this.path,
    required this.severity,
    required this.category,
  });

  Map<String, dynamic> toJson() {
    return {
      'message': message,
      'path': path,
      'severity': severity.name,
      'category': category.name,
    };
  }
}
