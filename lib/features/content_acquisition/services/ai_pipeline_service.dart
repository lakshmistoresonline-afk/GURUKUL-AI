import 'dart:convert';
import 'dart:io' as io;
import 'package:flutter/foundation.dart';
import 'package:path/path.dart' as p;
import 'package:sqflite/sqflite.dart';
import '../../curriculum/domain/models/concept_node.dart';
import '../../curriculum/domain/models/interactive_activity.dart';
import '../../content/data/modular_lesson_generator.dart';
import '../../../core/database/sqlite_service.dart';
import 'ai_validator_service.dart';

/// Production-grade AI Pipeline Service with incremental processing and validation.
class AIPipelineService {
  final String _baseDir = 'datasets/processed';
  final ModularLessonGenerator _generator;
  final SqliteService _db;
  final AIValidatorService _validator;

  AIPipelineService(this._generator, this._db, this._validator);

  /// Processes a [ConceptNode] through the AI Enrichment Pipeline.
  /// Supports incremental processing by checking checksums and automatic retry on failure.
  Future<ConceptNode> process(ConceptNode node, {String? targetDir, String? checksum, int maxRetries = 2}) async {
    // 1. Incremental Check
    if (checksum != null && await _isAlreadyProcessed(node.id, checksum)) {
      debugPrint('AI Pipeline: Skipping ${node.id} (Incremental)');
      return node;
    }

    int attempt = 0;
    while (attempt <= maxRetries) {
      try {
        debugPrint('AI Pipeline: Processing ${node.id} (Attempt ${attempt + 1})');

        // 2. Parallel Enrichment Tasks
        final results = await Future.wait([
          _generateSummary(node, targetDir: targetDir),
          _generator.generateQuizzes(topic: node.topic),
          _generator.generateFlashcards(topic: node.topic),
          _generator.generateImportantNotes(topic: node.topic),
          _generator.generateMindMapMarkdown(topic: node.topic),
          _generator.generateChildExplanation(topic: node.topic),
          _generator.generateTeacherExplanation(topic: node.topic, outcomes: node.learningObjectives),
          _generator.generateStory(topic: node.topic, outcomes: node.learningObjectives),
          _generator.generateActivities(topic: node.topic),
          _generator.generateTeacherNotes(topic: node.topic),
        ]);

        final summaryData = results[0] as Map<String, dynamic>;
        final quizData = results[1] as List<PracticeExercise>;
        final flashcardData = results[2] as List<Flashcard>;
        final revisionNotes = results[3] as String;
        final mindmapContent = results[4] as String;
        final childExplanation = results[5] as String;
        final teacherExplanation = results[6] as String;
        final storyExplanation = results[7] as String;
        final activities = results[8] as List<InteractiveActivity>;
        final gTeacherNotes = results[9] as String;

        // 5. Construct Enriched Node
        final enrichedNode = ConceptNode(
          id: node.id,
          subject: node.subject,
          classLevel: node.classLevel,
          chapter: node.chapter,
          topic: node.topic,
          subtopic: node.subtopic,
          difficulty: node.difficulty,
          bloomLevel: node.bloomLevel,
          examWeightage: node.examWeightage,
          estStudyTime: node.estStudyTime,
          prerequisites: node.prerequisites,
          dependencies: node.dependencies,
          relatedConcepts: node.relatedConcepts,
          learningObjectives: node.learningObjectives.isNotEmpty ? node.learningObjectives : (summaryData['key_takeaways'] as List?)?.cast<String>() ?? [],
          examples: node.examples,
          misconceptions: node.misconceptions,
          practiceExercises: quizData,
          flashcards: flashcardData,
          revisionNotes: revisionNotes,
          mindMapUrl: null, // Set after save
          commonMistakes: node.commonMistakes,
          vocabulary: node.vocabulary,
          interactiveActivities: node.interactiveActivities,
          masteryCheckpoints: node.masteryCheckpoints,
          introduction: summaryData['intro'] as String? ?? node.introduction,
          realLifeConnection: node.realLifeConnection,
          storyBasedExplanation: storyExplanation,
          childFriendlyExplanation: childExplanation,
          teacherExplanation: teacherExplanation,
          animatedLessonAsset: node.animatedLessonAsset,
          videoUrl: node.videoUrl,
          activities: activities,
          handsOnActivities: node.handsOnActivities,
          animationScript: node.animationScript,
          videoScript: node.videoScript,
          parentNotes: node.parentNotes,
          teacherNotes: gTeacherNotes,
          learningOutcomes: node.learningOutcomes,
          keyTakeaways: (summaryData['key_takeaways'] as List?)?.cast<String>() ?? node.keyTakeaways,
          faqs: node.faqs,
          importantNotes: revisionNotes,
          socraticPrompts: node.socraticPrompts,
          illustrationPrompts: node.illustrationPrompts,
          status: 'Processed',
          generationMetadata: {
            ...node.generationMetadata,
            'last_processed': DateTime.now().toIso8601String(),
            'checksum': checksum,
            // Quality score depends on the fully constructed node
          },
        );

        // Quality score check
        enrichedNode.generationMetadata['quality_score'] = _validator.calculateQualityScore(enrichedNode);

        // 3. Asset Persistence (Structured JSON)
        await _saveData('quizzes', node.id, quizData.map((e) => e.toMap()).toList(), targetDir: targetDir);
        await _saveData('flashcards', node.id, flashcardData.map((f) => f.toMap()).toList(), targetDir: targetDir);
        await _saveData('revision_notes', node.id, {'notes': revisionNotes}, targetDir: targetDir);
        final mindmapPath = await _saveData('mindmaps', node.id, {'markdown': mindmapContent}, targetDir: targetDir);

        // 6. Validation
        if (_validator.validate(enrichedNode)) {
          // 4. Update SQLite Tracking
          if (checksum != null) {
            await _updateProcessingStatus(node.id, checksum, 'Completed');
          }
          return enrichedNode;
        } else {
          debugPrint('AI Pipeline: Validation failed for ${node.id} (Attempt ${attempt + 1})');
          attempt++;
          if (attempt > maxRetries) {
             throw Exception('AI Pipeline: Max retries exceeded for ${node.id}');
          }
        }
      } catch (e) {
        debugPrint('AI Pipeline: Error processing ${node.id} - $e');
        attempt++;
        if (attempt > maxRetries) {
          if (checksum != null) {
            await _updateProcessingStatus(node.id, checksum, 'Failed');
          }
          rethrow;
        }
        await Future.delayed(const Duration(seconds: 2));
      }
    }
    throw Exception('AI Pipeline: Unexpected end of process loop for ${node.id}');
  }

  Future<Map<String, dynamic>> _generateSummary(ConceptNode node, {String? targetDir}) async {
    final keyTakeaways = await _generator.generateKeyTakeaways(topic: node.topic);
    final intro = await _generator.generateChildExplanation(topic: node.topic);

    final data = {
      'intro': intro,
      'key_takeaways': keyTakeaways,
      'full_content': 'Extracted and enriched from textbook material.'
    };
    final path = await _saveData('summaries', node.id, data, targetDir: targetDir);
    return {...data, 'file_path': path};
  }

  Future<bool> _isAlreadyProcessed(String id, String checksum) async {
    if (kIsWeb) return false;
    final db = await _db.database;
    final results = await db.query(
      'processing_queue',
      where: 'id = ? AND checksum = ? AND status = ?',
      whereArgs: [id, checksum, 'Completed'],
    );
    return results.isNotEmpty;
  }

  Future<void> _updateProcessingStatus(String id, String checksum, String status) async {
    if (kIsWeb) return;
    final db = await _db.database;
    await db.insert(
      'processing_queue',
      {
        'id': id,
        'checksum': checksum,
        'status': status,
        'updated_at': DateTime.now().toIso8601String(),
      },
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<String> _saveData(String subDir, String id, dynamic data, {String? targetDir}) async {
    final dirPath = targetDir ?? p.join(_baseDir, subDir);
    if (!kIsWeb) {
      final directory = io.Directory(dirPath);
      if (!await directory.exists()) {
        await directory.create(recursive: true);
      }
    }

    String fileName = '$id.json';
    if (targetDir != null) {
      if (subDir == 'quizzes') fileName = 'quiz.json';
      if (subDir == 'summaries') fileName = 'summary.json';
      if (subDir == 'flashcards') fileName = 'flashcards.json';
      if (subDir == 'revision_notes') fileName = 'revision_notes.json';
      if (subDir == 'mindmaps') fileName = 'mindmap.json';
    }

    final fullPath = p.join(dirPath, fileName);
    if (!kIsWeb) {
      final file = io.File(fullPath);
      await file.writeAsString(const JsonEncoder.withIndent('  ').convert(data));
    } else {
      debugPrint('AI Pipeline: Web environment detected. Skipping file save to $fullPath');
    }
    return fullPath;
  }
}
