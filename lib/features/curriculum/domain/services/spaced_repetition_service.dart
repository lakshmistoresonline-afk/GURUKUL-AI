import '../models/mastery.dart';

class SpacedRepetitionService {
  /// Calculates the next revision date based on mastery score.
  /// Standard intervals: 1 day, 3 days, 7 days, 15 days, 30 days.
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
}
