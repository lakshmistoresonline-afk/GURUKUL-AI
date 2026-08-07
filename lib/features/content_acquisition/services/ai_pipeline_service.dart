import 'dart:convert';
import 'dart:io';
import 'package:path/path.dart' as p;
import '../../curriculum/domain/models/concept_node.dart';
import '../../content/data/modular_lesson_generator.dart';

/// Service responsible for orchestrating the AI enrichment pipeline.
/// It processes ConceptNodes to generate summaries, quizzes, flashcards,
/// revision notes, mindmaps, and embeddings using Gemini AI.
class AIPipelineService {
  final String _baseDir = 'datasets/processed';
  final ModularLessonGenerator _generator;

  AIPipelineService(this._generator);

  /// Runs the full AI pipeline for a given [ConceptNode].
  /// Returns a new [ConceptNode] enriched with generated content and references.
  Future<ConceptNode> process(ConceptNode node) async {
    // Execute enrichment tasks asynchronously using the real generator
    final results = await Future.wait([
      _generateSummaryReal(node),
      _generator.generateQuizzes(topic: node.topic),
      _generator.generateFlashcards(topic: node.topic),
      _generator.generateImportantNotes(topic: node.topic),
      _generator.generateMindMapMarkdown(topic: node.topic),
      _generateEmbeddings(node), // Still mocked for now
    ]);

    final summaryData = results[0] as Map<String, dynamic>;
    final quizData = results[1] as List<PracticeExercise>;
    final flashcardData = results[2] as List<Flashcard>;
    final revisionNotes = results[3] as String;
    final mindmapContent = results[4] as String;
    final embeddingsPath = results[5] as String;

    // Save generated artifacts to disk
    await _saveData('quizzes', node.id, quizData.map((e) => e.toMap()).toList());
    await _saveData('flashcards', node.id, flashcardData.map((f) => f.toMap()).toList());
    await _saveData('revision_notes', node.id, {'notes': revisionNotes});
    final mindmapPath = await _saveData('mindmaps', node.id, {'markdown': mindmapContent});

    // Return the updated ConceptNode with enriched data and references
    return ConceptNode(
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
      learningObjectives: node.learningObjectives,
      examples: node.examples,
      misconceptions: node.misconceptions,
      practiceExercises: quizData,
      flashcards: flashcardData,
      revisionNotes: revisionNotes,
      mindMapUrl: mindmapPath,
      commonMistakes: node.commonMistakes,
      vocabulary: node.vocabulary,
      interactiveActivities: node.interactiveActivities,
      masteryCheckpoints: node.masteryCheckpoints,
      introduction: summaryData['intro'] as String? ?? node.introduction,
      realLifeConnection: node.realLifeConnection,
      storyBasedExplanation: node.storyBasedExplanation,
      childFriendlyExplanation: node.childFriendlyExplanation,
      teacherExplanation: node.teacherExplanation,
      animatedLessonAsset: node.animatedLessonAsset,
      videoUrl: node.videoUrl,
      activities: node.activities,
      handsOnActivities: node.handsOnActivities,
      animationScript: node.animationScript,
      videoScript: node.videoScript,
      parentNotes: node.parentNotes,
      teacherNotes: node.teacherNotes,
      learningOutcomes: node.learningOutcomes,
      keyTakeaways: (summaryData['key_takeaways'] as List?)?.cast<String>() ?? node.keyTakeaways,
      faqs: node.faqs,
      importantNotes: node.importantNotes,
      socraticPrompts: node.socraticPrompts,
      illustrationPrompts: node.illustrationPrompts,
      status: 'Processed',
      generationMetadata: {
        ...Map<String, dynamic>.from(node.generationMetadata),
        'last_processed': DateTime.now().toIso8601String(),
        'summary_file': summaryData['file_path'],
        'quiz_file': p.join(_baseDir, 'quizzes', '${node.id}.json'),
        'flashcards_file': p.join(_baseDir, 'flashcards', '${node.id}.json'),
        'revision_notes_file': p.join(_baseDir, 'revision_notes', '${node.id}.json'),
        'mindmap_file': mindmapPath,
        'embeddings_file': embeddingsPath,
      },
    );
  }

  /// Generates a summary using the real AI generator.
  Future<Map<String, dynamic>> _generateSummaryReal(ConceptNode node) async {
    final keyTakeaways = await _generator.generateKeyTakeaways(topic: node.topic);
    final data = {
      'intro': 'Overview of ${node.topic}: Essential concepts in ${node.subject} for Class ${node.classLevel}.',
      'key_takeaways': keyTakeaways,
      'full_content': 'Extracted from source textbook material.'
    };
    final path = await _saveData('summaries', node.id, data);
    return {...data, 'file_path': path};
  }

  /// Mocks the generation of embeddings and saves them to the embeddings directory.
  Future<String> _generateEmbeddings(ConceptNode node) async {
    await Future.delayed(const Duration(milliseconds: 400));
    // Simulated 1536-dimensional embedding vector
    final vector = List.generate(1536, (i) => (i * 0.001));
    return await _saveData('embeddings', node.id, {'vector': vector, 'model': 'text-embedding-004'});
  }

  /// Helper to save data as JSON and return the file path.
  Future<String> _saveData(String subDir, String id, dynamic data) async {
    final dirPath = p.join(_baseDir, subDir);
    final directory = Directory(dirPath);
    if (!await directory.exists()) {
      await directory.create(recursive: true);
    }
    final file = File(p.join(dirPath, '$id.json'));
    await file.writeAsString(const JsonEncoder.withIndent('  ').convert(data));
    return file.path;
  }
}
