import '../../domain/models/student_report.dart';
import '../../../curriculum/domain/models/mastery.dart';
import '../../../curriculum/data/framework_repository.dart';

class ReportService {
  final FrameworkRepository _frameworkRepository;

  ReportService(this._frameworkRepository);

  Future<StudentReport> generateStudentReport({
    required String studentId,
    required String studentName,
    required List<Mastery> masteryData,
    required String aiSummary,
  }) async {
    if (masteryData.isEmpty) {
      return StudentReport(
        studentId: studentId,
        studentName: studentName,
        averageMastery: 0.0,
        totalStudyTimeMinutes: 0,
        weakAreas: [],
        strongAreas: [],
        aiSummary: "No learning data available yet. Start a lesson to see progress!",
      );
    }

    double totalScore = 0;
    int totalTime = 0;
    List<String> weakIds = [];
    List<String> strongIds = [];

    for (var m in masteryData) {
      totalScore += m.masteryScore;
      totalTime += m.timeSpent.inMinutes;

      if (m.masteryScore < 0.5) {
        weakIds.add(m.conceptId);
      } else if (m.masteryScore >= 0.8) {
        strongIds.add(m.conceptId);
      }
    }

    // Resolve IDs to human-readable titles (simulated for now)
    final weakAreas = await _resolveConceptTitles(weakIds);
    final strongAreas = await _resolveConceptTitles(strongIds);

    return StudentReport(
      studentId: studentId,
      studentName: studentName,
      averageMastery: totalScore / masteryData.length,
      totalStudyTimeMinutes: totalTime,
      weakAreas: weakAreas,
      strongAreas: strongAreas,
      aiSummary: aiSummary,
    );
  }

  Future<List<String>> _resolveConceptTitles(List<String> ids) async {
    List<String> titles = [];
    for (var id in ids) {
      final details = await _frameworkRepository.getChapterDetails(id);
      titles.add(details?['title'] ?? id);
    }
    return titles;
  }
}
