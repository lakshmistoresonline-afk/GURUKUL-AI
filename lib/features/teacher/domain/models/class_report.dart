class ClassReport {
  final String classId;
  final int totalStudents;
  final double averageMastery;
  final List<String> topTopics;
  final List<String> strugglingTopics;
  final String aiInsight;

  ClassReport({
    required this.classId,
    required this.totalStudents,
    required this.averageMastery,
    required this.topTopics,
    required this.strugglingTopics,
    required this.aiInsight,
  });

  Map<String, dynamic> toMap() {
    return {
      'classId': classId,
      'totalStudents': totalStudents,
      'averageMastery': averageMastery,
      'topTopics': topTopics,
      'strugglingTopics': strugglingTopics,
      'aiInsight': aiInsight,
    };
  }
}
