import '../../../assessment/domain/models/question.dart';

enum PaperType { unitTest, midTerm, annual, model, sample, practice }

class QuestionPaper {
  final String id;
  final String title;
  final String subject;
  final int classLevel;
  final PaperType type;
  final List<Question> questions;
  final int totalMarks;
  final Duration duration;
  final DateTime? year;
  final String? board; // NCERT, CBSE, etc.

  QuestionPaper({
    required this.id,
    required this.title,
    required this.subject,
    required this.classLevel,
    required this.type,
    required this.questions,
    required this.totalMarks,
    required this.duration,
    this.year,
    this.board,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'subject': subject,
      'classLevel': classLevel,
      'type': type.name,
      'questions': questions.map((q) => q.toMap()).toList(),
      'totalMarks': totalMarks,
      'duration': duration.inMinutes,
      'year': year?.toIso8601String(),
      'board': board,
    };
  }
}
