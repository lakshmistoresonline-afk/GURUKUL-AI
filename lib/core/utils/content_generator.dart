import '../../features/curriculum/domain/models/concept_node.dart';
import '../../features/curriculum/data/media/lesson_media_repository.dart';
import '../di/injection.dart';

class ContentGenerator {
  static Future<ConceptNode> enrich(ConceptNode node) async {
    // If already has rich content, return as is
    if (node.introduction.isNotEmpty) return node;

    final subject = node.subject;
    final topic = node.topic;
    final chapter = node.chapter;

    final mediaRepo = sl<LessonMediaRepository>();
    final specificMedia = await mediaRepo.getMediaForChapter(node.id);

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
      practiceExercises: node.practiceExercises,
      flashcards: node.flashcards,
      revisionNotes: node.revisionNotes,
      mindMapUrl: node.mindMapUrl,
      commonMistakes: node.commonMistakes,
      vocabulary: node.vocabulary,
      interactiveActivities: node.interactiveActivities,
      masteryCheckpoints: node.masteryCheckpoints,

      // Generated Rich Content
      introduction: 'Welcome! Today we are starting a fascinating journey into "$topic" from your $subject chapter, "$chapter". Let\'s get ready to learn!',
      realLifeConnection: _generateRealLife(subject, topic),
      storyBasedExplanation: _generateStory(subject, topic),
      childFriendlyExplanation: 'Think of $topic like a puzzle where every piece helps you understand the world better. We will use simple steps to master it!',
      teacherExplanation: 'This lesson covers the fundamental concepts of $topic as per the NCERT syllabus for Class ${node.classLevel}. We will focus on conceptual clarity and application.',
      animatedLessonAsset: specificMedia?.animationAsset ?? _getAsset(subject, topic),
      videoUrl: specificMedia?.videoAsset ?? 'https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4',
      handsOnActivities: [
        'Draw a diagram of $topic in your notebook.',
        'Discuss what you learned about $topic with a friend or parent.'
      ],
    );
  }

  static String _generateRealLife(String subject, String topic) {
    switch (subject.toLowerCase()) {
      case 'mathematics': return 'We use $topic whenever we are measuring things, buying groceries, or even building a toy house!';
      case 'science': return 'Scientists use $topic to understand how plants grow, how planets move, and how our bodies work.';
      case 'evs': return 'Understanding $topic helps us take care of our environment and respect the animals and plants around us.';
      default: return 'Understanding $topic helps you become a smarter and more curious learner!';
    }
  }

  static String _generateStory(String subject, String topic) {
    return 'Once upon a time, there was a student just like you who wondered about $topic. They realized that by understanding this, they could solve many interesting problems!';
  }

  static String _getAsset(String subject, String topic) {
    // Return a relevant lottie asset path if it exists, else a default
    return 'assets/lottie/default_lesson.json';
  }
}
