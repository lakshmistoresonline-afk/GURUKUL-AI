import '../../../../core/theme/theme_service.dart';
import 'interactive_activity.dart';

enum Difficulty { beginner, intermediate, advanced }

enum BloomLevel { remember, understand, apply, analyze, evaluate, create }

class ConceptNode {
  final String id;
  final String subject;
  final int classLevel;
  final String chapter;
  final String topic;
  final String subtopic;
  final Difficulty difficulty;
  final BloomLevel bloomLevel;
  final int examWeightage;
  final Duration estStudyTime;
  final List<String> prerequisites;
  final List<String> dependencies;
  final List<String> relatedConcepts;
  final List<String> learningObjectives;
  final List<String> examples;
  final List<String> misconceptions;
  final List<PracticeExercise> practiceExercises;
  final List<Flashcard> flashcards;
  final String revisionNotes;
  final String? mindMapUrl;
  final List<String> commonMistakes;
  final Map<String, String> vocabulary;
  final List<String> interactiveActivities;
  final List<String> masteryCheckpoints;
  final String introduction;
  final String realLifeConnection;
  final String storyBasedExplanation;
  final String childFriendlyExplanation;
  final String teacherExplanation;
  final String animatedLessonAsset;
  final String? videoUrl;
  final List<InteractiveActivity> activities;
  final List<String> handsOnActivities;
  final String animationScript;
  final String videoScript;
  final String parentNotes;
  final String teacherNotes;
  final String learningOutcomes;
  final List<String> keyTakeaways;
  final Map<String, String> faqs;
  final String importantNotes;
  final List<String> socraticPrompts;
  final List<String> illustrationPrompts;
  final String status;
  final Map<String, dynamic> generationMetadata;

  ConceptNode({
    required this.id,
    required this.subject,
    required this.classLevel,
    required this.chapter,
    required this.topic,
    required this.subtopic,
    required this.difficulty,
    required this.bloomLevel,
    required this.examWeightage,
    required this.estStudyTime,
    this.prerequisites = const [],
    this.dependencies = const [],
    this.relatedConcepts = const [],
    this.learningObjectives = const [],
    this.examples = const [],
    this.misconceptions = const [],
    this.practiceExercises = const [],
    this.flashcards = const [],
    this.revisionNotes = '',
    this.mindMapUrl,
    this.commonMistakes = const [],
    this.vocabulary = const {},
    this.interactiveActivities = const [],
    this.masteryCheckpoints = const [],
    this.introduction = '',
    this.realLifeConnection = '',
    this.storyBasedExplanation = '',
    this.childFriendlyExplanation = '',
    this.teacherExplanation = '',
    this.animatedLessonAsset = '',
    this.videoUrl,
    this.activities = const [],
    this.handsOnActivities = const [],
    this.animationScript = '',
    this.videoScript = '',
    this.parentNotes = '',
    this.teacherNotes = '',
    this.learningOutcomes = '',
    this.keyTakeaways = const [],
    this.faqs = const {},
    this.importantNotes = '',
    this.socraticPrompts = const [],
    this.illustrationPrompts = const [],
    this.status = 'Draft',
    this.generationMetadata = const {},
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'subject': subject,
      'classLevel': classLevel,
      'chapter': chapter,
      'topic': topic,
      'subtopic': subtopic,
      'difficulty': difficulty.name,
      'bloomLevel': bloomLevel.name,
      'examWeightage': examWeightage,
      'estStudyTime': estStudyTime.inMinutes,
      'prerequisites': prerequisites,
      'dependencies': dependencies,
      'relatedConcepts': relatedConcepts,
      'learningObjectives': learningObjectives,
      'examples': examples,
      'misconceptions': misconceptions,
      'practiceExercises': practiceExercises.map((e) => e.toMap()).toList(),
      'flashcards': flashcards.map((e) => e.toMap()).toList(),
      'revisionNotes': revisionNotes,
      'mindMapUrl': mindMapUrl,
      'commonMistakes': commonMistakes,
      'vocabulary': vocabulary,
      'interactiveActivities': interactiveActivities,
      'masteryCheckpoints': masteryCheckpoints,
      'introduction': introduction,
      'realLifeConnection': realLifeConnection,
      'storyBasedExplanation': storyBasedExplanation,
      'childFriendlyExplanation': childFriendlyExplanation,
      'teacherExplanation': teacherExplanation,
      'animatedLessonAsset': animatedLessonAsset,
      'videoUrl': videoUrl,
      'activities': activities.map((e) => e.toMap()).toList(),
      'handsOnActivities': handsOnActivities,
      'animationScript': animationScript,
      'videoScript': videoScript,
      'parentNotes': parentNotes,
      'teacherNotes': teacherNotes,
      'learningOutcomes': learningOutcomes,
      'keyTakeaways': keyTakeaways,
      'faqs': faqs,
      'importantNotes': importantNotes,
      'socraticPrompts': socraticPrompts,
      'illustrationPrompts': illustrationPrompts,
      'status': status,
      'generationMetadata': generationMetadata,
    };
  }

  factory ConceptNode.fromMap(Map<String, dynamic> map) {
    return ConceptNode(
      id: map['id']?.toString() ?? '',
      subject: map['subject']?.toString() ?? '',
      classLevel: map['classLevel'] ?? 5,
      chapter: map['chapter']?.toString() ?? '',
      topic: map['topic']?.toString() ?? '',
      subtopic: map['subtopic']?.toString() ?? '',
      difficulty: Difficulty.values.firstWhere((e) => e.name == map['difficulty'], orElse: () => Difficulty.beginner),
      bloomLevel: BloomLevel.values.firstWhere((e) => e.name == map['bloomLevel'], orElse: () => BloomLevel.remember),
      examWeightage: map['examWeightage'] ?? 1,
      estStudyTime: Duration(minutes: map['estStudyTime'] ?? 30),
      prerequisites: safeStringList(map['prerequisites']),
      dependencies: safeStringList(map['dependencies']),
      relatedConcepts: safeStringList(map['relatedConcepts']),
      learningObjectives: safeStringList(map['learningObjectives']),
      examples: safeStringList(map['examples']),
      misconceptions: safeStringList(map['misconceptions']),
      practiceExercises: (map['practiceExercises'] as List? ?? []).map((e) => PracticeExercise.fromMap(Map<String, dynamic>.from(e))).toList(),
      flashcards: (map['flashcards'] as List? ?? []).map((f) => Flashcard.fromMap(Map<String, dynamic>.from(f))).toList(),
      revisionNotes: map['revisionNotes']?.toString() ?? '',
      mindMapUrl: map['mindMapUrl']?.toString(),
      commonMistakes: safeStringList(map['commonMistakes']),
      vocabulary: safeStringMap(map['vocabulary']),
      interactiveActivities: safeStringList(map['interactiveActivities']),
      masteryCheckpoints: safeStringList(map['masteryCheckpoints']),
      introduction: map['introduction']?.toString() ?? '',
      realLifeConnection: map['realLifeConnection']?.toString() ?? '',
      storyBasedExplanation: map['storyBasedExplanation']?.toString() ?? '',
      childFriendlyExplanation: map['childFriendlyExplanation']?.toString() ?? '',
      teacherExplanation: map['teacherExplanation']?.toString() ?? '',
      animatedLessonAsset: map['animatedLessonAsset']?.toString() ?? '',
      videoUrl: map['videoUrl']?.toString(),
      activities: (map['activities'] as List? ?? []).map((a) => InteractiveActivity.fromMap(Map<String, dynamic>.from(a))).toList(),
      handsOnActivities: safeStringList(map['handsOnActivities']),
      animationScript: map['animationScript']?.toString() ?? '',
      videoScript: map['videoScript']?.toString() ?? '',
      parentNotes: map['parentNotes']?.toString() ?? '',
      teacherNotes: map['teacherNotes']?.toString() ?? '',
      learningOutcomes: map['learningOutcomes']?.toString() ?? '',
      keyTakeaways: safeStringList(map['keyTakeaways']),
      faqs: safeStringMap(map['faqs']),
      importantNotes: map['importantNotes']?.toString() ?? '',
      socraticPrompts: safeStringList(map['socraticPrompts']),
      illustrationPrompts: safeStringList(map['illustrationPrompts']),
      status: map['status']?.toString() ?? 'Draft',
      generationMetadata: Map<String, dynamic>.from(map['generationMetadata'] ?? {}),
    );
  }
}

class PracticeExercise {
  final String question;
  final List<String> options;
  final String correctAnswer;
  final String? hint;
  final String? explanation;
  final bool isHots;

  const PracticeExercise({
    required this.question,
    required this.options,
    required this.correctAnswer,
    this.hint,
    this.explanation,
    this.isHots = false,
  });

  Map<String, dynamic> toMap() {
    return {
      'question': question,
      'options': options,
      'correctAnswer': correctAnswer,
      'hint': hint,
      'explanation': explanation,
      'isHots': isHots,
    };
  }

  factory PracticeExercise.fromMap(Map<String, dynamic> map) {
    return PracticeExercise(
      question: map['question']?.toString() ?? '',
      options: safeStringList(map['options']),
      correctAnswer: map['correctAnswer']?.toString() ?? '',
      hint: map['hint']?.toString(),
      explanation: map['explanation']?.toString(),
      isHots: map['isHots'] ?? false,
    );
  }
}

class Flashcard {
  final String front;
  final String back;

  const Flashcard({required this.front, required this.back});

  Map<String, dynamic> toMap() {
    return {'front': front, 'back': back};
  }

  factory Flashcard.fromMap(Map<String, dynamic> map) {
    return Flashcard(
      front: map['front']?.toString() ?? '',
      back: map['back']?.toString() ?? '',
    );
  }
}

// Global safety helpers for Web Type Compatibility
List<String> safeStringList(dynamic value) {
  if (value is List) {
    return value.map((e) => e?.toString() ?? '').toList();
  }
  return [];
}

Map<String, String> safeStringMap(dynamic value) {
  if (value is Map) {
    return value.map((k, v) => MapEntry(k.toString(), v?.toString() ?? ''));
  }
  return {};
}
