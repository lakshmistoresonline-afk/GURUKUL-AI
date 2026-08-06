import '../models/mastery.dart';
import '../models/concept_node.dart';
import '../../../assessment/domain/assessment_engine.dart';

class MasteryService {
  /// Calculates the new mastery score based on a new assessment result.
  /// Uses a simple weighted average where the new score has 40% weight.
  Mastery calculateNewMastery({
    required Mastery? currentMastery,
    required AssessmentResult result,
    required String studentId,
    required String conceptId,
  }) {
    final double newScore = result.score;
    double updatedScore;

    if (currentMastery == null) {
      updatedScore = newScore;
    } else {
      updatedScore = (currentMastery.masteryScore * 0.6) + (newScore * 0.4);
    }

    final int newAttempts = (currentMastery?.attempts ?? 0) + 1;
    final Duration newTimeSpent = (currentMastery?.timeSpent ?? Duration.zero) + result.timeTaken;

    // Determine Status
    LearningStatus status;
    if (updatedScore >= 0.8) {
      status = LearningStatus.mastered;
    } else if (updatedScore >= 0.4) {
      status = LearningStatus.inProgress;
    } else {
      status = LearningStatus.needsRevision;
    }

    return Mastery(
      studentId: studentId,
      conceptId: conceptId,
      masteryScore: updatedScore,
      status: status,
      lastReviewed: DateTime.now(),
      attempts: newAttempts,
      timeSpent: newTimeSpent,
    );
  }

  /// Manually checks if a concept needs revision due to time decay.
  LearningStatus checkRevisionStatus(Mastery mastery, bool isDue) {
    if (isDue && mastery.status == LearningStatus.mastered) {
      return LearningStatus.needsRevision;
    }
    return mastery.status;
  }
}
