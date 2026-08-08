import 'concept_node.dart';

enum LearningStatus {
  notStarted,
  inProgress,
  mastered,
  needsRevision,
}

class Mastery {
  final String studentId;
  final String conceptId;
  final double masteryScore;
  final LearningStatus status;
  final DateTime lastReviewed;
  final int attempts;
  final Duration timeSpent;

  Mastery({
    required this.studentId,
    required this.conceptId,
    required this.masteryScore,
    required this.status,
    required this.lastReviewed,
    required this.attempts,
    required this.timeSpent,
  });

  Map<String, dynamic> toMap() {
    return {
      'studentId': studentId,
      'conceptId': conceptId,
      'masteryScore': masteryScore,
      'status': status.name,
      'lastReviewed': lastReviewed.toIso8601String(),
      'attempts': attempts,
      'timeSpent': timeSpent.inMinutes,
    };
  }
}
