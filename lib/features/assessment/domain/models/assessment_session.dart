class AssessmentSession {
  final String id;
  final String conceptId;
  final String studentId;
  final Map<String, dynamic> responses;
  final DateTime startTime;

  AssessmentSession({
    required this.id,
    required this.conceptId,
    required this.studentId,
    required this.responses,
    required this.startTime,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'conceptId': conceptId,
      'studentId': studentId,
      'responses': responses,
      'startTime': startTime.toIso8601String(),
    };
  }

  factory AssessmentSession.fromMap(Map<String, dynamic> map) {
    return AssessmentSession(
      id: map['id'],
      conceptId: map['conceptId'],
      studentId: map['studentId'],
      responses: Map<String, dynamic>.from(map['responses']),
      startTime: DateTime.parse(map['startTime']),
    );
  }
}
