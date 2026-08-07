import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import '../../curriculum/data/framework_repository.dart';
import '../../curriculum/domain/models/concept_node.dart';
import 'modular_lesson_generator.dart';
import '../../../../core/di/injection.dart';

enum BatchJobStatus { idle, running, paused, completed, failed }

class BatchJobProgress {
  final String id;
  final String title;
  final int totalChapters;
  int completedChapters;
  BatchJobStatus status;
  String currentChapter;
  List<String> logs;

  BatchJobProgress({
    required this.id,
    required this.title,
    required this.totalChapters,
    this.completedChapters = 0,
    this.status = BatchJobStatus.idle,
    this.currentChapter = '',
    this.logs = const [],
  });

  double get percentage => totalChapters > 0 ? completedChapters / totalChapters : 0;
}

class AiBatchFactoryService {
  final ModularLessonGenerator _generator;
  final FrameworkRepository _repository;

  BatchJobProgress? _currentJob;
  StreamController<BatchJobProgress>? _progressController;

  AiBatchFactoryService(this._generator, this._repository);

  Stream<BatchJobProgress>? get progressStream => _progressController?.stream;
  BatchJobProgress? get currentJob => _currentJob;

  Future<void> startBatchGeneration({
    required String scope, // class_05, m5_math, m5_c1
    bool regenerate = false,
  }) async {
    if (_currentJob?.status == BatchJobStatus.running) return;

    _progressController ??= StreamController<BatchJobProgress>.broadcast();

    // 1. Identify chapters to process
    List<Map<String, dynamic>> targetChapters = [];
    String title = '';

    if (scope.startsWith('class_')) {
      final level = int.parse(scope.split('_')[1]);
      targetChapters = await _repository.getAllChapters(level);
      title = 'Entire Class $level Generation';
    } else if (scope.contains('_')) {
       // Assuming subject_id or chapter_id
       // For simplicity, we search in all Class 5/6
       final all5 = await _repository.getAllChapters(5);
       final all6 = await _repository.getAllChapters(6);
       final all = [...all5, ...all6];

       if (scope.endsWith('_c1') || scope.contains('_c')) { // Individual chapter
         targetChapters = all.where((c) => c['id'] == scope).toList();
         title = 'Chapter $scope Generation';
       } else { // Entire Subject
         targetChapters = all.where((c) => c['id'].startsWith(scope.substring(0, 1))).toList();
         title = 'Subject $scope Generation';
       }
    }

    _currentJob = BatchJobProgress(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      title: title,
      totalChapters: targetChapters.length,
      status: BatchJobStatus.running,
      logs: ['Starting job for $scope...'],
    );
    _progressController?.add(_currentJob!);

    // 2. Process each chapter
    for (var chapter in targetChapters) {
      if (_currentJob?.status == BatchJobStatus.paused) break;

      final chapterId = chapter['id'];
      _currentJob!.currentChapter = chapter['title'];
      _currentJob!.logs.insert(0, 'Processing $chapterId: ${chapter['title']}...');
      _progressController?.add(_currentJob!);

      try {
        final existing = await _repository.getConceptNode(chapterId);

        if (existing != null && existing.introduction.isNotEmpty && !regenerate) {
          _currentJob!.logs.insert(0, 'Skipping $chapterId (Already Enriched)');
        } else {
          await _enrichChapter(chapterId, chapter['title'], chapter['subject'], chapter['classLevel']);
          _currentJob!.logs.insert(0, 'Successfully Enriched $chapterId');
        }

        _currentJob!.completedChapters++;
      } catch (e) {
        _currentJob!.logs.insert(0, 'Error processing $chapterId: $e');
      }

      _progressController?.add(_currentJob!);
      // Avoid rate limiting
      await Future.delayed(const Duration(seconds: 1));
    }

    _currentJob!.status = BatchJobStatus.completed;
    _progressController?.add(_currentJob!);
  }

  Future<void> _enrichChapter(String id, String title, String subject, int classLevel) async {
    // Generate all components
    final outcomes = ['Understand $title', 'Apply $title in real life'];

    final story = await _generator.generateStory(topic: title, outcomes: outcomes);
    final teacherExp = await _generator.generateTeacherExplanation(topic: title, outcomes: outcomes);
    final childExp = await _generator.generateChildExplanation(topic: title);
    final flashcards = await _generator.generateFlashcards(topic: title);
    final quizzes = await _generator.generateQuizzes(topic: title);
    final activities = await _generator.generateActivities(topic: title);
    final takeaways = await _generator.generateKeyTakeaways(topic: title);
    final faqs = await _generator.generateFAQs(topic: title);
    final socratic = await _generator.generateSocraticPrompts(topic: title);
    final illustrationPrompts = await _generator.generateIllustrationPrompts(topic: title);
    final animationScript = await _generator.generateAnimationScript(topic: title);
    final prerequisites = await _generator.generatePrerequisites(topic: title);
    final importantNotes = await _generator.generateImportantNotes(topic: title);

    final node = ConceptNode(
      id: id,
      subject: subject,
      classLevel: classLevel,
      chapter: title,
      topic: title,
      subtopic: '',
      difficulty: Difficulty.intermediate,
      bloomLevel: BloomLevel.understand,
      examWeightage: 5,
      estStudyTime: const Duration(minutes: 45),
      prerequisites: prerequisites,
      dependencies: [],
      relatedConcepts: [],
      learningObjectives: outcomes,
      examples: [],
      misconceptions: [],
      practiceExercises: quizzes,
      flashcards: flashcards,
      activities: activities,
      keyTakeaways: takeaways,
      faqs: faqs,
      socraticPrompts: socratic,
      illustrationPrompts: illustrationPrompts,
      introduction: story.substring(0, story.length > 500 ? 500 : story.length), // Just a snippet
      storyBasedExplanation: story,
      teacherExplanation: teacherExp,
      childFriendlyExplanation: childExp,
      revisionNotes: importantNotes,
      animationScript: animationScript,
      status: 'AI Review',
      generationMetadata: {
        'date': DateTime.now().toIso8601String(),
        'model': 'gemini-1.5-flash',
        'phase': 56,
      }
    );

    await _repository.saveConceptNode(node);
  }

  void pauseJob() {
    if (_currentJob != null) {
      _currentJob!.status = BatchJobStatus.paused;
      _progressController?.add(_currentJob!);
    }
  }

  void resumeJob() {
     // Re-trigger the main loop logic (needs slight refactor of startBatch to handle resume)
  }
}
