import 'dart:io';
import 'package:hive/hive.dart';
import '../domain/models/concept_node.dart';
import '../../../../core/content/repository_scanner.dart';
import '../../../../core/utils/content_generator.dart';

class FrameworkRepository {
  static const String _frameworkBox = 'framework_cache';
  late final RepositoryScanner _scanner;
  Map<String, dynamic> _framework = {};

  Future<void> init() async {
    await Hive.openBox(_frameworkBox);
    // In production, this path would be determined dynamically
    // For now, we use the local project path
    final root = 'D:/GURUKUL-AI/content_repository';
    _scanner = RepositoryScanner(rootPath: root);
    await refresh();
  }

  Future<void> refresh() async {
    _framework = await _scanner.scanCurriculum();
    final box = Hive.box(_frameworkBox);
    await box.put('full_framework', _framework);
  }

  Future<List<String>> getSubjects(int classLevel) async {
    final classKey = 'class${classLevel.toString().padLeft(2, '0')}';
    if (_framework.containsKey(classKey)) {
      return (_framework[classKey] as Map<String, dynamic>).keys.toList();
    }
    return [];
  }

  Future<List<Map<String, dynamic>>> getChapters(int classLevel, String subject) async {
    final classKey = 'class${classLevel.toString().padLeft(2, '0')}';
    if (_framework.containsKey(classKey) && (_framework[classKey] as Map<String, dynamic>).containsKey(subject)) {
      return List<Map<String, dynamic>>.from(_framework[classKey][subject] as Iterable);
    }
    return [];
  }

  Future<Map<String, dynamic>?> getChapterDetails(String chapterId) async {
    for (var classLevel in _framework.values) {
      for (var subjectChapters in classLevel.values) {
        for (var chapter in subjectChapters) {
          if (chapter['id'] == chapterId) {
            return Map<String, dynamic>.from(chapter);
          }
        }
      }
    }
    return null;
  }

  Future<List<Map<String, dynamic>>> getAllChapters(int classLevel) async {
    final classKey = 'class${classLevel.toString().padLeft(2, '0')}';
    final framework = _framework[classKey] as Map<String, dynamic>?;
    List<Map<String, dynamic>> all = [];
    framework?.forEach((subject, chapters) {
      for (var c in chapters) {
        all.add({...c, 'subject': subject});
      }
    });
    return all;
  }

  Future<ConceptNode?> getConceptNode(String conceptId) async {
    // 1. Check in Hive for dynamic/imported content overrides
    final dynamicBox = await Hive.openBox('dynamic_content');
    if (dynamicBox.containsKey(conceptId)) {
       final data = Map<String, dynamic>.from(dynamicBox.get(conceptId));
       return ConceptNode.fromMap(data);
    }

    // 2. Scan the repository for the specific concept node
    // Extract class and subject from ID if possible, or search
    // For simplicity, we search all chapters in the loaded framework to find class/subject
    String? foundClass;
    String? foundSubject;

    for (var classKey in _framework.keys) {
      final subjects = _framework[classKey] as Map<String, dynamic>;
      for (var subject in subjects.keys) {
        final chapters = subjects[subject] as List;
        if (chapters.any((c) => c['id'] == conceptId)) {
          foundClass = classKey.replaceAll('class', '');
          foundSubject = subject;
          break;
        }
      }
      if (foundClass != null) break;
    }

    if (foundClass != null && foundSubject != null) {
      final data = await _scanner.getChapterDetails(foundClass, foundSubject, conceptId);
      if (data != null) {
        return ConceptNode.fromMap(data);
      }
    }

    return null;
  }

  Future<void> saveConceptNode(ConceptNode node) async {
    // 1. Update dynamic cache in Hive
    final dynamicBox = await Hive.openBox('dynamic_content');
    await dynamicBox.put(node.id, node.toMap());

    // 2. Persist to local Content Repository if possible
    final foundClass = node.classLevel.toString().padLeft(2, '0');
    final chapterFolderSuffix = node.id.split('_').last;
    final chapterDir = 'D:/GURUKUL-AI/content_repository/curriculum/class_$foundClass/${node.subject.toLowerCase()}/chapters/chapter_$chapterFolderSuffix';

    final dir = Directory(chapterDir);
    if (await dir.exists()) {
      final lessonFile = File('${dir.path}/lesson.json');
      await lessonFile.writeAsString(JsonEncoder.withIndent('  ').convert(node.toMap()));

      // Also update split files
      await File('${dir.path}/quiz.json').writeAsString(jsonEncode(node.practiceExercises.map((e) => e.toMap()).toList()));
      await File('${dir.path}/flashcards.json').writeAsString(jsonEncode(node.flashcards.map((f) => f.toMap()).toList()));
      await File('${dir.path}/objectives.json').writeAsString(jsonEncode(node.learningObjectives));

      debugPrint('FrameworkRepository: Saved chapter ${node.id} to repository.');
    } else {
      debugPrint('FrameworkRepository: Chapter directory not found at $chapterDir. Only saved to Hive.');
    }
  }

  Future<Map<String, dynamic>> getRepositoryHealth() async {
    return await _scanner.generateHealthReport();
  }
}

