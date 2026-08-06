class Assignment {
  final String id;
  final String teacherId;
  final String classId;
  final String title;
  final String description;
  final DateTime dueDate;
  final List<String> conceptIds;
  final Map<String, String> studentSubmissions; // studentId -> submissionStatus

  Assignment({
    required this.id,
    required this.teacherId,
    required this.classId,
    required this.title,
    required this.description,
    required this.dueDate,
    required this.conceptIds,
    this.studentSubmissions = const {},
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'teacherId': teacherId,
      'classId': classId,
      'title': title,
      'description': description,
      'dueDate': dueDate.toIso8601String(),
      'conceptIds': conceptIds,
      'studentSubmissions': studentSubmissions,
    };
  }
}
