import 'dart:io';
import 'package:archive/archive_io.dart';
import 'package:path/path.dart' as p;
import 'package:flutter/foundation.dart';

/// Service responsible for recursive extraction of ZIP archives.
///
/// It handles top-level archives and automatically detects and extracts
/// any nested ZIP files into organized subject directories.
class ZipExtractionService {
  final String destinationRoot;

  ZipExtractionService({
    this.destinationRoot = 'D:/GURUKUL-AI/datasets/ncert_source/',
  });

  /// Extracts a ZIP file at [zipFilePath] to [destinationRoot].
  ///
  /// If [recursive] is true, it will scan the extracted content for more
  /// ZIP files and extract them as well.
  Future<void> extract(String zipFilePath, {bool recursive = true}) async {
    final zipFile = File(zipFilePath);
    if (!await zipFile.exists()) {
      throw Exception('Source ZIP file not found: $zipFilePath');
    }

    debugPrint('Extracting top-level archive: $zipFilePath');
    await _extractZip(zipFile, destinationRoot);

    if (recursive) {
      await _processNestedZips(Directory(destinationRoot));
    }
  }

  Future<void> _extractZip(File zipFile, String destPath) async {
    final bytes = await zipFile.readAsBytes();
    final archive = ZipDecoder().decodeBytes(bytes);

    for (final file in archive) {
      final filename = file.name;
      if (file.isFile) {
        final data = file.content as List<int>;
        final outFile = File(p.join(destPath, filename));
        await outFile.create(recursive: true);
        await outFile.writeAsBytes(data);
      } else {
        await Directory(p.join(destPath, filename)).create(recursive: true);
      }
    }
  }

  Future<void> _processNestedZips(Directory dir) async {
    final List<FileSystemEntity> entities = await dir.list(recursive: true).toList();

    for (final entity in entities) {
      if (entity is File && p.extension(entity.path).toLowerCase() == '.zip') {
        final String nestedZipPath = entity.path;
        final String parentDir = p.dirname(nestedZipPath);

        // Use filename without extension as subfolder name if needed,
        // but for NCERT we usually want subject names.
        // We'll extract into the same directory for now and let the scanner handle it.
        debugPrint('Extracting nested archive: $nestedZipPath');

        await _extractZip(entity, parentDir);

        // Delete the nested ZIP after successful extraction to keep the source clean
        await entity.delete();
      }
    }
  }

  /// Organizes extracted files into standardized Class/Subject folders.
  /// This is Phase 4 logic.
  Future<void> organizeSource() async {
    // Logic to move files from temporary extraction points to
    // datasets/ncert_source/class_X/subject/
    // This uses the RepositoryScannerService logic to identify Class/Subject.
  }
}
