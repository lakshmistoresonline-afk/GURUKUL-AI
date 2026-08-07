import '../../../curriculum/data/framework_repository.dart';
import '../../../curriculum/domain/models/mastery.dart';

class CoverageReportService {
  final FrameworkRepository _frameworkRepo;

  CoverageReportService(this._frameworkRepo);

  Future<Map<String, dynamic>> generateReport(int classLevel, List<Mastery> studentMastery) async {
    final allChapters = await _frameworkRepo.getAllChapters(classLevel);
    Map<String, int> subjectTotal = {};
    Map<String, int> subjectMastered = {};

    for (var c in allChapters) {
      final subject = c['subject'] as String;
      subjectTotal[subject] = (subjectTotal[subject] ?? 0) + 1;

      final mastery = studentMastery.any((m) => m.conceptId == c['id'] && m.masteryScore >= 0.8);
      if (mastery) {
        subjectMastered[subject] = (subjectMastered[subject] ?? 0) + 1;
      }
    }

    return {
      'classLevel': classLevel,
      'totalChapters': allChapters.length,
      'masteredChapters': subjectMastered.values.fold(0, (a, b) => a + b),
      'breakdown': subjectTotal.keys.map((s) => {
        'subject': s,
        'total': subjectTotal[s],
        'mastered': subjectMastered[s] ?? 0,
      }).toList(),
    };
  }
}
