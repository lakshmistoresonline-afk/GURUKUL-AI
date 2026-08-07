import '../../curriculum/domain/models/concept_node.dart';
import '../../../core/telemetry/telemetry_service.dart';
import '../../../core/storage/local_storage_service.dart';
import 'models/question.dart';
import 'models/assessment_session.dart';

class AssessmentResult {
  final String assessmentId;
  final int totalQuestions;
  final int correctAnswers;
  final Duration timeTaken;
  final Map<String, dynamic> responses;

  AssessmentResult({
    required this.assessmentId,
    required this.totalQuestions,
    required this.correctAnswers,
    required this.timeTaken,
    required this.responses,
  });

  double get score => correctAnswers / totalQuestions;
}

class AssessmentEngine {
  final TelemetryService _telemetry;
  final LocalStorageService _storage;
  static const String _sessionKeyPrefix = 'assessment_session_';

  AssessmentEngine(this._telemetry, this._storage);

  Future<void> startAssessment({
    required String assessmentId,
    required String conceptId,
    required String studentId,
  }) async {
    final session = AssessmentSession(
      id: assessmentId,
      conceptId: conceptId,
      studentId: studentId,
      responses: {},
      startTime: DateTime.now(),
    );

    await _storage.save('$_sessionKeyPrefix$assessmentId', session.toMap());

    _telemetry.logEvent(
      eid: 'ASSESS',
      edata: {
        'type': 'start',
        'id': assessmentId,
        'conceptId': conceptId,
      },
    );
  }

  Future<void> updateResponse(String assessmentId, String questionId, dynamic response) async {
    final sessionMap = _storage.get('$_sessionKeyPrefix$assessmentId');
    if (sessionMap != null) {
      final session = AssessmentSession.fromMap(Map<String, dynamic>.from(sessionMap));
      session.responses[questionId] = response;
      await _storage.save('$_sessionKeyPrefix$assessmentId', session.toMap());
    }
  }

  Future<AssessmentSession?> recoverSession(String assessmentId) async {
    final sessionMap = _storage.get('$_sessionKeyPrefix$assessmentId');
    if (sessionMap != null) {
      return AssessmentSession.fromMap(Map<String, dynamic>.from(sessionMap));
    }
    return null;
  }

  Future<AssessmentResult> submitAssessment({
    required String assessmentId,
    required ConceptNode concept,
    required List<Question> questions,
    required Map<String, dynamic> userResponses,
    required Duration duration,
  }) async {
    int correctCount = 0;
    for (var question in questions) {
      if (userResponses[question.id] == question.correctAnswer) {
        correctCount++;
      }
    }

    final result = AssessmentResult(
      assessmentId: assessmentId,
      totalQuestions: questions.length,
      correctAnswers: correctCount,
      timeTaken: duration,
      responses: userResponses,
    );

    await _storage.save('$_sessionKeyPrefix$assessmentId', null); // Clear session

    _telemetry.logEvent(
      eid: 'ASSESS',
      edata: {
        'type': 'submit',
        'id': assessmentId,
        'conceptId': concept.id,
        'score': result.score,
        'duration': duration.inSeconds,
      },
    );

    return result;
  }
}
