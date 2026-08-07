import 'interactive_activity.dart';

enum Difficulty { beginner, intermediate, advanced }
enum BloomLevel { remember, understand, apply, analyze, evaluate, create }
enum LearningStatus { notStarted, inProgress, mastered, needsRevision }

class PracticeExercise {
  final String question;
  final String hint;
  final List<String> options;
  final String correctAnswer;
  final String explanation;
  final bool isHots;

  const PracticeExercise({
    required this.question,
    required this.hint,
    required this.options,
    required this.correctAnswer,
    required this.explanation,
    this.isHots = false,
  });

  Map<String, dynamic> toMap() {
    return {
      'question': question,
      'hint': hint,
      'options': options,
      'correctAnswer': correctAnswer,
      'explanation': explanation,
      'isHots': isHots,
    };
  }

  factory PracticeExercise.fromMap(Map<String, dynamic> map) {
    return PracticeExercise(
      question: map['question'] ?? '',
      hint: map['hint'] ?? '',
      options: List<String>.from(map['options'] ?? []),
      correctAnswer: map['correctAnswer'] ?? '',
      explanation: map['explanation'] ?? '',
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
      front: map['front'] ?? '',
      back: map['back'] ?? '',
    );
  }
}

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
  final List<String> interactiveActivities; // Legacy or string based
  final List<String> masteryCheckpoints;

  final String introduction;
  final String realLifeConnection;
  final String storyBasedExplanation;
  final String childFriendlyExplanation;
  final String teacherExplanation;
  final String animatedLessonAsset;
  final String? videoUrl;
  final List<InteractiveActivity> activities; // New structured activities
  final List<String> handsOnActivities;

  final String animationScript;
  final String videoScript;
  final String parentNotes;
  final String teacherNotes;
  final String learningOutcomes;

  // Phase 56 Additions
  final List<String> keyTakeaways;
  final Map<String, String> faqs;
  final String importantNotes;
  final List<String> socraticPrompts;
  final List<String> illustrationPrompts;
  final String status; // Draft, Review, Approved, Published
  final Map<String, dynamic> generationMetadata;

  const ConceptNode({
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
    required this.prerequisites,
    required this.dependencies,
    required this.relatedConcepts,
    required this.learningObjectives,
    required this.examples,
    required this.misconceptions,
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
      'flashcards': flashcards.map((f) => f.toMap()).toList(),
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
      'activities': activities.map((a) => a.toMap()).toList(),
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
      id: map['id'] ?? '',
      subject: map['subject'] ?? '',
      classLevel: map['classLevel'] ?? 5,
      chapter: map['chapter'] ?? '',
      topic: map['topic'] ?? '',
      subtopic: map['subtopic'] ?? '',
      difficulty: Difficulty.values.firstWhere((e) => e.name == map['difficulty'], orElse: () => Difficulty.beginner),
      bloomLevel: BloomLevel.values.firstWhere((e) => e.name == map['bloomLevel'], orElse: () => BloomLevel.remember),
      examWeightage: map['examWeightage'] ?? 1,
      estStudyTime: Duration(minutes: map['estStudyTime'] ?? 30),
      prerequisites: List<String>.from(map['prerequisites'] ?? []),
      dependencies: List<String>.from(map['dependencies'] ?? []),
      relatedConcepts: List<String>.from(map['relatedConcepts'] ?? []),
      learningObjectives: List<String>.from(map['learningObjectives'] ?? []),
      examples: List<String>.from(map['examples'] ?? []),
      misconceptions: List<String>.from(map['misconceptions'] ?? []),
      practiceExercises: (map['practiceExercises'] as List? ?? []).map((e) => PracticeExercise.fromMap(e)).toList(),
      flashcards: (map['flashcards'] as List? ?? []).map((f) => Flashcard.fromMap(f)).toList(),
      revisionNotes: map['revisionNotes'] ?? '',
      mindMapUrl: map['mindMapUrl'],
      commonMistakes: List<String>.from(map['commonMistakes'] ?? []),
      vocabulary: Map<String, String>.from(map['vocabulary'] ?? {}),
      interactiveActivities: List<String>.from(map['interactiveActivities'] ?? []),
      masteryCheckpoints: List<String>.from(map['masteryCheckpoints'] ?? []),
      introduction: map['introduction'] ?? '',
      realLifeConnection: map['realLifeConnection'] ?? '',
      storyBasedExplanation: map['storyBasedExplanation'] ?? '',
      childFriendlyExplanation: map['childFriendlyExplanation'] ?? '',
      teacherExplanation: map['teacherExplanation'] ?? '',
      animatedLessonAsset: map['animatedLessonAsset'] ?? '',
      videoUrl: map['videoUrl'],
      activities: (map['activities'] as List? ?? []).map((a) => InteractiveActivity.fromMap(a)).toList(),
      handsOnActivities: List<String>.from(map['handsOnActivities'] ?? []),
      animationScript: map['animationScript'] ?? '',
      videoScript: map['videoScript'] ?? '',
      parentNotes: map['parentNotes'] ?? '',
      teacherNotes: map['teacherNotes'] ?? '',
      learningOutcomes: map['learningOutcomes'] ?? '',
      keyTakeaways: List<String>.from(map['keyTakeaways'] ?? []),
      faqs: Map<String, String>.from(map['faqs'] ?? {}),
      importantNotes: map['importantNotes'] ?? '',
      socraticPrompts: List<String>.from(map['socraticPrompts'] ?? []),
      illustrationPrompts: List<String>.from(map['illustrationPrompts'] ?? []),
      status: map['status'] ?? 'Draft',
      generationMetadata: Map<String, dynamic>.from(map['generationMetadata'] ?? {}),
    );
  }
}
