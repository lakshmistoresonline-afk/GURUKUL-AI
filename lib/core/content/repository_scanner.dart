import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as p;

class RepositoryScanner {
  final String rootPath;

  RepositoryScanner({required this.rootPath});

  Future<Map<String, dynamic>> scanCurriculum() async {
    if (kIsWeb) {
      return _scanCurriculumFromAssets();
    }

    final Map<String, dynamic> framework = {};
    final curriculumDir = Directory(rootPath);

    if (!await curriculumDir.exists()) {
      debugPrint('RepositoryScanner: Curriculum directory not found at ${curriculumDir.path}');
      return framework;
    }

    final classDirs = curriculumDir.listSync().whereType<Directory>();
    for (var classDir in classDirs) {
      final className = p.basename(classDir.path).replaceAll('_', ''); // class_05 -> class05
      framework[className] = <String, dynamic>{};

      final subjectDirs = classDir.listSync().whereType<Directory>();
      for (var subjectDir in subjectDirs) {
        final subjectName = _capitalize(p.basename(subjectDir.path));
        framework[className][subjectName] = <dynamic>[];

        final chaptersDir = Directory(p.join(subjectDir.path, 'chapters'));
        if (await chaptersDir.exists()) {
          final chapterDirs = chaptersDir.listSync().whereType<Directory>().toList()
            ..sort((a, b) => p.basename(a.path).compareTo(p.basename(b.path)));

          for (var chapterDir in chapterDirs) {
            final metadataFile = File(p.join(chapterDir.path, 'metadata.json'));
            if (await metadataFile.exists()) {
              final metadata = jsonDecode(await metadataFile.readAsString());
              framework[className][subjectName].add(metadata);
            }
          }
        }
      }
    }
    return framework;
  }

  Future<Map<String, dynamic>?> getChapterDetails(String classLevel, String subject, String chapterId) async {
    final classDirName = 'class_${classLevel.padLeft(2, '0')}';
    final chapterFolderSuffix = chapterId.split('_').last;
    final relativePath = 'datasets/processed/chapters/$classDirName/${subject.toLowerCase()}/chapters/chapter_$chapterFolderSuffix/lesson.json';

    if (kIsWeb) {
      try {
        final String content = await rootBundle.loadString(relativePath);
        return jsonDecode(content);
      } catch (e) {
        debugPrint('RepositoryScanner: Error loading chapter details from assets ($relativePath): $e');
        return null;
      }
    }

    final path = p.join(rootPath, classDirName, subject.toLowerCase(), 'chapters', 'chapter_$chapterFolderSuffix', 'lesson.json');
    final file = File(path);
    if (await file.exists()) {
      return jsonDecode(await file.readAsString());
    }
    return null;
  }

  Future<Map<String, dynamic>> generateHealthReport() async {
    int totalLessons = 0;
    int missingMetadata = 0;
    int missingMedia = 0;
    List<String> brokenReferences = [];

    final curriculumDir = Directory(rootPath);
    if (await curriculumDir.exists()) {
      final allFiles = curriculumDir.listSync(recursive: true);
      for (var entity in allFiles) {
        if (entity is Directory && p.basename(entity.path).startsWith('chapter_')) {
          totalLessons++;
          final metadata = File(p.join(entity.path, 'metadata.json'));
          if (!await metadata.exists()) missingMetadata++;

          final lesson = File(p.join(entity.path, 'lesson.json'));
          if (await lesson.exists()) {
            final data = jsonDecode(await lesson.readAsString());
            if (data['animatedLessonAsset'] == null || data['animatedLessonAsset'].isEmpty) {
              missingMedia++;
            }
          }
        }
      }
    }

    return {
      'healthScore': totalLessons > 0 ? ((totalLessons - (missingMetadata + missingMedia)) / totalLessons * 100).round() : 0,
      'totalLessons': totalLessons,
      'missingMetadata': missingMetadata,
      'missingMedia': missingMedia,
      'brokenReferences': brokenReferences,
    };
  }

  String _capitalize(String s) => s.isEmpty ? s : s[0].toUpperCase() + s.substring(1);

  Future<Map<String, dynamic>> _scanCurriculumFromAssets() async {
    final Map<String, dynamic> framework = {};
    try {
      final String manifestStr = await rootBundle.loadString('datasets/manifests/manifest.json');
      final decoded = jsonDecode(manifestStr);
      final List manifest = decoded is List ? decoded : [];

      for (var entry in manifest) {
        final String classId = entry['class'];
        final String subject = entry['subject'];
        final String classKey = 'class${classId.padLeft(2, '0')}';

        if (!framework.containsKey(classKey)) framework[classKey] = <String, dynamic>{};
        if (!framework[classKey].containsKey(subject)) framework[classKey][subject] = <dynamic>[];

        framework[classKey][subject].add(<String, dynamic>{
          'id': entry['id'],
          'title': entry['title'],
          'subject': subject,
          'classLevel': int.parse(classId),
        });
      }
    } catch (e) {
      debugPrint('RepositoryScanner: Error loading manifest from assets: $e');
      // Fallback for demo if manifest is missing or empty
      if (framework.isEmpty) {
        framework['class05'] = {
          'Mathematics': [{'id': 'm5_c1', 'title': 'The Fish Tale', 'subject': 'Mathematics', 'classLevel': 5}],
          'EVS': [{'id': 'e5_c1', 'title': 'Super Senses', 'subject': 'EVS', 'classLevel': 5}],
        };
      }
    }
    return framework;
  }
}
