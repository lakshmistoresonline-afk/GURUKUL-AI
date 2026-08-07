import 'dart:convert';
import 'dart:io';
import 'package:crypto/crypto.dart';
import 'package:path/path.dart' as p;
import '../models/acquisition_file.dart';

/// Service responsible for generating and maintaining the content manifest.
class ManifestService {
  final String manifestPath;

  ManifestService({
    this.manifestPath = 'D:/GURUKUL-AI/datasets/manifests/manifest.json',
  });

  /// Generates or updates the manifest based on the provided list of [AcquisitionFile].
  Future<void> generateManifest(List<AcquisitionFile> files) async {
    final List<Map<String, dynamic>> manifestEntries = [];

    for (final file in files) {
      final checksum = await _calculateChecksum(File(file.path));

      manifestEntries.add({
        'class': file.classLevel,
        'subject': file.subject,
        'chapter': file.chapterIndex,
        'source_filename': file.name,
        'checksum': checksum,
        'page_count': 0, // Placeholder, updated during PDF processing
        'import_date': DateTime.now().toIso8601String(),
        'processing_status': 'Ingested',
        'path': p.relative(file.path, from: 'D:/GURUKUL-AI/datasets/'),
      });
    }

    final manifestFile = File(manifestPath);
    await manifestFile.create(recursive: true);
    final encoder = JsonEncoder.withIndent('  ');
    await manifestFile.writeAsString(encoder.convert({
      'generated_at': DateTime.now().toIso8601String(),
      'total_files': manifestEntries.length,
      'entries': manifestEntries,
    }));
  }

  Future<String> _calculateChecksum(File file) async {
    try {
      final bytes = await file.readAsBytes();
      return md5.convert(bytes).toString();
    } catch (e) {
      return 'error';
    }
  }
}
