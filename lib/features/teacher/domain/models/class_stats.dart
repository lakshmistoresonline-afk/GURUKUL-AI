class StudentAnalytics {
  final String studentId;
  final String name;
  final double averageMastery;
  final double attendanceRate;
  final List<String> topSubjects;
  final List<String> weakAreas;

  StudentAnalytics({
    required this.studentId,
    required this.name,
    required this.averageMastery,
    required this.attendanceRate,
    required this.topSubjects,
    required this.weakAreas,
  });
}

class ClassStats {
  final String classId;
  final String grade;
  final int totalStudents;
  final double classAverageMastery;
  final Map<String, double> subjectPerformance;
  final List<StudentAnalytics> studentPerformance;

  ClassStats({
    required this.classId,
    required this.grade,
    required this.totalStudents,
    required this.classAverageMastery,
    required this.subjectPerformance,
    required this.studentPerformance,
  });
}
