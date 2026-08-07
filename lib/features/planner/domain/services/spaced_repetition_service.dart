import '../../../curriculum/domain/models/concept_node.dart';
import '../../../curriculum/domain/models/mastery.dart';

class SpacedRepetitionService {
  /// Calculates the next revision date using SM-2 algorithm principles.
  /// [quality] - range from 0-5 (0 = forgot, 5 = perfect)
  DateTime calculateNextRevision(Mastery mastery, int quality) {
    int repetitions = mastery.attempts;
    int interval = 1;

    if (quality >= 3) {
      if (repetitions == 0) {
        interval = 1;
      } else if (repetitions == 1) {
        interval = 6;
      } else {
        interval = (mastery.attempts * 1.5).round();
      }
      repetitions++;
    } else {
      repetitions = 0;
      interval = 1;
    }

    return DateTime.now().add(Duration(days: interval));
  }

  List<String> getConceptsToRevise(List<Mastery> masteryList) {
    final now = DateTime.now();
    return masteryList
        .where((m) => m.status == LearningStatus.needsRevision ||
                     now.difference(m.lastReviewed).inDays >= 7)
        .map((m) => m.conceptId)
        .toList();
  }
}
