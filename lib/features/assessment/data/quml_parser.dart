import '../domain/models/question.dart';

class QuMLParser {
  /// Parses a QuML 3.0 JSON item into a Question object.
  Question parseItem(Map<String, dynamic> json) {
    final body = json['body'] ?? '';
    final typeStr = json['type']?.toString().toLowerCase() ?? 'mcq';

    QuestionType type;
    switch (typeStr) {
      case 'ftb': type = QuestionType.ftb; break;
      case 'mtc': type = QuestionType.mtc; break;
      default: type = QuestionType.mcq;
    }

    final interactions = json['interactions'] ?? {};
    List<String>? options;
    if (type == QuestionType.mcq) {
      final responseDeclaration = interactions['response1'] ?? {};
      final choices = responseDeclaration['options'] ?? [];
      options = choices.map<String>((c) => c['label'].toString()).toList();
    }

    return Question(
      id: json['identifier'] ?? '',
      text: body,
      type: type,
      options: options,
      correctAnswer: _extractCorrectAnswer(json),
      explanation: json['explanation'],
    );
  }

  dynamic _extractCorrectAnswer(Map<String, dynamic> json) {
    // Simplified logic for MVP
    return json['answer'];
  }
}
