import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:archive/archive.dart';
import 'package:path/path.dart' as p;

class DownloadManager {
  Future<String> getLocalPath(String fileName) async {
    final directory = await getApplicationDocumentsDirectory();
    return p.join(directory.path, 'downloads', fileName);
  }

  Future<String> getExtractionPath(String contentId) async {
    final directory = await getApplicationDocumentsDirectory();
    return p.join(directory.path, 'content', contentId);
  }

  Future<void> downloadFile(String url, String fileName) async {
    // Implement file download logic with background support
    // After download completion, trigger extraction if it's a zip/ecar
    if (fileName.endsWith('.zip') || fileName.endsWith('.ecar')) {
      final zipPath = await getLocalPath(fileName);
      final contentId = p.basenameWithoutExtension(fileName);
      final targetDir = await getExtractionPath(contentId);
      await extractContent(zipPath, targetDir);
    }
  }

  Future<void> extractContent(String zipPath, String targetDir) async {
    final bytes = File(zipPath).readAsBytesSync();
    final archive = ZipDecoder().decodeBytes(bytes);

    for (final file in archive) {
      final filename = file.name;
      if (file.isFile) {
        final data = file.content as List<int>;
        File(p.join(targetDir, filename))
          ..createSync(recursive: true)
          ..writeAsBytesSync(data);
      } else {
        Directory(p.join(targetDir, filename)).createSync(recursive: true);
      }
    }
  }

  Future<bool> isFileAvailable(String fileName) async {
    final path = await getLocalPath(fileName);
    return File(path).exists();
  }
}
