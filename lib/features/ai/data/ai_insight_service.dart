import 'package:google_generative_ai/google_generative_ai.dart';
import '../../parent/domain/models/student_report.dart';

class AiInsightService {
  final GenerativeModel _model;

  AiInsightService(String apiKey)
      : _model = GenerativeModel(model: 'gemini-1.5-flash', apiKey: apiKey);

  Future<String> generateParentSummary(StudentReport report) async {
    final prompt = '''
You are Gurukul AI, an empathetic educational consultant for parents.
Your task is to summarize a student's learning progress based on the data below.

### STUDENT DATA
- Name: ${report.studentName}
- Average Mastery: ${(report.averageMastery * 100).toStringAsFixed(0)}%
- Total Study Time: ${report.totalStudyTimeMinutes} minutes
- Strong Areas: ${report.strongAreas.join(', ')}
- Weak Areas: ${report.weakAreas.join(', ')}

### INSTRUCTIONS
1. Be encouraging and supportive.
2. Explain what the "Average Mastery" means in simple terms.
3. Provide one actionable tip for the parent to help with the "Weak Areas".
4. Keep the summary under 150 words.
''';

    final content = [Content.text(prompt)];
    final response = await _model.generateContent(content);
    return response.text ?? "Unable to generate summary at this time.";
  }

  Future<String> generateTeacherClassInsight({
    required int totalStudents,
    required double classAverage,
    required List<String> commonWeakTopics,
  }) async {
    final prompt = '''
You are Gurukul AI, a data analyst for teachers.
Summarize the following class performance data:

- Total Students: $totalStudents
- Class Average Mastery: ${(classAverage * 100).toStringAsFixed(0)}%
- Common Struggling Topics: ${commonWeakTopics.join(', ')}

### INSTRUCTIONS
1. Be analytical and professional.
2. Suggest a strategy for the teacher to address the common struggling topics (e.g., peer learning, remedial session).
3. Keep it concise.
''';

    final content = [Content.text(prompt)];
    final response = await _model.generateContent(content);
    return response.text ?? "Class insights unavailable.";
  }
}
