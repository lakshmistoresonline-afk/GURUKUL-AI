class StudentReport {
  final String studentId;
  final String studentName;
  final double averageMastery;
  final int totalStudyTimeMinutes;
  final List<String> weakAreas;
  final List<String> strongAreas;
  final String aiSummary;

  StudentReport({
    required this.studentId,
    required this.studentName,
    required this.averageMastery,
    required this.totalStudyTimeMinutes,
    required this.weakAreas,
    required this.strongAreas,
    required this.aiSummary,
  });

  Map<String, dynamic> toMap() {
    return {
      'studentId': studentId,
      'studentName': studentName,
      'averageMastery': averageMastery,
      'totalStudyTimeMinutes': totalStudyTimeMinutes,
      'weakAreas': weakAreas,
      'strongAreas': strongAreas,
      'aiSummary': aiSummary,
    };
  }
}
