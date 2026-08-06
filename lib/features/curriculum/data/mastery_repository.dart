import 'package:cloud_firestore/cloud_firestore.dart';
import '../domain/models/mastery.dart';
import '../domain/models/concept_node.dart';

class MasteryRepository {
  final FirebaseFirestore _firestore;

  MasteryRepository({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  Future<Mastery?> getMastery(String studentId, String conceptId) async {
    final doc = await _firestore
        .collection('mastery')
        .doc('${studentId}_$conceptId')
        .get();

    if (doc.exists) {
      return Mastery(
        studentId: doc['studentId'],
        conceptId: doc['conceptId'],
        masteryScore: (doc['masteryScore'] as num?)?.toDouble() ?? 0.0,
        status: LearningStatus.values.firstWhere((e) => e.name == doc['status'], orElse: () => LearningStatus.notStarted),
        lastReviewed: DateTime.parse(doc['lastReviewed'] ?? DateTime.now().toIso8601String()),
        attempts: doc['attempts'] ?? 0,
        timeSpent: Duration(minutes: doc['timeSpent'] ?? 0),
      );
    }
    return null;
  }

  Future<void> saveMastery(Mastery mastery) async {
    await _firestore
        .collection('mastery')
        .doc('${mastery.studentId}_${mastery.conceptId}')
        .set(mastery.toMap());
  }

  Future<List<Mastery>> getStudentMastery(String studentId) async {
    final snapshot = await _firestore
        .collection('mastery')
        .where('studentId', isEqualTo: studentId)
        .get();

    return snapshot.docs.map((doc) => Mastery(
      studentId: doc['studentId'],
      conceptId: doc['conceptId'],
      masteryScore: (doc['masteryScore'] as num?)?.toDouble() ?? 0.0,
      status: LearningStatus.values.firstWhere((e) => e.name == doc['status'], orElse: () => LearningStatus.notStarted),
      lastReviewed: DateTime.parse(doc['lastReviewed'] ?? DateTime.now().toIso8601String()),
      attempts: doc['attempts'] ?? 0,
      timeSpent: Duration(minutes: doc['timeSpent'] ?? 0),
    )).toList();
  }
}
