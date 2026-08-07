enum QuestionType { mcq, ftb, mtc, trueFalse, shortAnswer, assertion, caseStudy }

class Question {
  final String id;
  final String text;
  final QuestionType type;
  final List<String>? options;
  final dynamic correctAnswer;
  final String? explanation;
  final String? marks;
  final String? difficulty; // easy, medium, hard
  final String? topicId;
  final String? chapterId;
  final bool isHots;

  Question({
    required this.id,
    required this.text,
    required this.type,
    this.options,
    required this.correctAnswer,
    this.explanation,
    this.marks,
    this.difficulty,
    this.topicId,
    this.chapterId,
    this.isHots = false,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'text': text,
      'type': type.name,
      'options': options,
      'correctAnswer': correctAnswer,
      'explanation': explanation,
      'marks': marks,
      'difficulty': difficulty,
      'topicId': topicId,
      'chapterId': chapterId,
      'isHots': isHots,
    };
  }

  factory Question.fromMap(Map<String, dynamic> map) {
    return Question(
      id: map['id'] ?? '',
      text: map['text'] ?? '',
      type: QuestionType.values.firstWhere((e) => e.name == map['type'], orElse: () => QuestionType.mcq),
      options: map['options'] != null ? List<String>.from(map['options']) : null,
      correctAnswer: map['correctAnswer'],
      explanation: map['explanation'],
      marks: map['marks'],
      difficulty: map['difficulty'],
      topicId: map['topicId'],
      chapterId: map['chapterId'],
      isHots: map['isHots'] ?? false,
    );
  }
}
