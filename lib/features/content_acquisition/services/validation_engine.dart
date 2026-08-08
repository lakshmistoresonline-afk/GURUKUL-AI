import 'dart:io';
import 'package:path/path.dart' as p;
import '../models/validation_report.dart';
import '../models/acquisition_file.dart';
import 'repository_scanner_service.dart';

/// Service responsible for validating the integrity and completeness of the content repository.
class ValidationEngine {
  final String ncertSourcePath;
  final String processedChaptersPath;
  final RepositoryScannerService _scanner = RepositoryScannerService();

  ValidationEngine({
    this.ncertSourcePath = 'D:/GURUKUL-AI/datasets/ncert_source/',
    this.processedChaptersPath = 'D:/GURUKUL-AI/datasets/processed/chapters/',
  });

  /// Performs a full validation of the repository.
  Future<ValidationReport> validateRepository() async {
    final List<ValidationIssue> issues = [];
    final Map<String, int> stats = {
      'total_source_files': 0,
      'total_processed_chapters': 0,
      'errors': 0,
      'warnings': 0,
    };

    // 1. Scan Source Directory for issues
    final sourceFiles = await _scanSourceDirectory(issues, stats);

    // 2. Scan Processed Directory for issues
    final processedKeys = await _scanProcessedDirectory(issues, stats);

    // 3. Detect Missing Chapters
    _detectMissingChapters(sourceFiles, processedKeys, issues, stats);

    // Finalize statistics
    stats['errors'] = issues.where((i) => i.severity == ValidationSeverity.error).length;
    stats['warnings'] = issues.where((i) => i.severity == ValidationSeverity.warning).length;

    return ValidationReport(
      timestamp: DateTime.now(),
      issues: issues,
      statistics: stats,
    );
  }

  Future<List<AcquisitionFile>> _scanSourceDirectory(
    List<ValidationIssue> issues,
    Map<String, int> stats,
  ) async {
    final dir = Directory(ncertSourcePath);
    if (!await dir.exists()) {
      issues.add(ValidationIssue(
        message: 'NCERT source directory not found at configured path',
        path: ncertSourcePath,
        severity: ValidationSeverity.error,
        category: ValidationCategory.pathMismatch,
      ));
      return [];
    }

    final Set<String> fileFingerprints = {};
    final List<FileSystemEntity> entities = await dir.list(recursive: true).toList();

    for (final entity in entities) {
      if (entity is! File) continue;
      stats['total_source_files'] = (stats['total_source_files'] ?? 0) + 1;

      final filePath = entity.path;
      final fileName = p.basename(filePath);
      final extension = p.extension(filePath).toLowerCase();
      final size = entity.lengthSync();

      if (size == 0) {
        issues.add(ValidationIssue(
          message: 'Empty file detected (0 bytes)',
          path: filePath,
          severity: ValidationSeverity.error,
          category: ValidationCategory.emptyFile,
        ));
      }

      const supportedExts = {'.pdf', '.epub', '.docx', '.zip', '.jpg', '.jpeg', '.png', '.webp', '.bmp'};
      if (!supportedExts.contains(extension)) {
        issues.add(ValidationIssue(
          message: 'Unsupported file format: $extension',
          path: filePath,
          severity: ValidationSeverity.warning,
          category: ValidationCategory.unsupportedFormat,
        ));
      }

      final fingerprint = "$fileName-$size";
      if (fileFingerprints.contains(fingerprint)) {
        issues.add(ValidationIssue(
          message: 'Potential duplicate file detected (matching name and size)',
          path: filePath,
          severity: ValidationSeverity.warning,
          category: ValidationCategory.duplicateFile,
        ));
      } else {
        fileFingerprints.add(fingerprint);
      }

      if (extension == '.pdf' && size > 4) {
        if (!await _isPdfValid(entity)) {
          issues.add(ValidationIssue(
            message: 'Corrupted PDF: Invalid header magic number',
            path: filePath,
            severity: ValidationSeverity.error,
            category: ValidationCategory.corruptedFile,
          ));
        }
      }
    }

    return await _scanner.scan();
  }

  Future<bool> _isPdfValid(File file) async {
    try {
      final bytes = await file.openRead(0, 4).first;
      final header = String.fromCharCodes(bytes);
      return header.startsWith('%PDF');
    } catch (e) {
      return false;
    }
  }

  Future<Set<String>> _scanProcessedDirectory(
    List<ValidationIssue> issues,
    Map<String, int> stats,
  ) async {
    final dir = Directory(processedChaptersPath);
    if (!await dir.exists()) return {};

    final Set<String> processedKeys = {};
    final List<FileSystemEntity> entities = await dir.list(recursive: true).toList();

    for (final entity in entities) {
      if (entity is! File) continue;
      final path = entity.path;
      final fileName = p.basename(path);

      if (fileName == 'lesson.json') {
        stats['total_processed_chapters'] = (stats['total_processed_chapters'] ?? 0) + 1;

        final relativePath = p.relative(path, from: processedChaptersPath);
        final parts = p.split(relativePath);

        if (parts.length >= 4) {
          final classLevel = parts[0];
          final subject = parts[1];
          final chapter = parts[3];
          final key = "$classLevel-$subject-$chapter";

          if (processedKeys.contains(key)) {
            issues.add(ValidationIssue(
              message: 'Duplicate metadata: multiple lesson.json found for the same chapter index',
              path: path,
              severity: ValidationSeverity.error,
              category: ValidationCategory.duplicateMetadata,
            ));
          } else {
            processedKeys.add(key);
          }
        }

        if (entity.lengthSync() < 10) {
           issues.add(ValidationIssue(
            message: 'Empty or invalid metadata JSON file',
            path: path,
            severity: ValidationSeverity.error,
            category: ValidationCategory.emptyFile,
          ));
        }
      }
    }
    return processedKeys;
  }

  void _detectMissingChapters(
    List<AcquisitionFile> sourceFiles,
    Set<String> processedKeys,
    List<ValidationIssue> issues,
    Map<String, int> stats,
  ) {
    for (final file in sourceFiles) {
      final classKey = "class_${file.classLevel.toString().padLeft(2, '0')}";
      final chapterKey = "chapter_${file.chapterIndex.toString().padLeft(2, '0')}";
      final key = "$classKey-${file.subject.toLowerCase()}-$chapterKey";

      if (!processedKeys.contains(key)) {
        issues.add(ValidationIssue(
          message: 'Missing processed chapter: No lesson.json found for identified source file',
          path: file.path,
          severity: ValidationSeverity.warning,
          category: ValidationCategory.missingChapter,
        ));
      }
    }
  }
}
