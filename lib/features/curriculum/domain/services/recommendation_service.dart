import '../models/concept_node.dart';
import '../models/mastery.dart';

enum RecommendationType { foundation, advanced, revision, nextTopic }

class Recommendation {
  final String title;
  final String description;
  final RecommendationType type;
  final String conceptId;

  Recommendation({
    required this.title,
    required this.description,
    required this.type,
    required this.conceptId,
  });
}

class RecommendationService {
  Recommendation getRecommendation(ConceptNode concept, Mastery mastery) {
    if (mastery.masteryScore < 0.4) {
      return Recommendation(
        title: 'Strengthen Foundations',
        description: 'It looks like you might need to review some prerequisites for ${concept.topic}.',
        type: RecommendationType.foundation,
        conceptId: concept.prerequisites.isNotEmpty ? concept.prerequisites.first : concept.id,
      );
    } else if (mastery.masteryScore < 0.7) {
      return Recommendation(
        title: 'Keep Practicing',
        description: 'You are doing well! Try some more examples to master ${concept.topic}.',
        type: RecommendationType.nextTopic,
        conceptId: concept.id,
      );
    } else if (mastery.status == LearningStatus.needsRevision) {
      return Recommendation(
        title: 'Time for Revision',
        description: 'You mastered this a while ago. A quick review will help you remember!',
        type: RecommendationType.revision,
        conceptId: concept.id,
      );
    } else {
      return Recommendation(
        title: 'Ready for the Next Step',
        description: 'Excellent work! You have mastered ${concept.topic}. Let\'s move forward.',
        type: RecommendationType.advanced,
        conceptId: concept.dependencies.isNotEmpty ? concept.dependencies.first : concept.id,
      );
    }
  }
}
