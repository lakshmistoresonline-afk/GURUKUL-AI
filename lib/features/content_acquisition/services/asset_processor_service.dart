import 'dart:convert';
import 'dart:io';
import 'package:path/path.dart' as p;
import '../models/extraction_result.dart';

/// Service responsible for processing and organizing assets (images, tables)
/// extracted from educational content during the acquisition phase.
class AssetProcessorService {
  final String _imagePath = 'datasets/assets/images/';
  final String _diagramPath = 'datasets/assets/diagrams/';
  final String _tablePath = 'datasets/assets/tables/';
  final String _figurePath = 'datasets/assets/figures/';

  /// Processes extracted images and tables from an [ExtractionResult].
  ///
  /// This method:
  /// 1. Iterates through extracted images, renames them using a standard convention,
  ///    and moves/copies them to the appropriate directory (images or diagrams).
  /// 2. Saves table data as structured JSON files.
  /// 3. Returns a map of original references to their new storage paths.
  Future<Map<String, String>> processAssets(
    String chapterId,
    ExtractionResult extraction,
  ) async {
    final Map<String, String> assetMap = {};

    // 1. Process Extracted Images
    for (int i = 0; i < extraction.images.length; i++) {
      final oldPath = extraction.images[i];
      final extension = p.extension(oldPath).isEmpty ? '.png' : p.extension(oldPath);

      // Requirement: Renaming convention [chapter_id]_img_[index].png
      final newName = '${chapterId}_img_${i + 1}$extension';

      // Determine target directory based on image type (heuristic)
      final isDiagram = oldPath.toLowerCase().contains('diagram') ||
                        oldPath.toLowerCase().contains('chart') ||
                        oldPath.toLowerCase().contains('graph');

      final targetDir = isDiagram ? _diagramPath : _imagePath;
      final newPath = p.join(targetDir, newName);

      try {
        await _handleAssetFile(oldPath, newPath);
        assetMap[oldPath] = newPath;
      } catch (e) {
        stderr.writeln('Error processing image $oldPath: $e');
      }
    }

    // 2. Process Extracted Tables
    // Note: ExtractionResult.tables is List<List<String>> (a single table's rows).
    if (extraction.tables.isNotEmpty) {
      final tableName = '${chapterId}_table_1.json';
      final newPath = p.join(_tablePath, tableName);

      try {
        await _saveTableAsJson(extraction.tables, newPath);
        // Using a logical reference for the table since it doesn't have an "old path"
        assetMap['table_0'] = newPath;
      } catch (e) {
        stderr.writeln('Error processing table data: $e');
      }
    }

    return assetMap;
  }

  /// Copies an asset file to its new destination, ensuring the target directory exists.
  Future<void> _handleAssetFile(String sourcePath, String targetPath) async {
    final sourceFile = File(sourcePath);

    // In simulation environments, the source path might not point to a real file.
    // We check existence to avoid throwing errors during mock runs.
    if (!await sourceFile.exists()) {
      return;
    }

    final targetFile = File(targetPath);
    if (!await targetFile.parent.exists()) {
      await targetFile.parent.create(recursive: true);
    }

    // Using copy to preserve the original extraction artifact for auditing
    await sourceFile.copy(targetPath);
  }

  /// Serializes table row data into a structured JSON file.
  Future<void> _saveTableAsJson(List<List<String>> tableData, String targetPath) async {
    final targetFile = File(targetPath);
    if (!await targetFile.parent.exists()) {
      await targetFile.parent.create(recursive: true);
    }

    const encoder = JsonEncoder.withIndent('  ');
    final Map<String, dynamic> tableJson = {
      'metadata': {
        'source': 'extraction',
        'rowCount': tableData.length,
        'columnCount': tableData.isNotEmpty ? tableData.first.length : 0,
        'createdAt': DateTime.now().toIso8601String(),
      },
      'data': tableData,
    };

    await targetFile.writeAsString(encoder.convert(tableJson));
  }
}
