import 'dart:convert';
import 'dart:io';
import 'package:path/path.dart' as p;
import '../../curriculum/domain/models/concept_node.dart';
import '../models/acquisition_file.dart';
import '../models/extraction_result.dart';

/// Service responsible for building structured [ConceptNode] objects from raw extractions.
class ChapterBuilderService {
  final String _basePath = 'datasets/processed/chapters';

  /// Takes an [AcquisitionFile] and its [ExtractionResult] to generate, structure, and save chapters.
  Future<List<ConceptNode>> buildChapters(
    AcquisitionFile file,
    ExtractionResult extraction,
  ) async {
    final List<ConceptNode> chapters = [];
    final boundaries = extraction.chapterBoundaries;
    final rawText = extraction.rawText;

    for (int i = 0; i < boundaries.length; i++) {
      // Calculate start and end offsets for the current chapter
      final start = boundaries[i];
      final end = (i + 1 < boundaries.length) ? boundaries[i + 1] : rawText.length;
      final chapterText = rawText.substring(start, end).trim();

      if (chapterText.isEmpty) continue;

      final chapterIndex = i + 1;
      final subjectSlug = file.subject.toLowerCase().replaceAll(' ', '_');

      // Requirement: Generate IDs (e.g. c5_math_ch1)
      final chapterId = 'c${file.classLevel}_${subjectSlug}_ch$chapterIndex';

      // Determine chapter title
      final title = _determineTitle(chapterText, chapterIndex);

      // Intelligent splitting for introduction, sections, and summary
      final sections = _splitIntoSections(chapterText);
      final introduction = sections.isNotEmpty ? sections.first : '';
      final summary = sections.length > 1 ? sections.last : '';
      final bodyContent = sections.length > 2
          ? sections.sublist(1, sections.length - 1).join('\n\n')
          : '';

      // Use extracted content
      final keywords = _extractKeywords(chapterText);

      // Construct the ConceptNode
      final node = ConceptNode(
        id: chapterId,
        subject: file.subject,
        classLevel: file.classLevel,
        chapter: title,
        topic: title,
        subtopic: '',
        difficulty: Difficulty.beginner,
        bloomLevel: BloomLevel.remember,
        examWeightage: 5,
        estStudyTime: const Duration(minutes: 60),
        prerequisites: [],
        dependencies: [],
        relatedConcepts: [],
        learningObjectives: [], // Populated by AI Pipeline
        examples: [],
        misconceptions: [],
        introduction: introduction,
        teacherExplanation: bodyContent,
        revisionNotes: summary,
        practiceExercises: [], // Populated by AI Pipeline
        flashcards: [], // Populated by AI Pipeline
        keyTakeaways: keywords,
        status: 'Extracted',
        generationMetadata: {
          'sourceFile': file.name,
          'chapterIndex': chapterIndex,
          'processedAt': DateTime.now().toIso8601String(),
        },
      );

      chapters.add(node);

      // Requirement: Save to datasets/processed/chapters/class_XX/subject/chapters/chapter_XX/
      await _saveChapterData(node, file.classLevel, subjectSlug, extraction);
    }

    return chapters;
  }

  /// Attempts to extract a title from the beginning of the chapter text.
  String _determineTitle(String text, int index) {
    final firstLine = text.split('\n').first.trim();
    if (firstLine.toUpperCase().contains('CHAPTER')) {
      final parts = firstLine.split(':');
      if (parts.length > 1) return parts.last.trim();
      return firstLine.replaceAll(RegExp(r'=+'), '').trim();
    }
    return 'Chapter $index';
  }

  /// Splits the text into meaningful logical sections based on double newlines.
  List<String> _splitIntoSections(String text) {
    return text
        .split(RegExp(r'\n\s*\n'))
        .map((s) => s.trim())
        .where((s) => s.length > 50)
        .toList();
  }

  /// Extracts significant keywords to ground the mocked content generation.
  List<String> _extractKeywords(String text) {
    final stopWords = {'this', 'that', 'with', 'from', 'these', 'those', 'which', 'their', 'about'};
    final words = text.toLowerCase().split(RegExp(r'\W+'));
    final freq = <String, int>{};
    for (var w in words) {
      if (w.length > 4 && !stopWords.contains(w)) {
        freq[w] = (freq[w] ?? 0) + 1;
      }
    }
    final sorted = freq.keys.toList()..sort((a, b) => freq[b]!.compareTo(freq[a]!));
    return sorted.take(10).toList();
  }

  /// Saves the chapter [ConceptNode], [lesson.json], [metadata.json], and [media.json] to the filesystem.
  Future<void> _saveChapterData(ConceptNode node, int classLevel, String subjectSlug, ExtractionResult extraction) async {
    final classDir = 'class_${classLevel.toString().padLeft(2, '0')}';
    final dirPath = p.join(_basePath, classDir, subjectSlug, 'chapters', 'chapter_${node.id.split("_").last}');

    final directory = Directory(dirPath);
    if (!await directory.exists()) {
      await directory.create(recursive: true);
    }

    const encoder = JsonEncoder.withIndent('  ');

    // 1. metadata.json
    final metadata = {
      'id': node.id,
      'subject': node.subject,
      'classLevel': node.classLevel,
      'chapter': node.chapter,
      'topic': node.topic,
      'status': node.status,
      'generationMetadata': node.generationMetadata,
    };
    await File(p.join(dirPath, 'metadata.json')).writeAsString(encoder.convert(metadata));

    // 2. lesson.json
    await File(p.join(dirPath, 'lesson.json')).writeAsString(encoder.convert(node.toMap()));

    // 3. media.json
    final media = {
      'images': extraction.images,
      'tables': extraction.tables,
      'videos': [],
    };
    await File(p.join(dirPath, 'media.json')).writeAsString(encoder.convert(media));

    // Also save split files for redundancy as per previous structure
    await File(p.join(dirPath, 'quiz.json')).writeAsString(encoder.convert([]));
    await File(p.join(dirPath, 'flashcards.json')).writeAsString(encoder.convert([]));
    await File(p.join(dirPath, 'objectives.json')).writeAsString(encoder.convert([]));
    await File(p.join(dirPath, 'summary.json')).writeAsString(encoder.convert({'revisionNotes': node.revisionNotes}));
  }
}
