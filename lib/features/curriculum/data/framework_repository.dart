import 'package:hive/hive.dart';
import '../domain/models/concept_node.dart';
import 'ncert_framework_v1.dart';
import 'ncert_detailed_content.dart';

class FrameworkRepository {
  static const String _frameworkBox = 'framework_cache';

  Future<void> init() async {
    await Hive.openBox(_frameworkBox);
  }

  Future<List<String>> getSubjects(int classLevel) async {
    final box = Hive.box(_frameworkBox);
    final cacheKey = 'subjects_$classLevel';

    if (box.containsKey(cacheKey)) {
      return List<String>.from(box.get(cacheKey));
    }

    final classKey = 'class$classLevel';
    if (ncertFramework.containsKey(classKey)) {
      final subjects = ncertFramework[classKey]!.keys.toList();
      await box.put(cacheKey, subjects);
      return subjects;
    }
    return [];
  }

  Future<List<Map<String, dynamic>>> getChapters(int classLevel, String subject) async {
    final box = Hive.box(_frameworkBox);
    final cacheKey = 'chapters_${classLevel}_$subject';

    if (box.containsKey(cacheKey)) {
      final cached = box.get(cacheKey);
      return (cached as List).map((item) => Map<String, dynamic>.from(item)).toList();
    }

    final classKey = 'class$classLevel';
    if (ncertFramework.containsKey(classKey) && ncertFramework[classKey]!.containsKey(subject)) {
      final chapters = List<Map<String, dynamic>>.from(ncertFramework[classKey]![subject] as Iterable);
      await box.put(cacheKey, chapters);
      return chapters;
    }
    return [];
  }

  Future<Map<String, dynamic>?> getChapterDetails(String chapterId) async {
    // This would typically fetch from a local database or remote API
    // For now, we search the static map
    for (var classLevel in ncertFramework.values) {
      for (var subjectChapters in classLevel.values) {
        for (var chapter in subjectChapters) {
          if (chapter['id'] == chapterId) {
            return chapter;
          }
        }
      }
    }
    return null;
  }

  Future<ConceptNode?> getConceptNode(String conceptId) async {
    // Returns detailed metadata for a concept/chapter
    return ncertDetailedContent[conceptId];
  }
}
