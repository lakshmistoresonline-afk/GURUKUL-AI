import '../../curriculum/data/mastery_repository.dart';
import '../../curriculum/domain/services/mastery_service.dart';
import '../../gamification/data/gamification_repository.dart';
import '../../assessment/domain/assessment_engine.dart';
import '../../../core/telemetry/telemetry_service.dart';
import '../../curriculum/domain/models/concept_node.dart';

class LearningCoordinator {
  final MasteryRepository _masteryRepository;
  final MasteryService _masteryService;
  final GamificationRepository _gamificationRepository;
  final TelemetryService _telemetry;

  LearningCoordinator(
    this._masteryRepository,
    this._masteryService,
    this._gamificationRepository,
    this._telemetry,
  );

  Future<void> processAssessmentResult({
    required String studentId,
    required ConceptNode concept,
    required AssessmentResult result,
  }) async {
    // 1. Fetch current mastery
    final currentMastery = await _masteryRepository.getMastery(studentId, concept.id);

    // 2. Calculate updated mastery
    final updatedMastery = _masteryService.calculateNewMastery(
      currentMastery: currentMastery,
      result: result,
      studentId: studentId,
      conceptId: concept.id,
    );

    // 3. Save updated mastery
    await _masteryRepository.saveMastery(updatedMastery);

    // 4. Update Gamification (XP)
    // Award 50 XP for completing an assessment, +50 bonus if score > 0.8
    int xpAwarded = 50;
    if (result.score >= 0.8) xpAwarded += 50;
    await _gamificationRepository.addXp(studentId, xpAwarded);

    // 5. Log Telemetry (Processed Event)
    _telemetry.logEvent(
      eid: 'LEARN_LOOP_COMPLETE',
      edata: {
        'studentId': studentId,
        'conceptId': concept.id,
        'score': result.score,
        'xpAwarded': xpAwarded,
        'newStatus': updatedMastery.status.name,
      },
    );
  }
}
