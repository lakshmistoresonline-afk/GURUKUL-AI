import '../../features/curriculum/domain/models/mastery.dart';
import '../../features/curriculum/domain/models/concept_node.dart';

class SpacedRepetitionService {
  /// Calculates the next revision date using SM-2 algorithm principles.
  /// [quality] - range from 0-5 (0 = forgot, 5 = perfect)
  DateTime calculateNextRevisionSM2(Mastery mastery, int quality) {
    int repetitions = mastery.attempts;
    int interval = 1;

    if (quality >= 3) {
      if (repetitions == 0) {
        interval = 1;
      } else if (repetitions == 1) {
        interval = 6;
      } else {
        // Simple multiplier for interval expansion
        interval = (repetitions * 1.5).round();
      }
    } else {
      interval = 1;
    }

    return DateTime.now().add(Duration(days: interval));
  }

  /// Simple threshold-based interval calculation.
  DateTime calculateNextRevision(Mastery mastery) {
    int daysToAdd;
    final score = mastery.masteryScore;

    if (score >= 0.9) {
      daysToAdd = 30;
    } else if (score >= 0.8) {
      daysToAdd = 15;
    } else if (score >= 0.7) {
      daysToAdd = 7;
    } else if (score >= 0.5) {
      daysToAdd = 3;
    } else {
      daysToAdd = 1;
    }

    return mastery.lastReviewed.add(Duration(days: daysToAdd));
  }

  bool isRevisionDue(Mastery mastery) {
    final nextDate = calculateNextRevision(mastery);
    return DateTime.now().isAfter(nextDate);
  }

  List<String> getConceptsToRevise(List<Mastery> masteryList) {
    return masteryList
        .where((m) => m.status == LearningStatus.needsRevision ||
                     isRevisionDue(m))
        .map((m) => m.conceptId)
        .toList();
  }
}
