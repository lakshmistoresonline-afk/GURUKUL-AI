import 'dart:io';
import 'package:path/path.dart' as p;
import 'package:crypto/crypto.dart';
import '../models/acquisition_file.dart';

/// Service responsible for scanning the NCERT repository and extracting file metadata.
class RepositoryScannerService {
  final String rootDirectory;

  RepositoryScannerService({
    this.rootDirectory = 'D:/GURUKUL-AI/datasets/ncert_source/',
  });

  /// Generates a repository index and statistics.
  Future<Map<String, dynamic>> getRepositoryStats() async {
    final files = await scan();
    final Map<int, int> classCount = {};
    final Map<String, int> subjectCount = {};
    final Map<String, int> extensionCount = {};
    int totalSize = 0;

    for (final file in files) {
      subjectCount[file.subject] = (subjectCount[file.subject] ?? 0) + 1;
      classCount[file.classLevel] = (classCount[file.classLevel] ?? 0) + 1;
      extensionCount[file.extension] = (extensionCount[file.extension] ?? 0) + 1;
      totalSize += file.size;
    }

    return {
      'total_files': files.length,
      'total_size_bytes': totalSize,
      'class_distribution': classCount,
      'subject_distribution': subjectCount,
      'format_distribution': extensionCount,
    };
  }

  /// Scans the [rootDirectory] and returns a list of [AcquisitionFile] objects.
  Future<List<AcquisitionFile>> scan() async {
    final List<AcquisitionFile> acquisitionFiles = [];
    final dir = Directory(rootDirectory);

    if (!await dir.exists()) {
      return [];
    }

    try {
      final List<FileSystemEntity> entities = await dir.list(recursive: true).toList();

      for (final entity in entities) {
        if (entity is File) {
          final acqFile = _processFile(entity);
          if (acqFile != null) {
            acquisitionFiles.add(acqFile);
          }
        }
      }
    } catch (e) {
      rethrow;
    }

    return acquisitionFiles;
  }

  AcquisitionFile? _processFile(File file) {
    final String filePath = file.path;
    final String extension = p.extension(filePath).toLowerCase();

    if (!_isSupported(extension)) return null;

    final String relativePath = p.relative(filePath, from: rootDirectory);
    final List<String> parts = p.split(relativePath);

    if (parts.length < 3) return null;

    final String classFolder = parts[0];
    final String subjectFolder = parts[1];
    final String fileName = parts.last;

    final int? classLevel = _extractClassLevel(classFolder);
    if (classLevel == null) return null;

    final String subject = subjectFolder.toLowerCase();

    if (!_isPlacementValid(fileName, subject)) {
      return null;
    }

    final int chapterIndex = _extractChapterIndex(fileName);
    final String checksum = md5.convert(file.readAsBytesSync()).toString();

    return AcquisitionFile(
      path: filePath,
      name: fileName,
      extension: extension,
      size: file.lengthSync(),
      classLevel: classLevel,
      subject: subject,
      chapterIndex: chapterIndex,
      checksum: checksum,
    );
  }

  bool _isSupported(String ext) {
    const supported = {'.pdf', '.epub', '.docx', '.zip', '.jpg', '.jpeg', '.png', '.webp', '.bmp'};
    return supported.contains(ext);
  }

  int? _extractClassLevel(String folderName) {
    final match = RegExp(r'class_(\d+)').firstMatch(folderName.toLowerCase());
    if (match != null) {
      return int.tryParse(match.group(1)!);
    }
    return null;
  }

  int _extractChapterIndex(String fileName) {
    final patterns = [
      RegExp(r'(?:ch|chapter|unit)[\s_]*(\d+)', caseSensitive: false),
      RegExp(r'^(\d+)[\s_-]', caseSensitive: false),
    ];

    for (final regex in patterns) {
      final match = regex.firstMatch(fileName);
      if (match != null) {
        return int.tryParse(match.group(1)!) ?? 0;
      }
    }
    return 0;
  }

  bool _isPlacementValid(String fileName, String subject) {
    final name = fileName.toLowerCase();
    final sub = subject.toLowerCase();

    final Map<String, List<String>> validationRules = {
      'english': ['science', 'math', 'evs', 'hindi', 'history', 'geography'],
      'hindi': ['science', 'math', 'english', 'evs', 'sanskrit'],
      'mathematics': ['english', 'hindi', 'history', 'geography', 'science'],
      'science': ['english', 'hindi', 'history', 'geography', 'social'],
      'evs': ['english', 'hindi', 'mathematics'],
    };

    if (validationRules.containsKey(sub)) {
      for (final forbidden in validationRules[sub]!) {
        if (name.contains(forbidden)) {
          return false;
        }
      }
    }

    return true;
  }
}
