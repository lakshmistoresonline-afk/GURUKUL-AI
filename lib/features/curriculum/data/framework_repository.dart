import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:project_gurukul_ai/core/content/repository_scanner.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/concept_node.dart';
import 'package:hive/hive.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/interactive_activity.dart';

class FrameworkRepository {
  final RepositoryScanner _scanner;
  late Box _frameworkCache;
  Map<String, dynamic> _framework = {};

  FrameworkRepository(this._scanner);

  Future<void> init() async {
    _frameworkCache = await Hive.openBox('framework_cache');
    await refresh();
  }

  Future<void> refresh() async {
    final data = await _scanner.scanCurriculum();
    _framework = data;
    await _frameworkCache.put('master_framework', data);
  }

  Future<List<int>> getClasses() async {
    final List<int> levels = [];
    for (var key in _framework.keys) {
      if (key.startsWith('class')) {
        final level = int.tryParse(key.replaceAll('class', ''));
        if (level != null) levels.add(level);
      }
    }
    levels.sort();
    return levels;
  }

  Future<List<String>> getSubjects(int classLevel) async {
    final classKey = 'class${classLevel.toString().padLeft(2, '0')}';
    if (_framework.containsKey(classKey)) {
      return (_framework[classKey] as Map).keys.cast<String>().toList();
    }
    return [];
  }

  Future<List<Map<String, dynamic>>> getChapters(int classLevel, String subject) async {
    final classKey = 'class${classLevel.toString().padLeft(2, '0')}';
    if (_framework.containsKey(classKey)) {
      final subjects = _framework[classKey];
      if (subjects is Map && subjects.containsKey(subject)) {
        final chapters = subjects[subject] as List? ?? [];
        return chapters.map((c) => Map<String, dynamic>.from(c)).toList();
      }
    }
    return [];
  }

  Future<List<Map<String, dynamic>>> getAllChapters(int classLevel) async {
    final subjects = await getSubjects(classLevel);
    final List<Map<String, dynamic>> all = [];
    for (var s in subjects) {
      final chs = await getChapters(classLevel, s);
      all.addAll(chs.map((c) => {...c, 'subject': s}));
    }
    return all;
  }

  Future<ConceptNode?> getConceptNode(String conceptId) async {
    // Determine class and subject from ID if possible, or scan manifest
    String? foundClass;
    String? foundSubject;

    for (var classKey in _framework.keys) {
      final subjects = _framework[classKey];
      if (subjects is Map) {
        for (var subjectName in subjects.keys) {
          final chapters = subjects[subjectName] as List;
          if (chapters.any((c) => c['id'] == conceptId)) {
            foundClass = classKey.replaceAll('class', '');
            foundSubject = subjectName;
            break;
          }
        }
      }
      if (foundClass != null) break;
    }

    if (foundClass != null && foundSubject != null) {
      final data = await _scanner.getChapterDetails(foundClass, foundSubject, conceptId);
      if (data != null) {
        return ConceptNode.fromMap(data);
      } else if (kIsWeb) {
        // Fallback for demo when assets are tricky on Web
        return _generateFallbackNode(conceptId, foundClass, foundSubject);
      }
    }

    return null;
  }

  Future<Map<String, dynamic>?> getChapterDetails(String id) async {
    for (var classKey in _framework.keys) {
      final subjects = _framework[classKey];
      if (subjects is Map) {
        for (var subjectName in subjects.keys) {
          final chapters = subjects[subjectName] as List;
          final ch = chapters.firstWhere((c) => c['id'] == id, orElse: () => null);
          if (ch != null) return Map<String, dynamic>.from(ch);
        }
      }
    }
    return null;
  }

  Future<void> saveConceptNode(ConceptNode node) async {
    // This is primarily for AI generation flow.
    // In production, this might sync to Firestore or write to a local asset-linked folder.
    // For now, we'll cache it in Hive.
    final box = await Hive.openBox('concept_nodes');
    await box.put(node.id, node.toMap());
  }

  Future<Map<String, dynamic>> getRepositoryHealth() async {
    return _scanner.generateHealthReport();
  }

  ConceptNode _generateFallbackNode(String id, String classLevel, String subject) {
    String title = 'Chapter Detail';
    for (var classKey in _framework.keys) {
      final subjects = _framework[classKey];
      if (subjects is Map && subjects.containsKey(subject)) {
        final chapters = subjects[subject] as List? ?? [];
        final ch = chapters.firstWhere((c) => c['id'] == id, orElse: () => null);
        if (ch != null) title = ch['title'] ?? title;
      }
    }

    return ConceptNode(
      id: id,
      subject: subject,
      classLevel: int.tryParse(classLevel) ?? 5,
      chapter: title,
      topic: title,
      subtopic: 'General Overview',
      difficulty: Difficulty.beginner,
      bloomLevel: BloomLevel.understand,
      examWeightage: 5,
      estStudyTime: const Duration(minutes: 40),
      prerequisites: [],
      dependencies: [],
      relatedConcepts: [],
      learningObjectives: ['Understand the core concepts of $title', 'Apply learning to real-world scenarios'],
      examples: ['Example from $subject context'],
      misconceptions: [],
      practiceExercises: [
        const PracticeExercise(
          question: 'What is the main theme of this chapter?',
          options: ['Option A', 'Option B', 'Option C', 'Option D'],
          correctAnswer: 'Option A',
          hint: 'Think about the title.',
          explanation: 'This is a sample explanation for the chapter.',
        )
      ],
      flashcards: [
        const Flashcard(front: 'Key Term', back: 'Description of the term')
      ],
      revisionNotes: 'Key points for $title',
      commonMistakes: [],
      vocabulary: {},
      interactiveActivities: [],
      masteryCheckpoints: [],
      introduction: 'Welcome to $title.',
      realLifeConnection: 'This concept is used in everyday life.',
      storyBasedExplanation: 'Once upon a time, we explored $title...',
      childFriendlyExplanation: 'Let\'s learn $title in a fun way!',
      teacherExplanation: 'Formal NCERT curriculum explanation for $title.',
      animatedLessonAsset: '',
      activities: [],
      handsOnActivities: [],
      animationScript: '',
      videoScript: '',
      parentNotes: '',
      teacherNotes: '',
      learningOutcomes: 'Understand $title',
      keyTakeaways: [],
      faqs: {},
      importantNotes: '',
      socraticPrompts: [],
      illustrationPrompts: [],
      status: 'Fallback',
      generationMetadata: {},
    );
  }
}
