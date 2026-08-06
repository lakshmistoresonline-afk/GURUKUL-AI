enum QuestionType { mcq, ftb, mtc }

class Question {
  final String id;
  final String text;
  final QuestionType type;
  final List<String>? options;
  final dynamic correctAnswer;
  final String? explanation;

  Question({
    required this.id,
    required this.text,
    required this.type,
    this.options,
    required this.correctAnswer,
    this.explanation,
  });
}
