import 'package:flutter_test/flutter_test.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/mastery.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/concept_node.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/services/mastery_service.dart';
import 'package:project_gurukul_ai/features/assessment/domain/assessment_engine.dart';

void main() {
  late MasteryService service;

  setUp(() {
    service = MasteryService();
  });

  test('should calculate first mastery score correctly', () {
    final result = AssessmentResult(
      assessmentId: 'a1',
      totalQuestions: 10,
      correctAnswers: 8,
      timeTaken: const Duration(minutes: 5),
      responses: {},
    );

    final mastery = service.calculateNewMastery(
      currentMastery: null,
      result: result,
      studentId: 's1',
      conceptId: 'c1',
    );

    expect(mastery.masteryScore, 0.8);
    expect(mastery.status, LearningStatus.mastered);
    expect(mastery.attempts, 1);
  });

  test('should update mastery score with weighted average', () {
    final currentMastery = Mastery(
      studentId: 's1',
      conceptId: 'c1',
      masteryScore: 0.5,
      status: LearningStatus.inProgress,
      lastReviewed: DateTime.now(),
      attempts: 1,
      timeSpent: const Duration(minutes: 10),
    );

    final result = AssessmentResult(
      assessmentId: 'a2',
      totalQuestions: 10,
      correctAnswers: 10,
      timeTaken: const Duration(minutes: 5),
      responses: {},
    );

    final mastery = service.calculateNewMastery(
      currentMastery: currentMastery,
      result: result,
      studentId: 's1',
      conceptId: 'c1',
    );

    // (0.5 * 0.6) + (1.0 * 0.4) = 0.3 + 0.4 = 0.7
    expect(mastery.masteryScore, closeTo(0.7, 0.01));
    expect(mastery.status, LearningStatus.inProgress);
    expect(mastery.attempts, 2);
    expect(mastery.timeSpent.inMinutes, 15);
  });
}
