import 'package:flutter_test/flutter_test.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/concept_node.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/mastery.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/services/recommendation_service.dart';

void main() {
  late RecommendationService service;
  late ConceptNode mockConcept;

  setUp(() {
    service = RecommendationService();
    mockConcept = ConceptNode(
      id: 'test_1',
      subject: 'Math',
      classLevel: 5,
      chapter: 'Shapes',
      topic: 'Angles',
      subtopic: 'Right Angle',
      difficulty: Difficulty.beginner,
      bloomLevel: BloomLevel.understand,
      examWeightage: 5,
      estStudyTime: const Duration(minutes: 20),
      prerequisites: ['foundation_1'],
      dependencies: ['next_topic_1'],
      relatedConcepts: [],
      learningObjectives: [],
      examples: [],
      misconceptions: [],
    );
  });

  test('should recommend foundation if mastery is low', () {
    final mastery = Mastery(
      studentId: 's1',
      conceptId: 'test_1',
      masteryScore: 0.2,
      status: LearningStatus.inProgress,
      lastReviewed: DateTime.now(),
      attempts: 5,
      timeSpent: const Duration(minutes: 50),
    );

    final result = service.getRecommendation(mockConcept, mastery);
    expect(result.type, RecommendationType.foundation);
    expect(result.conceptId, 'foundation_1');
  });

  test('should recommend next topic if mastery is high', () {
    final mastery = Mastery(
      studentId: 's1',
      conceptId: 'test_1',
      masteryScore: 0.9,
      status: LearningStatus.mastered,
      lastReviewed: DateTime.now(),
      attempts: 2,
      timeSpent: const Duration(minutes: 20),
    );

    final result = service.getRecommendation(mockConcept, mastery);
    expect(result.type, RecommendationType.advanced);
    expect(result.conceptId, 'next_topic_1');
  });
}
